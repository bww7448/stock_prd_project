import pandas as pd
# from sklearn.metrics import confusion_matrix, classification_report
# from modules.stockpred_apriori import stockpred_apriori
from modules.load_data import get_stockData_using_stockCode


#sample_df = stockpred_apriori(stock_code=None, weight=0.05, min_P_score=20, N_items=3)
#print(sample_df)
#print(confusion_matrix(sample_df["predict"], sample_df["real"]))
#print(classification_report(sample_df["predict"], sample_df["real"]))

stock_list2 = pd.read_csv('resources/stockcode.csv',
                          dtype={"종목코드": str, "회사명": str})
r = 0
for i in stock_list2["종목코드"]:
    r += 1
    df = get_stockData_using_stockCode(i)
    df.to_csv("resources/ohlcv_p1p2p3_nasdq/{}.csv".format(i))
    print("{}저장 완료({}번째)".format(i, r))
# stock_list2 = pd.read_csv('resources/stockcode.csv', dtype = {"종목코드": str, "회사명": str})
# stockData = pd.read_csv('resources/ohlcv/{}.csv'.format("000020"), parse_dates=['날짜'])
# print(stockData)
# df = get_stockData_using_stockCode("000020")
# print(df)
