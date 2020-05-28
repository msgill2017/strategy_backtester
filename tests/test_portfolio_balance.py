from unittest import TestCase
from strategy_backtester.portfolio_balance import get_strike_price_list_from_contract_names, combine_same_contract, \
    find_avg_and_add_col_to_df, combine_same_contract_col, find_avg_and_add_col_to_df_col
try:
    import pandas as pd
    import numpy as np
except ImportError:
    pass
from pandas.util.testing import assert_frame_equal


class TestPortfolioBalance(TestCase):
    def setUp(self):
        """ Your setUp """
        # test data file path, the fils is a csv file.
        option_file = './data/OPTSTK.csv'
        trade_file = './data/TRADEBOOK.csv'

        try:
            df = pd.read_csv(option_file)
            tb_df = pd.read_csv(trade_file)
        except IOError:
            print('cannot open file')
        self.fixture_df = df
        self.fixture_tb_df = tb_df

    def tearDown(self):
        del self.fixture_df
        del self.fixture_tb_df

    def test_get_strike_price_from_contract_name(self):

        assert get_strike_price_list_from_contract_names(['DLF-220.0-CE']) == [220.0]
        assert isinstance(get_strike_price_list_from_contract_names(['DLF-220.0-CE']), list) is True

    def test_combine_same_contract(self):
        c_lst = [
                        ['DLF-190.0-CE',  'BUY', 2600, 3120.0],
                        ['DLF-195.0-PE',  'SELL', 2600, 5200.0],
                        ['DLF-210.0-PE',  'BUY', 5200, 6240.0],
                        ['DLF-220.0-CE',  'SELL', 5200, 7800.0]
                        ]
        c_df = pd.DataFrame(c_lst, columns=combine_same_contract_col)
        assert c_df.equals(combine_same_contract(self.fixture_tb_df)) is True
        # assert_frame_equal(combine_same_contract(self.fixture_tb_df), expected_df)

    def test_find_avg_and_add_col_to_df(self):
        a_lst = [
            ['DLF-190.0-CE',  'BUY', 2600, 1.2, 3120.0],
            ['DLF-195.0-PE',  'SELL', 2600, 2.0, 5200.0],
            ['DLF-210.0-PE',  'BUY', 5200, 1.2, 6240.0],
            ['DLF-220.0-CE',  'SELL', 5200, 1.5, 7800.0]
                ]
        a_df = pd.DataFrame(a_lst, columns=find_avg_and_add_col_to_df_col)

        c_df = combine_same_contract(self.fixture_tb_df)

        assert a_df.equals(find_avg_and_add_col_to_df(c_df)) is True
        # assert_frame_equal(find_avg_and_add_col_to_df(c_df), a_df)
