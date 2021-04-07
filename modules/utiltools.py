import pandas as pd


def get_strDate(daysDelta=None, dateFormat="YYMMDD"):

    date = pd.Timestamp.now()
    if daysDelta is not None:
        date += pd.Timedelta(days=daysDelta)

    date = str(date.date()) # YYYY-MM-DD

    if dateFormat == "YYYY-MM-DD":
        return date
    elif dateFormat == "YY-MM-DD":
        return date[2:10]
    elif dateFormat == "MM-DD":
        return date[4:10]

    date = date.replace('-','') # YYYYMMDD

    if dateFormat == "YYYYMMDD":
        return date
    elif dateFormat == "YYMMDD":
        return date[2:8]
    elif dateFormat == "MMDD":
        return date[4:8]
    else:
        raise Exception("utiltools.get_strDate의 dateFormat에 유효하지 않은 형식이 입력되었습니다.")
    