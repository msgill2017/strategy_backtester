#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 2020

@author: Mandeep S Gill

email : msg8930@yahoo.com

"""
from strategy_backtester.config import TRADE_COL
from strategy_backtester.commons import is_inp_str_number

from strategy_backtester.commons import open_file, trade_book, trading_days, exit_loop, save_df,\
                    dic_to_df, no_trade_entry
from strategy_backtester.config import symbol, expiry_date, data_dir

filename = data_dir + '/{}-OPTSTK-{}.csv'.format(symbol, expiry_date)

option_chain_df = open_file(filename)

try:
    import pandas as pd
except ImportError:
    pass


def display_underline_price(df):
    print("Underlying Price: {}".format(get_underline_price(df)))


def display_strike_price(df):
    print("Available Strike Price: ")
    print('{}'.format(get_strike_price(df)))


def get_underline_price(df):
    # return df['Underlying'].values[0]
    try:
        return df['Underlying'].values[0]
    except :
        print("Oops!  That was not valid dataframe.  Try again...")


def get_strike_price(df):
    try:
        return df['Strike Price'].tolist()
    except TypeError:
        print("Oops!  That was no valid dataframe.  Try again...")


def place_trade(option_df):
    display_underline_price(option_df)
    display_strike_price(option_df)
    trade = {}
    for key in TRADE_COL:
        res = input("Enter the Trade {}: ".format(key))
        validator = get_validator(key)
        trade[key] = validate(func=validator, key=key, res=res, option_df=option_df, trade=trade)
    return trade


def get_validator(k):
    return {'Type': validate_type,
            'Option': validate_option,
            'Strike Price': validate_strike_price,
            'Premium': validate_premium,
            'Qty': validate_qty
            }[k]


def validate(func, key, res, option_df, trade):
    if key in ['Type', 'Option', 'Qty']:
        args = {'res': res}
    else:
        args = {'res': res, 'option_df': option_df, 'user_trade': trade}

    val = func(**args)
    if val[0]:
        return val[1]
    else:
        while True:
            user_res = input('Update {}: '.format(val[1]))
            if key in ['Type', 'Option', 'Qty']:
                updated_args = {'res': user_res}
            else:
                updated_args = {'res': user_res, 'option_df': option_df, 'user_trade': trade}

            validate_user_res = func(**updated_args)
            if validate_user_res[0] is True:
                return validate_user_res[1]


def validate_type(res):
    res = res.upper()
    if res in ['BUY', 'SELL']:
        return True, res
    return False, 'Sell or Buy'


def validate_option(res):
    res = res.upper()
    if res in ['CALL', 'PUT']:
        return True, 'CE' if res == 'CALL' else 'PE'
    return False, 'CALL or PUT'


def validate_strike_price(res, option_df, user_trade=None):
    if is_inp_str_number(res):
        try:
            sp = float(res)
        except:
            print("validate_strike_price program expected user_input_dic type but received {} with type of {} ".
                  format(res, type(res)))

        sp_lst = get_strike_price(option_df)
        if sp in sp_lst:
            return True, sp
    return False, 'Valid Strike Price from Available list '


def validate_premium(res, option_df, user_trade=None):
    if is_inp_str_number(res):
        try:
            p = float(res)
        except:
            print("validate_premium function expected number str but received {} with type of {} ".format(
                res, type(res)))
        sp = user_trade['Strike Price']
        op = user_trade['Option']
        col_lst = premium_cols(op)
        pr = premium_range(option_df, col_lst, sp)
        if is_premium_in_range(res, pr):
            return True, p
    return False, ' Premium within range {} '.format(pr)


def premium_cols(option):
    option = option[0].upper()
    if option in ['C', 'P']:
        return ['CE High', 'CE Low'] if option == 'C' else ['PE High', 'PE Low']
    else:
        raise ValueError('could not find {} in [CE , PE]'.format(option))


def premium_range(option_df, col_lst, strike_price):
    row = option_df['Strike Price'] == strike_price
    return option_df.loc[row, col_lst].values[0].tolist()


def is_premium_in_range(premium, lst):
    if lst[1] <= float(premium) <= lst[0]:
        return True
    return False


def validate_qty(res):
    if res.isnumeric():
        try:
            q = int(res)
        except:
            print("validate_qty function expected number string value but received {} with type of {} ".format(res, type(res)))
        return True, q
    return False, ' Qty with positive integer number only: '

