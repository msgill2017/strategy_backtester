#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 2020

@author: Mandeep S Gill

email : msg8930@yahoo.com

"""
from re import compile as re_compile
from strategy_backtester.config import ORDER_COL

try:
    import pandas as pd
except ImportError:
    pass


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
            order = user_response_to_order_dic(inp)
            validate_or_update_values(order, data_df)
            print("your in trade")
            print(inp)
            return inp


def user_response_to_order_dic(res):

    # Create a zip object from two lists
    zipbObj = zip(ORDER_COL, res)

    # Create a dictionary from zip object
    return dict(zipbObj)


def get_available_strike_price(df):
    try:
        strike_price_range = df['Strike Price'].tolist()
        print("Available Strike Price: ")
        print(strike_price_range)
        return strike_price_range
    except TypeError:
        print("Oops!  That was no valid dataframe.  Try again...")


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
    col_lst = premium_cols(lst[1])
    print(lst)
    sp = lst[2]
    pr = premium_range(data_df, col_lst, sp)
    print(pr)

    return is_premium_in_high_low(val, pr)


def premium_cols(option):
    option = option.upper()
    if option in ['CE', 'PE']:
        return ['CE High', 'CE Low'] if option == 'CE' else ['PE High', 'PE Low']
    else:
        raise ValueError('could not find {} in [CE , PE]'.format(option))


def is_premium_in_high_low(pre, lst):
    if lst[1] <= float(pre) <= lst[0]:
        return True
    return False


def premium_range(df, col_lst, sp):
    filter_sp_row = filter_strike_price_row(df, sp)
    return df.loc[filter_sp_row, col_lst].values[0]


def filter_strike_price_row(df, sp):
    return df['Strike Price'] == sp
