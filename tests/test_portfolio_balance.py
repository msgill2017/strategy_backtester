from unittest import TestCase

from strategy_backtester import portfolio_balance
from strategy_backtester import config

from tests.data import trade_book_data

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
        # trade_file = './data/TRADEBOOK.csv'

        try:
            df = pd.read_csv(option_file)
            tb_df = pd.DataFrame(trade_book_data.trade_book_lst, columns=config.trade_book_col)
        except IOError:
            print('cannot open file')
        self.fixture_df = df
        self.fixture_tb_df = tb_df

    def tearDown(self):
        del self.fixture_df
        del self.fixture_tb_df

    def test_get_unique_contracts_lst(self):
        assert portfolio_balance.get_unique_contracts_lst(self.fixture_tb_df) == ['DLF-220.0-CE', 'DLF-210.0-PE', 'DLF-195.0-PE',
                                                                'DLF-190.0-CE', 'DLF-200.0-PE']
        assert isinstance(portfolio_balance.get_unique_contracts_lst(self.fixture_tb_df), list) is True

    def test_get_strike_price_from_contract_name(self):

        assert portfolio_balance.get_strike_price_list_from_contract_names(['DLF-220.0-CE']) == [220.0]
        assert isinstance(portfolio_balance.get_strike_price_list_from_contract_names(['DLF-220.0-CE']), list) is True

    def test_sort_df_with_column(self):

        expected_df = pd.DataFrame(trade_book_data.expected_sorted_lst,
                                   columns=config.trade_book_col)
        # print(expected_df)
        assert expected_df.equals(portfolio_balance.sort_df_with_column(self.fixture_tb_df,
                                                      column=config.trade_book['Contract_name'])) is True

    def test_sum_qty_and_trade_value_contracts(self):

        c_df = pd.DataFrame(trade_book_data.expected_sum_qty_trade_value_lst,
                            columns=config.sum_qty_trade_value_col)
        assert c_df.equals(portfolio_balance.sum_qty_and_trade_value_contracts(self.fixture_tb_df)) is True
        # assert_frame_equal(sum_qty_and_trade_value_contracts(self.fixture_tb_df), expected_df)

    def test_find_avg_and_add_col_to_df(self):

        a_df = pd.DataFrame(trade_book_data.expected_avg_lst,
                            columns=config.find_avg_and_add_col_to_df_col)

        c_df = portfolio_balance.sum_qty_and_trade_value_contracts(self.fixture_tb_df)

        assert a_df.equals(portfolio_balance.find_avg_and_add_col_to_df(c_df)) is True
        # assert_frame_equal(find_avg_and_add_col_to_df(c_df), a_df)

    def test_display_buy_and_sell_side_by_side(self):

        d_df = pd.DataFrame(trade_book_data.expected_display_lst,
                            columns=config.display_buy_and_sell_side_by_side_col)

        c_df = portfolio_balance.sum_qty_and_trade_value_contracts(self.fixture_tb_df)

        a_df = portfolio_balance.find_avg_and_add_col_to_df(c_df)

        assert d_df.equals(portfolio_balance.display_buy_and_sell_side_by_side(a_df)) is True

    def test_trade_type_conversion(self):
        assert portfolio_balance.trade_type_conversion(-1) == 'Buy'
        assert portfolio_balance.trade_type_conversion(1) == 'Sell'
        assert portfolio_balance.trade_type_conversion(0) == 'None'

    def test_find_pending_trade(self):
        expected_res = pd.Series(['Sell', 'Buy', 'Sell', 'Buy', 'Buy'])
        c_df = portfolio_balance.sum_qty_and_trade_value_contracts(self.fixture_tb_df)
        a_df = portfolio_balance.find_avg_and_add_col_to_df(c_df)
        d_df = portfolio_balance.display_buy_and_sell_side_by_side(a_df)
        pd.testing.assert_series_equal((portfolio_balance.find_pending_trade(d_df)), expected_res,
                                       check_names=False)

    # def test_open_trade_positions(self):
    #
    #     op_df = pd.DataFrame(trade_book_data.expected_open_positions_lst, columns=config.open_trade_positions_col)
    #     c_df = portfolio_balance.sum_qty_and_trade_value_contracts(self.fixture_tb_df)
    #     a_df = portfolio_balance.find_avg_and_add_col_to_df(c_df)
    #     d_df = portfolio_balance.display_buy_and_sell_side_by_side(a_df)
    #     assert op_df.equals(portfolio_balance.open_trade_positions(d_df)) is True

    def test_get_close_data(self):
        expected_res1 = pd.DataFrame([['DLF-190.0-CE', 4.25]], columns=['Contract_name', 'Close'])
        expected_res2 = pd.DataFrame([['DLF-195.0-PE', 3.35]], columns=['Contract_name', 'Close'])

        assert expected_res1.equals(portfolio_balance.get_close_data(['DLF-190.0-CE'], self.fixture_df)) is True
        assert expected_res2.equals(portfolio_balance.get_close_data(['DLF-195.0-PE'], self.fixture_df)) is True

