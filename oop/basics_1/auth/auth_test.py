"""
    Created on 25 Mar 2014

    @author: Max Demian
"""

import unittest
from auth import (Authorizor, Authenticator, PasswordTooShort,
                  UsernameAlreadyExists, InvalidPassword, NotLoggedInError,
                  NotPermittedError, InvalidUsername, PermissionError,
                  authenticator, authorizor)


# 100% Coverage :o)
class AuthTest(unittest.TestCase):


    def setUp(self):
        authenticator.add_user("frank", "thetank")

    # tearDown and instance import is only necessary because we chose to do the
    # instantiating in the main module. Would be better to just instantiate
    # in the setUp fixture and the client modules.
    def tearDown(self):
        del authenticator.users["frank"]
        authorizor.permissions = {}

    def test_user_exists_in_dictionary(self):
        self.assertTrue("frank" in authenticator.users)
        self.assertTrue(authenticator.users["frank"].check_password("thetank"))

    def test_exception_password_too_short(self):
        with self.assertRaises(PasswordTooShort):
            authenticator.add_user("struppi", "tim")

    def test_exception_username_exists(self):
        with self.assertRaises(UsernameAlreadyExists):
            authenticator.add_user('frank', 'number2')

    def test_exception_invalid_password(self):
        with self.assertRaises(InvalidPassword):
            authenticator.login("frank", "")

    def test_exception_invalid_username(self):
        with self.assertRaises(InvalidUsername):
            authenticator.login("tom", "")
        authorizor.add_permission("paint")
        with self.assertRaises(InvalidUsername):
            authorizor.permit_user("paint", "fran")

    def test_exception_not_logged_in(self):
        authorizor.add_permission("paint")
        with self.assertRaises(NotLoggedInError):
            authorizor.check_permission("paint", "frank")

    def test_exception_not_permitted(self):
        authenticator.login("frank", "thetank")
        authorizor.add_permission("paint")
        with self.assertRaises(NotPermittedError):
            authorizor.check_permission("paint", "frank")

    def test_add_user(self):
        authenticator.add_user("tim", "struppi")
        self.assertTrue("frank" in authenticator.users)

    def test_login(self):
        self.assertFalse(authenticator.is_logged_in("dick"))
        authenticator.login("frank", "thetank")
        self.assertTrue(authenticator.is_logged_in("frank"))

    def test_check_permission(self):
        authenticator.login("frank", "thetank")
        authorizor.add_permission("paint")
        authorizor.permit_user("paint", "frank")
        self.assertTrue(authorizor.check_permission("paint", "frank"))
        with self.assertRaises(PermissionError):
            authorizor.check_permission("doesntexist", "frank")

    def test_exception_permission_error(self):
        authorizor.add_permission("paint")
        with self.assertRaises(PermissionError):
            authorizor.add_permission("paint")
        authenticator.login("frank", "thetank")
        with self.assertRaises(PermissionError):
            authorizor.permit_user("doesntexist", "frank")

if __name__ == "__main__":
    unittest.main()
