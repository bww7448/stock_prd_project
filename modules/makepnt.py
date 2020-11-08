import pandas as pd
from time import time
import numpy as np

def tripleScreenAnalysis(emaSpan, startDate = None, endDate = None):

    startTime = time()

    stock_list = pd.read_csv("resources/stockcode.csv",dtype = {"종목코드": str, "회사명": str}, index_col=[0])
    df_res = pd.DataFrame({"날짜":[],"종목코드":[],"회사명":[],'거래량':[]})
    df_res_modified = pd.DataFrame({"날짜":[],"종목코드":[],"회사명":[],'거래량':[]})


    for idx in range(len(stock_list)):
        stockcode = stock_list.iloc[idx]
        stockname = stockcode.회사명
        stockcode = stockcode.종목코드

        df = pd.read_csv(f"resources/ohlcv_p1p2p3_nasdq/{stockcode}.csv", parse_dates=['date'], index_col=['date'])
        today = pd.Timestamp.now().date()
        if df.iloc[-1].name != today:
            raise Exception("리소스가 최근 파일이 아닙니다. 먼저 리소스를 갱신해주세요.")   # TODO: 필터 다르게 넣어야함
        else:
            df = df[['open','high','low','close','volume']].iloc[0:len(df)-1]

        if df.volume.values[-1] < 50000:
            continue
        ema = df.close.ewm(span=emaSpan).mean()
        df = df.assign(ema=ema).dropna()

        ndays_high = df.high.rolling(window=5, min_periods=1).max()
        ndays_low = df.low.rolling(window=5, min_periods=1).min()

        fast_k = (df.close - ndays_low) / (ndays_high - ndays_low) * 100
        df = df.assign(fast_k=fast_k).dropna()

        if startDate is None and endDate is None:
            df = df.iloc[[-2,-1]]
        elif endDate is None:
            temp1 = np.where(df.index >= startDate)[0][0]
            df = df.iloc[temp1-1 : len(df)]
        elif startDate is None:
            temp2 = np.where(df.index <= endDate)[0]
            temp2 = temp2[len(temp2)-1]
            df = df.iloc[temp2-1:temp2+1]
        else:
            temp1 = np.where(df.index >= startDate)[0][0]
            temp2 = np.where(df.index <= endDate)[0]
            temp2 = temp2[len(temp2)-1]
            df = df.iloc[temp1-1:temp2+1]

        for i in range(1,len(df)):
            if df.ema.values[i-1] < df.ema.values[i]:
                if df.fast_k.values[i-1] >= 20 and df.fast_k.values[i] < 20:
                    df_res = df_res.append({'날짜':df.index.values[i],'종목코드':stockcode,'회사명':stockname,'거래량':df.volume.values[i]},ignore_index=True)
                elif df.fast_k.values[i] >= 20 and df.fast_k.values[i-1] < 20:
                    df_res_modified = df_res_modified.append({'날짜':df.index.values[i],'종목코드':stockcode,'회사명':stockname,'거래량':df.volume.values[i]},ignore_index=True)

    df_res = df_res.sort_values(by=['날짜'])
    df_res_modified = df_res_modified.sort_values(by=['날짜'])
    df_res.to_csv(f"resources/2year_tripleScreen{emaSpan}.csv")
    df_res_modified.to_csv(f"resources/new_tripleScreen_modified{emaSpan}.csv")

    endTime = time()

    print(f"{(endTime-startTime)*1000}ms")

if __name__ == "__main__":
    # tripleScreenAnalysis(60)
    tripleScreenAnalysis(60, "2020-11-04", "2020-11-09")