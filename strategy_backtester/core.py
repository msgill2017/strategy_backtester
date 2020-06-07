#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 2020

@author: Mandeep S Gill

email : msg8930@yahoo.com

"""
try:
    import pandas as pd
except ImportError:
    pass

from strategy_backtester.commons import open_file, open_trade_book, trading_days, exit_loop, save_df,\
                    dic_to_df, no_trade_entry
from strategy_backtester.config import symbol, expiry_date, data_dir
from strategy_backtester.portfolio_balance import profit_and_loss_statement, get_unique_contracts_lst
from strategy_backtester.trade import place_trade

filename = data_dir + '/{}-OPTSTK-{}.csv'.format(symbol, expiry_date)

option_chain_df = open_file(filename)

working_days = trading_days(option_chain_df)

previous_trade_book = open_trade_book(symbol, expiry_date)

already_trade_days = trading_days(previous_trade_book, col='Open_date')

remaining_working_days = [elem for elem in working_days if elem not in already_trade_days]
previous_day = working_days[0]

if already_trade_days:
    previous_day = already_trade_days[-1]
    # profit_and_loss_statement(trade_book, option_chain_df, previous_day)

order_book = pd.DataFrame()
orders = pd.DataFrame()

for day in remaining_working_days:

    filter_date = option_chain_df['Date'] == previous_day
    previous_day_option_chain_df = option_chain_df[filter_date]

    filter_date = option_chain_df['Date'] == day
    current_day_option_chain_df = option_chain_df[filter_date]

    if already_trade_days:
        profit_and_loss_statement(previous_trade_book, previous_day_option_chain_df, previous_day)

    while True:

        trade = input("Are you interested in Trade {} (Yes or No) oR (Exit or e) for Exit:".format(day))
        order = []
        if trade == '' or trade[0].upper() == 'Y':

            order = place_trade(current_day_option_chain_df)
            order['Date'] = day
            order_df = dic_to_df(order)
            orders = orders.append(order_df, sort=False, ignore_index=True)

        if exit_loop(trade):
            # print("Exit")
            break

        if trade and trade[0].upper() != 'Y':
            if get_unique_contracts_lst(previous_trade_book):
                profit_and_loss_statement(previous_trade_book, current_day_option_chain_df, day)

            nte_df = no_trade_entry(day)

            orders = orders.append(nte_df, sort=False, ignore_index=True)

            previous_day = day

            break

    if not orders.empty:
        previous_trade_book = previous_trade_book.append(orders)
        order_book = order_book.append(orders)
        orders = pd.DataFrame()

    if exit_loop(trade):
        if not order_book.empty:
            save_df(order_book, symbol, expiry_date)
        break
