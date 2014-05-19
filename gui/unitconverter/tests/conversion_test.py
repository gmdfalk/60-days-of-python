#!/usr/bin/env python2
import unittest
from gui.unitconverter.conversion import Length, Volume, Data


class LengthTest(unittest.TestCase):


    def setUp(self):
        self.L = Length()
        self.L.decplaces = 4

    def test_base_case(self):
        self.L.inches = 2
        self.assertEqual(self.L.millimeters, "50.8")
        self.assertEqual(self.L.centimeters, "5.08")
        self.assertEqual(self.L.meters, "0.0508")
        self.assertEqual(self.L.kilometers, "0.0001")
        self.assertEqual(self.L.inches, "2")
        self.assertEqual(self.L.feet, "0.1667")
        self.assertEqual(self.L.yards, "0.0556")
        self.assertEqual(self.L.miles, "0")

    def test_high_precision(self):
        self.L.decplaces = 9
        self.L.centimeters = 34.56789123456
        self.assertEqual(self.L.millimeters, "345.678912346")
        self.assertEqual(self.L.centimeters, "34.567891235")
        self.assertEqual(self.L.meters, "0.345678912")
        self.assertEqual(self.L.kilometers, "0.000345679")
        self.assertEqual(self.L.inches, "13.609405998")
        self.assertEqual(self.L.feet, "1.134117166")
        self.assertEqual(self.L.yards, "0.378039055")
        self.assertEqual(self.L.miles, "0.000214795")

    def test_zero(self):
        self.L.miles = 0
        self.assertEqual(self.L.meters, "0")


class VolumeTest(unittest.TestCase):


    def setUp(self):
        self.v = Volume()
        self.v.decplaces = 4


    def test_base_case(self):
        self.v.ounces = 40
        self.assertEqual(self.v.milliliters, "1182.9412")
        self.assertEqual(self.v.centiliters, "118.2941")
        self.assertEqual(self.v.liters, "1.1829")
        self.assertEqual(self.v.kiloliters, "0.0012")
        self.assertEqual(self.v.ounces, "40")
        self.assertEqual(self.v.pints, "2.5")
        self.assertEqual(self.v.gallons, "0.3125")
        self.assertEqual(self.v.barrels, "0.0099")

    def test_high_precision(self):
        self.v.decplaces = 9
        self.v.centiliters = 123.4567890123
        self.assertEqual(self.v.milliliters, "1234.567890123")
        self.assertEqual(self.v.centiliters, "123.456789012")
        self.assertEqual(self.v.liters, "1.23456789")
        self.assertEqual(self.v.kiloliters, "0.001234568")
        self.assertEqual(self.v.ounces, "41.745706663")
        self.assertEqual(self.v.pints, "2.609106667")
        self.assertEqual(self.v.gallons, "0.326138333")
        self.assertEqual(self.v.barrels, "0.010353598")


class DataTest(unittest.TestCase):

    def setUp(self):
        self.d = Data()

    def test_high_precision(self):
        self.d.decplaces = 10
        self.d.megabytes = 1
        self.assertEqual(self.d.bits, "8000000")
        self.assertEqual(self.d.bytes, "1000000")
        self.assertEqual(self.d.kilobytes, "1000")
        self.assertEqual(self.d.megabytes, "1")
        self.assertEqual(self.d.gigabytes, "0.001")
        self.assertEqual(self.d.terrabytes, "0.000001")
        self.assertEqual(self.d.petabytes, "0.000000001")
        self.assertEqual(self.d.kibibytes, "976.5625")
        self.assertEqual(self.d.mebibytes, "0.9536743164")
        self.assertEqual(self.d.gibibytes, "0.0009313226")
        self.assertEqual(self.d.tebibytes, "0.0000009095")
        self.assertEqual(self.d.pebibytes, "0.0000000009")


if __name__ == "__main__":
    unittest.main()
