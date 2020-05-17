try:
    import pandas as pd
except ImportError:
    pass


def open_file(filename):
    try:
        return pd.read_csv(filename)
    except:
        print("File is Missing")


def trading_days(df):
    days_row = df['Date'].tolist()
    days = []
    [days.append(x) for x in days_row if x not in days]
    return days
