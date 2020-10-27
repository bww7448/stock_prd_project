# module import 영역
from modules.stockpred_apriori import stockpred_apriori
from modules.load_data import *


# main function 영역
if __name__ == "__main__":
    # call_nasdaq()
    # write_stockData_to_csv()
    # stockpred_apriori(5930, min_P_score=0)

    # update_stockData()
    import pandas as pd
    list_stockCode = pd.read_csv("saved.csv", encoding="UTF-8", index_col=[0], dtype={'종목코드':str})

    for code in list_stockCode['종목코드']:
        get_stockData_using_stockCode(code, wr=True)



'''
[하루 일과]
1) modules.load_data.call_nasdaq(today)로 nasdaq.csv 파일을 최신으로 갱신하기
'''