from unittest import TestCase
from strategy_backtester.portfolio_balance import get_unique_contracts_lst, get_strike_price_list_from_contract_names, \
    combine_same_contract, find_avg_and_add_col_to_df, display_buy_and_sell_side_by_side

from strategy_backtester.config import combine_same_contract_col, find_avg_and_add_col_to_df_col, display_buy_and_sell_side_by_side_col
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

    def test_get_unique_contracts_lst(self):
        assert get_unique_contracts_lst(self.fixture_tb_df) == ['DLF-220.0-CE', 'DLF-210.0-PE', 'DLF-195.0-PE',
                                                                'DLF-190.0-CE', 'DLF-200.0-PE']
        assert isinstance(get_unique_contracts_lst(self.fixture_tb_df), list) is True

    def test_get_strike_price_from_contract_name(self):

        assert get_strike_price_list_from_contract_names(['DLF-220.0-CE']) == [220.0]
        assert isinstance(get_strike_price_list_from_contract_names(['DLF-220.0-CE']), list) is True

    def test_combine_same_contract(self):
        c_lst = [
                        ['DLF-190.0-CE',  'Buy', 2600, 3120.0],
                        ['DLF-195.0-PE',  'Sell', 2600, 5200.0],
                        ['DLF-200.0-PE',  'Buy', 2600, 3120.0],
                        ['DLF-200.0-PE',  'Sell', 5200, 10400.0],
                        ['DLF-210.0-PE',  'Buy', 5200, 6240.0],
                        ['DLF-220.0-CE',  'Sell', 5200, 7800.0]
                        ]
        c_df = pd.DataFrame(c_lst, columns=combine_same_contract_col)
        assert c_df.equals(combine_same_contract(self.fixture_tb_df)) is True
        # assert_frame_equal(combine_same_contract(self.fixture_tb_df), expected_df)

    def test_find_avg_and_add_col_to_df(self):
        a_lst = [
            ['DLF-190.0-CE',  'Buy', 2600, 1.2, 3120.0],
            ['DLF-195.0-PE',  'Sell', 2600, 2.0, 5200.0],
            ['DLF-200.0-PE', 'Buy', 2600,   1.2, 3120.0],
            ['DLF-200.0-PE', 'Sell', 5200,  2.0, 10400.0],
            ['DLF-210.0-PE',  'Buy', 5200, 1.2, 6240.0],
            ['DLF-220.0-CE',  'Sell', 5200, 1.5, 7800.0]
                ]
        a_df = pd.DataFrame(a_lst, columns=find_avg_and_add_col_to_df_col)

        c_df = combine_same_contract(self.fixture_tb_df)

        assert a_df.equals(find_avg_and_add_col_to_df(c_df)) is True
        # assert_frame_equal(find_avg_and_add_col_to_df(c_df), a_df)

    def test_display_buy_and_sell_side_by_side(self):
        d_lst = [
                ['DLF-190.0-CE', 2600, 1.2, 3120.0, 0.0,    0.0, 0.0],
                ['DLF-200.0-PE', 2600, 1.2, 3120.0, 5200.0, 2.0, 10400.0],
                ['DLF-210.0-PE', 5200, 1.2, 6240.0, 0.0,    0.0, 0.0],
                ['DLF-195.0-PE',  0.0, 0.0,  0.0,   2600.0, 2.0, 5200.0],
                ['DLF-220.0-CE',  0.0, 0.0,  0.0,   5200.0, 1.5, 7800.0]
                ]
        d_df = pd.DataFrame(d_lst, columns=display_buy_and_sell_side_by_side_col)
        c_df = combine_same_contract(self.fixture_tb_df)
        a_df = find_avg_and_add_col_to_df(c_df)

        assert d_df.equals(display_buy_and_sell_side_by_side(a_df)) is True
