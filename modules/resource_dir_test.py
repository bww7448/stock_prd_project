import pandas as pd
zzin_weight = pd.DataFrame({"day_weight" : [0], "nas_weight" : [0], "accuracy" : [0], "Nasdaq_weight" : ["mola"]})
zzin_weight.to_csv("/resources/item_best_te_100_test_df.csv" , encoding = "euc-kr")