import pandas as pd
from os.path import isfile
from tailer import tail
from FinanceDataReader import DataReader
from pykrx.stock import get_market_ohlcv_by_ticker, get_market_ohlcv_by_date
from time import sleep

from modules.pattern_labelling import *

stock_list = pd.read_csv("resources/stockcode.csv",
                         dtype={"종목코드": str, "회사명": str})


def update_stockData_with_labels(start_date=None):
    '''
    라벨링된 데이터에 최신 주식 데이터를 업데이트합니다.
    '''
    # 15시 30분 이후부터는 다음 날을 예측할 수 있도록 오늘 날짜에 8.5시간을 더합니다.
    pd_destDate = pd.to_datetime(pd.Timestamp.now()) + pd.Timedelta(hours=8.5)
    pd_destDate = pd.to_datetime(pd_destDate.date())

    df_std = pd.read_csv('resources/stock_market_data/950200.csv', parse_dates=['date'], index_col=[0])
    pd_lastSavedDate = df_std.date.values[-1]
    if start_date == None:
        pd_startDate = pd_lastSavedDate
    else:
        pd_startDate = pd.to_datetime(start_date)

    # 리소스의 마지막 줄을 검사
    if df_std.open.values[-1] == -1:
        for stock_code in stock_list['종목코드'].iloc:
            filename = f'resources/stock_market_data/{stock_code}.csv'
            try:    
                update_target = pd.read_csv(filename, parse_dates=['date'], index_col=[0])
            except FileNotFoundError:
                continue
            lastIdx = len(update_target) -1
            if update_target.open[lastIdx] == -1:
                update_target = update_target.drop([lastIdx])
                update_target.to_csv(filename)
    else:
        pd_lastSavedDate += pd.Timedelta(days=1)

    pd_dateRange = pd.date_range(pd_startDate, pd_destDate)

    for pd_date in pd_dateRange:
        # pd_date 날짜의 한국거래소 시장 데이터를 불러옵니다.
        df_update = get_market_ohlcv_by_ticker(pd_date)
        if not len(df_update) and pd_date != pd_destDate:
            continue
        df_update = df_update.reset_index()


        for stock_code in stock_list['종목코드'].iloc:
            filename = f'resources/stock_market_data/{stock_code}.csv'
            try:    
                update_target = pd.read_csv(filename, parse_dates=['date'], index_col=[0])
            except FileNotFoundError:
                continue

            if pd_date < pd_destDate:
                stock_ = df_update[df_update['종목코드'] == stock_code].values[0]
            else:
                stock_ = [-1, -1, -1, -1, -1, -1, -1]

            if pd_date >= pd_lastSavedDate:
                update_target = update_target.append({'date': pd_date, 'open': stock_[2], 'high': stock_[3], 'low': stock_[4], 'close': stock_[5], 'volume': stock_[6]},
                                                        ignore_index=True)
                last_idx = len(update_target)-1
                update_target['pattern1'].values[last_idx] = labellingD0(update_target.iloc[last_idx])
                update_target['new_pat1'].values[last_idx] = labellingD0_new(update_target.iloc[last_idx], update_target.close.values[last_idx-1])

                temp = update_target.values[last_idx]
                temp[0] = temp[0].date()
                temp = "".join([str(last_idx), ","]+[str(temp[i//2]) if i % 2 == 0 else "," for i in range(15)])
                temp += '\n'
                with open(filename, 'a', encoding='UTF-8') as f:
                    f.write(temp)
            else:
                target_idx = update_target[update_target.date == pd_date].index[0]
                update_target.open.values[target_idx] = stock_[2]
                update_target.high.values[target_idx] = stock_[3]
                update_target.low.values[target_idx] = stock_[4]
                update_target.close.values[target_idx] = stock_[5]
                update_target.volume.values[target_idx] = stock_[6]
                update_target.pattern1.values[target_idx] = labellingD0(update_target.iloc[target_idx])
                update_target.new_pat1.values[target_idx] = labellingD0_new(update_target.iloc[target_idx], update_target.close.values[target_idx-1])
                update_target.to_csv(filename)

def cleanup_stockData():
    '''
    테스트용으로 남은 columns를 지우고 필요한 데이터만을 남깁니다.
    '''
    for stock_code in stock_list['종목코드'].iloc:
        filename = f'resources/stock_market_data/{stock_code}.csv'
        try:    
            update_target = pd.read_csv(filename, parse_dates=['date'], index_col=[0])
        except FileNotFoundError:
            continue        
        update_target = update_target[['date','open','high','low','close','volume','pattern1']]
        update_target.to_csv(filename)

def add_new_pat1():
    '''
    'new_pat1' column을 모든 데이터에 추가합니다.
    '''
    for stock_code in stock_list['종목코드'].iloc:
        print(f'{stock_code}')
        filename = f'resources/stock_market_data/{stock_code}.csv'
        try:    
            update_target = pd.read_csv(filename, parse_dates=['date'], index_col=[0])
        except FileNotFoundError:
            continue

        try:
            update_target.new_pat1.values[0]
        except AttributeError:
            update_target['new_pat1'] = None

        for i in range(1,len(update_target)):
            update_target.new_pat1.values[i] = labellingD0_new(update_target.iloc[i], update_target.close.values[i-1])
        
        update_target = update_target[['date','open','high','low','close','volume','pattern1','new_pat1']]
        update_target.to_csv(filename)
# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------

# DUMMY

# nsq_p = pd.read_csv("resources/nasdaq.csv",
#                     parse_dates=['date'])[['date', 'nasdaq']]

def update_stockData():
    '''
    라벨링이 되지 않은 상태로 업데이트되므로, 대신 update_stockData_with_labels()를 사용하세요.
    '''
    # pd_가 붙은 것은 pd.timestamp, 붙지 않은 것은 'YYYY-MM-DD' 형식의 str
    pd_lastSavedDate = tail(open('resources/ohlcv/950200.csv'), 1)
    pd_lastSavedDate = pd_lastSavedDate[1][:10]
    pd_lastSavedDate = pd.to_datetime(pd_lastSavedDate)
    pd_destDate = pd.Timestamp.now()
    pd_destDate = pd.to_datetime(pd_destDate.date())

    # 데이터를 갱신할 날짜 범위
    pd_last_p1 = pd_lastSavedDate + pd.Timedelta(days=1)
    pd_dateRange = pd.date_range(pd_last_p1, pd_destDate)

    for pd_date in pd_dateRange:
        df_update = get_market_ohlcv_by_ticker(pd_date)
        if not len(df_update):  # 장이 열리지 않은 날이면 skip
            continue
        df_update = df_update.reset_index()
        for stock_ in df_update.iloc:
            stock_code = stock_['종목코드']
            filename = f'resources/ohlcv/{stock_code}.csv'
            str_date = str(pd_date.date())
            if (isfile(filename)):
                with open(filename, 'a', encoding='UTF-8') as f:
                    f.write(
                        f"{str_date},{stock_['시가']},{stock_['고가']},{stock_['저가']},{stock_['종가']},{stock_['거래량']}\n")
            else:
                new_stock = get_market_ohlcv_by_date(
                    "20120101", pd_date, stock_code)
                new_stock.to_csv(filename, encoding='UTF-8')
                sleep(1)


def get_stockData_using_stockCode(stockCode, wr=False):
    '''
    라벨링되지 않은 데이터의 모든 행에 라벨링 작업을 수행하므로, 대신 update_stockData_with_labels()를 사용하세요.
    '''
    stockData = pd.read_csv(
        'resources/ohlcv/{}.csv'.format(stockCode), parse_dates=['날짜'])
    stockData.columns = pd.Index(
        ["date", "open", "high", "low", "close", "volume"])

    stockData['pattern1'] = None
    for i in range(len(stockData)):
        stockData['pattern1'].values[i] = labellingD0(stockData.iloc[i])

    stockData['pattern2'] = None
    for i in range(1, len(stockData)):
        stockData['pattern2'].values[i] = labellingD1(stockData.iloc[i-1:i+1])

    stockData['pattern3'] = None
    for i in range(2, len(stockData)):
        stockData['pattern3'].values[i] = labellingD2(stockData.iloc[i-2:i+1])

    # stockData = pd.merge(stockData, nsq_p, on='date', how='left')
    # nan_list = stockData[stockData['nasdaq'].isnull()].index
    # stockData['nasdaq'].fillna(-1)

    # 해당 날짜에 나스닥 지수가 존재하지 않을 경우, 이전 날짜의 나스닥 지수를 적용합니다.
    # for i in nan_list:
    #     pointer = i
    #     while (pointer > 0):
    #         pointer -= 1
    #         temp = stockData['nasdaq'].values[pointer]
    #         if temp != -1:
    #             stockData['nasdaq'].values[i] = temp
    #             break

    if wr:
        stockData.to_csv(f"resources/stock_market_data/{stockCode}.csv")

    return stockData


def call_nasdaq():
    '''
    나스닥 지수 데이터를 최신으로 불러옵니다.
    '''
    today = pd.Timestamp.now()
    today = str(today.year)+"-"+str(today.month)+"-"+str(today.day)
    nq = DataReader('IXIC', '2012-01-01', today)
    nq = nq.reset_index()
    nq.columns = pd.Index(["date", "close", "open", "high",
                           "low", "volume", "change"], name=nq.columns.name)

    # date 쪼개기
    nq_date = pd.DataFrame(nq['date'])

    # 아래에 빈 행 추가
    nq_date.loc['today'] = pd.to_datetime(today)
    nq_date.reset_index(inplace=True)

    del nq_date['index']

    # 나머지 컬럼들
    nq_remain = pd.DataFrame(nq[['close', 'open', 'change']])

    # 윗 행 생성
    first_row = {'close': [0], 'open': [0], 'change': [0]}
    first_row = pd.DataFrame(first_row)

    # 윗 행 합치기
    plus_data = pd.concat([first_row, nq_remain])

    #reset_index
    plus_data.reset_index(inplace=True)

    #del index
    del plus_data['index']

    # date + plus_data
    nsq_data = pd.concat([nq_date, plus_data], axis=1)

    # clean variables
    del nq_date, plus_data, first_row, nq, nq_remain

    # 라벨링 작업
    nsq_data['nasdaq'] = None
    for i in range(1, len(nsq_data)):
        temp = nsq_data['change'].values[i]
        nsq_data['nasdaq'].values[i] = labellingNASDAQ(temp)

    nsq_data = nsq_data[['date','nasdaq']]
    nsq_data.to_csv("resources/nasdaq.csv")

# # 데이터 modify용
# def check_labellingNASDAQ(stockCode=None):
#     if stockCode == None:
#         check_list = stock_list['종목코드'].iloc
#     elif type(stockCode) == str:
#         check_list = [stockCode]
#     elif type(stockCode) == list:
#         check_list = stockCode
#     else:
#         raise Exception("^~^")

#     for stock_code in check_list:
#         filename = f'resources/stock_market_data/{stock_code}.csv'
#         try:    # 갱신 대상 데이터 불러오기
#             check_target = pd.read_csv(filename, parse_dates=['date'], index_col=[0])
#         except FileNotFoundError:
#             continue

#         check_target = pd.merge(check_target[check_target.columns[0:9]], nsq_p, on='date', how='left')
#         nan_list = check_target[check_target['nasdaq'].isnull()].index
#         check_target['nasdaq'].fillna(-1)

#         # 해당 날짜에 나스닥 지수가 존재하지 않을 경우, 이전 날짜의 나스닥 지수를 적용합니다.
#         for i in nan_list:
#             pointer = i
#             while (pointer > 0):
#                 pointer -= 1
#                 temp = check_target['nasdaq'].values[pointer]
#                 if temp != -1:
#                     check_target['nasdaq'].values[i] = temp
#                     break

#         check_target.to_csv(filename, encoding="UTF-8")