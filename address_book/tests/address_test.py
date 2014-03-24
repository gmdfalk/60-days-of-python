"""
    Created on 23 Mar 2014

    @author: Max Demian
"""

import unittest
from ..address_book import Address


class Test(unittest.TestCase):


    def test_address(self):
        a = Address()
        a.tst = "testattribute"


if __name__ == "__main__":
    unittest.main()
