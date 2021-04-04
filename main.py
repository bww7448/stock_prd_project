from modules.load_data import update_stockData_with_labels, update_valid_stocklist
from modules.triple_screen import tripleScreenAnalysis
from modules.samjung_stock_pred_test import samjung_stock_pred
from modules.warehouse import get_strDate

# from sklearn.metrics import confusion_matrix, classification_report
from time import time


if __name__ == "__main__":

    startTime = time()
    update_stockData_with_labels()
    endTime = time()
    print("데이터 업데이트 완료 -> spent time: {}ms".format((endTime - startTime)*1000))

    # # TODO: 시점 결정을 자동으로
    # update_valid_stocklist("20210402")

    startTime = time()
    tripleScreenAnalysis(60)
    endTime = time()
    print("분석 대상 종목 추출 완료 -> spent time: {}ms".format((endTime - startTime)*1000))

    samjung_test = samjung_stock_pred(day_weight=0.5, N_items=5)
    print(samjung_test)
    samjung_test.to_csv(f"resources/RECOMMEND/{get_strDate(1)}_recommend.csv", encoding = "euc-kr")
    #print(confusion_matrix(samjung_test["predict"], samjung_test["real"]))
    #print(classification_report(samjung_test["predict"], samjung_test["real"]))
    