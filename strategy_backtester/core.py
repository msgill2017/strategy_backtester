#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 2020

@author: Mandeep S Gill

email : msg8930@yahoo.com

"""

from strategy_backtester.commons import open_file, trade_book, trading_days, exit_loop, save_df,\
                    list_to_df, no_trade_entry
from strategy_backtester.config import symbol, expiry_date, data_dir
from strategy_backtester.portfolio_balance import portfolio_balance
from strategy_backtester.order import order_place

filename = data_dir + '/{}-OPTSTK-{}.csv'.format(symbol, expiry_date)

option_chain_df = open_file(filename)

working_days = trading_days(option_chain_df)

trade_book = trade_book(symbol, expiry_date)

already_trade_days = trading_days(trade_book, col='Open_date')

remaining_working_days = [elem for elem in working_days if elem not in already_trade_days]

previous_day = working_days[0]
if already_trade_days:
    previous_day = already_trade_days[-1]
    portfolio_balance(trade_book, option_chain_df, previous_day)

for day in remaining_working_days:

    filter_date = option_chain_df['Date'] == previous_day
    previous_day_option_chain_df = option_chain_df[filter_date]

    filter_date = option_chain_df['Date'] == day
    current_day_option_chain_df = option_chain_df[filter_date]

    # print(current_day_optionchain_df)
    while True:

        trade = input("Are you interested in Trade Today (Yes or No) oR Enter (Exit or e) for Exit:")
        order = []
        if trade == '' or trade[0].upper() == 'Y':

            order = order_place(current_day_option_chain_df)
            order.append(day)
            # print(order)
            order_df = list_to_df(order)

            trade_book = trade_book.append(order_df, sort=False, ignore_index=True)
            # print(trade_book)
            portfolio_balance(trade_book, previous_day_option_chain_df, previous_day)

        if exit_loop(trade):
            print("Exit")
            break

        if trade and trade[0].upper() != 'Y':

            portfolio_balance(trade_book, previous_day_option_chain_df, previous_day)

            nte_df = no_trade_entry(trade_book, day)
            trade_book = trade_book.append(nte_df, sort=False, ignore_index=True)
            previous_day = day
            break
    if exit_loop(trade):
        save_df(trade_book, symbol, expiry_date)
        break
