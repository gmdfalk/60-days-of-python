#===============================================================================
# ContactManager
#===============================================================================

class AddressHolder(object):
    def __init__(self, street, city, state, code):
        self.street = street
        self.city = city
        self.state = state
        self.code = code

class ContactList(list):
    # Extending list type with our own methods!
    def search(self, name):
        "Return all contacts that contain the search value in their name"
        matching_contacts = []
        for contact in self:
            if name in contact.name:
                matching_contacts.append(contact)
        return matching_contacts

    def delete_all(self):
        return []

class Contact(object):

    # Class attribute, available to all instances.
    all_contacts = ContactList()

    def __init__(self, name, email):
        self.name = name
        self.email = email
        # I think we could use a class method instead here. Or maybe not, at
        # least for __init__. Anyway, accessing class attribute:
        self.all_contacts.append(self)

    def __repr__(self):
        return self.name + ", " + self.email


class Supplier(Contact):
    def order(self, order):
        return order


class Friend(Contact, AddressHolder):
#     def __init__(self, name, email, phone):
#         # In Python3, we can just use super() instead of super(Child, self).
#         super(Friend, self).__init__(name, email)
#         self.phone = phone
    def __init__(self, name, email, phone, street, city, state, code):
        Contact.__init__(self, name, email)
        AddressHolder.__init__(self, street, city, state, code)
        self.phone = phone

    def __repr__(self):
        # Overloading Contact's __repr__
        return self.name + ", " + self.email + ", " + self.phone


class MailSender(object):

    def send_mail(self, message):
        print "Sending mail to ", self.email
        return message

class EmailableContact(Contact, MailSender):
    pass


#==============================================================================
# LongNameDict
#==============================================================================

class LongNameDict(dict):

    def longest_key(self, longest=None):
        for key in self:
            if not longest or len(key) > len(longest):
                longest = key
        return longest

#==============================================================================
# Improved ContactMan
#==============================================================================
# class Contact(object):
#     all_contacts = []
#     def __init__(self, name='', email='', **kwargs):
#         super().__init__(**kwargs)
#         self.name = name
#         self.email = email
#         self.all_contacts.append(self)
#
# class AddressHolder(object):
#     def __init__(self, street='', city='', state='', code='',
#                  **kwargs):
#         super().__init__(**kwargs)
#         self.street = street
#         self.city = city
#         self.state = state
#         self.code = code
#
# class Friend(Contact, AddressHolder):
#     def __init__(self, phone='', **kwargs):
#         super().__init__(**kwargs)
#         self.phone = phone
