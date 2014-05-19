from __future__ import division

from decimal import Decimal, getcontext
from string import ascii_lowercase, maketrans


def format_num(num, decplaces=10):
    "Converts a number into a more a readable string-version."
    try:
        dec = Decimal(num)
        # Cut the decimal off at "precision" decimal places.
        if decplaces < 1:
            dec = dec.quantize(Decimal("0"))
        else:
            # Set our precision to at least 28 or twice our precision, lest
            # Decimal.quantize complains about "result has too many digits".
            getcontext().prec = max(28, int(decplaces * 2))
            dec = dec.quantize(Decimal(".{}".format("0" * decplaces)))
    except:
        return "bad"
    # Split the decimal into sign, digits and exponent.
    tup = dec.as_tuple()
    delta = len(tup.digits) + tup.exponent
    digits = "".join(str(d) for d in tup.digits)
    # Put the number back together considering the delta.
    if delta <= 0:
        zeros = abs(tup.exponent) - len(tup.digits)
        val = "0." + ("0" * zeros) + digits
    else:
        val = digits[:delta] + ("0" * tup.exponent) + '.' + digits[delta:]
    # Strip trailing 0s and/or trailing dot:
    val = val.rstrip("0")
    if val[-1] == ".":
        val = val[:-1]

    if tup.sign:
        return "-" + val
    return val


def rot(message, shift=3):
    "Employs the Ceasar Cipher to encode/decode messages."
    alphabet = ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = maketrans(alphabet, shifted_alphabet)
    return message.lower().translate(table)


class Base(object):

    def __init__(self):
        self._decimal = 0
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    def from_decimal(self, n, base=10):
        "Input: base10 integer. Output: base2-64 string."
        try:
            n = int(n)
        except (ValueError, TypeError):
            return "NaN"
        if base < 2 or base > 64:
            return "N/A"

        basecases = "0123456789" + self.alphabet
        if 63 <= base <= 64:
            basecases = self.alphabet + "0123456789+/"
        if n < base:
            return basecases[n]

        encoded = []
        while n:
            remainder, n = n % base, n // base
            encoded.insert(0, basecases[remainder])

        return "".join(encoded)

    def to_decimal(self, s, base=10):
        "Input: base2-64 string. Output: base10 integer."
        try:
            s = str(s)
        except (ValueError, TypeError):
            return "NaN"
        if base < 2 or base > 64:
            return "N/A"

        basecases = "0123456789" + self.alphabet
        if 63 <= base <= 64:
            basecases = self.alphabet + "0123456789+/"
        basecases = basecases[:base]

        slen = len(s)
        n, idx = 0, 0
        # Allow lowercase letters for base11-36 (single alphabet).
        if base <= 36:
            s = s.upper()
        for c in s:
            if c not in basecases:
                return "NaN"
            power = slen - (idx + 1)
            n += basecases.index(c) * (base ** power)
            idx += 1

        return n


class Data(object):

    def __init__(self):
        self.decplaces = 4  # Decimal points of accuracy.
        self._bytes = 0

    @property
    def bits(self):
        return format_num(self._bytes * 8, self.decplaces)

    @bits.setter
    def bits(self, value):
        self._bytes = value / 8

    @property
    def bytes(self):
        "8 bits"
        return format_num(self._bytes, self.decplaces)

    @bytes.setter
    def bytes(self, value):
        self._bytes = value

    @property
    def kilobytes(self):
        "1000 bytes, kB or KB"
        return format_num(self._bytes / 1000, self.decplaces)

    @kilobytes.setter
    def kilobytes(self, value):
        self._bytes = value * 1000

    @property
    def megabytes(self):
        "1000^2 bytes, MB"
        return format_num(self._bytes / (1000 ** 2), self.decplaces)

    @megabytes.setter
    def megabytes(self, value):
        self._bytes = value * (1000 ** 2)

    @property
    def gigabytes(self):
        "1000^3 bytes, GB"
        return format_num(self._bytes / (1000 ** 3), self.decplaces)

    @gigabytes.setter
    def gigabytes(self, value):
        self._bytes = value * (1000 ** 3)

    @property
    def terrabytes(self):
        "1000^4 bytes, TB"
        return format_num(self._bytes / (1000 ** 4), self.decplaces)

    @terrabytes.setter
    def terrabytes(self, value):
        self._bytes = value * (1000 ** 4)

    @property
    def petabytes(self):
        "1000^5 bytes, PB"
        return format_num(self._bytes / (1000 ** 5), self.decplaces)

    @petabytes.setter
    def petabytes(self, value):
        self._bytes = value * (1000 ** 5)

    @property
    def kibibytes(self):
        "1024 bytes, KiB or KB"
        return format_num(self._bytes / 1024, self.decplaces)

    @kibibytes.setter
    def kibibytes(self, value):
        self._bytes = value * 1024

    @property
    def mebibytes(self):
        "1024^2 bytes, MiB"
        return format_num(self._bytes / (1024 ** 2), self.decplaces)

    @mebibytes.setter
    def mebibytes(self, value):
        self._bytes = value * (1024 ** 2)

    @property
    def gibibytes(self):
        "1024^3 bytes, GiB"
        return format_num(self._bytes / (1024 ** 3), self.decplaces)

    @gibibytes.setter
    def gibibytes(self, value):
        self._bytes = value * (1024 ** 3)

    @property
    def tebibytes(self):
        "1024^4 bytes, TiB"
        return format_num(self._bytes / (1024 ** 4), self.decplaces)

    @tebibytes.setter
    def tebibytes(self, value):
        self._bytes = value * (1024 ** 4)

    @property
    def pebibytes(self):
        "1024^5 bytes, PiB"
        return format_num(self._bytes / (1024 ** 5), self.decplaces)

    @pebibytes.setter
    def pebibytes(self, value):
        self._bytes = value * (1024 ** 5)


