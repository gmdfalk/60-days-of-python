"""
    Created on 25 Mar 2014

    @author: Max Demian
"""

import unittest
from auth import (Authorizor, Authenticator, PasswordTooShort,
                  UsernameAlreadyExists, InvalidPassword, NotLoggedInError,
                  NotPermittedError, InvalidUsername, PermissionError)


# 100% Coverage :o)
class AuthTest(unittest.TestCase):


    def setUp(self):
        self.authenticator = Authenticator()
        self.auth = Authorizor(self.authenticator)
        self.authenticator.add_user("frank", "thetank")

    def test_user_exists_in_dictionary(self):
        self.assertTrue("frank" in self.authenticator.users)
        self.assertTrue(self.authenticator.users["frank"].check_password("thetank"))

    def test_exception_password_too_short(self):
        with self.assertRaises(PasswordTooShort):
            self.authenticator.add_user("struppi", "tim")

    def test_exception_username_exists(self):
        with self.assertRaises(UsernameAlreadyExists):
            self.authenticator.add_user('frank', 'number2')

    def test_exception_invalid_password(self):
        with self.assertRaises(InvalidPassword):
            self.authenticator.login("frank", "")

    def test_exception_invalid_username(self):
        with self.assertRaises(InvalidUsername):
            self.authenticator.login("tom", "")
        self.auth.add_permission("paint")
        with self.assertRaises(InvalidUsername):
            self.auth.permit_user("paint", "fran")

    def test_exception_not_logged_in(self):
        self.auth.add_permission("paint")
        with self.assertRaises(NotLoggedInError):
            self.auth.check_permission("paint", "frank")

    def test_exception_not_permitted(self):
        self.authenticator.login("frank", "thetank")
        self.auth.add_permission("paint")
        with self.assertRaises(NotPermittedError):
            self.auth.check_permission("paint", "frank")

    def test_add_user(self):
        self.authenticator.add_user("tim", "struppi")
        self.assertTrue("frank" in self.authenticator.users)

    def test_login(self):
        self.assertFalse(self.authenticator.is_logged_in("dick"))
        self.authenticator.login("frank", "thetank")
        self.assertTrue(self.authenticator.is_logged_in("frank"))

    def test_check_permission(self):
        self.authenticator.login("frank", "thetank")
        self.auth.add_permission("paint")
        self.auth.permit_user("paint", "frank")
        self.assertTrue(self.auth.check_permission("paint", "frank"))
        with self.assertRaises(PermissionError):
            self.auth.check_permission("doesntexist", "frank")

    def test_exception_permission_error(self):
        self.auth.add_permission("paint")
        with self.assertRaises(PermissionError):
            self.auth.add_permission("paint")
        self.authenticator.login("frank", "thetank")
        with self.assertRaises(PermissionError):
            self.auth.permit_user("doesntexist", "frank")

if __name__ == "__main__":
    unittest.main()
