# module import 영역
from modules.pattern_labelling import write_stockData_to_csv
from modules.stockpred_apriori import stockpred_apriori
from modules.load_data import call_nasdaq


# main function 영역
if __name__ == "__main__":
    # call_nasdaq()
    # write_stockData_to_csv("20201023")
    stockpred_apriori(5930, min_P_score=0)
'''
[하루 일과]
1) modules.load_data.call_nasdaq(today)로 nasdaq.csv 파일을 최신으로 갱신하기
'''