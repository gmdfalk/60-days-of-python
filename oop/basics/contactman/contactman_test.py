"""
    Created on 22 Mar 2014
    @author: Max Demian
"""
# 100% coverage

import unittest
from contactman import Contact, ContactList, Friend, Supplier
from contactman import EmailableContact, LongNameDict


class ContactmanTest(unittest.TestCase):

    def test_contact(self):
        c = Contact("max", "demian@gmx.de")
        d = Contact("1", "2")
        self.assertEqual(str(d), "1, 2")
        self.assertEqual(c.name, "max")
        self.assertEqual(c.email, "demian@gmx.de")
        self.assertEqual([c, d], Contact.all_contacts)

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
        new_friend = Friend("Tom", "tom@gmail.com", "1-504-298", "Common St 1",
                            "New Orleans", "Louisiana", "70112")
        self.assertEqual(Contact.all_contacts.search("Tom"), [new_friend])
        print new_friend

    def test_mailsender(self):
        e = EmailableContact("John Smith", "jsmith@ex.net")
        self.assertEqual(e.send_mail("msg"), "msg")


class VariousTest(unittest.TestCase):


    def test_long(self):
        longkeys = LongNameDict()
        longkeys['hello'] = 1
        longkeys['longest yet'] = 5
        longkeys['superlong'] = "world"
        self.assertEqual(longkeys.longest_key(), "longest yet")
