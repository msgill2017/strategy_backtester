from unittest import TestCase
from strategy_backtester.config import TRADE_COL
from strategy_backtester.trade import get_validator, validate_type, validate_option, validate_strike_price,\
    validate_premium, validate_qty, get_underline_price, get_strike_price, premium_cols, premium_range, \
    is_premium_in_range


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
        assert isinstance(validate_type('Sell')[1], str) is True

    def test_validate_option(self):
        expected_input = ['Call', 'CALL', 'PUT', 'put', 'Put', 'call']

        for item in expected_input:
            assert validate_option(item) == (True, 'CE' if item.upper()=='CALL' else 'PE')
        assert validate_option('coll') == (False, 'CALL or PUT')
        assert validate_option('pot') == (False, 'CALL or PUT')
        assert isinstance(validate_option('put')[1], str) is True

    def test_validate_strike_price(self):
        # strike_price_available = [210, 205, 200, 195, 190, 185, 180, 175, 170, 165]

        assert validate_strike_price('210', df) == (True, 210.0)
        assert validate_strike_price('270', df) == (False, 'Valid Strike Price from Available list ')
        assert validate_strike_price('210.0', df) == (True, 210.0)
        assert validate_strike_price('210.5', df) == (False, 'Valid Strike Price from Available list ')
        assert isinstance(validate_strike_price('210', df)[1], float) is True

    def test_validate_premium(self):
        # CE Open,CE High,CE Low,CE Close,Strike Price,Underlying,PE Strike Price,PE Open,PE High,PE Low,PE Close
        # 4.3,      4.3,   2.95,   3.1,     195,        174.3,      160,            2.9,    3.7,    2.9, 3.35
        trade1 ={'Option': 'CE','Strike Price': 195.0, 'Type': 'BUY'}
        trade2 = {'Option': 'PE', 'Strike Price': 195.0, 'Type': 'BUY'}

        assert validate_premium('3', df, trade1) == (True, 3.0)
        assert validate_premium('2.96', df, trade1) == (True, 2.96)
        assert validate_premium('2.94', df, trade1) == (False, ' Premium within range [4.3, 2.95] ')
        assert validate_premium('3', df, trade2) == (True, 3.0)
        assert validate_premium('2.96', df, trade2) == (True, 2.96)
        assert validate_premium('2.89', df, trade2) == (False, ' Premium within range [3.7, 2.9] ')
        assert isinstance(validate_premium('2.96', df, trade2)[1], float) is True

    def test_premium_cols(self):

        assert premium_cols('CE') == ['CE High', 'CE Low']
        assert premium_cols('PE') == ['PE High', 'PE Low']

    def test_premium_range(self):
        call = ['CE High', 'CE Low']
        put = ['PE High', 'PE Low']
        c_h_l = [4.3, 2.95]
        p_h_l = [3.7, 2.9]
        assert all([a == b for a, b in zip(c_h_l, premium_range(df, call, 195))])
        assert all([a == b for a, b in zip(p_h_l, premium_range(df, put, 195))])
        assert isinstance(premium_range(df, put, 195), list) is True
        assert len(premium_range(df, put, 195)) == 2

    def test_is_premium_in_range(self):

        assert is_premium_in_range('25.3', [28, 22]) is True
        assert is_premium_in_range('28.3', [28, 22]) is False
        assert is_premium_in_range('21.3', [28, 22]) is False
        assert is_premium_in_range('28', [28, 22]) is True
        assert is_premium_in_range('22', [28, 22]) is True
        assert is_premium_in_range('0', [28, 22]) is False

    def test_validate_qty_value(self):

        assert validate_qty('1') == (True, 1)
        assert isinstance(validate_qty('1')[1], int) is True
        assert validate_qty('1.1') == (False, ' Qty with positive integer number only: ')
        assert validate_qty('1.a') == (False, ' Qty with positive integer number only: ')
