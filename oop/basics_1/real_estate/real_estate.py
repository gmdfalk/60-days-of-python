from __future__ import print_function

class Property(object):

    def __init__(self, square_feet="", beds="",
                 baths="", **kwargs):
        super(Property, self).__init__(**kwargs)
        self.square_feet = square_feet
        self.num_beds = beds
        self.num_baths = baths

    def display(self):
        print("PROPERTY DETAILS")
        print("================")
        print("square footage:", self.square_feet)
        print("bedrooms:", self.num_beds)
        print("bathrooms:", self.num_baths)

    @staticmethod
    def prompt_init():
        return dict(square_feet=raw_input("Enter the square feet: "),
                    beds=raw_input("Enter number of bedrooms: "),
                    baths=raw_input("Enter number of baths: "))

def get_valid_input(input_string, valid_options):
    input_string += " ({}) ".format(", ".join(valid_options))
    response = raw_input(input_string)
    while response.lower() not in valid_options:
        response = raw_input(input_string)
    return response

class Apartment(Property):

    valid_laundries = ("coin", "ensuite", "none")
    valid_balconies = ("yes", "no", "solarium")

    def __init__(self, balcony='', laundry='', **kwargs):
        super(Apartment, self).__init__(**kwargs)
        self.balcony = balcony
        self.laundry = laundry

    def display(self):
        super(Apartment, self).display()
        print("APARTMENT DETAILS")
        print("laundry:", self.laundry)
        print("has balcony:", self.balcony)

    @staticmethod
    def prompt_init():
        # Composition
        parent_init = Property.prompt_init()
        laundry = get_valid_input(
              "What laundry facilities does "
              " the property have? ",
              Apartment.valid_laundries)
        balcony = get_valid_input(
              "Does the property have a balcony? ",
              Apartment.valid_balconies)
        parent_init.update({
                            "laundry": laundry,
                            "balcony": balcony
                            })
        return parent_init

class House(Property):

    valid_garage = ("attached", "detached", "none")
    valid_fence = ("yes", "no")

    def __init__(self, stories='', garage='', fence='', **kwargs):
        super(House, self).__init__(**kwargs)
        self.stories = stories
        self.garage = garage
        self.fence = fence

    def display(self):
        super(House, self).display()
        print("HOUSE DETAILS")
        print("# of stories:", self.stories)
        print("garage:", self.garage)
        print("fence:", self.fence)

    @staticmethod
    def prompt_init():
        parent_init = Property.prompt_init()
        fence = get_valid_input("Is the yard fenced? ",
                                House.valid_fence)
        garage = get_valid_input("Is there a garage? ",
                                 House.valid_garage)
        stories = raw_input("How many stories? ")

        parent_init.update({
                            "fence": fence,
                            "garage": garage,
                            "stories": stories
                            })
        return parent_init


class Purchase(object):

    def __init__(self, price="", taxes="", **kwargs):
        super(Purchase, self).__init__(**kwargs)
        self.price = price
        self.taxes = taxes

    def display(self):
        super(Purchase, self).display()
        print("PURCHASE DETAILS")
        print("selling price:", self.price)
        print("estimated taxes:", self.taxes)

    @staticmethod
    def prompt_init():
        return dict(
            price=raw_input("What is the selling price? "),
            taxes=raw_input("What are the estimated taxes? "))


class Rental(object):

    def __init__(self, furnished='', utilities='',
                 rent='', **kwargs):
        super(Rental, self).__init__(**kwargs)
        self.furnished = furnished
        self.utilities = utilities
        self.rent = rent

    def display(self):
        super(Rental, self).display()
        print("RENTAL DETAILS")
        print("rent:", self.rent)
        print("estimated utilities:", self.utilities)
        print("furnished:", self.furnished)

    @staticmethod
    def prompt_init():
        return dict(
            rent=raw_input("What is the monthly rent? "),
            utilities=raw_input("What are the estimated utilities? "),
            furnished=get_valid_input(
                "Is the property furnished? ",
                    ("yes", "no")))


class HouseRental(Rental, House):

    @staticmethod
    def prompt_init():
        init = House.prompt_init()
        init.update(Rental.prompt_init())
        return init


class ApartmentRental(Rental, Apartment):

    @staticmethod
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Rental.prompt_init())
        return init


class ApartmentPurchase(Purchase, Apartment):

    @staticmethod
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Purchase.prompt_init())
        return init


class HousePurchase(Purchase, House):

    @staticmethod
    def prompt_init():
        init = House.prompt_init()
        init.update(Purchase.prompt_init())
        return init


class Agent(object):

    def __init__(self):
        self.property_list = []

    def display_properties(self):
        for prop in self.property_list:
            prop.display()


if __name__ == "__main__":
#     init = HouseRental.prompt_init()
#     house = HouseRental(**init)
#     house.display()
    p = Property()
    p.prompt_init()
    p.display()
