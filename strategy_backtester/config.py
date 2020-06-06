#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Sun May 14 2020

@author: Mandeep S Gill

email : msg8930@yahoo.com

'''
import os.path


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))

symbol = 'DLF'
expiry_date = '30-05-2019'
lot_size = 2600
TRADE_COL = ['Type', 'Option', 'Strike Price', 'Premium', 'Qty']
trade_book = {'Contract_name': 'Contract_name', 'Open_date': 'Open_date', 'Type': 'Type',
              'Qty': 'Qty', 'Premium': 'Premium', 'Trade_value': 'Trade_value'}

trade_book_col = ['Contract_name', 'Open_date', 'Type', 'Qty', 'Premium', 'Trade_value']

sum_qty_trade_value_col = ['Contract_name', 'Type', 'Qty', 'Trade_value']

find_avg_and_add_col_to_df_col = ['Contract_name', 'Type', 'Qty', 'Avg', 'Trade_value']

display_buy_and_sell_side_by_side_col = ['Contract_name', 'Buy_Qty', 'Buy_Avg', 'Buy_Value', 'Sell_Qty', 'Sell_Avg',
                                         'Sell_Value']

open_trade_positions_col = ['Contract_name', 'Open_Type', 'Open_Qty']

trade_types = ['Buy', 'Sell']

message = {'Type': 'Type (Buy/Sell)', 'Option': 'Option (Call/Put)', 'Strike Price': 'Strike Price (from above list)',
           'Premium': 'Premium ', 'Qty': 'Qty (No. of Lots) '}
