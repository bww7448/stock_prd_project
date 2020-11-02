import pandas as pd
# from sklearn.metrics import confusion_matrix, classification_report
from modules.stock_pred_zzin import stockpred_apriori


if __name__ == "__main__":
    zzin_df = pd.DataFrame({'P_score': [], 'predict' : [], 'stock_name' : [], 'stock_code': [], 'Date' : []})
    sample_df = stockpred_apriori(stock_code="all", day_weight=0.05, nas_weight = 2,min_P_score=50, N_items=6)
    sample_df = sample_df.sort_values(by=['P_score'], axis=0, ascending=False).head(10)
    zzin_df = zzin_df.append(sample_df)
    print(zzin_df)
    # print(confusion_matrix(sample_df["predict"], sample_df["real"]))
    # print(classification_report(sample_df["predict"], sample_df["real"]))