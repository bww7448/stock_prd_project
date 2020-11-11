from modules.load_data import update_stockData_with_labels
from modules.triple_screen import tripleScreenAnalysis
from modules.samjung_stock_pred_test import samjung_stock_pred

from sklearn.metrics import confusion_matrix, classification_report
from time import time


if __name__ == "__main__":

    startTime = time()
    update_stockData_with_labels()
    endTime = time()
    print("데이터 업데이트 완료 -> spent time: {}ms".format((endTime - startTime)*1000))

    startTime = endTime
    tripleScreenAnalysis(60)
    endTime = time()
    print("분석 대상 종목 추출 완료 -> spent time: {}ms".format((endTime - startTime)*1000))

    samjung_test = samjung_stock_pred(day_weight=0.5, N_items=5)
    print(samjung_test)
    samjung_test.to_csv("resources/1111_recommend.csv", encoding = "euc-kr")
    print(confusion_matrix(samjung_test["predict"], samjung_test["real"]))
    print(classification_report(samjung_test["predict"], samjung_test["real"]))
    