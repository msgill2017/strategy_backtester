from unittest import TestCase
from strategy_backtester.commons import trading_days, is_inp_str_number


class TestCommons(TestCase):
    def test_trading_days(self):
        pass

    def test_is_inp_str_number(self):
        assert is_inp_str_number('25') is True
        assert is_inp_str_number('26.5') is True
        assert is_inp_str_number('A') is False
        assert is_inp_str_number('25.2.1') is False
        assert is_inp_str_number('25.2a') is False
        assert is_inp_str_number('-25.1') is False
        # assert is_inp_str_number(1) is TypeError
