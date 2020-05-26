from unittest import TestCase


from strategy_backtester.order import get_underline_price, get_strike_price,  \
    user_response_to_dic, user_input_type_option_purification, request_user_updated_input, \
    validate_strike_price, validate_premium_price, premium_cols, premium_range, is_premium_in_range, \
    validate_qty_value, empty_order

import pytest

try:
    import pandas as pd
except ImportError:
    pass

# test data file path, the fils is a csv file.
test_data_file_path = './Data/OPTSTK.csv'

df = pd.read_csv(test_data_file_path)


class TestOrder(TestCase):
    # def test_empty_order(self):
    #     assert empty_order() == 'aa'

    def test_get_underline_price(self):
        assert get_underline_price(df) == 174.3

    def test_get_strike_price(self):
        expected = [210, 205, 200, 195, 190, 185, 180, 175, 170, 165]

        assert get_strike_price(df) == expected

    def test_user_response_to_dic(self):
        inp = ['Long', 'CE', '210.0', '1', '1']
        expected = {'Type': 'Long', 'Option': 'CE', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        result = user_response_to_dic(inp)
        assert result == expected
        for val in result:
            assert type(val) == type('str')

    def test_user_input_type_option_purification(self):
        o1 = {'Type': 'Long', 'Option': 'CE', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        o2 = {'Type': 'Short', 'Option': 'PE', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        o3 = {'Type': 'S', 'Option': 'Call', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        o4 = {'Type': 'L', 'Option': 'Put', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        o5 = {'Type': 'wrong', 'Option': 'wrong', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        o6 = {'Type': 'local', 'Option': 'copper', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        o7 = {'Type': 'copper', 'Option': 'local', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        assert user_input_type_option_purification(o1, 'Type') == (True, 'Long')
        assert user_input_type_option_purification(o1, 'Option') == (True, 'CE')
        assert user_input_type_option_purification(o2, 'Type') == (True, 'Short')
        assert user_input_type_option_purification(o2, 'Option') == (True, 'PE')
        assert user_input_type_option_purification(o3, 'Type') == (True, 'Short')
        assert user_input_type_option_purification(o3, 'Option') == (True, 'CE')
        assert user_input_type_option_purification(o4, 'Type') == (True, 'Long')
        assert user_input_type_option_purification(o4, 'Option') == (True, 'PE')
        assert user_input_type_option_purification(o5, 'Type') == (False, ' ')
        assert user_input_type_option_purification(o5, 'Option') == (False, ' ')
        assert user_input_type_option_purification(o6, 'Type') == (False, ' ')
        assert user_input_type_option_purification(o6, 'Option') == (False, ' ')
        assert user_input_type_option_purification(o7, 'Type') == (False, ' ')
        assert user_input_type_option_purification(o7, 'Option') == (False, ' ')

    # def test_request_user_updated_input(self, monkeypatch):
    #     o1 = {'Type': 'Long', 'Option': 'CE', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
    #     o2 = {'Type': 'Short', 'Option': 'PE', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
    #     monkeypatch.setattr('builtins.input', lambda: "Mark")
    #     assert request_user_updated_input(user_input_type_option_purification, 'Type') == (False, ' ')

    def test_validate_strike_price(self):

        # strike_price_available = [210, 205, 200, 195, 190, 185, 180, 175, 170, 165]
        o1 = {'Type': 'Long', 'Option': 'CE', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        o2 = {'Type': 'Short', 'Option': 'PE', 'Strike Price': '270.0', 'Premium': '1', 'Qty': '1'}
        assert validate_strike_price(o1, df) == (True, 210.0)
        assert validate_strike_price(o2, df) == (False, ' ')
        assert validate_strike_price(o2, df, res='210') == (True, 210.0)
        assert validate_strike_price(o2, df, res='268') == (False, ' ')

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

    def test_validate_premium_price(self):

        # strike_price_available = [210, 205, 200, 195, 190, 185, 180, 175, 170, 165]
        o1 = {'Type': 'Long', 'Option': 'CE', 'Strike Price': '195.0', 'Premium': '3', 'Qty': '1'}
        o2 = {'Type': 'Short', 'Option': 'PE', 'Strike Price': '195.0', 'Premium': '3', 'Qty': '1'}
        o3 = {'Type': 'Long', 'Option': 'CE', 'Strike Price': '195.0', 'Premium': '5', 'Qty': '1'}
        o4 = {'Type': 'Short', 'Option': 'PE', 'Strike Price': '195.0', 'Premium': '4', 'Qty': '1'}
        o5 = {'Type': 'Long', 'Option': 'CE', 'Strike Price': '195.0', 'Premium': '2.94', 'Qty': '1'}
        o6 = {'Type': 'Short', 'Option': 'PE', 'Strike Price': '195.0', 'Premium': '2.8', 'Qty': '1'}
        assert validate_premium_price(o1, df) == (True, 3.0)
        assert validate_premium_price(o2, df) == (True, 3.0)
        assert validate_premium_price(o3, df) == (False, ' ')
        assert validate_premium_price(o4, df) == (False, ' ')
        assert validate_premium_price(o5, df) == (False, ' ')
        assert validate_premium_price(o6, df) == (False, ' ')
        assert validate_premium_price(o3, df, res='3.3') == (True, 3.3)
        assert validate_premium_price(o3, df, res='6') == (False, ' ')

    def test_validate_qty_value(self):

        # strike_price_available = [210, 205, 200, 195, 190, 185, 180, 175, 170, 165]
        o1 = {'Type': 'Long', 'Option': 'CE', 'Strike Price': '195.0', 'Premium': '3', 'Qty': '1'}
        o2 = {'Type': 'Short', 'Option': 'PE', 'Strike Price': '195.0', 'Premium': '3', 'Qty': '-1'}
        o3 = {'Type': 'Long', 'Option': 'CE', 'Strike Price': '195.0', 'Premium': '5', 'Qty': 'a'}
        o4 = {'Type': 'Short', 'Option': 'PE', 'Strike Price': '195.0', 'Premium': '4', 'Qty': '1.1'}
        o5 = {'Type': 'Long', 'Option': 'CE', 'Strike Price': '195.0', 'Premium': '2.94', 'Qty': '1'}
        o6 = {'Type': 'Short', 'Option': 'PE', 'Strike Price': '195.0', 'Premium': '2.8', 'Qty': '1'}
        assert validate_qty_value(o1) == (True, 1)
        assert validate_qty_value(o2) == (False, ' ')
        assert validate_qty_value(o3) == (False, ' ')
        assert validate_qty_value(o3, res='2') == (True, 2)
        assert validate_qty_value(o3, res='-2') == (False, ' ')
        assert validate_qty_value(o6, res='a') == (False, ' ')
        # assert validate_premium_price(o3, df, res='3.3') == (True, 3.3)
        # assert validate_premium_price(o3, df, res='6') == (False, ' ')
