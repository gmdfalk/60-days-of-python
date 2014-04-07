#!/usr/bin/env python2
# coding: utf-8

def exceptions():
    class EvenOnly(list):
        def append(self, integer):
            if not isinstance(integer, int):
                raise TypeError("Only integers can be added")
            if integer % 2:
                raise ValueError("Only even numbers can be added")
            super(EvenOnly, self).append(integer)

    e = EvenOnly()
    for i in range(20):
        try:
            e.append(i)
        except:
            continue

    def no_return():
        print("I am about to raise an exception")
        raise ValueError("This is always raised")
        print("This line will never execute")
        return "I won't be returned"

    def call_exceptor():
        print("call_exceptor starts here...")
        try:
            no_return()
        except:
            pass
        print("an exception was raised...")
        print("...so these lines don't run")

    def funny_division(num):
        try:
            if num == 13:
                raise ValueError("13 is a unlucky number")
            return 100 / num
        except ZeroDivisionError:
            return "Need a number other than zero!"
        except TypeError:
            return "Enter a numerical value"
        except ValueError:
            print "No, no, not 13!"
            raise

    def exception_argument():
        try:
            raise ValueError("This is an argument")
        except ValueError as e:
            print "The exception arguments were", e.args
            print dir(e), e.message

    class InvalidWithdrawal(Exception):

        def __init__(self, balance, amount):
            super(InvalidWithdrawal, self).__init__("account doesn't have {}€".format(amount))
            self.amount = amount
            self.balance = balance

        def overage(self):
            return self.amount - self.balance

    # ~ raise InvalidWithdrawal("You don't have 50€ in your account")
    def throw_invalid_withdrawal():
        try:
            raise InvalidWithdrawal(25, 50)
        except InvalidWithdrawal as e:
            print("I'm sorry, but your withdrawal is "
            "more than your balance by "
            "${}".format(e.overage()))


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
        item_type = 'widgt'
        inv = Inventory()
        # ~ inv.lock(item_type)
        inv.purchase(item_type)
        inv.unlock(item_type)
        inv.purchase(item_type)

    test_inventory()

def oop_vs_functional():
    import math
    square = [(1, 1), (1, 2), (2, 2), (2, 1)]

    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def perimeter(polygon):
        perimeter = 0
        points = polygon + [polygon[0]]
        for i in range(len(polygon)):
            perimeter += distance(points[i], points[i + 1])
        return perimeter

    class Point(object):

        def __init__(self, x, y):
            self.x = x
            self.y = y

        def distance(self, p2):
            return math.sqrt((self.x - p2.x) ** 2 + (self.y - p2.y) ** 2)

    class Polygon(object):

        def __init__(self, points=[]):
            self.vertices = []
            for point in points:
                if isinstance(point, tuple):
                    point = Point(*point)
                self.vertices.append(point)

        def perimeter(self):
            perimeter = 0
            points = self.vertices + [self.vertices[0]]
            for i in range(len(self.vertices)):
                perimeter += points[i].distance(points[i + 1])
            return perimeter

    p = Polygon(square)
    print p.perimeter()
    print perimeter(square)


def properties():
    class Silly(object):
        @property
        def silly(self):
            "This is a silly property"
            print("You are getting silly")
            return self._silly

        @silly.setter
        def silly(self, value):
            print("You are making silly {}".format(value))
            self._silly = value

        @silly.deleter
        def silly(self):
            print("Whoah, you killed silly!")
            del self._silly

    s = Silly()
    s.silly = "bla"
    s.silly
    del s.silly

    class Foo(object):

        @property
        def foo(self):
            print "getting"
            return self._foo

        @foo.setter
        def foo(self, value):
            print "setting"
            self._foo = value

        @foo.deleter
        def foo(self):
            print "deleting"
            del self._foo

    f = Foo()
    f.foo = "dick"
    f.foo
    del f.foo

    from urllib2 import urlopen
    import time

    class WebPage(object):
        def __init__(self, url):
            self.url = url
            self._content = None
        @property
        def content(self):
            if not self._content:
                print("Retrieving New Page...")
                self._content = self.url

    w = WebPage("http://ccphillips.net/")
    now = time.time()
    content1 = w.content
    print time.time() - now
    now = time.time()
    time.sleep(1)
    content2 = w.content
    print time.time() - now
    print content2 == content1


