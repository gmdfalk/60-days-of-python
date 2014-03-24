class Property(object):

    def __init__(self, area=0, beds=0, bathrooms=0, **kwargs):
        super(Property, self).__init__(**kwargs)
        self.square_feet = area
        self.beds = beds
        self.baths = bathrooms

    def display(self):
        print "PROPERTY DETAILS"
        print "================"
        print "square footage:", self.square_feet
        print "bedrooms:", self.beds
        print "bathrooms:", self.baths
        print

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
        print "APARTMENT DETAILS"
        print "laundry:", self.laundry
        print "has balcony:", self.balcony

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
        print "HOUSE DETAILS"
        print "# of stories:", self.stories
        print "garage:", self.garage
        print "fence:", self.fence

    @staticmethod
    def prompt_init():
        pass

class Agent(object):

    def __init__(self, property_list):
        self.property_list = property_list

class Rental(object):

    pass

class Purchase(object):
    pass


class HouseRental(Rental):
    pass

class HousePurchase(Purchase):
    pass

class ApartmentRental(Rental):
    pass

class ApartmentPurchase(Purchase):
    pass

if __name__ == "__main__":
    a = Apartment()
    a.prompt_init()
