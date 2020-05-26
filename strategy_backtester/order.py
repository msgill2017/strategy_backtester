#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 2020

@author: Mandeep S Gill

email : msg8930@yahoo.com

"""
from strategy_backtester.config import ORDER_COL
from strategy_backtester.commons import is_inp_str_number

try:
    import pandas as pd
except ImportError:
    pass


def place_order(data_df):

    return validate_user_input(data_df)


def validate_user_input(data_df):
    display_underline_price(data_df)
    display_strike_price(data_df)

    while True:
        print("Enter the Order in given format Long/Short Call/Put Strike_Price Premium Lot_Qty (long call 210 12.0 1) ")
        inp = list(input().split())

        cond = [inp, len(inp) == 5]

        if all(cond):
            o = user_response_to_dic(inp)
            return validate_order_values(o, data_df)


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


def user_response_to_dic(res):

    # Create a zip object from two lists
    zipbObj = zip(ORDER_COL, res)

    # Create a dictionary from zip object
    return dict(zipbObj)


def validate_order_values(user_input, data_df):
    order = {}
    # for k in ['Type']:
    for k in ORDER_COL:
        order[k] = validate_and_update(user_input, data_df, k)
    return order


def validate_and_update(user_inp, df, k):

    if k in ['Type', 'Option']:
        return validate_str_values(user_input_type_option_purification, user_inp, k)
    else:
        validator_func = get_validator(k)
        return validate_non_str_values(validator_func, user_inp, df, k)


def validate_str_values(func, order, k):

    if func(order, k)[0]:
        return func(order, k)[1]
    else:
        while True:
            user_res = request_user_updated_input(func=func, order=order, key=k)
            if user_res[0] is True:
                return user_res[1]


def user_input_type_option_purification(o, k, res=None):
    val = res.upper() if res else o[k].upper()

    if val in ['L', 'S', 'LONG', 'SHORT'] and k == 'Type':
        return {'L': (True, 'Long'), 'S': (True, 'Short')}[val[0]]
    elif val in ['C', 'P', 'CE', 'PE', 'CALL', 'PUT'] and k == 'Option':
        return {'C': (True, 'CE'), 'P': (True, 'PE')}[val[0]]
    else:
        return False, ' '


def validate_non_str_values(func, order, df, k):
    val = {'Strike Price': func(order=order, option_df=df), 'Premium': func(order, df), 'Qty': func(order)}[k]
    if is_inp_str_number(order[k]) and val[0]:
        return val[1]
    else:
        while True:
            user_res = request_user_updated_input(func=func, order=order, key=k, df=df)
            if user_res[0] is True:
                return user_res[1]


def request_user_updated_input(func, order, key, df=None):

        r = message("Updated {}".format(key))
        if key in ['Strike Price', 'Premium', 'Qty']:
            val = {'Strike Price': func(order, df, res=r), 'Premium': validate_premium_price(order, df, res=r),
                   'Qty': validate_qty_value(order, res=r)}[key]
            if is_inp_str_number(r) and val[0]:
                return True, val[1]
            else:
                return False, ' '
        elif func(order, key, res=r)[0]:
            return True, func(order, key, res=r)[1]
        return False, ' '


def get_validator(k):
    return {'Strike Price': validate_strike_price,
            'Premium': validate_premium_price,
            'Qty': validate_qty_value
            }[k]


def validate_strike_price(order, option_df, res=None):
    try:
        sp = float(order['Strike Price'])
    except:
        print("validate_strike_price program expected Order_dic type but received {} with type of {} ".format(order, type(order)))
    sp = float(res) if res else sp
    sp_lst = get_strike_price(option_df)
    if sp in sp_lst:
        return True, sp
    return False, ' '


def validate_premium_price(order, option_df, res=None):
    try:
        p = float(order['Premium'])
    except:
        print("validate_strike_price program expected Order_dic type but received {} with type of {} ".format(order, type(order)))
    p = float(res) if res else p

    if is_premium_available(order, p, option_df):
        return True, p
    return False, ' '


def is_premium_available(order, premium, option_df):
    col_lst = premium_cols(order['Option'])
    sp = float(order['Strike Price'])
    pr = premium_range(option_df, col_lst, sp)

    return is_premium_in_range(premium, pr)


def premium_cols(option):
    option = option.upper()
    if option in ['CE', 'PE']:
        return ['CE High', 'CE Low'] if option == 'CE' else ['PE High', 'PE Low']
    else:
        raise ValueError('could not find {} in [CE , PE]'.format(option))


def premium_range(option_df, col_lst, strike_price):
    row = option_df['Strike Price'] == strike_price
    return option_df.loc[row, col_lst].values[0].tolist()


def is_premium_in_range(premium, lst):
    if lst[1] <= float(premium) <= lst[0]:
        return True
    return False


def validate_qty_value(order, res=None):
    try:
        q = order['Qty']
    except:
        print("validate_strike_price program expected Order_dic type but received {} with type of {} ".format(order, type(order)))
    q = res if res else q

    if q.isnumeric():
        return True, int(q)
    return False, ' '


def message(msg):
    return input("Enter {} :".format(msg))
