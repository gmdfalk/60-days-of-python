"""
    Created on 28 Mar 2014

    @author: Max Demian
"""

# Ideally, we would do this with collections.Counter or just str.count but here
# are some ways to use data structures to count letters in a string.

#==============================================================================
# Dicts
#==============================================================================

# Using setdefault to count letters.
def letter_frequency(sentence):
    frequencies = {}
    for letter in sentence:
        frequency = frequencies.setdefault(letter, 0)
        frequencies[letter] += 1
    return frequencies

# We could instead use the collections module.
# Int as constructor works because it returns 0 if called without
# arguments.
from collections import defaultdict
def letter_freq(sentence):
    frequencies = defaultdict(int)
    for letter in sentence:
        frequencies[letter] += 1
    return frequencies
print letter_frequency("banana")
print letter_freq("banana")

#==============================================================================
# Lists.& Tuples
#==============================================================================

import string
CHARS = list(string.ascii_letters) + [" "]
def letter_fre(sentence):
    # Create our base list with tuple(letter, 0) as items.
    frequencies = [(c, 0) for c in CHARS]
    for letter in sentence:
        index = CHARS.index(letter)
        frequencies[index] = (letter, frequencies[index][1] + 1)
    return [i for i in frequencies if i[1] > 0]


print letter_fre("the quick brown fox jumps over the lazy dog")

class WeirdSortee(object):

    def __init__(self, string, number, sort_num):
        self.string = string
        self.number = number
        self.sort_num = sort_num

    def __lt__(self, object):
        if self.sort_num:
            return self.number < object.number
        return self.string < object.string

    def __repr__(self):
        return "{}:{}".format(self.string, self.number)

a = WeirdSortee("a", 4, True)
b = WeirdSortee("b", 3, True)
c = WeirdSortee("c", 2, True)
d = WeirdSortee("d", 1, True)
L = [a, b, c, d]
L.sort()
print L
for i in L:
    i.sort_num = False
L.sort()
print L
# Sorting tuple pairs by either the first or second value.
x = [(1, "c"), (2, "a"), (3, "b")]
print sorted(x)
# Return the index 1 instead of 0 as sort argument/key.
x.sort(key=lambda i: i[1])
print x

#==============================================================================
# Sets
#==============================================================================
my_artists = {"Sarah Brightman", "Guns N' Roses", "Opeth", "Vixy and Tony"}
auburns_artists = {"Nickelback", "Guns N' Roses", "Savage Garden"}

song_library = [("Phantom Of The Opera", "Sarah Brightman"),
                ("Knocking On Heaven's Door", "Guns N' Roses"),
                ("Captain Nemo", "Sarah Brightman"),
                ("Patterns In The Ivy", "Opeth"),
                ("November Rain", "Guns N' Roses"),
                ("Beautiful", "Sarah Brightman"),
                ("Mal's Song", "Vixy and Tony")]
artists = set()
for song, artist in song_library:
    artists.add(artist)
print(artists)
{'key': 'value', 'key2': 'value2'}  # Dict
{'key', 'value', 'key2', 'value2'}  # Set
print "Opiates" in artists  # yeah, right
# Get the common item (intersection) from sets with "&".
set1 = {1, 2, 3}
set2 = {3, 4, 5}
set3 = {0, 3, 6}
print set1 & set2 & set3
# The three major uses of sets: intersection, union and difference.
print("Both: {}".format(auburns_artists.intersection(my_artists)))
print("All: {}".format(my_artists.union(auburns_artists)))
print("Either but not both: {}".format(
my_artists.symmetric_difference(auburns_artists)))
# Subsets and supersets:
my_artists = {"Sarah Brightman", "Guns N' Roses",
"Opeth", "Vixy and Tony"}
bands = {"Guns N' Roses", "Opeth"}
print
print("my_artists is to bands:")
print("issuperset: {}".format(my_artists.issuperset(bands)))
print("issubset: {}".format(my_artists.issubset(bands)))
print("difference: {}".format(my_artists.difference(bands)))
print("*"*20)
print("bands is to my_artists:")
print("issuperset: {}".format(bands.issuperset(my_artists)))
print("issubset: {}".format(bands.issubset(my_artists)))
print("difference: {}".format(bands.difference(my_artists)))

# Extending the dictionary type to remember the order the keys are added in.
from collections import KeysView, ItemsView, ValuesView
class DictSorted(dict):

    def __new__(*args, **kwargs):
        new_dict = dict.__new__(*args, **kwargs)
        new_dict.ordered_keys = []
        return new_dict

    def __setitem__(self, key, value):
        '''self[key] = value syntax'''
        if key not in self.ordered_keys:
            self.ordered_keys.append(key)
        super(DictSorted, self).__setitem__(key, value)

    def setdefault(self, key, value):
        if key not in self.ordered_keys:
            self.ordered_keys.append(key)
        return super(DictSorted, self).setdefault(key, value)

    def keys(self):
        return KeysView(self)

    def values(self):
        return ValuesView(self)

    def items(self):
        return ItemsView(self)

    def __iter__(self):
        '''for x in self syntax'''
        return self.ordered_keys.__iter__()

ds = DictSorted()
d = {}
ds["a"] = 1
ds["b"] = 2
ds.setdefault("c", 3)
d["a"] = 1
d["b"] = 2
d.setdefault("c", 3)

for k, v in ds.items():
    print k, v

for k, v in d.items():
    print k, v

# Note: collections actually has this functionality with OrderedDict (along with
# other interesting data structures like namedtuple).
