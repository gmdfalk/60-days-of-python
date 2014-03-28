
"""
    ContactManager

    Template for an address manager without the use of a database

    Notes for future refactoring:
    * cut out the inheritance altogether (use composition).
    * separate storage of contacts from Contact and probably use a dict. This
      would also allow keeping several lists/dicts of contacts.
    * don't extend the list type but rather write methods/functions that take a
      list as argument.
    * and for god's sake, no multiple inheritance.
"""


class ContactList(list):
    "Extending list type with our own methods!"

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
    "Top of the inheritance chain for creating new contacts"
    all_contacts = ContactList()

    def __init__(self, name="", email="", **kwargs):
        super(Contact, self).__init__(**kwargs)
        self.name = name
        self.email = email
        self.all_contacts.append(self)

    # Basic contacts only have a name & email so print those if we access one.
    def __repr__(self):
        return self.name + ", " + self.email


class AddressHolder(object):
    "If the contact has location information, this is where we initialize it"
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
    "Contacts we want to send mail to, e.g. for a newsletter"
    pass


class Supplier(Contact):
    "Contacts we regularly buy from"
    def order(self, order):
        return order

class Friend(Contact, AddressHolder):
    "Multiple Inheritance example"
    def __init__(self, phone="", **kwargs):
        super(Friend, self).__init__(**kwargs)
        self.phone = phone

    def __repr__(self):
        # Overloading Contact's __repr__
        return self.name + ", " + self.email + ", " + self.phone

