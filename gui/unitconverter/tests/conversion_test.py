#!/usr/bin/env python2
"""
    Created on 17 Apr 2014

    @author: Max Demian
"""

import unittest
from gui.unitconverter.conversion import Length


class Test(unittest.TestCase):


    def setUp(self):
        self.L = Length()
        self.L.inches = 2

    def tearDown(self):
        self.L.precision = 4

    def test_base_case(self):
        self.assertEqual(self.L.millimeters, 50.8)
        self.assertEqual(self.L.centimeters, 5.08)
        self.assertEqual(self.L.meters, 0.0508)
        self.assertEqual(self.L.kilometers, 0.0001)

    def test_high_precision(self):
        self.L.precision = 9
        self.L.centimeters = 34.56789123456
        self.assertEqual(self.L.millimeters, 345.678912346)
        self.assertEqual(self.L.centimeters, 34.567891235)
        self.assertEqual(self.L.meters, 0.345678912)
        self.assertEqual(self.L.kilometers, 0.000345679)
        self.assertEqual(self.L.miles, 0.000214795)

if __name__ == "__main__":
    unittest.main()
