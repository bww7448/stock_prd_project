# module import 영역
from modules.stockpred_apriori import stockpred_apriori
from modules.load_data import *
from time import time

# main function 영역
if __name__ == "__main__":
    startTime = time()

    call_nasdaq()
    update_stockData_with_labels()
    
    endTime = time()
    print("time: {}ms".format((endTime - startTime)*1000))


'''
[하루 일과]
1) modules.load_data.call_nasdaq(today)로 nasdaq.csv 파일을 최신으로 갱신하기
'''