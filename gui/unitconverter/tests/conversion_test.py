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

    def tearDown(self):
        pass

    def test_from_centimeters(self):
        self.L.from_centimeters(100)
        self.assertAlmostEqual(self.L.meters, 1, places=5)


if __name__ == "__main__":
    unittest.main()
