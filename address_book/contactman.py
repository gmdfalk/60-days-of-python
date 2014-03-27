
"""
    ContactManager

    Template for an address manager without the use of a database
"""


class ContactList(list):
    "Extending list type with a search method"

    def search(self, name):
        "Return all contacts that contain the search value"
        matching_contacts = []
        for contact in self:
            if name in contact.name:
                matching_contacts.append(contact)
        return matching_contacts

    def delete_all(self):
        return []


class Contact(object):

    all_contacts = ContactList()

    def __init__(self, name="", email="", **kwargs):
        super(Contact, self).__init__(**kwargs)
        self.name = name
        self.email = email
        self.all_contacts.append(self)

    def __repr__(self):
        return self.name + ", " + self.email


class AddressHolder(object):
    "If the contact has location information, this is where we store it"

    def __init__(self, street="", city="", state="", code="", **kwargs):
        super(AddressHolder, self).__init__(**kwargs)
        self.street = street
        self.city = city
        self.state = state
        self.code = code


class MailSender(object):
    "Template for sending mail to a contact"
    def send_mail(self, message):
        print "Sending mail to", self.email
        return message


class EmailableContact(Contact, MailSender):
    pass


class Supplier(Contact):
    def order(self, order):
        return order

class Friend(Contact, AddressHolder):
    ""
    def __init__(self, phone="", **kwargs):

        super(Friend, self).__init__(**kwargs)
        self.phone = phone

    def __repr__(self):
        # Overloading Contact's __repr__
        return self.name + ", " + self.email + ", " + self.phone

