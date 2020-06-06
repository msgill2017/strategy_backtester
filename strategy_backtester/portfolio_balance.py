#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 2020

@author: Mandeep S Gill

email : msg8930@yahoo.com

"""

try:
    import pandas as pd
    import numpy as np
except ImportError:
    pass


from strategy_backtester.config import trade_book, trade_book_col, \
    find_avg_and_add_col_to_df_col, trade_types, open_trade_positions_col, sum_qty_trade_value_col


def profit_and_loss_statement(portfolio, df, previous_date):
    print("Current Portfolio with Profit and Loss as on {}".format(previous_date))

    p_df = portfolio_positions(portfolio)
    open_df = open_trade_positions(p_df, df)
    portfolio_positions_df = merge_df(p_df, open_df)
    portfolio_positions_df = merge_realized_profit_and_lost_to_positions(portfolio_positions_df)
    portfolio_positions_df = merge_unrealized_profit_and_lost_to_positions(portfolio_positions_df)

    print(portfolio_positions_df)


def get_unique_contracts_lst(portfolio_df):
    s = portfolio_df[trade_book['Contract_name']].unique().tolist()
    if 'NO-TRADE-DAY' in s:
        s.remove('NO-TRADE-DAY')
    return s


def portfolio_positions(trade_df):
    combine_df = sum_qty_and_trade_value_contracts(trade_df)
    avg_df = find_avg_and_add_col_to_df(combine_df)

    return display_buy_and_sell_side_by_side(avg_df)


def sum_qty_and_trade_value_contracts(trade_df):
    c = trade_df.groupby([trade_book['Contract_name'], trade_book['Type']], as_index=False)\
        .agg({'Qty': 'sum', 'Trade_value': 'sum'}, index=False)

    return c[sum_qty_trade_value_col]


def find_avg_and_add_col_to_df(combine_df):
    combine_df.insert(3, 'Avg', (combine_df[trade_book['Trade_value']] / combine_df[trade_book['Qty']]))

    combine_df.round(2)
    return combine_df[find_avg_and_add_col_to_df_col]


def display_buy_and_sell_side_by_side(trade_df):

    pos = {}

    for t in trade_types:
        temp_df = trade_df[trade_df[trade_book['Type']] == t]
        del temp_df[trade_book['Type']]
        h_q = '{}_Qty'.format(t)
        h_a = '{}_Avg'.format(t)
        h_v = '{}_Value'.format(t)
        temp_df.columns = [trade_book['Contract_name'], h_q, h_a, h_v]
        pos[t] = temp_df

    return pos['Buy'].merge(pos['Sell'], on='Contract_name', how='outer').fillna(0.0)


def merge_df(df1, df2):
    return df1.merge(df2, on='Contract_name', how='outer').fillna(0.0)


def open_trade_positions(p_df, option_df):
    op_df = pd.DataFrame()
    symbols = get_unique_contracts_lst(p_df)
    op_df[trade_book['Contract_name']] = p_df[trade_book['Contract_name']]
    op_df['Open_Qty'] = abs(p_df['Buy_Qty'] - p_df['Sell_Qty'])

    op_df['Open_Type'] = find_pending_trade(p_df)
    op_df[open_trade_positions_col]
    adjust_close_df = get_close_data(symbols, option_df)

    return merge_df(op_df, adjust_close_df)


def common_elements(lst1, lst2):
    return list(set(lst1).intersection(lst2))


def sort_df_with_column(df, column):

    return df.sort_values(by=column).reset_index(drop=True)


# Create a function to apply to each row of the data frame
def find_pending_trade(df):
    """ Find the trade value according to its sign like negative number means Sell type
    or positive number means Buy """
    p_df = pd.DataFrame()
    p_df['Type'] = df['Buy_Qty'] - df['Sell_Qty']

    return p_df['Type'].map(lambda val: trade_type_conversion(val))


def trade_type_conversion(num):
    if num < 0:
        return 'Buy'
    elif num == 0:
        return 'None'
    else:
        return 'Sell'


def merge_unrealized_profit_and_lost_to_positions(df):
    unr_pnl_lst = []
    for row in df.itertuples():
        cn = row.Contract_name
        if row.Open_Type != 'None':
            if row.Open_Type == 'Buy':
                val = row.Open_Qty * (row.Close - row.Buy_Avg)
                val = round(val, 2)
                unr_pnl_lst.append([cn, val])
            else:
                val = row.Open_Qty * (row.Sell_Avg - row.Close)
                val = round(val, 2)
                unr_pnl_lst.append([cn, val])
    unr_df = pd.DataFrame(unr_pnl_lst, columns=['Contract_name', 'UnRealized_PnL'])
    return merge_df(df, unr_df)


def merge_realized_profit_and_lost_to_positions(df):
    closed_contract_filter = (df['Buy_Qty'] > 0) & (df['Sell_Qty'] > 0)
    closed_df = df[closed_contract_filter]
    lists = []
    for row in closed_df.itertuples():
        cn = row.Contract_name
        if row.Buy_Qty < row.Sell_Qty:
            qty = row.Buy_Qty
            pnl = round(row.Buy_Qty * (row.Sell_Avg - row.Buy_Avg), 2)
            lists.append([cn, qty, pnl])
        else:
            qty = row.Sell_Qty
            pnl = round(row.Sell_Qty * (row.Sell_Avg - row.Buy_Avg), 2)
            lists.append([cn, qty, pnl])
    r_df = pd.DataFrame(lists, columns=['Contract_name', 'Squared_Qty', 'Realized_PnL'])
    return merge_df(df, r_df)


def get_close_data(symbols_lst, df):

    sp = get_strike_price_list_from_contract_names(symbols_lst)
    closes = []
    temp = df[df['Strike Price'].isin(sp)]
    temp = temp[['Strike Price', 'CE Close', 'PE Close']].reset_index()

    for item in symbols_lst:

        lst = item.split('-')

        sp_filter = temp['Strike Price'] == float(lst[1])

        val = temp.loc[sp_filter, '{} Close'.format(lst[2])].values[0]

        closes.append([item, val])

    return pd.DataFrame(closes, columns=['Contract_name', 'Close'])


def get_strike_price_list_from_contract_names(sym_lst):
    sp = []
    for elem in sym_lst:
        sp.append(float(elem.split('-')[1]))
    return sp

