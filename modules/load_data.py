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

    # 장 마감 시간이 지나지 않으면 오늘의 결과를, 지나면 다음 날의 결과를 예측함
    pd_destDate = pd.to_datetime(pd.Timestamp.now() - pd.Timedelta(hours=15.5))
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

        # 너무 많은 요청 시 IP block을 방지하기 위한 sleep
        timeSleep = 1+2*random()
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