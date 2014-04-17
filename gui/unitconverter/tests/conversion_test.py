#!/usr/bin/env python2
"""
    Created on 17 Apr 2014

    @author: Max Demian
"""

import unittest
from gui.unitconverter.conversion import Length, Volume


class LengthTest(unittest.TestCase):


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
        self.assertEqual(self.L.inches, 2)
        self.assertEqual(self.L.feet, 0.1667)
        self.assertEqual(self.L.yards, 0.0556)
        self.assertEqual(self.L.miles, 0.0000)

    def test_high_precision(self):
        self.L.precision = 9
        self.L.centimeters = 34.56789123456
        self.assertEqual(self.L.millimeters, 345.678912346)
        self.assertEqual(self.L.centimeters, 34.567891235)
        self.assertEqual(self.L.meters, 0.345678912)
        self.assertEqual(self.L.kilometers, 0.000345679)
        self.assertEqual(self.L.inches, 13.609413347)
        self.assertEqual(self.L.feet, 1.134117203)
        self.assertEqual(self.L.yards, 0.378037915)
        self.assertEqual(self.L.miles, 0.000214795)


class VolumeTest(unittest.TestCase):


    def setUp(self):
        self.v = Volume()
        self.v.ounces = 40

    def tearDown(self):
        self.v.precision = 4

    def test_base_case(self):
        self.assertEqual(self.v.milliliters, 1182.942)
        self.assertEqual(self.v.centiliters, 118.2942)
        self.assertEqual(self.v.liters, 1.1829)
        self.assertEqual(self.v.kiloliters, 0.0012)
        self.assertEqual(self.v.ounces, 40)
        self.assertEqual(self.v.pints, 2.5)
        self.assertEqual(self.v.gallons, 0.3125)
        self.assertEqual(self.v.barrels, 0.0099)

    def test_high_precision(self):
        self.v.precision = 9
#         self.v.centimeters = 34.56789123456

#     def test_high_precision(self):
#         self.L.precision = 9
#         self.L.centimeters = 34.56789123456
#         self.assertEqual(self.L.millimeters, 345.678912346)
#         self.assertEqual(self.L.centimeters, 34.567891235)
#         self.assertEqual(self.L.meters, 0.345678912)
#         self.assertEqual(self.L.kilometers, 0.000345679)
#         self.assertEqual(self.L.miles, 0.000214795)


if __name__ == "__main__":
    unittest.main()
