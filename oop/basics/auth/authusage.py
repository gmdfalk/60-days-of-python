"""
    Created on 25 Mar 2014

    @author: Max Demian
"""

import auth


# Set up a test user and permission
auth.authenticator.add_user("joe", "joepassword")
auth.authorizor.add_permission("test program")
auth.authorizor.add_permission("change program")
auth.authorizor.permit_user("test program", "joe")
# auth.authorizor.permit_user("change program", "joe")

class Editor(object):

    def __init__(self):
        self.username = None
        self.menu_map = {
                         "login": self.login,
                         "test": self.test,
                         "change": self.change,
                         "quit": self.quit
                         }

    def login(self):
        logged_in = False
        while not logged_in:
            username = raw_input("username: ")
            password = raw_input("password: ")
            try:
                logged_in = auth.authenticator.login(
                                                     username, password)
            except auth.InvalidUsername:
                print "Sorry, that username does not exist"
            except auth.InvalidPassword:
                print "Sorry, incorrect password"
            else:
                self.username = username

    def is_permitted(self, permission):
        try:
            auth.authorizor.check_permission(permission, self.username)
        except auth.NotLoggedInError as e:
            print e.username, "is not logged in"
            return False
        except auth.NotPermittedError as e:
            print e.username, "cannot", permission
            return False
        return True

    def test(self):
        if self.is_permitted("test program"):
            print "Testing program now..."

    def change(self):
        if self.is_permitted("change program"):
            print "Changing program now..."

    def quit(self):
        raise SystemExit()

    def menu(self):
        try:
            answer = ""
            while True:
                print """
Please enter a command:
\tlogin\tLogin
\ttest\tTest the program
\tchange\tChange the program
\tquit\tQuit
"""
                answer = raw_input("Enter a command: ").lower()
                try:
                    func = self.menu_map[answer]
                except KeyError:
                    print answer, "is not a valid option"
                else:
                    func()
        finally:
            print "Thank you for testing the auth API"

if __name__ == '__main__':
    Editor().menu()
