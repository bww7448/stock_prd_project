from modules.load_data import *
from time import time
from modules.triple_screen import tripleScreenAnalysis

if __name__ == "__main__":

    startTime = time()
    tripleScreenAnalysis(60)
    endTime = time()
    print("time: {}ms".format((endTime - startTime)*1000))