def zip_processing():

    import sys
    import os
    import shutil
    import zipfile
    from pygame import image
    from pygame.transform import scale

    class ZipProcessor(object):
        "Base class that processes a zip archive"
        def __init__(self, zipname):
            self.zipname = zipname
            self.temp_directory = "unzipped-{}".format(zipname[:-4])

        def _full_filename(self, filename):
            return os.path.join(self.temp_directory, filename)

        def process_zip(self):
            self.unzip_files()
            self.process_files()
            self.zip_files()

        def unzip_files(self):
            os.mkdir(self.temp_directory)
            zip = zipfile.ZipFile(self.zipname)
            try:
                zip.extractall(self.temp_directory)
            finally:
                zip.close_logs()

        def zip_files(self):
            file = zipfile.ZipFile(self.zipname, "w")
            for filename in os.listdir(self.temp_directory):
                file.write(self._full_filename(filename), filename)
            shutil.rmtree(self.temp_directory)


    class ZipReplace(ZipProcessor):
        "Replace all occurrences of a string in a zip archive"
        def __init__(self, filename, search_string, replace_string):
            super(ZipReplace, self).__init__(filename)
            self.filename = filename
            self.search_string = search_string
            self.replace_string = replace_string

        def process_files(self):
            "Perform a search and replace on all files in the temp_directory"
            for filename in os.listdir(self.temp_directory):
                with open(self._full_filename(filename)) as file:
                    contents = file.read()
                contents = contents.replace(self.search_string,
                                            self.replace_string)
                with open(self._full_filename(filename), "w") as file:
                    file.write(contents)

    class ZipScale(ZipProcessor):
        "Replace images in a zip file with scaled versions"
        # Overload inherited method to modify picture size instead of string.
        def process_files(self):
            "Scale each image in the directory to 640x480"
            for filename in os.listdir(self.temp_directory):
                im = image.load(self._full_filename(filename))
                scaled = scale(im, (640, 480))
                image.save(scaled, self._full_filename(filename))

    # ZipReplace("hello.zip", "hello", "hi").zip_find_replace()
    # ZipScale("horse.zip").process_zip()

    # Same thing as composition:
    class ZipProcessorComp(object):
        "Base class that processes a zip archive"
        def __init__(self, zipname, processor):
            self.zipname = zipname
            self.temp_directory = "unzipped-{}".format(zipname[:-4])
            self.processor = processor

        def _full_filename(self, filename):
            return os.path.join(self.temp_directory, filename)

        def process_zip(self):
            self.unzip_files()
            self.processor.process(self)
            self.zip_files()

        def unzip_files(self):
            os.mkdir(self.temp_directory)
            zip = zipfile.ZipFile(self.zipname)
            try:
                zip.extractall(self.temp_directory)
            finally:
                zip.close_logs()

        def zip_files(self):
            file = zipfile.ZipFile(self.zipname, "w")
            for filename in os.listdir(self.temp_directory):
                file.write(self._full_filename(filename), filename)
            shutil.rmtree(self.temp_directory)

    class ZipReplaceComp(object):

        def __init__(self, search_string, replace_string):
            self.search_string = search_string
            self.replace_string = replace_string

        def process(self, zipprocessor):
            '''Perform a search and replace on all files in the
            temporary directory'''
            for filename in os.listdir(zipprocessor.temp_directory):
                with open(zipprocessor._full_filename(filename)) as file:
                    contents = file.read()
                contents = contents.replace(
                    self.search_string, self.replace_string)
                with open(zipprocessor._full_filename(filename), "w") as file:
                    file.write(contents)

    class ZipScaleComp(object):

        def process(self, zipprocessor):
            "Scale each image in the directory to 640x480"
            for filename in os.listdir(zipprocessor.temp_directory):
                im = image.load(zipprocessor._full_filename(filename))
                scaled = scale(im, (640, 480))
                image.save(scaled, zipprocessor._full_filename(filename))

#     zipreplace = ZipReplaceComp("hello", "hi")
#     ZipProcessorComp("hello.zip", zipreplace).process_zip()
    zipscale = ZipScaleComp()
    ZipProcessorComp("horse.zip", zipscale).process_zip()
    # Note: Composition is great. Use it over Inheritance where possible.

if __name__ == "__main__":
#     properties()
    # zipreplace()
    zip_processing()
