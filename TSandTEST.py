from modules.triple_screen import tripleScreenAnalysis
from modules.samjung_stock_pred_test import samjung_stock_pred


if __name__ == "__main__":
    # tripleScreenAnalysis(60, startDate = "2018-11-01", endDate = "2020-10-31", memo="ts70vol50", GWAMAESU=70, VOLUME=500000)
    # samjung_test = samjung_stock_pred(day_weight=0.5, N_items=5, memo="ts70vol50")
    # print(samjung_test)
    # samjung_test.to_csv("resources/RECOMMEND/ts70vol50_recommend.csv", encoding = "euc-kr")

    # tripleScreenAnalysis(60, startDate = "2018-11-01", endDate = "2020-10-31", memo="ts80vol50", GWAMAESU=80, VOLUME=500000)
    # samjung_test = samjung_stock_pred(day_weight=0.5, N_items=5, memo="ts80vol50")
    # print(samjung_test)
    # samjung_test.to_csv("resources/RECOMMEND/ts80vol50_recommend.csv", encoding = "euc-kr")

    tripleScreenAnalysis(60, startDate = "2018-11-01", endDate = "2020-10-31", memo="ts90vol50", GWAMAESU=80, VOLUME=500000)
    samjung_test = samjung_stock_pred(day_weight=0.5, N_items=5, memo="ts90vol50")
    print(samjung_test)
    samjung_test.to_csv("resources/RECOMMEND/ts90vol50_recommend.csv", encoding = "euc-kr")