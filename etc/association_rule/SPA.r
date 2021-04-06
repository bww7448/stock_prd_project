df_test = read.csv("samsung.csv", encoding="UTF-8")
df_test

Date(df_test['날짜'], "YYYY-MM-DD")

seq_rule_1 <- cspade(df_test,
                     parameter = list(support = 0.3, maxsize = 5, maxlen = 4), 
                     control= list(verbose = TRUE))


data(zaki)
str(zaki)

# Formal class 'transactions' [package "arules"] with 3 slots
zaki
