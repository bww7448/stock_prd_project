import pandas as pd
import FinanceDataReader as fdr

def labellingNASDAQ(change):
    if change > 0.0003:
        if change< 0.0010:
            return 'U01'
        if change < 0.0017:
            return 'U02'
        if change < 0.0028:
            return 'U03'
        else : 
            return 'U04'
    elif change < -0.0028:
        if change > -0.0017:
            return 'D03'
        if change > -0.0010:
            return 'D02'
        if change > -0.0003:
            return 'D01'
        return 'D04'
    else : 
        return 'T01'

# 나스닥지수 한국시간으로 맞추기
def call_nasdaq():
    today = pd.Timestamp.now()
    today = str(today.year)+"-"+str(today.month)+"-"+str(today.day)
    nq = fdr.DataReader('IXIC', '2012-01-01', today)
    nq = nq.reset_index()
    nq.columns = pd.Index(["date", "close", "open","high","low","volume","change"],name=nq.columns.name)
    
    # date 쪼개기
    nq_date = pd.DataFrame(nq['date'])
    
    # 아래에 빈 행 추가
    nq_date.loc['today'] = pd.to_datetime(today)
    nq_date.reset_index(inplace=True)
    
    del nq_date['index']
    
    # 나머지 컬럼들
    nq_remain = pd.DataFrame(nq[['close', 'open','change']])

    # 윗 행 생성
    first_row= {'close':[0],'open':[0],'change':[0]}
    first_row= pd.DataFrame(first_row)

    # 윗 행 합치기
    plus_data = pd.concat([first_row, nq_remain])
    
    #reset_index
    plus_data.reset_index(inplace=True)

    #del index
    del plus_data['index']
    
    # date + plus_data
    nsq_data = pd.concat([nq_date, plus_data], axis=1)

    # clean variables
    del nq_date, plus_data, first_row, nq, nq_remain

    # 라벨링 작업
    nsq_data['nasdaq'] = None
    for i in range(1,len(nsq_data)):
        temp = nsq_data['change'].values[i]
        nsq_data['nasdaq'].values[i] = labellingNASDAQ(temp)

    # nsq_data = nsq_data[['date','nasdaq']]
    nsq_data.to_csv("resources/nasdaq.csv")