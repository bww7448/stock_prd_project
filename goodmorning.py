from modules.load_data import *
from time import time


if __name__ == "__main__":
    '''
    csv 갱신용
    '''
    startTime = time()

    update_stockData_with_labels()

    
    endTime = time()
    print("time: {}ms".format((endTime - startTime)*1000))
    