class Length(object):

    def __init__(self):
        self.decplaces = 4  # Decimal points of accuracy.
        self._meters = 0

    @property
    def millimeters(self):
        return format_num(self._meters * 1000, self.decplaces)

    @millimeters.setter
    def millimeters(self, value):
        self._meters = value / 1000

    @property
    def centimeters(self):
        return format_num(self._meters * 100, self.decplaces)

    @centimeters.setter
    def centimeters(self, value):
        self._meters = value / 100

    @property
    def meters(self):
        return format_num(self._meters, self.decplaces)

    @meters.setter
    def meters(self, value):
        self._meters = value

    @property
    def kilometers(self):
        return format_num(self._meters / 1000, self.decplaces)

    @kilometers.setter
    def kilometers(self, value):
        self._meters = value * 1000

    @property
    def inches(self):
        return format_num(self._meters * 39.37007874, self.decplaces)

    @inches.setter
    def inches(self, value):
        self._meters = value / 39.37007874

    @property
    def feet(self):
        return format_num(self._meters * 3.280839895, self.decplaces)

    @feet.setter
    def feet(self, value):
        self._meters = value / 3.280839895

    @property
    def yards(self):
        return format_num(self._meters * 1.0936132983, self.decplaces)

    @yards.setter
    def yards(self, value):
        self._meters = value / 1.0936132983

    @property
    def miles(self):
        return format_num(self._meters * 0.00062137119224, self.decplaces)

    @miles.setter
    def miles(self, value):
        self._meters = value / 0.00062137119224


class Volume(object):

    def __init__(self):
        # NOTE: maybe pass decplaces as an argument instead of keeping it here.
        self.decplaces = 4  # Decimal points of accuracy.
        self._liters = 0

    @property
    def milliliters(self):
        return format_num(self._liters * 1000, self.decplaces)

    @milliliters.setter
    def milliliters(self, value):
        self._liters = value / 1000

    @property
    def centiliters(self):
        return format_num(self._liters * 100, self.decplaces)

    @centiliters.setter
    def centiliters(self, value):
        self._liters = value / 100

    @property
    def liters(self):
        return format_num(self._liters, self.decplaces)

    @liters.setter
    def liters(self, value):
        self._liters = value

    @property
    def kiloliters(self):
        return format_num(self._liters / 1000, self.decplaces)

    @kiloliters.setter
    def kiloliters(self, value):
        self._liters = value * 1000

    @property
    def ounces(self):
        return format_num(self._liters * 33.814022701, self.decplaces)

    @ounces.setter
    def ounces(self, value):
        self._liters = value / 33.814022701

    @property
    def pints(self):
        return format_num(self._liters * 2.1133764189, self.decplaces)

    @pints.setter
    def pints(self, value):
        self._liters = value / 2.1133764189

    @property
    def gallons(self):
        return format_num(self._liters * 0.26417205236, self.decplaces)

    @gallons.setter
    def gallons(self, value):
        self._liters = value / 0.26417205236

    @property
    def barrels(self):
        return format_num(self._liters * 0.0083864143603, self.decplaces)

    @barrels.setter
    def barrels(self, value):
        self._liters = value / 0.0083864143603


class Weight(object):

    def __init__(self):
        # NOTE: maybe pass decplaces as an argument instead of keeping it here.
        self.decplaces = 4  # Decimal points of accuracy.
        self._kilograms = 0

    @property
    def milligrams(self):
        return format_num(self._kilograms * 1000000, self.decplaces)

    @milligrams.setter
    def milligrams(self, value):
        self._kilograms = value / 1000000

    @property
    def grams(self):
        return format_num(self._kilograms * 1000, self.decplaces)

    @grams.setter
    def grams(self, value):
        self._kilograms = value / 1000

    @property
    def kilograms(self):
        return format_num(self._kilograms, self.decplaces)

    @kilograms.setter
    def kilograms(self, value):
        self._kilograms = value

    @property
    def tons(self):
        return format_num(self._kilograms / 1000, self.decplaces)

    @tons.setter
    def tons(self, value):
        self._kilograms = value * 1000

    @property
    def drams(self):
        return format_num(self._kilograms * 564.3833912, self.decplaces)

    @drams.setter
    def drams(self, value):
        self._kilograms = value / 564.3833912

    @property
    def ounces(self):
        return format_num(self._kilograms * 35.27396195, self.decplaces)

    @ounces.setter
    def ounces(self, value):
        self._kilograms = value / 35.27396195

    @property
    def pounds(self):
        return format_num(self._kilograms * 2.2046226218, self.decplaces)

    @pounds.setter
    def pounds(self, value):
        self._kilograms = value / 2.2046226218

    @property
    def ustons(self):
        return format_num(self._kilograms * 0.0011023113109, self.decplaces)

    @ustons.setter
    def ustons(self, value):
        self._kilograms = value / 0.0011023113109
