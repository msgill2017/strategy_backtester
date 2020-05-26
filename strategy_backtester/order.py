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


order = {}


def get_order():
    return order


def place_order(data_df):

    return validate_user_input(data_df)


def validate_user_input(data_df):
    display_underline_price(data_df)
    display_strike_price(data_df)

    while True:
        print("Enter the user_input in given format Long/Short Call/Put Strike_Price Premium Lot_Qty "
              "(long call 210 12.0 1) ")
        inp = list(input().split())

        cond = [inp, len(inp) == 5]

        if all(cond):
            o = user_response_to_dic(inp)
            return validate_user_input_values(o, data_df)


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


def validate_user_input_values(user_input, data_df):
    # for k in ['Type', 'Option', 'Strike Price', 'Premium']:
    for k in ORDER_COL:
        order[k] = validate_and_update(user_input, data_df, k)
    return order


def validate_and_update(user_inp, df, k):

    if k in ['Type', 'Option']:
        return validate_str_values(user_input_type_option_purification, user_inp, k)
    else:
        validator_func = get_validator(k)
        return validate_non_str_values(validator_func, user_inp, df, k)


def validate_str_values(func, user_input, k):

    if func(user_input, k)[0]:
        return func(user_input, k)[1]
    else:
        while True:
            user_res = request_user_updated_input(func=func, user_input=user_input, key=k)
            if user_res[0] is True:
                return user_res[1]


def user_input_type_option_purification(user_input, key, res=None):
    val = res.upper() if res else user_input[key].upper()

    if val in ['L', 'S', 'LONG', 'SHORT'] and key == 'Type':
        return {'L': (True, 'Long'), 'S': (True, 'Short')}[val[0]]
    elif val in ['C', 'P', 'CE', 'PE', 'CALL', 'PUT'] and key == 'Option':
        return {'C': (True, 'CE'), 'P': (True, 'PE')}[val[0]]
    else:
        return False, ' '


def request_user_updated_input(func, user_input, key, df=None):

    r = message("Updated {}".format(key))
    if key in ['Strike Price', 'Premium', 'Qty']:
        val = {'Strike Price': func(user_input, df, res=r), 'Premium': validate_premium_price(user_input, df, res=r),
               'Qty': validate_qty_value(user_input, res=r)}[key]
        if is_inp_str_number(r) and val[0]:
            return True, val[1]
        else:
            return False, ' '
    elif func(user_input, key, res=r)[0]:
        return True, func(user_input, key, res=r)[1]
    return False, ' '


def validate_non_str_values(func, user_input, df, key):
    if key == 'Qty':
        val = func(user_input=user_input)
    else:
        val = func(user_input=user_input, option_df=df)

    if is_inp_str_number(user_input[key]) and val[0]:
        return val[1]
    else:
        while True:
            user_res = request_user_updated_input(func=func, user_input=user_input, key=key, df=df)
            if user_res[0] is True:
                return user_res[1]


def get_validator(k):
    return {'Strike Price': validate_strike_price,
            'Premium': validate_premium_price,
            'Qty': validate_qty_value
            }[k]


def validate_strike_price(user_input, option_df, res=None):
    try:
        sp = float(user_input['Strike Price'])
    except:
        print("validate_strike_price program expected user_input_dic type but received {} with type of {} ".
              format(user_input, type(user_input)))

    sp = float(res) if res else sp
    sp_lst = get_strike_price(option_df)
    if sp in sp_lst:
        return True, sp
    return False, ' '


def validate_premium_price(user_input, option_df, res=None):
    try:
        p = float(user_input['Premium'])
    except:
        print("validate_strike_price program expected user_input_dic type but received {} with type of {} ".format(user_input, type(user_input)))
    p = float(res) if res else p
    o = get_order()
    if is_premium_available(o, p, option_df):
        return True, p
    return False, ' '


def is_premium_available(updated_user_input, premium, option_df):
    col_lst = premium_cols(updated_user_input['Option'])
    sp = float(updated_user_input['Strike Price'])
    pr = premium_range(option_df, col_lst, sp)

    return is_premium_in_range(premium, pr)


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


def validate_qty_value(user_input, res=None):
    try:
        q = user_input['Qty']
    except:
        print("validate_strike_price program expected user_input_dic type but received {} with type of {} ".format(user_input, type(user_input)))
    q = res if res else q

    if q.isnumeric():
        return True, int(q)
    return False, ' '


def message(msg):
    return input("Enter {} :".format(msg))
