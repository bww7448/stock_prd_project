import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from random import sample
from modules.pattern_labelling import get_stockData_using_stockCode


def stockpred_apriori(stock_code=None, weight=0.05, min_P_score=50, N_items=3):
    '''
    n-items serial association rule analysis를 통해 다음 주식 패턴을 예측합니다.

    [parameter]
    - stock_code    종목코드를 int 또는 list 형태로 입력, 미입력 시 무작위로 샘플링한 10개의 종목으로 테스트합니다.
    - weight        시간에 따른 가중치를 입력합니다. 미입력 시 0.05로 적용됩니다.
    - min_P_score   입력된 값(0 ~ 100) 미만의 P_score를 보이는 결과는 보여주지 않습니다. 미입력 시 50으로 적용됩니다.
    - N_items       연관 규칙 시 장바구니에 묶을 item 수를 정합니다. 미입력 시 3개씩 묶습니다.
    '''
    if stock_code == None:
        stock_list = pd.read_csv('resources/stockcode.csv')
        stock_sample = sample(list(stock_list['종목코드']), 10)
    elif type(stock_code) == int:
        stock_sample = [stock_code]
    elif type(stock_code) == list:
        stock_sample = stock_code.copy()
    else:
        raise TypeError("stock_code에 잘못된 parameter type이 입력되었습니다.")

    if N_items > 9 or N_items < 2:
        raise TypeError("N_items에는 2 이상 9 이하의 정수가 입력되어야 합니다.")

    for stock_code in stock_sample:
        stockData = get_stockData_using_stockCode(stock_code)

        bong_list = []
        for i in range(0, len(stockData) - N_items):
            pattern_list = []
            for n in range(N_items):
                pattern_list.append(f"0{n+1}" + stockData["pattern1"][i+n])
            bong_list.append(pattern_list)

        D = []
        for i in range(1, N_items):
            D.append(f"0{i}" + stockData['pattern1'][-N_items-1+i])

        A = {'P_score': 0, 'real': stockData['pattern1'][-1], 'stock_name': stockData.columns.name, 'stock_code': stock_code,
             'P0': 0, 'P1': 0, 'M0': 0, 'M1': 0, 'K0': 0}
        print("연관 분석 시작... ", end="")
        for bong_order in range(len(bong_list)):
            date_weight = bong_order//10
            current_bong = bong_list[bong_order].copy()
            next_bong = current_bong.pop()
            if D == current_bong:
                next_bong = next_bong[2:4]
                if "P0" == next_bong:
                    A["P0"] += 1+(weight*date_weight)
                elif "P1" == next_bong:
                    A["P1"] += 1+(weight*date_weight)
                elif "M0" == next_bong:
                    A["M0"] += 1+(weight*date_weight)
                elif "M1" == next_bong:
                    A["M1"] += 1+(weight*date_weight)
                elif "K0" == next_bong:
                    A["K0"] += 1+(weight*date_weight)
        print("완료")
        if (A['P0']+A['P1']+A['M0']+A['M1']+A['K0']) == 0:
            print("[Failed] 연관 규칙이 발견되지 않았습니다.")
        else:
            A['P_score'] = round(
                ((A['P0']+A['P1']) / (A['P0']+A['P1']+A['M0']+A['M1']+A['K0']))*100, 2)
            if A['P_score'] >= min_P_score:
                print(A)
        print()
