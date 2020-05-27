from unittest import TestCase
from strategy_backtester.config import TRADE_COL
from strategy_backtester.trade import get_validator, validate_type, validate_option, validate_strike_price,\
    validate_premium, validate_qty, get_underline_price, get_strike_price


try:
    import pandas as pd
except ImportError:
    pass

# test data file path, the fils is a csv file.
test_data_file_path = './Data/OPTSTK.csv'

df = pd.read_csv(test_data_file_path)


class TestTrade(TestCase):

    def test_get_underline_price(self):
        assert get_underline_price(df) == 174.3

    def test_get_strike_price(self):
        expected = [210, 205, 200, 195, 190, 185, 180, 175, 170, 165]

        assert get_strike_price(df) == expected

    def test_get_validator(self):
        expected = [validate_type, validate_option, validate_strike_price, validate_premium, validate_qty]

        for index, key in enumerate(TRADE_COL):
            assert get_validator(key) == expected[index]

    def test_validate_type(self):
        expected_input = ['BUY', 'Buy', 'buy','SELL','Sell','sell']

        for item in expected_input:
            assert validate_type(item) == (True, item.upper())
        assert validate_type('sall') == (False, 'Sell or Buy')

    def test_validate_option(self):
        expected_input = ['Call', 'CALL', 'PUT', 'put', 'Put', 'call']

        for item in expected_input:
            assert validate_option(item) == (True, 'CE' if item.upper()=='CALL' else 'PE')
        assert validate_option('coll') == (False, 'CALL or PUT')
        assert validate_option('pot') == (False, 'CALL or PUT')
