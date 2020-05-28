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


from strategy_backtester.config import TRADE_BOOK_COL, lot_size, symbol, data_dir


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)


def open_file(filename):
    try:
        return pd.read_csv(filename)
    except:
        print("{} File is Missing.. Please check the file".format(filename))


def open_trade_book(sym, exp):
    file_path = "data/{}-TRDBOOK-{}.csv".format(sym, exp)
    if os.path.exists(file_path):
        return open_file(file_path)
    else:
        df = pd.DataFrame(columns=TRADE_BOOK_COL)
        return df


def save_df(df, sym, exp):
    file_path = data_dir + "/{}-TRDBOOK-{}.csv".format(sym, exp)
    print("Trade Book is Saving at this location {}".format(file_path))
    with open(file_path, 'a') as f:
        df.to_csv(f, header=f.tell() == 0, index=False)
   

def dic_to_df(o):
    # df col. = Contract Name,Open Date,Qty,Type,Adj. Cost
    # lst ['Long', 'CE', 210.0, 1.2, 1, '2019-04-26']
    contract_name = '{}-{}-{}'.format(symbol, o['Strike Price'], o['Option'])
    date = o['Date']
    qty = o['Qty'] * lot_size
    ty = o['Type']
    p = o['Premium']
    adj_cost = qty * o['Premium']

    lst_update = [contract_name, date, ty, qty, p, adj_cost]

    return pd.DataFrame([lst_update], columns=TRADE_BOOK_COL)


def exit_loop(val):
    if val and val[0].upper() == 'E':
        return True


def no_trade_entry(tb, date):
    contract_name = 'NO-TRADE-DAY'
    lst_update = [contract_name, date, 0.0, 'NoTrade', 0.0]
    return pd.DataFrame([lst_update], columns=TRADE_BOOK_COL)


def trading_days(df, col="Date"):
    days = []
    if df.empty:
        return days
    try:
        days_row = df['{}'.format(col)].tolist()
        [days.append(x) for x in days_row if x not in days]
    except None:
        print("Expect the pandas dataframe, but received the {} type of {}".format(df, type(df)))
    return days


comp = re_compile("^\d+?\.\d+?$")


def is_inp_str_number(s):
    """ Returns True is string is a number. """
    if not s:
        return False
    try:
        if comp.match(s) is None:
            return s.isdigit()
    except:
        print("Enter value must be string, Value received {}, type of {}".format(s, type(s)))
    return True
