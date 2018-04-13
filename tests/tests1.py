# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 14:26:43 2018

@author: pwin
@version: 0.1
@since: 2018-04-13

"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from StockManager import StockManager


class ModuleTest(unittest.TestCase):
    """unit tests for the module"""
    def setUp(self):
        self.c = StockManager.StockManager()

    def test_geom_mean(self):
        self.assertAlmostEqual(self.c.geom_mean([1, 3 , 9, 27, 81]), 9)

    def test_calculate_p_e_ratio_POP(self):
        stock_code = 'POP'
        market_price = 24
        self.assertEqual(self.c.calculate_p_e_ratio(stock_code, market_price),3 )

    def test_calculate_p_e_ratio_TEA(self):
        stock_code = 'TEA'
        market_price = 24
        self.assertRaises(ZeroDivisionError, self.c.calculate_p_e_ratio(stock_code, market_price))

    def test_calculate_dividend_yield_POP(self):
        stock_code = 'POP'
        market_price = 24
        self.assertAlmostEqual(self.c.calculate_dividend_yield(stock_code, market_price),0.33333333 )

    def test_calculate_dividend_yield_GIN(self):
        stock_code = 'GIN'
        market_price = 24
        self.assertAlmostEqual(self.c.calculate_dividend_yield(stock_code, market_price),0.08333333 )

    def tearDown(self):
            self.c = None
            
if __name__ == "__main__":
    unittest.main()