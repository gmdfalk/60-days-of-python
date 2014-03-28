"""
    Created on 22 Mar 2014
    @author: Max Demian
"""
#==============================================================================
# Multiple Inheritance
#==============================================================================
# We use super() here. If we used direct class calls instead i.e.
# BaseClass.call_me(self) etc, we'd end up with 2 calls to BaseClass
# Why? Because LeftSubclass calls RightSubclass with super() as next class
class BaseClass(object):
    num_base_calls = 0
    def call_me(self):
        print "Calling method on Base Class"
        self.num_base_calls += 1

class LeftSubclass(BaseClass):
    num_left_calls = 0
    def call_me(self):
        super(LeftSubclass, self).call_me()
        print "Calling method on Left Subclass"
        self.num_left_calls += 1

class RightSubclass(BaseClass):
    num_right_calls = 0
    def call_me(self):
        super(RightSubclass, self).call_me()
        print "Calling method on Right Subclass"
        self.num_right_calls += 1

class Subclass(LeftSubclass, RightSubclass):
    num_sub_calls = 0
    def call_me(self):
        super(Subclass, self).call_me()
        print "Calling method on Subclass"
        self.num_sub_calls += 1

#==============================================================================
# Polymorphism
#==============================================================================
class AudioFile(object):

    def __init__(self, filename):
        if not filename.endswith(self.ext):
            raise Exception("Invalid file format")

        self.filename = filename

class MP3File(AudioFile):

    ext = "mp3"

    def play(self):
        print "playing {} as mp3".format(self.filename)

class WavFile(AudioFile):

    ext = "wav"

    def play(self):
        print "playing {} as wav".format(self.filename)

class OggFile(AudioFile):

    ext = "ogg"

    def play(self):
        print "playing {} as ogg".format(self.filename)

class FlacFile(object):
    def __init__(self, filename):
        if not filename.endswith(".flac"):
            raise Exception("Invalid file format")

        self.filename = filename

    def play(self):
        print "playing {} as flac".format(self.filename)

class InvalidItemType(Exception):
    def __init__(self, item_type):
        super(InvalidItemType).__init__("Sorry, we don't sell", item_type)

class Inventory(object):

    stock = {"widget": 2}

    def __init__(self):
        self.locked = False

    def lock(self, item_type):
        print item_type, "locked"
        self.locked = True

    def unlock(self, item_type):
        print item_type, "unlocked"
        self.locked = False

    def purchase(self, item_type):
        if self.locked:
            raise Exception("Sorry, item is locked.")
        if item_type not in self.stock:
            raise Exception("Sorry, we don't sell", item_type)
        if not self.stock[item_type]:
            raise InvalidItemType(item_type)
        print "Purchase complete. There are {} {}s left.".format(
            self.stock[item_type] - 1, item_type)


def test_inventory():
    item_type = 'widget'
    inv = Inventory()
    # ~ inv.lock(item_type)
    inv.purchase(item_type)
    inv.unlock(item_type)
    inv.purchase(item_type)


if __name__ == '__main__':
    s = Subclass()
    s.call_me()
    print(s.num_sub_calls, s.num_left_calls, s.num_right_calls,
        s.num_base_calls)
    ogg = OggFile("myfile.ogg")
    ogg.play()
    mp3 = MP3File("myfile.mp3")
    mp3.play()
    # This will raise the exception for wrong filetype, even though we don't
    # actually check the type of the file.
#     not_mp3 = MP3File("myfile.ogg")

    # Custom Exceptions
    test_inventory()

