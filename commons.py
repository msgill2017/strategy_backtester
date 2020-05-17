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

def order_place(date, data_df):
    uprice = data_df['Underlying'].values[0]
    print("Underlying Price: ", uprice)
    get_available_strike_price(data_df)
        # validate_input()
        # # strike_price = get_strike_price(df)
        # # premium = get_premium(df, strike_price)
        # order_type = long_short()
        # option = call_put()
        # qty = int(message("Enter Qty of Options"))
        #
        # # uprice = 675.45
        # # return Trade(date, order_type, option, strike_price, premium, qty, underlying=uprice)


def get_available_strike_price(df):
    strike_price_range = df['Strike Price'].tolist()
    print("Available Strike Price: ")
    print(strike_price_range)
