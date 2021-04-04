import pandas as pd
import numpy as np

from pykrx.stock import get_market_ohlcv_by_ticker, get_market_ohlcv_by_date, get_market_ticker_list

from random import random
from time import sleep
from sys import stdout

from modules.pattern_labelling import labellingD0


stock_list = pd.read_csv("resources/stockcode.csv",
                         dtype={"종목코드": str})


def update_stockData_with_labels(start_date=None):
    '''
    pykrx를 이용하여 증시 데이터를 업데이트합니다.
    - start_date    갱신이 필요한 시점으로, 미입력 시 마지막으로 장 마감한 날짜부터 갱신됩니다.
                    장 마감 이전에 업데이트했을 경우 마지막 날짜의 데이터는 실제와 다를 수 있습니다.
                    형식은 'YYYYMMDD' 또는 Datetime
    '''
    sys_print = stdout.write    # stack print method

    pd_destDate = pd.to_datetime(pd.Timestamp.now() - pd.Timedelta(hours=15.5)) # 15시 30분이 지나기 전까지는 증시 데이터는 전날까지만 로드
    pd_destDate = pd.to_datetime(pd_destDate.date())

    if start_date is None:
        # TODO: 상장된 종목 리스트 갱신, 충분한 양의 데이터가 쌓인 종목만 선별
        with open('resources/stock_market_data/900140.csv', 'r') as file:
            standard = file.readlines()
        standard = standard[-2].split(",")  # 장 마감 전 업데이트했을 가능성을 고려하여 어제를 갱신 대상에 포함시킴
        pd_startDate = pd.to_datetime(standard[1])
    else:
        pd_startDate = pd.to_datetime(start_date)

    sys_print("증시 데이터 로드를 시작합니다.\n")
    pd_dateRange = pd.date_range(pd_startDate, pd_destDate)
    df_update_all = pd.DataFrame()
    for pd_date in pd_dateRange:
        # pd_date 날짜의 한국거래소 시장 데이터를 불러옵니다.
        df_update = get_market_ohlcv_by_ticker(pd_date)
        if df_update.거래량.sum() == 0:
            sys_print(f"{str(pd_date)} 에는 증시 데이터가 없습니다.\n")
            continue
        df_update = df_update.reset_index()
        df_update = df_update[df_update.시가 > 0]   # 거래정지된 종목은 종가를 제외한 column이 0으로 채워짐

        df_update['date'] = pd_date
        df_update_all = df_update_all.append(df_update)

        timeSleep = 1+2*random()    # 너무 많은 요청 시 IP block을 방지. 작업량이 적은 경우 0으로 설정하세요.
        sys_print(f"{str(pd_date)} 의 증시 데이터를 로드했습니다 --- {timeSleep:.2f}초 대기\n")
        sleep(timeSleep)

    df_update_all.rename(columns={'티커':'종목코드'}, inplace=True) # TODO: 리소스 자체의 column명을 변경
    sys_print("필요한 증시 데이터 로드 완료.\n")

    for stock_code in stock_list['종목코드'].iloc:
        filename = f'resources/stock_market_data/{stock_code}.csv'
        try:
            update_target = pd.read_csv(filename, parse_dates=[
                                        'date'], index_col=[0])
        except FileNotFoundError:
            continue

        try:
            while pd_startDate <= update_target.date.iloc[-1]:
                update_target = update_target.drop(len(update_target)-1)
        except IndexError:
            pass    # start_date보다 상장일이 더 최신

        start = len(update_target)
        update_obj = df_update_all[df_update_all['종목코드'] == stock_code]
        update_obj = update_obj[['date', '시가', '고가', '저가', '종가', '거래량']]
        update_obj.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        update_target = update_target.append(update_obj)
        update_target = update_target.reset_index(drop=True)

        for i in range(start, len(update_target)):
            update_target.pattern1.values[i] = labellingD0(
                update_target.iloc[i])

        lastline = {'date': pd.to_datetime(pd_destDate + pd.Timedelta(days=1)),
                    'open': -1,
                    'high': -1,
                    'low': -1,
                    'close': -1,
                    'volume': -1,
                    'pattern1': "XXX"}
        update_target = update_target.append(lastline, ignore_index=True)
        update_target.to_csv(filename)
        sys_print(f"{stock_code} 갱신 완료\n")

def update_valid_stocklist(date):
    '''
    date 기준으로 상장된 종목 리스트를 업데이트합니다.
    '''
    stockList = get_market_ticker_list(date)
    stockList.sort()
    stockList = np.array(stockList)
    np.save("resources/stockList", stockList)

def cleanup_columns():
    '''
    필요한 columns를 제외한 나머지 더미 데이터를 제거합니다.
    '''
    for stock_code in stock_list['종목코드'].iloc:
        filename = f'resources/stock_market_data/{stock_code}.csv'
        try:
            update_target = pd.read_csv(filename, parse_dates=[
                                        'date'], index_col=[0])
        except FileNotFoundError:
            continue
        update_target = update_target[[
            'date', 'open', 'high', 'low', 'close', 'volume', 'pattern1']]
        update_target.to_csv(filename)


# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------

# # TEMP SAVED

# from os.path import isfile
# from FinanceDataReader import DataReader

# nsq_p = pd.read_csv("resources/nasdaq.csv",
#                     parse_dates=['date'])[['date', 'nasdaq']]

