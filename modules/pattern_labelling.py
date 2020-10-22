from pykrx import stock
import sys
import pandas as pd


def labellingD0(d0) -> str:
    '''
    D0 시점의 각 봉에 대한 라벨링 25가지
    '''
    openP = d0['open']
    highP = d0['high']
    lowP = d0['low']
    closeP = d0['close']

    # 장대 양봉
    if closeP >= 1.1*openP:
        if closeP < highP:
            if openP > lowP:
                return "P15"
            if highP - 2*closeP + openP >= 0:
                return "P14"
            return "P13"
        if openP > lowP:
            return "P11"
        return "P10"

    # 짧은 양봉
    elif closeP >= 1.005*openP:
        if closeP < highP:
            if openP > lowP:
                return "P05"
            if highP - 3*closeP + 2*openP >= 0:
                return "P04"
            return "P03"
        if openP > lowP:
            if 2*highP - 3*openP + lowP >= 0:
                return "P01"
            return "P02"
        return "P00"

    # 보합
    elif closeP >= openP:
        end_min = closeP - lowP
        Max_end = highP - closeP
        if end_min > Max_end*3:
            return "K01"
        elif end_min*3 < Max_end:
            return "K02"
        return "K00"

    # 짧은 음봉
    elif closeP >= 0.9*openP:
        if openP < highP:
            if closeP > lowP:
                return "M05"
            if highP - 3*openP + 2*closeP < 0:
                return "M03"
            return "M04"
        if closeP > lowP:
            if 3*closeP - lowP - 2*openP < 0:
                return "M01"
            return "M02"
        return "M00"

    # 장대 음봉
    else:
        if closeP > lowP:
            if openP < highP:
                return "M15"
            return "M11"
        if openP < highP:
            if highP - 2*openP + closeP >= 0:
                return "M14"
            return "M13"
        return "M10"


def labellingD1(d10) -> str:
    '''
    D1 5가지 x D0 25가지
    '''
    temp = d10.iloc[0]
    openP = temp['open']
    # highP = temp['high']
    # lowP = temp['low']
    closeP = temp['close']

    # 장대 양봉
    if closeP >= 1.1*openP:
        res = "P10"

    # 짧은 양봉
    elif closeP >= 1.005*openP:
        res = "P00"

    # 보합
    elif closeP >= openP:
        res = "K00"

    # 짧은 음봉
    elif closeP >= 0.9*openP:
        res = "M00"

    # 장대 음봉
    else:
        res = "M10"

    return res + labellingD0(d10.iloc[1])


def labellingD2(d210):
    '''
    D2D1 12가지 x D0 25가지
    '''
    d2_openP = d210.iloc[0]['open']
    d2_closeP = d210.iloc[0]['close']
    d1_openP = d210.iloc[1]['open']
    d1_closeP = d210.iloc[1]['close']

    d21_max = max(d2_openP, d2_closeP, d1_openP, d1_closeP)
    d21_avg = (d21_max + min(d2_openP, d2_closeP, d1_openP, d1_closeP))/2
    if d21_max/d21_avg <= 1.005:
        res = "S04"
    elif d2_openP <= d2_closeP:  # D2 양봉
        if d1_openP <= d1_closeP:
            res = "P10"
        elif d2_openP >= d1_closeP:
            res = "S07"
        elif d2_closeP > d1_openP:
            res = "S06"
        elif d2_closeP >= d1_closeP:
            res = "S03"
        else:
            res = "S05"
    elif d2_openP >= d2_closeP:  # D2 음봉
        if d1_openP >= d1_closeP:
            res = "M10"
        elif d2_closeP < d1_openP:
            res = "S01"
        elif d2_openP <= d1_closeP:
            res = "S02"
        elif d2_closeP >= d1_closeP:
            res = "S08"
        else:
            res = "S00"
    else:
        res = "S09"

    return res + labellingD0(d210.iloc[2])


def write_stockData_to_csv():
    '''
    패터닝된 pd.DataFrame을 리턴하면서 csv 파일로 저장
    '''
    sys.stdout.write("[Labelling Test]\n불러올 기업명을 입력하시오: ")
    comName = sys.stdin.readline().rstrip()
    stockCode = pd.read_csv("resources/stockcode.csv")

    try:
        stockCode = str(int(stockCode[stockCode['회사명'] == comName]['종목코드']))
    except:
        sys.stdout.write("유효하지 않은 입력입니다. \n")
        return -1

    return get_stockData_using_stockCode(stockCode)


def get_stockData_using_stockCode(stockCode):
    print("Loading stock data from KRX...")
    stockCode = str(stockCode)
    stockCode = "0"*(6-len(stockCode)) + stockCode

    # today에 현재 시간을 불러옵니다.
    today = pd.Timestamp.now()
    today = str(today.year)+str(today.month)+str(today.day)

    stockData = stock.get_market_ohlcv_by_date("20120101", today, stockCode)
    comName = stockData.columns.name
    stockData.columns = pd.Index(
        ["open", "high", "low", "close", "volume"], name=comName)

    stockData['pattern1'] = None
    for i in range(len(stockData)):
        stockData['pattern1'].values[i] = labellingD0(stockData.iloc[i])

    stockData['pattern2'] = None
    for i in range(1, len(stockData)):
        stockData['pattern2'].values[i] = labellingD1(stockData.iloc[i-1:i+1])

    stockData['pattern3'] = None
    for i in range(2, len(stockData)):
        stockData['pattern3'].values[i] = labellingD2(stockData.iloc[i-2:i+1])

    # stockData.to_csv(f"resources/{stockData.columns.name}.csv")
    print(f"{comName}({stockCode})의 주식 데이터를 가져오는 데에 성공했습니다 (기간: 20120101~{today})")
    return stockData
