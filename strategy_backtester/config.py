#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 2020

@author: Mandeep S Gill

email : msg8930@yahoo.com

"""
import os.path
# import sys
# import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Data'))
print(ROOT_DIR)
print(data_dir)
symbol = 'DLF'
expiry_date = '30-05-2019'
lot_size = 2600

TRADE_BOOK_COL = ["Contract_name", "Open_date", "Qty", "Type", "Trade_Value"]