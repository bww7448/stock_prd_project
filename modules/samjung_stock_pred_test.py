import pandas as pd
# from sklearn.metrics import confusion_matrix, classification_report

def samjung_stock_pred(day_weight=0.5, N_items=5, memo=""):
    '''
    n-items serial association rule analysis를 통해 다음 주식 패턴을 예측합니다.

    [parameter]
    - day_weight        시간에 따른 가중치를 입력합니다. 미입력 시 0.05로 적용됩니다.
    - N_items       연관 규칙 시 장바구니에 묶을 item 수를 정합니다. 미입력 시 3개씩 묶습니다.
    '''
    #기본 데이터 셋 만들기
    all_stock_pred_df = pd.DataFrame({'P_score': [], 'predict' : [], 'real' : [], 'stock_name' : [], 'stock_code': [], 'Date' : []})
    stock_pred_df = pd.DataFrame({'P_score': [], 'predict' : [],'real' : [], 'stock_name' : [], 'stock_code': [], 'Date' : []})
    stock_list = pd.read_csv(f'resources/TripleScreen60_{memo}.csv', dtype = {"종목코드": str}, 
                             parse_dates = ['날짜'], index_col = [0])
    stock_date = "뒁이 바보"
    len_stock_list = len(stock_list)

    for list_num in range(len_stock_list):
        print(list_num, "/", len_stock_list)

        #날짜가 달라지면 all_stock_pred에 상위 5개만 저장
        if stock_list.iloc[list_num, 0] != stock_date :
            stock_pred_df = stock_pred_df.sort_values(by=['P_score'], axis=0, ascending = False)
            stock_pred_df = stock_pred_df.head()
            all_stock_pred_df = all_stock_pred_df.append(stock_pred_df)
            stock_pred_df = pd.DataFrame({'P_score': [], 'predict' : [],'stock_name' : [], 'stock_code': [], 'Date' : []})
            print(stock_date, "완료")
            
        #삼중창에서 날짜, 코드 찾고 그에 해당하는 데이터 불러오기
        stock_code = stock_list.iloc[list_num, 1]
        stock_date = stock_list.iloc[list_num, 0]
        stockData = pd.read_csv(f'resources/stock_market_data/{stock_code}.csv', parse_dates=['date'], index_col=[0])

        #stockData의 마지막 날짜를 stock_date와 맞추기
        while stockData.iloc[-1,0] != stock_date :
            stockData = stockData.drop(len(stockData)-1)
        if len(stockData) < 500 or\
            not stockData.iloc[-1, 2] or\
            not stockData.iloc[-2, 2] or\
            not stockData.iloc[-3, 2] or\
            not stockData.iloc[-4, 2] or\
            not stockData.iloc[-5, 2]:
            # 데이터를 분석하기에 너무 적은 데이터가 쌓여 있는 종목,
            # 거래가 멈춘 종목에 대해서는 분석 대상에서 제외합니다.
            continue

        # N_items개만큼 담은 장바구니 리스트를 생성합니다.
        bong_list = []
        for i in range(0, len(stockData) - N_items):
            pattern_list = []
            for n in range(N_items):
                pattern_list.append(f"0{n+1}" + stockData["pattern1"][i+n])
            bong_list.append(pattern_list)
        # 대상을 예측하기 위한 데이터를 모읍니다.
        target = []
        for i in range(1, N_items):
            target.append(f"0{i}" + stockData['pattern1'].iloc[-N_items-1+i])
        stock_name = stock_list.회사명[stock_list['종목코드'] == stock_code].values[0]

        A = {'P0': 0, 'P1': 0, 'M0': 0, 'M1': 0, 'K0': 0}
        A_pr = {'P_score': 0, 'real': stockData['pattern1'].iloc[-1], 
                'stock_name' : stock_name,'stock_code': stock_code, 'Date' : stockData["date"].iloc[-1]}
        pattern_count = 0
        for bong_order in range(len(bong_list)):
            current_bong = bong_list[bong_order].copy()
            next_bong = current_bong.pop()
            if target == current_bong:
                date_weight = (bong_order//10)*day_weight
                score = 1 + date_weight
                next_bong = next_bong[2:4]
                if "P0" == next_bong:
                    A["P0"] += score
                elif "P1" == next_bong:
                    A["P1"] += score
                elif "M0" == next_bong:
                    A["M0"] += score
                elif "M1" == next_bong:
                    A["M1"] += score
                elif "K0" == next_bong:
                    A["K0"] += score
                pattern_count += 1
        if pattern_count < 3 :
            continue    # 패턴이 일정 횟수 이상 발견되지 않으면 분석 대상에서 제외합니다.
        A_pr['P_score'] = round(
            ((A['P0']+A['P1']) / (A['P0']+A['P1']+A['M0']+A['M1']+A['K0']))*100, 2)
        predict = max(A.keys(), key = (lambda k : A[k]))
        A_pred_df = pd.DataFrame({'P_score': [A_pr["P_score"]], 'predict' : [predict], 'real':[ A_pr["real"][0:2]], 
            'stock_name' : [A_pr['stock_name']], 'stock_code': [A_pr['stock_code']], 'Date' : [A_pr['Date']]})
        stock_pred_df = stock_pred_df.append(A_pred_df)

    stock_pred_df = stock_pred_df.sort_values(by=['P_score'], axis=0, ascending = False)
    stock_pred_df = stock_pred_df.head()
    all_stock_pred_df = all_stock_pred_df.append(stock_pred_df)
    print("끝")
        
    return all_stock_pred_df


if __name__ == "__main__":
    samjung_test = samjung_stock_pred(day_weight=0.5, N_items=5)
    print(samjung_test)
    samjung_test.to_csv("resources/RECOMMEND/1110_recommend.csv", encoding = "euc-kr")
    # print(confusion_matrix(samjung_test["predict"], samjung_test["real"]))
    # print(classification_report(samjung_test["predict"], samjung_test["real"]))