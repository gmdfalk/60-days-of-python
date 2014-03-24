"""
    Created on 23 Mar 2014
    @author: Max Demian
"""

import unittest
from ..real_estate import Property, House, Apartment, Agent, Purchase, Rental
from ..real_estate import (HouseRental, HousePurchase, ApartmentPurchase,
                           ApartmentRental)


class RealEstateTest(unittest.TestCase):


    def setUp(self):
        self.p = Property()
        self.h = House(144, 3, 3, 3, True, False)
        self.a = Apartment()

    def test_property(self):
        self.assertIsInstance(self.p, Property)
        self.assertEqual(self.p.square_feet, 0)

    def test_house(self):
        self.assertIsInstance(self.h, Property)
        self.assertEqual(self.h.fence, False)


if __name__ == "__main__":
    unittest.main()
