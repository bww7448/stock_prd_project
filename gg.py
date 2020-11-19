from modules.triple_screen import tripleScreenAnalysis
from modules.samjung_stock_pred_test import samjung_stock_pred
from time import time


if __name__ == "__main__":
    # startTime = time()
    # memo = "f190101_80"

    # tripleScreenAnalysis(60, startDate = "2019-01-01", endDate = "2020-10-31", memo=memo)
    # endTime = time()
    # print("분석 대상 종목 추출 완료 -> spent time: {}ms".format((endTime - startTime)*1000))

    # samjung_test = samjung_stock_pred(memo=memo)
    # print(samjung_test)
    # samjung_test.to_csv(f"resources/RECOMMEND/{memo}_recommend.csv", encoding = "euc-kr")
    

    startTime = time()
    memo = "f190101_90"

    tripleScreenAnalysis(60, startDate = "2019-01-01", endDate = "2020-10-31", GWAMAESU=80, memo=memo)
    endTime = time()
    print("분석 대상 종목 추출 완료 -> spent time: {}ms".format((endTime - startTime)*1000))

    samjung_test = samjung_stock_pred(memo=memo)
    print(samjung_test)
    samjung_test.to_csv(f"resources/RECOMMEND/{memo}_recommend.csv", encoding = "euc-kr")