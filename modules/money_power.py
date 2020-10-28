import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from random import sample
from sklearn.metrics import confusion_matrix, classification_report
from pattern_labelling import get_stockData_using_stockCode
from stock_pred_zzin import stockpred_apriori

zzin_df = pd.DataFrame({'P_score': [], 'predict' : [], 'stock_name' : [], 'stock_code': [], 'Date' : []})
sample_df = stockpred_apriori(stock_code="all", weight=0.03, min_P_score=65, N_items=7)
sample_df = sample_df.sort_values(by=['P_score'], axis=0, ascending=False).head(10)
zzin_df = zzin_df.append(sample_df)
print(zzin_df)
