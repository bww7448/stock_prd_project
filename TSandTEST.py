from modules.triple_screen import tripleScreenAnalysis
from modules.samjung_stock_pred_test import samjung_stock_pred, samjung_stock_pred_new


if __name__ == "__main__":
    # tripleScreenAnalysis(60, startDate = "2018-11-01", endDate = "2020-10-31", memo="ts70vol50", GWAMAEDO=70, VOLUME=500000)
    # samjung_test = samjung_stock_pred(day_weight=0.5, N_items=5, memo="ts70vol50")
    # print(samjung_test)
    # samjung_test.to_csv("resources/RECOMMEND/ts70vol50_recommend.csv", encoding = "euc-kr")

    # tripleScreenAnalysis(60, startDate = "2018-11-01", endDate = "2020-10-31", memo="ts80vol50", GWAMAEDO=80, VOLUME=500000)
    # samjung_test = samjung_stock_pred(day_weight=0.5, N_items=5, memo="ts80vol50")
    # print(samjung_test)
    # samjung_test.to_csv("resources/RECOMMEND/ts80vol50_recommend.csv", encoding = "euc-kr")

    # samjung_test = samjung_stock_pred(day_weight=0.5, N_items=5, memo="ts90vol50")
    # print(samjung_test)
    # samjung_test.to_csv("resources/RECOMMEND/ts90vol50_recommend.csv", encoding = "euc-kr")



    tripleScreenAnalysis(60, startDate = "2019-01-01", endDate = "2020-10-31", memo="newtest")
    samjung_test = samjung_stock_pred_new(day_weight=0.5, N_items=5, memo='newtest')
    print(samjung_test)
    samjung_test.to_csv(f"resources/RECOMMEND/2years_new_recommend.csv", encoding = "euc-kr")