import pandas as pd
from random import sample
from sklearn.metrics import confusion_matrix, classification_report
# U01, U02, U03, U04, D01, D02, D03, D04, T01
NASDAQ_weight = [
    [13.98,13.07,12.36,10.79,12.57,13.45, 6.88, 3.47,13.42],
    [13.48,14.49,13.70, 9.95,13.92,12.90, 5.62, 1.84,14.10],
    [13.45,14.59,15.48, 9.46,15.22,12.79, 4.56, 0.30,14.15],
    [11.63,10.88,10.28,14.28,10.46,12.07,11.03, 8.20,11.17],
    [13.41,14.50,14.87, 9.58,15.11,12.78, 4.88, 0.78,14.09],
    [13.41,12.54,11.86,11.37,12.06,13.92, 7.62, 4.35,12.88],
    [10.29, 9.63, 9.10,12.64, 9.25,10.68,15.52,13.01, 9.88],
    [ 9.80, 9.17, 8.67,12.04, 8.81,10.17,14.78,17.16, 9.41],
    [13.62,13.85,13.09,10.24,13.31,13.06, 6.10, 2.50,14.22]
]
NASDAQ_weight_dict = {"U01":0, "U02":1, "U03":2, "U04":3, "D01":4, "D02":5, "D03":6, "D04":7, "T01":8}

def get_NASDAQ_weight(standardL, relativeL):
    i = NASDAQ_weight_dict[standardL]
    j = NASDAQ_weight_dict[relativeL]
    return NASDAQ_weight[i][j]

