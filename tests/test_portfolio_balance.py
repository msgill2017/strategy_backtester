from unittest import TestCase
from strategy_backtester.portfolio_balance import get_strike_price_list_from_contract_names, combine_same_contract
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
        option_file = './Data/OPTSTK.csv'
        trade_file = './Data/TRADEBOOK.csv'

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
        expected_lst = [
                        ['DLF-190.0-CE',  'BUY', 2600, 3120.0],
                        ['DLF-195.0-PE',  'SELL', 2600, 5200.0],
                        ['DLF-210.0-PE',  'BUY', 5200, 6240.0],
                        ['DLF-220.0-CE',  'SELL', 5200, 7800.0]
                        ]
        col = ['Contract_name',  'Type',  'Qty',  'Trade_Value']
        expected_df = pd.DataFrame(expected_lst, columns=col)
        assert expected_df.equals(combine_same_contract(self.fixture_tb_df)) is True

        # assert_frame_equal(combine_same_contract(self.fixture_tb_df), expected_df)
