import sys
import pandas as pd


def labellingD0(d0) -> str:
    '''
    D0 시점의 각 봉에 대한 라벨링(25가지)을 수행합니다.
    당일 1일치(1 row) pd.DataFrame을 입력해주세요.
    '''
    openP = d0['open']
    highP = d0['high']
    lowP = d0['low']
    closeP = d0['close']

    # 장대 양봉
    if closeP >= 1.1*openP:
        if closeP < highP:  # 윗꼬리 있음
            if openP > lowP:
                return "P15"
            elif (highP - closeP) >= 0.07*openP:
                return "P14"
            else:
                return "P13"
        elif openP > lowP:  # 윗꼬리는 없는데 아랫꼬리는 있음
            return "P11"
        else:
            return "P10"    # 꼬리 없음

    # 짧은 양봉
    elif closeP >= 1.005*openP:
        if closeP < highP:
            if openP > lowP:
                return "P05"
            elif (highP - closeP) >= 0.07*openP:
                return "P04"
            else:
                return "P03"
        elif openP > lowP:
            if 2*highP - 3*openP + lowP >= 0:
                return "P01"
            else:
                return "P02"
        else:
            return "P00"

    # 보합
    elif closeP >= openP:
        end_min = closeP - lowP
        Max_end = highP - closeP
        if end_min > Max_end*3:
            return "K01"
        elif end_min*3 < Max_end:
            return "K02"
        return "K00"

    # 짧은 음봉
    elif closeP >= 0.9*openP:
        if openP < highP:
            if closeP > lowP:
                return "M05"
            if highP - 3*openP + 2*closeP < 0:
                return "M03"
            return "M04"
        if closeP > lowP:
            if 3*closeP - lowP - 2*openP < 0:
                return "M01"
            return "M02"
        return "M00"

    # 장대 음봉
    else:
        if closeP > lowP:
            if openP < highP:
                return "M15"
            return "M11"
        if openP < highP:
            if highP - 2*openP + closeP >= 0:
                return "M14"
            return "M13"
        return "M10"


def labellingD0_new(d0, prev_close) -> str:
    '''
    여기 적어
    '''

    prev_closeP = prev_close
    openP = d0['open']
    highP = d0['high']
    lowP = d0['low']
    closeP = d0['close']

    label_0 = 0  # 0, 1, 2
    label_1 = 0  # 0, 1
    label_2 = 0

    label_0 += closeP >= openP
    label_0 += closeP > openP*1.005

    label_1 += ((closeP >= openP*1.1) or (closeP <= openP*0.9))
    label_1

    if label_0 == 1:
        headP = highP - max(openP, closeP)
        tailP = min(openP, closeP) - lowP
        if tailP:
            temp = headP/tailP
        else:
            temp = 15
        if temp >= 7/4:
            label_2 = 2
        elif temp <= 4/7:
            label_2 = 1    
    else:
        if label_0 == 0:
            headP = highP - openP
            tailP = closeP - lowP
        else:  # label_0 == 2:
            headP = highP - closeP
            tailP = openP - lowP

        if headP < prev_closeP * 0.02: # 윗꼬리가 너무 미미함
            label_2 += (tailP >= prev_closeP * 0.02)
            label_2 += (tailP >= prev_closeP * 0.07)
        elif tailP < prev_closeP * 0.02: # 윗꼬리는 눈에 보이고 아랫꼬리가 미미함
            label_2 += (headP >= prev_closeP * 0.01)
            label_2 += (headP >= prev_closeP * 0.05)
            label_2 += 2
        else:
            if tailP:
                temp = headP/tailP
            else:
                temp = 15
            
            if label_1:
                if temp >= 3/1:
                    label_2 = 4
                elif temp >= 4/3:
                    label_2 = 3
                elif temp < 3/4:
                    label_2 = 1
                else:
                    label_2 = 5
            else:
                if temp >= 9/1:
                    label_2 = 4
                elif temp >= 4/1:
                    label_2 = 3
                elif temp < 1/9:
                    label_2 = 2
                elif temp < 1/4:
                    label_2 = 1
                else:
                    label_2 = 5
                
    label_0 = "M" if label_0 == 0 else ("K" if label_0 == 1 else "P")
    label_1 = str(label_1)
    label_2 = str(label_2)
    return "".join([label_0,label_1,label_2])


def labellingD1(d10) -> str:
    '''
    D1 5가지 x D0 25가지
    '''
    temp = d10.iloc[0]
    openP = temp['open']
    # highP = temp['high']
    # lowP = temp['low']
    closeP = temp['close']

    # 장대 양봉
    if closeP >= 1.1*openP:
        res = "P10"

    # 짧은 양봉
    elif closeP >= 1.005*openP:
        res = "P00"

    # 보합
    elif closeP >= openP:
        res = "K00"

    # 짧은 음봉
    elif closeP >= 0.9*openP:
        res = "M00"

    # 장대 음봉
    else:
        res = "M10"

    return res + labellingD0(d10.iloc[1])


def labellingD2(d210):
    '''
    D2D1 12가지 x D0 25가지
    '''
    d2_openP = d210.iloc[0]['open']
    d2_closeP = d210.iloc[0]['close']
    d1_openP = d210.iloc[1]['open']
    d1_closeP = d210.iloc[1]['close']

    d21_max = max(d2_openP, d2_closeP, d1_openP, d1_closeP)
    d21_avg = (d21_max + min(d2_openP, d2_closeP, d1_openP, d1_closeP))/2
    if d21_max/d21_avg <= 1.005:
        res = "S04"
    elif d2_openP <= d2_closeP:  # D2 양봉
        if d1_openP <= d1_closeP:
            res = "P10"
        elif d2_openP >= d1_closeP:
            res = "S07"
        elif d2_closeP > d1_openP:
            res = "S06"
        elif d2_closeP >= d1_closeP:
            res = "S03"
        else:
            res = "S05"
    elif d2_openP >= d2_closeP:  # D2 음봉
        if d1_openP >= d1_closeP:
            res = "M10"
        elif d2_closeP < d1_openP:
            res = "S01"
        elif d2_openP <= d1_closeP:
            res = "S02"
        elif d2_closeP >= d1_closeP:
            res = "S08"
        else:
            res = "S00"
    else:
        res = "S09"

    return res + labellingD0(d210.iloc[2])

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
        return 'D04'
    else : 
        return 'T01'

