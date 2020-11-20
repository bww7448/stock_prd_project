import pandas as pd
from random import sample
from sklearn.metrics import confusion_matrix, classification_report
import random

def test_zzin(stock_code=None, day_weight=0.05, min_P_score=50, N_items=5, past_num = 1) : #, last_date=None):
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

    for stock_code in stock_sample:
        stockData = pd.read_csv('resources/stock_market_data/{}.csv'.format(stock_code), parse_dates=['date'], index_col=[0])
        pattern_count = 0
        if len(stockData) - past_num < 500 :
            pass
        else:
            ################################################################
            #테스트용으로 stockData 맨 밑에 줄 제거하기
            for _ in range(past_num) :
                stockData = stockData.drop(len(stockData)-1)
            #print(stockData)
            stockData = stockData.drop(0)
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
                        pattern_list.append(f"0{n+1}" + stockData["new_pat1"].iloc[i+n])
                    bong_list.append(pattern_list)
                target = []
                for i in range(1, N_items):
                    target.append(f"0{i}" + stockData['new_pat1'].iloc[-N_items-1+i])
                ssa = stock_list.회사명[stock_list['종목코드'] == stock_code]
                stock_name = ssa.values[0]
                A = {'P0': 0, 'P1': 0, 'M0': 0, 'M1': 0, 'K0': 0}
                A_pr = {'P_score': 0, 'real': stockData['new_pat1'].iloc[-1], 'stock_name' : stock_name,
                        'stock_code': stock_code, 'Date' : stockData["date"].iloc[-1]}
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
                if (A['P0']+A['P1']+A['M0']+A['M1']+A['K0']) == 0:
                    pass
                elif pattern_count < 5 :
                    pass
                else:
                    A_pr['P_score'] = round(
                        ((A['P0']+A['P1']) / (A['P0']+A['P1']+A['M0']+A['M1']+A['K0']))*100, 2)
                    if A_pr['P_score'] >= min_P_score:
                        predict = max(A.keys(), key = (lambda k : A[k]))
                        A_pred_df = pd.DataFrame({'P_score': [A_pr["P_score"]], 'predict' : [predict],'real':[ A_pr["real"][0:2]], 
                        'stock_name' : [A_pr['stock_name']], 'stock_code': [A_pr['stock_code']], 'Date' : [A_pr['Date']]})
                        stock_pred_df = stock_pred_df.append(A_pred_df)
    stock_pred_df = stock_pred_df.sort_values(by=['P_score'], axis=0, ascending = False)
    return stock_pred_df
######################################################################################################################################
if __name__ == "__main__":
    zzin_df = pd.DataFrame({'P_score': [], 'predict' : [],'real':[], 'stock_name' : [], 'stock_code': [], 'Date' : [], 'Nasdaq' : []})

    # for j in range(21,31) :
    #     sample_df = test_zzin(stock_code="all", day_weight=0.5, min_P_score=5, N_items=5, past_num = j).head()
    #     zzin_df = zzin_df.append(sample_df)
    #     print(f"{j} / 30")
    # zzin_df.to_csv("resources/new_labelling_test/new_labelling_test1.csv", encoding = "euc-kr")

    # for j in range(31,41) :
    #     sample_df = test_zzin(stock_code="all", day_weight=0.5, min_P_score=5, N_items=5, past_num = j).head()
    #     zzin_df = zzin_df.append(sample_df)
    #     print(f"{j} / 40")
    # zzin_df.to_csv("resources/new_labelling_test/new_labelling_test2.csv", encoding = "euc-kr")

    # for j in range(41,51) :
    #     sample_df = test_zzin(stock_code="all", day_weight=0.5, min_P_score=5, N_items=5, past_num = j).head()
    #     zzin_df = zzin_df.append(sample_df)
    #     print(f"{j} / 50")
    # zzin_df.to_csv("resources/new_labelling_test/new_labelling_test3.csv", encoding = "euc-kr")

    # for j in range(51,61) :
    #     sample_df = test_zzin(stock_code="all", day_weight=0.5, min_P_score=5, N_items=5, past_num = j).head()
    #     zzin_df = zzin_df.append(sample_df)
    #     print(f"{j} / 60")
    # zzin_df.to_csv("resources/new_labelling_test/new_labelling_test4.csv", encoding = "euc-kr")

    # for j in range(61,71) :
    #     sample_df = test_zzin(stock_code="all", day_weight=0.5, min_P_score=5, N_items=5, past_num = j).head()
    #     zzin_df = zzin_df.append(sample_df)
    #     print(f"{j} / 70")
    # zzin_df.to_csv("resources/new_labelling_test/new_labelling_test5.csv", encoding = "euc-kr")

    # for j in range(71,81) :
    #     sample_df = test_zzin(stock_code="all", day_weight=0.5, min_P_score=5, N_items=5, past_num = j).head()
    #     zzin_df = zzin_df.append(sample_df)
    #     print(f"{j} / 80")
    # zzin_df.to_csv("resources/new_labelling_test/new_labelling_test6.csv", encoding = "euc-kr")

    # for j in range(81,91) :
    #     sample_df = test_zzin(stock_code="all", day_weight=0.5, min_P_score=5, N_items=5, past_num = j).head()
    #     zzin_df = zzin_df.append(sample_df)
    #     print(f"{j} / 90")
    # zzin_df.to_csv("resources/new_labelling_test/new_labelling_test7.csv", encoding = "euc-kr")

    # for j in range(91,101) :
    #     sample_df = test_zzin(stock_code="all", day_weight=0.5, min_P_score=5, N_items=5, past_num = j).head()
    #     zzin_df = zzin_df.append(sample_df)
    #     print(f"{j} / 100")
    # zzin_df.to_csv("resources/new_labelling_test/new_labelling_test8.csv", encoding = "euc-kr")

    # for j in range(101,111) :
    #     sample_df = test_zzin(stock_code="all", day_weight=0.5, min_P_score=5, N_items=5, past_num = j).head()
    #     zzin_df = zzin_df.append(sample_df)
    #     print(f"{j} / 110")
    # zzin_df.to_csv("resources/new_labelling_test/new_labelling_test9.csv", encoding = "euc-kr")

    for j in range(111,121) :
        sample_df = test_zzin(stock_code="all", day_weight=0.5, min_P_score=5, N_items=5, past_num = j).head()
        zzin_df = zzin_df.append(sample_df)
        print(f"{j} / 120")
    zzin_df.to_csv("resources/new_labelling_test/new_labelling_test10.csv", encoding = "euc-kr")
