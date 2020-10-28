import pandas as pd
from random import sample

# U01, U02, U03, U04, D01, D02, D03, D04, T01
NASDAQ_weight = [
    [30,15,5,5,8,7,5,5,20],
    [22,23,8,8,7,6,6,5,15],
    [10,17,23,17,7,5,5,3,13],
    [5,5,5,30,8,7,5,5,20],
    [8,7,5,5,30,15,5,5,20],
    [7,6,6,5,22,23,8,8,15],
    [7,5,5,5,10,17,23,17,13],
    [8,7,5,5,5,5,5,30,20],
    [15,7,7,6,15,7,7,6,30]
]
NASDAQ_weight_dict = {"U01":0, "U02":1, "U03":2, "U04":3, "D01":4, "D02":5, "D03":6, "D04":7, "T01":8}

def get_NASDAQ_weight(standardL, relativeL):
    i = NASDAQ_weight_dict[standardL]
    j = NASDAQ_weight_dict[relativeL]
    return NASDAQ_weight[i][j]

def stockpred_apriori(stock_code=None, weight=0.05, min_P_score=50, N_items=3):
    '''
    n-items serial association rule analysis를 통해 다음 주식 패턴을 예측합니다.

    [parameter]
    - stock_code    종목코드를 int 또는 list 형태로 입력, 
                    미입력 시 무작위로 샘플링한 10개의 종목으로 테스트합니다.
                    str "all" 입력 시 전체 종목으로 테스트합니다.
    - weight        시간에 따른 가중치를 입력합니다. 미입력 시 0.05로 적용됩니다.
    - min_P_score   입력된 값(0 ~ 100) 미만의 P_score를 보이는 결과는 보여주지 않습니다. 미입력 시 50으로 적용됩니다.
    - N_items       연관 규칙 시 장바구니에 묶을 item 수를 정합니다. 미입력 시 3개씩 묶습니다.
    '''
    stock_pred_df = pd.DataFrame({'P_score': [], 'predict' : [],'stock_name' : [], 'stock_code': [], 'Date' : []})
    stock_list = pd.read_csv('resources/stockcode.csv', dtype = {"종목코드": str, "회사명": str})

    # input 처리
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

    for stock_code in stock_sample:
        stockData = pd.read_csv(f'resources/ohlcv_p1p2p3_nasdq/{stock_code}.csv', parse_dates=['date'], index_col=[0])
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
        target_nasdaq = stockData['nasdaq'].iloc[-N_items]

        stock_name = stock_list.회사명[stock_list['종목코드'] == stock_code].values[0]

        A = {'P0': 0, 'P1': 0, 'M0': 0, 'M1': 0, 'K0': 0}
        A_pr = {'P_score': 0, 'stock_name' : stock_name,'stock_code': stock_code, 'Date' : stockData["date"].iloc[-1]}
        pattern_count = 0
        for bong_order in range(len(bong_list)):
            current_bong = bong_list[bong_order].copy()
            next_bong = current_bong.pop()
            if target == current_bong:
                date_weight = bong_order//10*weight
                nasdaq_weight = get_NASDAQ_weight(target_nasdaq, stockData['nasdaq'][bong_order+N_items])
                score = 1 + date_weight + 2*nasdaq_weight
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
        if pattern_count < 5 :
            continue    # 패턴이 일정 횟수 이상 발견되지 않으면 분석 대상에서 제외합니다.
        A_pr['P_score'] = round(
            ((A['P0']+A['P1']) / (A['P0']+A['P1']+A['M0']+A['M1']+A['K0']))*100, 2)
        if A_pr['P_score'] >= min_P_score:
            predict = max(A.keys(), key = (lambda k : A[k]))
            A_pred_df = pd.DataFrame({'P_score': [A_pr["P_score"]], 'predict' : [predict],
            'stock_name' : [A_pr['stock_name']], 'stock_code': [A_pr['stock_code']], 'Date' : [A_pr['Date']]})
            stock_pred_df = stock_pred_df.append(A_pred_df)

    return stock_pred_df