def making_zzin(stock_code=None, day_weight=0.05, min_P_score=50, N_items=3, past_num = 1, nas_weight = 2) : #, last_date=None):
    '''
    n-items serial association rule analysis를 통해 다음 주식 패턴을 예측합니다.

    [parameter]
    - stock_code    종목코드를 int 또는 list 형태로 입력, 미입력 시 무작위로 샘플링한 10개의 종목으로 테스트합니다.
    - weight        시간에 따른 가중치를 입력합니다. 미입력 시 0.05로 적용됩니다.
    - min_P_score   입력된 값(0 ~ 100) 미만의 P_score를 보이는 결과는 보여주지 않습니다. 미입력 시 50으로 적용됩니다.
    - N_items       연관 규칙 시 장바구니에 묶을 item 수를 정합니다. 미입력 시 3개씩 묶습니다.
    - last_date      예측하고 싶은 마지막 시점을 "YYYYMMDD" 형식으로 입력합니다. 미입력 시 오늘 날짜로 입력됩니다.
    '''
    stock_pred_df = pd.DataFrame({'P_score': [], 'predict' : [],'real': [],'stock_name' : [], 'stock_code': [], 'Date' : []})
    # if last_date == None:
    #     # today에 현재 시간을 불러옵니다.
    #     today = pd.Timestamp.now()
    #     today = str(today.year)+str(today.month)+str(today.day)
    # else:
    #     today = str(last_date)
    stock_list = pd.read_csv('resources/stockcode.csv', dtype = {"종목코드": str, "회사명": str})
    if stock_code == None:
        stock_sample = sample(list(stock_list['종목코드']), 10)
    elif type(stock_code) == int:
        stock_sample = [stock_code]
    elif stock_code == "all":
        stock_sample = stock_list["종목코드"]
    elif type(stock_code) == list:
        stock_sample = stock_code.copy()
    else:
        raise TypeError("stock_code에 잘못된 parameter type이 입력되었습니다.")

    if N_items > 9 or N_items < 2:
        raise TypeError("N_items에는 2 이상 9 이하의 정수가 입력되어야 합니다.")
    himdlda = 1
    for stock_code in stock_sample:
        #stockData = get_stockData_using_stockCode(stock_code)
        stockData = pd.read_csv('resources/ohlcv_p1p2p3_nasdq/{}.csv'.format(stock_code), parse_dates=['date'], index_col=[0])
        pattern_count = 0
        # sssssa = stockData.volume[-1]
        # sssssa_val = sssssa.values[0]
        # if sssssa_val == 0:
        #     pass
        # else :
        if len(stockData) < 500 :
            pass
        else:
            ################################################################
            #테스트용으로 stockData 맨 밑에 줄 제거하기
            for drop_num in range(past_num) :
                stockData = stockData.drop(len(stockData)-1)
            #print(stockData)
            ################################################################
            if stockData.iloc[-1, 2] == 0 :
                pass
            elif stockData.iloc[-2, 2] == 0 :
                pass
            elif stockData.iloc[-3, 2] == 0 :
                pass
            elif stockData.iloc[-4, 2] == 0 :
                pass
            elif stockData.iloc[-5, 2] == 0 :
                pass
            else :
                bong_list = []
                for i in range(0, len(stockData) - N_items):
                    pattern_list = []
                    for n in range(N_items):
                        pattern_list.append(f"0{n+1}" + stockData["pattern1"][i+n])
                    bong_list.append(pattern_list)

                target = []
                for i in range(1, N_items):
                    target.append(f"0{i}" + stockData['pattern1'].iloc[-N_items-1+i])
                target_nasdaq = stockData['nasdaq'].iloc[-N_items]

                ssa = stock_list.회사명[stock_list['종목코드'] == stock_code]
                stock_name = ssa.values[0]

                A = {'P0': 0, 'P1': 0, 'M0': 0, 'M1': 0, 'K0': 0}
                A_pr = {'P_score': 0, 'real': stockData['pattern1'].iloc[-1], 'stock_name' : stock_name,
                        'stock_code': stock_code, 'Date' : stockData["date"].iloc[-1], 'Nasdaq' : stockData["nasdaq"].iloc[-1]}
                #print("연관 분석 시작... ", end="")
                for bong_order in range(len(bong_list)):
                    current_bong = bong_list[bong_order].copy()
                    next_bong = current_bong.pop()
                    if target == current_bong:
                        date_weight = (bong_order//10)*day_weight
                        nasdaq_weight = get_NASDAQ_weight(target_nasdaq, stockData['nasdaq'][bong_order+N_items])
                        score = 1 + date_weight + nas_weight*nasdaq_weight
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
                #print("완료")
                if (A['P0']+A['P1']+A['M0']+A['M1']+A['K0']) == 0:
                    pass
                    #print("[Failed] 연관 규칙이 발견되지 않았습니다.")
                elif pattern_count < 5 :
                    pass
                    #print("이전 관련 패턴 횟수가 부족합니다.")
                else:
                    A_pr['P_score'] = round(
                        ((A['P0']+A['P1']) / (A['P0']+A['P1']+A['M0']+A['M1']+A['K0']))*100, 2)
                    if A_pr['P_score'] >= min_P_score:
                        #print(A_pr)
                        predict = max(A.keys(), key = (lambda k : A[k]))
                        A_pred_df = pd.DataFrame({'P_score': [A_pr["P_score"]], 'predict' : [predict],'real':[ A_pr["real"][0:2]], 
                        'stock_name' : [A_pr['stock_name']], 'stock_code': [A_pr['stock_code']], 'Date' : [A_pr['Date']], 'Nasdaq' : [A_pr['Nasdaq']]})
                        stock_pred_df = stock_pred_df.append(A_pred_df)
                        himdlda += 1
                    #else:
                        #print("[Failed] 발견된 연관 규칙에서 유의미한 P_score를 보이지 않습니다.")
                #print()
                #print("won_do_su_seok")
        #if himdlda % 100 == 0 :
            #print(stock_pred_df)
    #stock_pred_df = stock_pred_df.set_index('stock_name')
    stock_pred_df = stock_pred_df.sort_values(by=['P_score'], axis=0, ascending = False)
    return stock_pred_df

zzin_df = pd.DataFrame({'P_score': [], 'predict' : [],'real':[], 'stock_name' : [], 'stock_code': [], 'Date' : [], 'Nasdaq' : []})
for i in range(5,105) :
    sample_df = making_zzin(stock_code="all", day_weight=0.05, nas_weight = 2, min_P_score=60, N_items=6, past_num = i).head()
    print(len(sample_df))
    zzin_df = zzin_df.append(sample_df)
print(zzin_df)
print(confusion_matrix(zzin_df["predict"], zzin_df["real"]))
print(classification_report(zzin_df["predict"], zzin_df["real"]))
zzin_df.to_csv("resources/item6_zzin_winlose_test.csv", encoding = "euc-kr")