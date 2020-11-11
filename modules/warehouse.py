import pandas as pd


def get_strDate(daysDelta=None, dateFormat="YYMMDD"):

    date = pd.Timestamp.now()
    if daysDelta is not None:
        date += pd.Timedelta(days=daysDelta)

    if dateFormat == "YYYY-MM-DD":
        return str(date.date())
    elif dateFormat == "YY-MM-DD":
        return str(date.date())[2:10]
    elif dateFormat == "YYYYMMDD":
        yyyymmdd = [date.year, date.month, date.day]
        yyyymmdd = list(map(str,yyyymmdd))
        return "".join(yyyymmdd)
    elif dateFormat == "YYMMDD":
        yymmdd = [date.year%100, date.month, date.day]
        yymmdd = list(map(str,yymmdd))
        return "".join(yymmdd)
    elif dateFormat == "MMDD":
        mmdd = [date.month, date.day]
        mmdd = list(map(str,mmdd))
        return "".join(mmdd)
    