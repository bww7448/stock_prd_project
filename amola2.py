from sklearn.metrics import confusion_matrix, classification_report
from modules.stockpred_apriori import stockpred_apriori


sample_df = stockpred_apriori(
    stock_code="all", weight=0.1, min_P_score=80, N_items=3)
print(sample_df)
print(confusion_matrix(sample_df["predict"], sample_df["real"]))
print(classification_report(sample_df["predict"], sample_df["real"]))
