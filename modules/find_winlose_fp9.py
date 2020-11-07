import pandas as pd
def win_lose_test(zzin_df = "zzin_df_item6", first_profit = 0.05, first_loss = 0.05, second_profit = 0.05, second_loss = 0.05, third_profit = 0.05):
    stock_list = pd.read_csv('resources/stockcode.csv', dtype = {"종목코드": str, "회사명": str}, encoding = "UTF-8")
    zzin_df = pd.read_csv('resources/{}.csv'.format(zzin_df), dtype = {"stock_code" :str}, parse_dates=['Date'], index_col=[0], encoding = "949")
    stock_sample = zzin_df["stock_code"]
    date_sample = zzin_df["Date"]
    win_lose_table = pd.DataFrame({"Date" : [],"stock_name" : [],"today_win" : [], "today_lose" : [], "tomorrow_win" : [], "tomorrow_lose" : [],
                                    "day2_win" : [], "day2_lose" : [], "real_profit" : [], "Nasdaq" : []})
    #print(stock_sample)
    for i in range (len(stock_sample)) :
        stock_code = str(stock_sample.iloc[i])
        if len(stock_code) == 6:
            pass
        else : 
            code_plus = "0" * (6 - len(stock_code))
            stock_code = code_plus + stock_code
        #print(stock_code)
        stock_date = date_sample.iloc[i]
        stockData = pd.read_csv('resources/ohlcv_p1p2p3_nasdq/{}.csv'.format(stock_code), parse_dates=['date'], index_col=[0])
        ssa = stock_list.회사명[stock_list['종목코드'] == stock_code]
        stock_name = ssa.values[0]
        vs_index = stockData.index[stockData['date'] == stock_date]
        win_lose_score = {"Date" : stock_date, "stock_name" : stock_name,
        "today_win" : 0, "today_lose" : 0, "tomorrow_win" : 0, "tomorrow_lose" : 0, "day2_win" : 0, "day2_lose" : 0,
        "real_profit" : 0, "Nasdaq" : stockData.iloc[vs_index]["nasdaq"].values[0]}
        first_bong = stockData.iloc[vs_index]
        #print(first_bong)
        second_bong = stockData.iloc[vs_index+1]
        #print(second_bong)
        third_bong = stockData.iloc[vs_index+2]
        #print(third_bong)
        buy_price = first_bong["open"].values[0]
        #print(buy_price)
        if buy_price * (1 + first_profit) < first_bong["high"].values[0]:
            win_lose_score["today_win"] += 1
            win_lose_score["real_profit"] += first_profit
        elif buy_price * (1.01)  <= first_bong["close"].values[0] :
            win_lose_score["today_win"] += 1
            win_lose_score["real_profit"] += ((first_bong["close"].values[0] - buy_price)/buy_price)
        elif buy_price * (1-first_loss) > first_bong["close"].values[0]:
            win_lose_score["today_lose"] += 1
            win_lose_score["real_profit"] += ((first_bong["close"].values[0] - buy_price)/buy_price)
        # elif buy_price * 1.01 < first_bong["close"].values[0] :
        #     win_lose_score["today_win"] += 1
        #     win_lose_score["real_profit"] += ((first_bong["close"].values[0] - buy_price) / buy_price )
        else :
            if buy_price * (1 + second_profit) < second_bong["high"].values[0] :
                win_lose_score["tomorrow_win"] += 1
                win_lose_score["real_profit"] += second_profit
            elif buy_price * (1.01) <= second_bong["close"].values[0] :
                win_lose_score["tomorrow_win"] += 1
                win_lose_score["real_profit"] += ((second_bong["close"].values[0] - buy_price)/buy_price)
            elif buy_price * (1-second_loss) > second_bong["close"].values[0] :
                win_lose_score["tomorrow_lose"] += 1
                win_lose_score["real_profit"] += ((second_bong["close"].values[0] - buy_price)/buy_price)
                #win_lose_score["real_profit"] += ((second_bong["close"].values[0] - buy_price)/buy_price)
            else :
                #if buy_price*0.95 > third_bong["low"].values[0] :
                    #win_lose_score["day2_lose"] += 1
                    #win_lose_score["real_profit"] += -0.05
                if buy_price * (1 + third_profit) < third_bong["high"].values[0] :
                    win_lose_score["day2_win"] += 1
                    win_lose_score["real_profit"] += third_profit
                else :
                    win_lose_score["day2_lose"] += 1
                    #if ((third_bong["close"].values[0] - buy_price)/buy_price) > -0.05:
                    win_lose_score["real_profit"] += ((third_bong["close"].values[0] - buy_price)/buy_price) 
                    #else :
                    #    win_lose_score["real_profit"] += -0.03

        win_lose_score_df = pd.DataFrame({"Date" : [win_lose_score["Date"]], "stock_name" : [win_lose_score["stock_name"]],
        "today_win" : [win_lose_score["today_win"]], "today_lose" : [win_lose_score["today_lose"]],
        "tomorrow_win" : [win_lose_score["tomorrow_win"]], "tomorrow_lose" : [win_lose_score["tomorrow_lose"]],
        "day2_win" : [win_lose_score["day2_win"]], "day2_lose" : [win_lose_score["day2_lose"]],
        "real_profit" : [win_lose_score["real_profit"]], "Nasdaq" : [win_lose_score["Nasdaq"]]})
        win_lose_table = win_lose_table.append(win_lose_score_df)
    #print(win_lose_table)
#    win_lose_table.to_csv("resources/fp3winlose_table.csv", encoding = 'euc-kr') 
    return win_lose_table
sum_real_profit = 0
for f_loss in range(0,10) :
    fir_loss = f_loss*0.01
    for s_profit in range(0,10) :
        sec_profit = s_profit*0.01
        for s_loss in range(0,10) :
            sec_loss = s_loss*0.01
            win_lose_table = win_lose_test(zzin_df = "best_100_df_5", first_profit = 0.09, first_loss = fir_loss, second_profit = sec_profit, second_loss = sec_loss, third_profit = 0.01)
            if win_lose_table['real_profit'].sum() > sum_real_profit :
                sum_real_profit = win_lose_table['real_profit'].sum()
                win_lose_table.to_csv("resources/fp9winlose_table_5.csv", encoding = 'euc-kr')
                print(fir_loss, sec_profit, sec_loss)
print(sum_real_profit)