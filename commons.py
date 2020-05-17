from re import compile as re_compile

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

    validate_input(data_df)
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
    return strike_price_range


def validate_input(data_df):
    uprice = data_df['Underlying'].values[0]
    print("Underlying Price: ", uprice)
    sp = get_available_strike_price(data_df)
    while True:
        print("Enter the Order in given format Long/Short Call/Put Strike_Price Premium Qty (long call 210 12.0 1) ")
        inp = list(input().split())

        conds_and = [inp, len(inp) == 5, check_trade_type(inp and inp[0][0]), check_option_type(inp and inp[1][0]), \
                     compiled_regex(inp and inp[2]), compiled_regex(inp and inp[3]), compiled_regex(inp and inp[4])]

        if all(conds_and):
            if not is_strike_price_available(inp[2], sp):
                print("Strike Price is not Available")
                inp[2] = message("Update Strike Price:")

            print("your in trade")
            break


def check_trade_type(val):
    if not val:
        # print(message("Trade Type:"))
        return False
    elif val.upper() == 'L' or val.upper() == 'S':
        return True


def check_option_type(val):
    if not val:
        return False
    if val.upper() == 'C' or val.upper() == 'P':
        return True


comp = re_compile("^\d+?\.\d+?$")


def compiled_regex(s):
    """ Returns True is string is a number. """
    if not s:
        return False
    if comp.match(s) is None:
        return s.isdigit()
    return True


def is_strike_price_available(sp, lst):
    if sp in lst:
        return True


def message(msg):
    return input("Enter {} :".format(msg))


