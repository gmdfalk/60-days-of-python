"""
    Created on 22 Mar 2014
    @author: Max Demian
"""

# 100% coverage
import unittest
from contactman import Contact, ContactList, Friend, Supplier, EmailableContact


class TestContactman(unittest.TestCase):

    def setUp(self):
        self.config = Contact("max", "demian@gmx.de")
        self.d = Contact("1", "2")

    def test_contact(self):
        self.assertEqual(str(self.d), "1, 2")
        self.assertEqual(self.config.name, "max")
        self.assertEqual(self.config.email, "demian@gmx.de")
        self.assertEqual([self.config, self.d], Contact.all_contacts)

    def test_supplier(self):
        s = Supplier("mix", "dimian@gmx.de")
        self.assertEqual(s.order("pizza"), "pizza")

    def test_contact_list(self):
        new = Contact("tst", "tst@t.st")
        self.assertEqual(Contact.all_contacts.search("tst"), [new])

#     def test_oldfriend(self):
#         ContactList().delete_all()
#         new_friend = Friend("tom", "mail", "phone")
#         self.assertEqual(Contact.all_contacts.search("tom"), [new_friend])
#         print new_friend

    def test_friend(self):
        ContactList().delete_all()
#         new_friend = Contact("Tom")
        new_friend = Friend(name="Tom", email="tom@gmail.com", phone="1-504-298", street="Common St 1",
                            city="New Orleans", state="Louisiana", code="70112")
        self.assertEqual(Contact.all_contacts.search("Tom"), [new_friend])
        print new_friend

    def test_mailsender(self):
        e = EmailableContact("John Smith", "jsmith@ex.net")
        self.assertEqual(e.send_mail("msg"), "msg")

if __name__ == "__main__":
    unittest.main()
