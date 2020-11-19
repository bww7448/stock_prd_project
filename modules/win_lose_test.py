import pandas as pd


def win_lose_test(pred_list, first_profit=0.05, first_loss=0.05, second_profit=0.05, second_loss=0.05, third_profit=0.05):
    '''
    양봉으로 예측된 종목들을 실제로 매수하고 최대 3일 후 매도했을 때의 일차별 승률과 수익률을 계산합니다,
    - pred_list     예측종목 파일명을 '.csv'를 제외하고 입력
    - first_profit  첫날 익절 기준이 될 수익률
    - first_loss    첫날 손절 기준이 될 손실률
    - second_profit 둘째날 익절 기준이 될 수익률
    - second_loss   둘째날 손절 기준이 될 수익률
    - third_profit  마지막 날 익절 기준이 될 수익률.
                    마지막 날까지 조건에 충족하지 못했다면 '패배'
    '''
    stock_list = pd.read_csv('resources/stockcode.csv',
                             dtype={"종목코드": str}, encoding="UTF-8")
    try:
        pred_list = pd.read_csv(f'resources/{pred_list}.csv', dtype={
            "stock_code": str}, parse_dates=['Date'], index_col=[0], encoding="949")
    except UnicodeDecodeError:
        pred_list = pd.read_csv(f'resources/{pred_list}.csv', dtype={
            "stock_code": str}, parse_dates=['Date'], index_col=[0])
    stock_sample = pred_list["stock_code"]
    date_sample = pred_list["Date"]
    win_lose_table = pd.DataFrame({"Date": [], "stock_name": [], "today_big_win": [], "today_small_win": [], "today_lose": [],
                                   "tomorrow_big_win": [], "tomorrow_small_win": [], "tomorrow_lose": [],
                                   "day2_big_win": [], "day2_small_win": [], "day2_lose": [], "real_profit": []})

    for i in range(len(stock_sample)):
        if len(stock_code) != 6:
            code_plus = "0" * (6 - len(stock_code))
            stock_code = code_plus + stock_code
        print(stock_code)
        stock_date = date_sample.iloc[i]
        stockData = pd.read_csv(
            'resources/stock_market_data/{}.csv'.format(stock_code), parse_dates=['date'], index_col=[0])
        stock_name = stock_list.회사명[stock_list['종목코드'] == stock_code].values[0]
        vs_index = stockData.index[stockData['date'] == stock_date]
        win_lose_score = {"Date": stock_date, "stock_name": stock_name,
                          "today_big_win": 0, "today_small_win": 0, "today_lose": 0,
                          "tomorrow_big_win": 0, "tomorrow_small_win": 0, "tomorrow_lose": 0,
                          "day2_big_win": 0, "day2_small_win": 0, "day2_lose": 0,
                          "real_profit": 0}

        last_bong = stockData.iloc[vs_index-1]
        first_bong = stockData.iloc[vs_index]
        second_bong = stockData.iloc[vs_index+1]
        third_bong = stockData.iloc[vs_index+2]
        buy_price = last_bong["close"].values[0]

        # 오늘
        if buy_price * (1 + first_profit) < first_bong["high"].values[0]:
            win_lose_score["today_big_win"] += 1
            win_lose_score["real_profit"] += first_profit
        elif buy_price * (1.01) <= first_bong["close"].values[0]:
            win_lose_score["today_small_win"] += 1
            win_lose_score["real_profit"] += (
                (first_bong["close"].values[0] - buy_price)/buy_price)
        elif buy_price * (1-first_loss) > first_bong["close"].values[0]:
            win_lose_score["today_lose"] += 1
            win_lose_score["real_profit"] += (
                (first_bong["close"].values[0] - buy_price)/buy_price)

        # 다음날
        elif buy_price * (1 + second_profit) < second_bong["high"].values[0]:
            win_lose_score["tomorrow_big_win"] += 1
            win_lose_score["real_profit"] += second_profit
        elif buy_price * (1.01) <= second_bong["close"].values[0]:
            win_lose_score["tomorrow_small_win"] += 1
            win_lose_score["real_profit"] += (
                (second_bong["close"].values[0] - buy_price)/buy_price)
        elif buy_price * (1-second_loss) > second_bong["close"].values[0]:
            win_lose_score["tomorrow_lose"] += 1
            win_lose_score["real_profit"] += (
                (second_bong["close"].values[0] - buy_price)/buy_price)

        # 다다음날 (마지막 기회)
        elif buy_price * (1 + third_profit) < third_bong["high"].values[0]:
            win_lose_score["day2_big_win"] += 1
            win_lose_score["real_profit"] += third_profit
        elif buy_price * (1.01) <= third_bong["close"].values[0]:
            win_lose_score["day2_small_win"] += 1
            win_lose_score["real_profit"] += (
                (third_bong["close"].values[0] - buy_price)/buy_price)
        else:
            win_lose_score["day2_lose"] += 1
            win_lose_score["real_profit"] += (
                (third_bong["close"].values[0] - buy_price)/buy_price)

        win_lose_table = win_lose_table.append(
            win_lose_score, ignore_index=True)

    win_lose_table.to_csv(
        f"resources/{pred_list}_winlose_table_{first_profit*100},{first_loss*100},{second_profit*100},{second_loss*100},{third_profit*100}.csv", encoding='euc-kr')

    return win_lose_table


if __name__ == "__main__":
    win_lose_test(pred_list="wdhs_ver3/wdsh_ver3.9",
                  first_profit=0.1, first_loss=0.04,
                  second_profit=0.075, second_loss=0.03,
                  third_profit=0.05)
