#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 2020

@author: Mandeep S Gill

email : msg8930@yahoo.com

"""

from commons import open_file, trade_book, trading_days, order_place, exit_loop, save_df, list_to_df, portfolio_start_balance
from config import symbol, expiry_date

option_chain_df = open_file("Data/{}-OPTSTK-{}.csv".format(symbol, expiry_date))

working_days = trading_days(option_chain_df)

trade_book = trade_book(symbol, expiry_date)

already_trade_days = trading_days(trade_book, col='Open Date')

remaining_working_days = [elem for elem in working_days if elem not in already_trade_days]

for day in remaining_working_days:
    portfolio_start_balance(trade_book, day)

    filter_date = option_chain_df['Date'] == day
    current_day_option_chain_df = option_chain_df[filter_date]

    # print(current_day_optionchain_df)
    while True:
        trade = input("Are you interested in Trade Today (Yes or No) oR Enter (Exit or e) for Exit:")
        order = []
        if trade == '' or trade[0].upper() == 'Y':
            order = order_place(current_day_option_chain_df)
            order.append(day)
            print(order)
            order_df = list_to_df(order)
            print("order-df", order_df)
            trade_book = trade_book.append(order_df, sort=False, ignore_index=True)
            print("Trade Book is ", trade_book)
        #     orders_list.append(order)
        #     # print("Order List", len(orders_list))
        #     display_trade_info(orders_list)
        if exit_loop(trade):
            print("Exit")
            break
        if trade and trade[0].upper() != 'Y':
            # if orders_lst:
                # display_trade_info(orders_list)
            # else:
            print("----------------------------------")
            print("No trade is available to display yet")
            break
    if exit_loop(trade):
        save_df(trade_book, symbol, expiry_date)
        break
