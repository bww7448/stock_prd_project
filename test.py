from modules.load_data import *
from time import time


if __name__ == "__main__":

    startTime = time()
    # call_nasdaq()
    check_labellingNASDAQ()
    endTime = time()
    print("time: {}ms".format((endTime - startTime)*1000))