# def update_stockData():   # TODO: tail 제거
#     '''
#     라벨링이 되지 않은 상태로 업데이트되므로, 대신 update_stockData_with_labels()를 사용하세요.
#     '''
#     # pd_가 붙은 것은 pd.timestamp, 붙지 않은 것은 'YYYY-MM-DD' 형식의 str
#     pd_lastSavedDate = tail(open('resources/ohlcv/950200.csv'), 1)
#     pd_lastSavedDate = pd_lastSavedDate[1][:10]
#     pd_lastSavedDate = pd.to_datetime(pd_lastSavedDate)
#     pd_destDate = pd.Timestamp.now()
#     pd_destDate = pd.to_datetime(pd_destDate.date())

#     # 데이터를 갱신할 날짜 범위
#     pd_last_p1 = pd_lastSavedDate + pd.Timedelta(days=1)
#     pd_dateRange = pd.date_range(pd_last_p1, pd_destDate)

#     for pd_date in pd_dateRange:
#         df_update = get_market_ohlcv_by_ticker(pd_date)
#         if not len(df_update):  # 장이 열리지 않은 날이면 skip
#             continue
#         df_update = df_update.reset_index()
#         for stock_ in df_update.iloc:
#             stock_code = stock_['종목코드']
#             filename = f'resources/ohlcv/{stock_code}.csv'
#             str_date = str(pd_date.date())
#             if (isfile(filename)):
#                 with open(filename, 'a', encoding='UTF-8') as f:
#                     f.write(
#                         f"{str_date},{stock_['시가']},{stock_['고가']},{stock_['저가']},{stock_['종가']},{stock_['거래량']}\n")
#             else:
#                 new_stock = get_market_ohlcv_by_date(
#                     "20120101", pd_date, stock_code)
#                 new_stock.to_csv(filename, encoding='UTF-8')
#                 sleep(1)


# def get_stockData_using_stockCode(stockCode, wr=False):
#     '''
#     라벨링되지 않은 데이터의 모든 행에 라벨링 작업을 수행하므로, 대신 update_stockData_with_labels()를 사용하세요.
#     '''
#     stockData = pd.read_csv(
#         'resources/ohlcv/{}.csv'.format(stockCode), parse_dates=['날짜'])
#     stockData.columns = pd.Index(
#         ["date", "open", "high", "low", "close", "volume"])

#     stockData['pattern1'] = None
#     for i in range(len(stockData)):
#         stockData['pattern1'].values[i] = labellingD0(stockData.iloc[i])

#     stockData['pattern2'] = None
#     for i in range(1, len(stockData)):
#         stockData['pattern2'].values[i] = labellingD1(stockData.iloc[i-1:i+1])

#     stockData['pattern3'] = None
#     for i in range(2, len(stockData)):
#         stockData['pattern3'].values[i] = labellingD2(stockData.iloc[i-2:i+1])

#     # stockData = pd.merge(stockData, nsq_p, on='date', how='left')
#     # nan_list = stockData[stockData['nasdaq'].isnull()].index
#     # stockData['nasdaq'].fillna(-1)

#     # 해당 날짜에 나스닥 지수가 존재하지 않을 경우, 이전 날짜의 나스닥 지수를 적용합니다.
#     # for i in nan_list:
#     #     pointer = i
#     #     while (pointer > 0):
#     #         pointer -= 1
#     #         temp = stockData['nasdaq'].values[pointer]
#     #         if temp != -1:
#     #             stockData['nasdaq'].values[i] = temp
#     #             break

#     if wr:
#         stockData.to_csv(f"resources/stock_market_data/{stockCode}.csv")

#     return stockData


# def call_nasdaq():
#     '''
#     나스닥 지수 데이터를 최신으로 불러옵니다.
#     '''
#     today = pd.Timestamp.now()
#     today = str(today.year)+"-"+str(today.month)+"-"+str(today.day)
#     nq = DataReader('IXIC', '2012-01-01', today)
#     nq = nq.reset_index()
#     nq.columns = pd.Index(["date", "close", "open", "high",
#                            "low", "volume", "change"], name=nq.columns.name)

#     # date 쪼개기
#     nq_date = pd.DataFrame(nq['date'])

#     # 아래에 빈 행 추가
#     nq_date.loc['today'] = pd.to_datetime(today)
#     nq_date.reset_index(inplace=True)

#     del nq_date['index']

#     # 나머지 컬럼들
#     nq_remain = pd.DataFrame(nq[['close', 'open', 'change']])

#     # 윗 행 생성
#     first_row = {'close': [0], 'open': [0], 'change': [0]}
#     first_row = pd.DataFrame(first_row)

#     # 윗 행 합치기
#     plus_data = pd.concat([first_row, nq_remain])

#     #reset_index
#     plus_data.reset_index(inplace=True)

#     #del index
#     del plus_data['index']

#     # date + plus_data
#     nsq_data = pd.concat([nq_date, plus_data], axis=1)

#     # clean variables
#     del nq_date, plus_data, first_row, nq, nq_remain

#     # 라벨링 작업
#     nsq_data['nasdaq'] = None
#     for i in range(1, len(nsq_data)):
#         temp = nsq_data['change'].values[i]
#         nsq_data['nasdaq'].values[i] = labellingNASDAQ(temp)

#     nsq_data = nsq_data[['date','nasdaq']]
#     nsq_data.to_csv("resources/nasdaq.csv")

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
