import pandas as pd
import numpy as np

def tripleScreenAnalysis(emaSpan, startDate = None, endDate = None, memo="", GWAMAESU=80, VOLUME=500000):
    '''
    삼중창 매매 시스템의 기준 중 EMA와 stochastic(Fast-K) 지표를 활용합니다.

    '''
    stock_list = pd.read_csv("resources/stockcode.csv",dtype = {"종목코드": str}, index_col=[0])
    df_res = pd.DataFrame({"날짜":[],"종목코드":[],"회사명":[],'거래량':[]})


    for idx in range(len(stock_list)):
        stockcode = stock_list.iloc[idx]
        stockname = stockcode.회사명
        stockcode = stockcode.종목코드

        # if stockcode == "068760":
            # print("????") # 종단점 찍고 디버깅할 용도의 코드

        df = pd.read_csv(f"resources/stock_market_data/{stockcode}.csv", parse_dates=['date'], index_col=[0])
        df = df[['date','open','high','low','close','volume']]
        lastIdx = len(df) -1

        # 더미 데이터 제거
        if df.open.values[lastIdx] == -1:
            df = df.drop([lastIdx])
        if df.volume.values[-1] < VOLUME:
            continue

        # EMA: 종가의 span일 지수 이동평균. span=60일 경우 60일(12주)
        ema = df.close.ewm(span=emaSpan).mean()
        df = df.assign(ema=ema).dropna()

        # Stochastic: 지난 5일 동안의 거래 범위에서 현재 가격의 위치
        ndays_high = df.high.rolling(window=5, min_periods=1).max()
        ndays_low = df.low.rolling(window=5, min_periods=1).min()
        fast_k = (df.close - ndays_low) / (ndays_high - ndays_low) * 100
        df = df.assign(fast_k=fast_k).dropna()

        if startDate is None and endDate is None:
            df = df.iloc[[-2,-1]]
        elif endDate is None:
            startDate = pd.Timestamp(startDate)
            temp1 = np.where(df.date >= startDate)[0][0]
            df = df.iloc[temp1-1 : len(df)]
        elif startDate is None:
            endDate = pd.Timestamp(endDate)
            temp2 = np.where(df.date <= endDate)[0]
            temp2 = temp2[len(temp2)-1]
            df = df.iloc[temp2-1:temp2+1]
        else:
            startDate = pd.Timestamp(startDate)
            endDate = pd.Timestamp(endDate)
            temp1 = np.where(df.date >= startDate)[0][0]
            temp2 = np.where(df.date <= endDate)[0]
            temp2 = temp2[len(temp2)-1]
            df = df.iloc[temp1-1:temp2+1]

        for i in range(1,len(df)):
            if (df.close.values[i] + df.open.values[i] + df.high.values[i] + df.low.values[i])*df.volume.values[i] < 40000000000:
                continue

            if df.ema.values[i-1] < df.ema.values[i]:
                if df.fast_k.values[i] >= 20 and df.fast_k.values[i] < GWAMAESU and df.fast_k.values[i-1] < 20:
                    df_res = df_res.append({'날짜':df.date.values[i],'종목코드':stockcode,'회사명':stockname,'거래량':df.volume.values[i]},ignore_index=True)

    df_res = df_res.sort_values(by=['날짜'])
    df_res = df_res.reset_index(drop=True)
    df_res.to_csv(f"resources/TripleScreen{emaSpan}_{memo}.csv")




if __name__ == "__main__":
    # tripleScreenAnalysis(60, startDate = "2018-11-01", endDate = "2020-10-31", memo="ts80")
    pass