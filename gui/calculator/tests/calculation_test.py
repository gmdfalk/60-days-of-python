#!/usr/bin/env python2
"""
    Created on 22 Apr 2014

    @author: Max Demian
"""

import unittest
from gui.calculator.calculation import Calculation


class CalculationTest(unittest.TestCase):

    def setUp(self):
        self.c = Calculation()

    def test_evaluate(self):
        self.c.test = 10
        self.assertEqual(self.c.test, 10)
        self.assertEqual(self.c.evaluate("17*3"), 51)


if __name__ == "__main__":
    unittest.main()
