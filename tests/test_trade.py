from unittest import TestCase
from strategy_backtester.config import TRADE_COL
from strategy_backtester.trade import get_validator, validate_type, validate_option, validate_strike_price,\
    validate_premium, validate_qty


class TestTrade(TestCase):

    def test_get_validator(self):
        expected = [validate_type, validate_option, validate_strike_price, validate_premium, validate_qty]

        for index, key in enumerate(TRADE_COL):
            assert get_validator(key) == expected[index]

    def test_validate_type(self):
        expected_input = ['BUY', 'Buy', 'buy','SELL','Sell','sell']

        for item in expected_input:
            assert validate_type(item) == (True, item.upper())
        assert validate_type('sall') == (False, 'Sell or Buy')
