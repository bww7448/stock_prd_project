from modules.load_data import update_stockData_with_labels, update_valid_stocklist
from modules.triple_screen import tripleScreenAnalysis
from modules.samjung_stock_pred_test import samjung_stock_pred
from modules.utiltools import get_strDate

# from sklearn.metrics import confusion_matrix, classification_report
from time import time


if __name__ == "__main__":

    # 증시 데이터 갱신
    startTime = time()
    update_stockData_with_labels()
    endTime = time()
    print("데이터 업데이트 완료 -> spent time: {}ms".format((endTime - startTime)*1000))


    # # TODO: 거래정지가 해제된 종목을 갱신할 수 있어야 함, 그때까지 사용 중지
    # pykrx에서 취급하는 KOSPI 상장종목 갱신
    # update_valid_stocklist("20210402")


    # 활용할 삼중창 지표 갱신
    startTime = time()
    tripleScreenAnalysis(60)
    endTime = time()
    print("분석 대상 종목 추출 완료 -> spent time: {}ms".format((endTime - startTime)*1000))


    # 상승할 것으로 예측된 종목을 resources/RECOMMEND 폴더에 기록
    samjung_test = samjung_stock_pred(day_weight=0.5, N_items=5)
    print(samjung_test)
    samjung_test.to_csv(f"resources/RECOMMEND/{get_strDate(1)}_recommend.csv", encoding = "euc-kr")


    # 검증용. 성능 테스트를 위한 이전 날짜 검증용으로만 사용할 것
    #print(confusion_matrix(samjung_test["predict"], samjung_test["real"]))
    #print(classification_report(samjung_test["predict"], samjung_test["real"]))
    