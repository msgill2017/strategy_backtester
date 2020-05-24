# -*- coding: utf-8 -*-

from strategy_backtester import order


try:
    import pandas as pd
except ImportError:
    pass

import unittest

# test data file path, the fils is a csv file.
test_data_file_path = './Data/OPTSTK.csv'

df = pd.read_csv(test_data_file_path)


class OrderTestSuite(unittest.TestCase):

    """Basic test cases."""

    def test_get_available_strike_price(self):

        data = [210, 205, 200, 195, 190, 185, 180, 175, 170, 165]
        result = order.get_available_strike_price(df)

        self.assertEqual(data, result)
        self.assertRaises(TypeError, order.get_available_strike_price(data))

    def test_is_strike_price_available(self):
        data = [210, 205, 200, 195, 190, 185, 180, 175, 170, 165]

        self.assertTrue(order.is_strike_price_available(205, data))
        self.assertFalse(order.is_strike_price_available(150, data))

    def test_is_inp_str_number(self):

        self.assertTrue(order.is_inp_str_number('25'))
        self.assertFalse(order.is_inp_str_number('A'))
        self.assertFalse(order.is_inp_str_number('25.2.1'))
        self.assertFalse(order.is_inp_str_number('25.2a'))
        self.assertTrue(order.is_inp_str_number('25.3'))
        self.assertFalse(order.is_inp_str_number('-25.3'))

    def test_premium_cols(self):
        def broken_function():
            raise Exception('This is broken')

        with self.assertRaises(Exception) as context:
            broken_function()

        self.assertEqual(order.premium_cols('CE'), ['CE High', 'CE Low'])
        self.assertEqual(order.premium_cols('PE'), ['PE High', 'PE Low'])
        self.assertEqual(order.premium_cols('ce'), ['CE High', 'CE Low'])
        self.assertEqual(order.premium_cols('pe'), ['PE High', 'PE Low'])
        self.assertTrue('This is broken' in str(context.exception))

    def test_is_premium_in_high_low(self):

        self.assertTrue(order.is_premium_in_high_low('25.3', [28, 22]))
        self.assertFalse(order.is_premium_in_high_low('28.3', [28, 22]))
        self.assertFalse(order.is_premium_in_high_low('21.8', [28, 22]))
        self.assertTrue(order.is_premium_in_high_low('28', [28, 22]))
        self.assertTrue(order.is_premium_in_high_low('22', [28, 22]))
        self.assertTrue(order.is_premium_in_high_low(22, [28, 22]))

    def test_user_response_to_order_dic(self):
        inp = ['Long', 'CE', '210.0', '1', '1']
        out = {'Type': 'Long', 'Option': 'CE', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        self.assertEqual(order.user_response_to_order_dic(inp), out)

    def test_user_input_type_and_option_purification(self):
        o1 = {'Type': 'Long', 'Option': 'CE', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        o2 = {'Type': 'Short', 'Option': 'PE', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        o3 = {'Type': 'S', 'Option': 'Call', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        o4 = {'Type': 'L', 'Option': 'Put', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}
        o5 = {'Type': 'Other', 'Option': 'l', 'Strike Price': '210.0', 'Premium': '1', 'Qty': '1'}

        self.assertTupleEqual(order.user_input_type_option_purification(o1, 'Type'), (True, 'Long'))
        self.assertTupleEqual(order.user_input_type_option_purification(o2, 'Type'), (True, 'Short'))
        self.assertTupleEqual(order.user_input_type_option_purification(o3, 'Type'), (True, 'Short'))
        self.assertTupleEqual(order.user_input_type_option_purification(o4, 'Type'), (True, 'Long'))
        self.assertTupleEqual(order.user_input_type_option_purification(o5, 'Type'), (False, ' '))

        self.assertTupleEqual(order.user_input_type_option_purification(o1, 'Option'), (True, 'CE'))
        self.assertTupleEqual(order.user_input_type_option_purification(o2, 'Option'), (True, 'PE'))
        self.assertTupleEqual(order.user_input_type_option_purification(o3, 'Option'), (True, 'CE'))
        self.assertTupleEqual(order.user_input_type_option_purification(o4, 'Option'), (True, 'PE'))
        self.assertTupleEqual(order.user_input_type_option_purification(o5, 'Option'), (False, ' '))

if __name__ == '__main__':
    unittest.main()