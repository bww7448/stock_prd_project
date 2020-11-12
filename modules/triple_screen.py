import pandas as pd
import numpy as np
from modules.warehouse import get_strDate

def tripleScreenAnalysis(emaSpan, startDate = None, endDate = None):

    stock_list = pd.read_csv("resources/stockcode.csv",dtype = {"종목코드": str, "회사명": str}, index_col=[0])
    df_res = pd.DataFrame({"날짜":[],"종목코드":[],"회사명":[],'거래량':[]})


    for idx in range(len(stock_list)):
        stockcode = stock_list.iloc[idx]
        stockname = stockcode.회사명
        stockcode = stockcode.종목코드

        # if stockcode == "068760":
            # print("????") # 디버깅용

        df = pd.read_csv(f"resources/stock_market_data/{stockcode}.csv", parse_dates=['date'], index_col=[0])
        df = df[['date','open','high','low','close','volume']]
        lastIdx = len(df) -1
        if df.open.values[lastIdx] == -1:
            df = df.drop([lastIdx])
        if df.volume.values[-1] < 1000000:
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
                if df.fast_k.values[i] >= 20 and df.fast_k.values[i] < 70 and df.fast_k.values[i-1] < 20:
                    df_res = df_res.append({'날짜':df.date.values[i],'종목코드':stockcode,'회사명':stockname,'거래량':df.volume.values[i]},ignore_index=True)

    df_res = df_res.sort_values(by=['날짜'])
    df_res = df_res.reset_index(drop=True)
    df_res.to_csv(f"resources/TripleScreen{emaSpan}.csv")

if __name__ == "__main__":
    tripleScreenAnalysis(60)
