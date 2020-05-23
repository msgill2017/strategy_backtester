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
        sp = 205
        result = order.is_strike_price_available(sp, data)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()