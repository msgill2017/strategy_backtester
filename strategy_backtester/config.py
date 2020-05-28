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
TRADE_BOOK_COL = ['Contract_name', 'Open_date', 'Type', 'Qty', 'Premium', 'Trade_value']
trade_book = {'Contract_name': 'Contract_name', 'Open_date': 'Open_date', 'Type': 'Type',
              'Qty': 'Qty', 'Premium': 'Premium', 'Trade_value': 'Trade_value'}

combine_same_contract_col = ['Contract_name', 'Type', 'Qty', 'Trade_value']

find_avg_and_add_col_to_df_col = ['Contract_name', 'Type', 'Qty', 'Avg', 'Trade_value']

trade_types = ['Buy', 'Sell']
