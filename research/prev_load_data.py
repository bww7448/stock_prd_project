
'''
나스닥 지수를 활용하려고 했으나 결과에 좋은 영향을 주지 않아 기각됨
'''

import pandas as pd
import numpy as np

from pykrx.stock import get_market_ohlcv_by_ticker, get_market_ohlcv_by_date, get_market_ticker_list

from random import random
from time import sleep
from sys import stdout

from modules.pattern_labelling import labellingD0

from os.path import isfile
from FinanceDataReader import DataReader

nsq_p = pd.read_csv("resources/nasdaq.csv",
                    parse_dates=['date'])[['date', 'nasdaq']]

def update_stockData():   # TODO: tail 제거
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
        filename = f'resources/stock_market_data/{stock_code}.csv'
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
