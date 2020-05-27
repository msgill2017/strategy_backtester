from unittest import TestCase
from strategy_backtester.commons import trading_days, is_inp_str_number, dic_to_df
from strategy_backtester.config import TRADE_BOOK_COL
try:
    import pandas as pd
    import numpy as np
except ImportError:
    pass
from pandas.util.testing import assert_frame_equal


class TestCommons(TestCase):
    """ class for running unittests """

    def setUp(self):
        """ Your setUp """
        # test data file path, the fils is a csv file.
        option_file = './Data/OPTSTK.csv'
        trade_file = './Data/TRADEBOOKDATE.csv'

        try:
            df = pd.read_csv(option_file)
            tr_date_df = pd.read_csv(trade_file)
        except IOError:
            print('cannot open file')
        self.fixture_df = df
        self.fixture_tr_date_df = tr_date_df

    def tearDown(self):
        del self.fixture_df
        del self.fixture_tr_date_df

    def test_dic_to_df(self):
        trade = {'Type': 'BUY', 'Premium': 1.2, 'Qty': 1, 'Option': 'CE', 'Strike Price': 210.0, 'Date': '2019-04-26'}
        lst = ['DLF-210.0-CE', '2019-04-26', 'BUY', 2600, 1.2, 3120.0]
        trade_df = pd.DataFrame([lst], columns=TRADE_BOOK_COL)
        assert_frame_equal(dic_to_df(trade), trade_df)

    def test_trading_days(self):
        assert trading_days(self.fixture_df) == ['2019-04-26']
        assert trading_days(self.fixture_tr_date_df, col='Open_date') == ['2019-04-26', '2019-04-30']
        assert isinstance(trading_days(self.fixture_df), list) is True

    def test_is_inp_str_number(self):
        assert is_inp_str_number('25') is True
        assert is_inp_str_number('26.5') is True
        assert is_inp_str_number('A') is False
        assert is_inp_str_number('25.2.1') is False
        assert is_inp_str_number('25.2a') is False
        assert is_inp_str_number('-25.1') is False
        # assert is_inp_str_number(1) is TypeError
