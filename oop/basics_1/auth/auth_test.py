"""
    Created on 25 Mar 2014

    @author: Max Demian
"""

import unittest
from auth import User, Authorizor, Manager


class AuthTest(unittest.TestCase):


    def setUp(self):
        u = User()
        a = Authorizor()
        m = Manager()
        m.add_user()

    def test_user(self):
        u = User("frank", "password")
        self.assertEqual(u.password, "password")

    def test_add_user(self):
        pass

    def test_authorize(self):
        pass

if __name__ == "__main__":
    unittest.main()
