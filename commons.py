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



def validate_input(data_df):
    uprice = data_df['Underlying'].values[0]
    print("Underlying Price: ", uprice)
    sp = get_available_strike_price(data_df)
    while True:
        print("Enter the Order in given format Long/Short Call/Put Strike_Price Premium Qty (long call 210 12.0 1) ")
        inp = list(input().split())
        # conds_and = [inp, len(inp) == 5, check_trade_type(inp and inp[0][0]), check_option_type(inp and inp[1][0]), \
        #              compiled_regex(inp and inp[2]), compiled_regex(inp and inp[3]), compiled_regex(inp and inp[4])]
        conds_and = [inp, len(inp) == 5]
        if all(conds_and):
            update_values(inp, data_df)
            print("your in trade")
            print(inp)
            break


def get_available_strike_price(df):
    strike_price_range = df['Strike Price'].tolist()
    print("Available Strike Price: ")
    print(strike_price_range)
    return strike_price_range


def update_values(inp_lst, data_df):
    validate_trade_value(inp_lst)
    validate_option_value(inp_lst)
    validate_strike_price_value(inp_lst, data_df)


def validate_trade_value(lst):
        if lst and lst[0].upper() == 'L':
            lst[0] = 'Long'
        elif lst and lst[0].upper() == 'S':
            lst[0] = 'Short'
        else:
            while True:
                res = message("Updated trade type:")
                if res and res[0].upper() == 'L':
                    lst[0] = 'Long'
                    break
                elif res and res[0].upper() == 'S':
                    lst[0] = 'Short'
                    break


def validate_option_value(lst):
    if lst and lst[1].upper() == 'C':
        lst[1] = 'CE'
    elif lst and lst[1].upper() == 'P':
        lst[1] = 'PE'
    else:
        while True:
            res = message("Updated Option type:")
            if res and res[1].upper() == 'C':
                lst[1] = 'CE'
                break
            elif res and res[0].upper() == 'P':
                lst[1] = 'PE'
                break


def validate_strike_price_value(lst, data_df):
    sp_lst = get_available_strike_price(data_df)
    if is_inp_str_number(lst[2]):
        if is_strike_price_available(lst[2], sp_lst):
            lst[2] = float(lst[2])
        else:
            while True:
                res = message("Updated Strike Price:")
                if is_inp_str_number(res):
                    if is_strike_price_available(res, sp_lst):
                        lst[2] = float(res)
                    break


comp = re_compile("^\d+?\.\d+?$")


def is_inp_str_number(s):
    """ Returns True is string is a number. """
    if not s:
        return False
    if comp.match(s) is None:
        return s.isdigit()
    return True


def is_strike_price_available(sp, lst):
    if float(sp) in lst:
        return True


def message(msg):
    return input("Enter {} :".format(msg))


# def is_premium_available(sp, data_df):
#     print(data_df['Strike Price'] == sp[3])

