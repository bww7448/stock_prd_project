# module import 영역
from modules.stockpred_apriori import stockpred_apriori


# main function 영역
if __name__ == "__main__":
    stockpred_apriori(1360,0.05,20,2)
    stockpred_apriori(1360,0.05,20,3)