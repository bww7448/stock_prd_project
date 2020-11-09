import pandas as pd
from os.path import isfile
from tailer import tail
from FinanceDataReader import DataReader
from pykrx import stock
from time import sleep

from modules.pattern_labelling import *

nsq_p = pd.read_csv("resources/nasdaq.csv",
                    parse_dates=['date'])[['date', 'nasdaq']]
stock_list = pd.read_csv("resources/stockcode.csv",
                         dtype={"종목코드": str, "회사명": str})


def update_stockData_with_labels(start_date=None, NOT_NEXT_DAY=True):
    '''
    라벨링된 데이터에 최신 주식 데이터를 업데이트합니다.
    '''
    pd_today = pd.to_datetime(pd.Timestamp.now().date())

    if NOT_NEXT_DAY:
        # 가장 마지막 주식 데이터의 갱신 상태를 확인해서 갱신할 날짜의 범위를 지정합니다.
        first_df = pd.read_csv(
            'resources/ohlcv_p1p2p3_nasdq/950200.csv', parse_dates=['date'], index_col=[0])
        if start_date == None:
            pd_last_date = first_df['date'].iloc[-1]    # 데이터의 마지막 행을 갱신 범위에 포함시킵니다.
        else:
            pd_last_date = pd.to_datetime(start_date)
        pd_drange = pd.date_range(pd_last_date, pd_today)
    else:
        # NOT_NEXT_DAY에 False 입력 시 
        pd_drange = [pd_today + pd.Timedelta(days=1)]

    for pd_date in pd_drange:
        df_update = stock.get_market_ohlcv_by_ticker(pd_date)
        if pd_date != pd_today and not len(df_update) and NOT_NEXT_DAY:  # 장이 열리지 않은 날이면 skip
            continue
        df_update = df_update.reset_index()

        for stock_code in stock_list['종목코드'].iloc:
            try:    # pykrx로 불러온 데이터에서 해당 주식 데이터 불러오기
                stock_ = df_update[df_update['종목코드'] == stock_code].values[0]
            except IndexError:
                # if len(df_update):
                #     raise Exception(f"{stock_code} 종목의 데이터가 정상적으로 로드되지 않았습니다.\n상장 폐지된 종목이라면 stockcode.csv를 갱신하세요.\n그렇지 않다면, 시간이 지난 후 다시 시도하세요.")
                stock_ = [pd_date,-1,-1,-1,-1,-1,-1]    # 거래정지, 상장폐지, ...

            filename = f'resources/ohlcv_p1p2p3_nasdq/{stock_code}.csv'
            try:    # 갱신 대상 데이터 불러오기
                update_target = pd.read_csv(filename, parse_dates=['date'], index_col=[0])
            except FileNotFoundError:
                continue

            if update_target['date'].values[-1] > pd_date:
                continue    # 이전에 오류나서 이미 일부가 업데이트된 상태인 경우, skip
            elif update_target['date'].values[-1] == pd_date:
                # 데이터의 마지막 행을 갱신합니다.
                update_target['open'].values[-1] = stock_[2]
                update_target['high'].values[-1] = stock_[3]
                update_target['low'].values[-1] = stock_[4]
                update_target['close'].values[-1] = stock_[5]
                update_target['volume'].values[-1] = stock_[6]
                flag = 0
            else:
                # 데이터를 추가합니다. 이 경우 pandas의 to_csv 대신 io를 이용합니다.
                update_target = update_target.append({'date': pd_date, 'open': stock_[2], 'high': stock_[3], 'low': stock_[4], 'close': stock_[5], 'volume': stock_[6]},
                                                     ignore_index=True)
                flag = 1

            # 갱신 혹은 추가된 데이터에 대해 새로 라벨링 작업을 진행합니다.
            last_idx = len(update_target)-1
            update_target['pattern1'].values[last_idx] = labellingD0(
                update_target.iloc[last_idx])
            update_target['pattern2'].values[last_idx] = labellingD1(
                update_target.iloc[last_idx-1:last_idx+1])
            update_target['pattern3'].values[last_idx] = labellingD2(
                update_target.iloc[last_idx-2:last_idx+1])
            # try:
            #     update_target['nasdaq'].values[last_idx] = nsq_p[nsq_p['date']
            #                                                      == pd_date].values[0][1]
            # except IndexError:
            #     update_target['nasdaq'].values[last_idx] = update_target['nasdaq'].values[last_idx-1]

            if flag:
                temp = update_target.values[last_idx]
                temp[0] = temp[0].date()
                for i in range(6):
                    temp[i] = str(temp[i])
                temp = "".join([str(last_idx), ","]+[str(temp[i//2]) if i % 2 == 0 else "," for i in range(19)])
                temp += '\n'
                with open(filename, 'a', encoding='UTF-8') as f:
                    f.write(temp)
            else:
                update_target.to_csv(filename)










# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------

# DUMMY

def update_stockData():
    '''
    라벨링이 되지 않은 상태로 업데이트되므로, 대신 update_stockData_with_labels()를 사용하세요.
    '''
    # pd_가 붙은 것은 pd.timestamp, 붙지 않은 것은 'YYYY-MM-DD' 형식의 str
    pd_last_date = tail(open('resources/ohlcv/950200.csv'), 1)
    pd_last_date = pd_last_date[1][:10]
    pd_last_date = pd.to_datetime(pd_last_date)
    pd_today = pd.Timestamp.now()
    pd_today = pd.to_datetime(pd_today.date())

    # 데이터를 갱신할 날짜 범위
    pd_last_p1 = pd_last_date + pd.Timedelta(days=1)
    pd_drange = pd.date_range(pd_last_p1, pd_today)

    for pd_date in pd_drange:
        df_update = stock.get_market_ohlcv_by_ticker(pd_date)
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
                new_stock = stock.get_market_ohlcv_by_date(
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

    stockData = pd.merge(stockData, nsq_p, on='date', how='left')
    nan_list = stockData[stockData['nasdaq'].isnull()].index
    stockData['nasdaq'].fillna(-1)

    # 해당 날짜에 나스닥 지수가 존재하지 않을 경우, 이전 날짜의 나스닥 지수를 적용합니다.
    for i in nan_list:
        pointer = i
        while (pointer > 0):
            pointer -= 1
            temp = stockData['nasdaq'].values[pointer]
            if temp != -1:
                stockData['nasdaq'].values[i] = temp
                break

    if wr:
        stockData.to_csv(f"resources/ohlcv_p1p2p3_nasdq/{stockCode}.csv")

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

# 데이터 modify용
def check_labellingNASDAQ(stockCode=None):
    if stockCode == None:
        check_list = stock_list['종목코드'].iloc
    elif type(stockCode) == str:
        check_list = [stockCode]
    elif type(stockCode) == list:
        check_list = stockCode
    else:
        raise Exception("^~^")

    for stock_code in check_list:
        filename = f'resources/ohlcv_p1p2p3_nasdq/{stock_code}.csv'
        try:    # 갱신 대상 데이터 불러오기
            check_target = pd.read_csv(filename, parse_dates=['date'], index_col=[0])
        except FileNotFoundError:
            continue

        check_target = pd.merge(check_target[check_target.columns[0:9]], nsq_p, on='date', how='left')
        nan_list = check_target[check_target['nasdaq'].isnull()].index
        check_target['nasdaq'].fillna(-1)

        # 해당 날짜에 나스닥 지수가 존재하지 않을 경우, 이전 날짜의 나스닥 지수를 적용합니다.
        for i in nan_list:
            pointer = i
            while (pointer > 0):
                pointer -= 1
                temp = check_target['nasdaq'].values[pointer]
                if temp != -1:
                    check_target['nasdaq'].values[i] = temp
                    break

        check_target.to_csv(filename, encoding="UTF-8")