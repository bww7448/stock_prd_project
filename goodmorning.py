from modules.load_data import *
from time import time
from modules.makepnt import tripleScreenAnalysis


if __name__ == "__main__":
    '''
    csv 갱신용
    '''
    startTime = time()

    print("리소스를 업데이트 하는 중입니다...", end=" ")
    update_stockData_with_labels()
    print("DONE")

    # print("분석 대상을 추출중입니다...", end=" ")
    # tripleScreenAnalysis(60)
    # print("DONE")
    
    endTime = time()
    print("time: {}ms".format((endTime - startTime)*1000))
    
