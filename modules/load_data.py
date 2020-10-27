import pandas as pd
import FinanceDataReader as fdr
from modules.pattern_labelling import * 
import sys

# 나스닥지수 한국시간으로 맞추기
def call_nasdaq():
    '''
    나스닥 지수 데이터를 최신으로 불러옵니다.
    @ TODO: 파일이 존재할 경우, 없는 날짜만 불러와서 붙이기
    '''
    today = pd.Timestamp.now()
    today = str(today.year)+"-"+str(today.month)+"-"+str(today.day)
    nq = fdr.DataReader('IXIC', '2012-01-01', today)
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

    # nsq_data = nsq_data[['date','nasdaq']]
    nsq_data.to_csv("resources/nasdaq.csv")


def get_stockData_using_stockCode(stockCode, wr=False):
    '''
    주식 데이터을 라벨링해서 불러옵니다.\n
    wr=True 시, 라벨링된 데이터를 저장합니다.
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
        stockData.to_csv(f"resources/ohlcv_p1p2p3_nasdq/{stockData.columns.name}.csv")

    return stockData


def write_stockData_to_csv():
    '''
    테스트용, 기업 입력해서 데이터 임시로 불러오기
    '''
    sys.stdout.write("[Labelling Test]\n불러올 기업명을 입력하시오: ")
    comName = sys.stdin.readline().rstrip()
    stockCode = pd.read_csv("resources/stockcode.csv")
    try:
        stockCode = str(int(stockCode[stockCode['회사명'] == comName]['종목코드']))
    except:
        sys.stdout.write("유효하지 않은 입력입니다. \n")
        return -1

    target = get_stockData_using_stockCode(stockCode)
    target.to_csv(f"resources/{comName}.csv")

def update_stockData():
    '''
    주식 데이터를 생성하거나 최신 버전으로 갱신합니다.
    '''
    pass
