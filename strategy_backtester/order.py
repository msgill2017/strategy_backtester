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
    up = data_df['Underlying'].values[0]
    print("Underlying Price: ", up)

    get_available_strike_price(data_df)
    while True:
        print("Enter the Order in given format Long/Short Call/Put Strike_Price Premium Lot_Qty (long call 210 12.0 1) ")
        inp = list(input().split())

        cond = [inp, len(inp) == 5]

        if all(cond):
            order = user_response_to_order_dic(inp)
            validate_or_update_values(order, data_df)
            return order


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


def validate_or_update_values(user_input, data_df):
    validate_type_and_option_value(user_input, 'Type')
    validate_type_and_option_value(user_input, 'Option')
    validate_strike_price_value(user_input, data_df)
    validate_premium_value(user_input, data_df)
    validate_lot_qty_value(user_input)


def validate_type_and_option_value(order, k):

    if user_input_type_option_purification(order, k)[0]:
        order[k] = user_input_type_option_purification(order, k)[1]
    else:
        while True:
            res = message("Updated {}".format(k))
            if user_input_type_option_purification(res, k)[0]:
                order[k] = user_input_type_option_purification(order, k)[1]
                break


def user_input_type_option_purification(o, k):
    if o[k][0].upper() not in ['L', 'S', 'C', 'P']:
        return False, ' '
    else:
        return{'L': (True, 'Long'), 'S': (True, 'Short'),
               'C': (True, 'CE'), 'P': (True, 'PE')}[o and o[k][0].upper()]


def validate_strike_price_value(order, data_df):
    sp = order['Strike Price']
    sp_lst = get_available_strike_price(data_df)
    if is_inp_str_number(sp):
        if is_strike_price_available(sp, sp_lst):
            order['Strike Price'] = float(sp)
        else:
            while True:
                inp = message("Updated Strike Price:")
                if is_inp_str_number(inp):
                    if is_strike_price_available(inp, sp_lst):
                        order['Strike Price'] = float(inp)
                        break


def validate_premium_value(order, data_df):
    if is_inp_str_number(order['Premium']):
        if is_premium_available(order, order['Premium'], data_df):
            order['Premium'] = float(order['Premium'])
        else:
            while True:
                res = message("Updated Premium Price:")
                if is_inp_str_number(res):
                    if is_premium_available(order, res, data_df):
                        order['Premium'] = float(res)
                        break


def validate_lot_qty_value(order):
    if is_inp_str_number(order['Qty']):
        order['Qty'] = int(order['Qty'])
    else:
        while True:
            res = message("Updated Lot qty:")
            if is_inp_str_number(res):
                order['Qty'] = int(res)
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


def is_premium_available(o, val, data_df):
    col_lst = premium_cols(o['Option'])

    sp = o['Strike Price']
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
