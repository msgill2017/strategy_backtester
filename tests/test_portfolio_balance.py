from unittest import TestCase
from strategy_backtester.portfolio_balance import get_strike_price_list_from_contract_name


class TestPortfolioBalance(TestCase):

    def test_get_strike_price_from_contract_name(self):

        assert get_strike_price_list_from_contract_name(['DLF-220.0-CE']) == [220.0]
        assert isinstance(get_strike_price_list_from_contract_name(['DLF-220.0-CE']), list) is True

        