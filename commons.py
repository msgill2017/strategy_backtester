#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 2020

@author: Mandeep S Gill

email : msg8930@yahoo.com

"""
import os.path

from re import compile as re_compile

try:
    import pandas as pd
except ImportError:
    pass


from config import TRADE_BOOK_COL, lot_size, symbol, expiry_date


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)


def open_file(filename):
    try:
        return pd.read_csv(filename)
    except:
        print("{} File is Missing.. Please check the file".format(filename))


def trade_book(sym, exp):
    file_path = "Data/{}-TRDBOOK-{}.csv".format(sym, exp)
    if os.path.exists(file_path):
        return open_file(file_path)
    else:
        df = pd.DataFrame(columns=TRADE_BOOK_COL)
        return df


def save_df(df, sym, exp):
    file_path = "Data/{}-TRDBOOK-{}.csv".format(sym, exp)
    print("Trade Book is Saving at this location {}".format(file_path))
    df.to_csv(file_path, index=False)


def list_to_df(lst):
    # df col. = Contract Name,Open Date,Qty,Type,Adj. Cost
    # lst ['Long', 'CE', 210.0, 1.2, 1, '2019-04-26']
    contract_name = '{}-{}-{}'.format(symbol, str(lst[2]), lst[1])
    date = lst[5]
    qty = lst[4] * lot_size
    ty = lst[0]
    adj_cost = qty * lst[3]

    lst_update = [contract_name, date, qty, ty, adj_cost]

    return pd.DataFrame([lst_update], columns=TRADE_BOOK_COL)


def exit_loop(val):
    if val and val[0].upper() == 'E':
        return True


def no_trade_entry(tb, date):
    contract_name = 'NO-TRADE-DAY'
    lst_update = [contract_name, date, 0.0, 'NoTrade', 0.0]
    return pd.DataFrame([lst_update], columns=TRADE_BOOK_COL)


def portfolio_balance(portfolio, df, previous_date):
    print("Current Portfolio with Profit and Loss as on {}".format(previous_date))
    symbols = portfolio['Contract_name'].unique().tolist()
    symbols.remove('NO-TRADE-DAY')

    print(symbols)
    long_positions = long_positions_df(portfolio)
    print(long_positions)
    short_positions = short_positions_df(portfolio)
    print(short_positions)

    combine_positions = long_positions.merge(short_positions, on='Contract_name', how='outer').fillna(0.0)

    # print(combine_positions)
    open_qty(combine_positions)
    # common_contract = common_elements(long_positions['Contract_name'].unique().tolist(), short_positions['Contract_name'].unique().tolist())
    # print(common_contract)
    # for contract in common_contract:
    #     print(contract)
    #     long_row_filter = long_positions['Contract_name']==contract
    #     short_row_filter = short_positions['Contract_name'] == contract
    #     if long_positions.loc[long_row_filter, 'Qty'] <= short_positions.loc[short_row_filter, 'Qty']:
    #         short_positions[short_row_filter]['Qty'] -= long_positions[long_row_filter]['Qty']
    #         print(short_positions['S_qty'])
    #     else:
    #         long_positions[long_row_filter]['Qty'] -= short_positions[short_row_filter]['Qty']
    #         # sale[1]['Qty'] -= sale[1]['Qty']
    #         print(long_positions)
        # print(
    # positions_no_change = long_positions[~long_positions['Contract_name'].isin(short_positions['Contract_name'].unique())]
    # print("positon no change", positions_no_change)
    # daily_adj_close = get_data(symbols, df)
    # print(daily_adj_close)


def rename_col_names(df, val):
    headers = {'Qty': '{}_qty'.format(val), 'Adj_cost': '{}_value'.format(val)}
    return df.rename(columns=headers)


def long_positions_df(df):
    long_positions = df[df['Type'] == 'Long'].groupby('Contract_name', as_index=False)['Qty', 'Adj_cost'].sum()
    long_positions.insert(2, 'Long_avg', (long_positions.Adj_cost / long_positions.Qty))

    return rename_col_names(long_positions, 'Long')


def short_positions_df(df):
    short_positions = df[df['Type'] == 'Short'].groupby('Contract_name', as_index=False)['Qty', 'Adj_cost'].sum()
    short_positions.insert(2, 'Short_avg', (short_positions.Adj_cost / short_positions.Qty))

    return rename_col_names(short_positions, 'Short')


def common_elements(lst1, lst2):
    return list(set(lst1).intersection(lst2))


def open_qty(df):

    df['Open_qty'] = abs(df['Long_qty'] - df['Short_qty'])
    df['Type'] = find_pending_trade_type(df)
    # trade_type_col(df)
    print(df)


# Create a function to apply to each row of the data frame
def find_pending_trade_type(df):
    """ Find the trade value according to its sign like negative number means Short type
    or positive number means Long """
    df['Type'] = df['Long_qty'] - df['Short_qty']
    # df['a'] = df['a'].map(lambda a: a / 2.)

    return df['Type'].map(lambda val: check_trade_type(val))


def check_trade_type(num):
    if num > 0:
        return 'Long'
    elif num == 0:
        return 'None'
    else:
        return 'Short'


def realized_profit():
    pass


def un_realized_profit():
    pass


def get_data(sym, df):
    sp = symbol_to_strike_price(sym)
    closes = []
    temp = df[df['Strike Price'].isin(sp)]
    temp = temp[['Strike Price', 'CE Close', 'PE Close']].reset_index()

    for item in sym:

        lst = item.split('-')

        sp_filter = temp['Strike Price'] == float(lst[1])

        val = temp.loc[sp_filter, '{} Close'.format(lst[2])].values[0]

        closes.append([item, val])

    return pd.DataFrame(closes, columns=['Contract name', 'Close'])


def symbol_to_strike_price(sym):
    sp = []
    for elem in sym:
        sp.append(elem.split('-')[1])
    return sp


def trading_days(df, col="Date"):
    days = []
    try:
        days_row = df['{}'.format(col)].tolist()
        [days.append(x) for x in days_row if x not in days]
    except:
        days =[]
    return days


def order_place(data_df):

    return validate_input(data_df)


def validate_input(data_df):
    uprice = data_df['Underlying'].values[0]
    print("Underlying Price: ", uprice)
    get_available_strike_price(data_df)
    while True:
        print("Enter the Order in given format Long/Short Call/Put Strike_Price Premium Lot_Qty (long call 210 12.0 1) ")
        inp = list(input().split())

        cond = [inp, len(inp) == 5]

        if all(cond):
            validate_or_update_values(inp, data_df)
            print("your in trade")
            print(inp)
            return inp


def get_available_strike_price(df):
    strike_price_range = df['Strike Price'].tolist()
    print("Available Strike Price: ")
    print(strike_price_range)
    return strike_price_range


def validate_or_update_values(inp_lst, data_df):
    validate_trade_value(inp_lst)
    validate_option_value(inp_lst)
    validate_strike_price_value(inp_lst, data_df)
    validate_premium_value(inp_lst, data_df)
    validate_lot_qty_value(inp_lst)


def validate_trade_value(lst):
        if lst and lst[0][0].upper() == 'L':
            lst[0] = 'Long'
        elif lst and lst[0][0].upper() == 'S':
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
    if lst and lst[1][0].upper() == 'C':
        lst[1] = 'CE'
    elif lst and lst[1][0].upper() == 'P':
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


def validate_premium_value(lst, data_df):
    if is_inp_str_number(lst[3]):
        if is_premium_available(lst, lst[3], data_df):
            lst[3] = float(lst[3])
        else:
            while True:
                res = message("Updated Premium Price:")
                if is_inp_str_number(res):
                    if is_premium_available(lst, res, data_df):
                        lst[3] = float(res)
                        break


def validate_lot_qty_value(lst):
    if is_inp_str_number(lst[4]):
        lst[4] = int(lst[4])
    else:
        while True:
            res = message("Updated Lot qty:")
            if is_inp_str_number(res):
                lst[4] = int(res)
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


def is_premium_available(lst, val, data_df):

    filter_sp_row = data_df['Strike Price'] == lst[2]
    col_lst = ['CE High', 'CE Low'] if lst[1] == 'CE' else ['PE High', 'PE Low']

    premium_range = data_df.loc[filter_sp_row, col_lst].values[0]
    print(premium_range)

    if premium_range[1] <= float(val) <= premium_range[0]:
        return True
    return False

