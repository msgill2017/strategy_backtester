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

    def test_check_premium_in_high_low(self):

        self.assertTrue(order.check_premium_in_high_low('25.3', [28, 22]))
        self.assertFalse(order.check_premium_in_high_low('28.3', [28, 22]))
        self.assertFalse(order.check_premium_in_high_low('21.8', [28, 22]))
        self.assertTrue(order.check_premium_in_high_low('28', [28, 22]))
        self.assertTrue(order.check_premium_in_high_low('22', [28, 22]))
        self.assertTrue(order.check_premium_in_high_low(22, [28, 22]))


if __name__ == '__main__':
    unittest.main()