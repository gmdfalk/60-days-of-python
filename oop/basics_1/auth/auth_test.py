"""
    Created on 25 Mar 2014

    @author: Max Demian
"""

import unittest
from auth import User, Authorizor, Authenticator, PasswordTooShort
from auth import UsernameAlreadyExists, InvalidPassword


class AuthTest(unittest.TestCase):


    def setUp(self):
        self.authenticator = Authenticator()
        self.auth = Authorizor(self.authenticator)
        self.authenticator.add_user("frank", "thetank")

    def test_user_exists_in_dictionary(self):
        self.assertTrue("frank" in self.authenticator.users)
        self.assertTrue(self.authenticator.users["frank"].check_password("thetank"))

    def test_exception_password_too_short(self):
        self.assertRaises(PasswordTooShort,
                          self.authenticator.add_user("tim", "struppi"))

    def test_exception_username_exists(self):
        with self.assertRaises(UsernameAlreadyExists):
            self.authenticator.add_user('frank', 'number2')

    def test_exception_invalid_password(self):
        with self.assertRaises(InvalidPassword):
            self.authenticator.login("frank", "")

    def test_add_user(self):
        self.authenticator.add_user("tim", "struppi")
        self.assertTrue("frank" in self.authenticator.users)

    def test_is_logged_in(self):
        self.assertFalse(self.authenticator.is_logged_in("frank"))
        self.authenticator.login("frank", "thetank")
        self.assertTrue(self.authenticator.is_logged_in("frank"))


    def test_add_permission(self):
        pass

    def test_permit_user(self):
        pass

if __name__ == "__main__":
    unittest.main()
