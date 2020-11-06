from modules.load_data import *
from time import time


if __name__ == "__main__":
    '''
    평일 아침에 돌릴 것들
    '''
    startTime = time()

    call_nasdaq()
    update_stockData_with_labels()
    #check_labellingNASDAQ()
    
    endTime = time()
    print("time: {}ms".format((endTime - startTime)*1000))
