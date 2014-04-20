from __future__ import division

from decimal import Decimal, getcontext

# TODO: Number systems conversion, Temperature
def format_num(num, precision=10):
    try:
        dec = Decimal(num)
        # Cut the decimal off at "precision" decimal places.
        if precision < 1:
            dec = dec.quantize(Decimal("0"))
        else:
            # Set our precision to at least 28 or 5 times our precision. Other-
            # wise quantize complains "result has too many digits".
            getcontext().prec = max(28, int(precision * 2))
            dec = dec.quantize(Decimal(".{}".format("0"*precision)))
    except:
        return "bad"
    tup = dec.as_tuple()
    delta = len(tup.digits) + tup.exponent
    digits = ''.join(str(d) for d in tup.digits)
    if delta <= 0:
        zeros = abs(tup.exponent) - len(tup.digits)
        val = '0.' + ('0' * zeros) + digits
    else:
        val = digits[:delta] + ('0' * tup.exponent) + '.' + digits[delta:]
    val = val.rstrip('0')
    if val[-1] == '.':
        val = val[:-1]
    if tup.sign:
        return '-' + val
    return val


class Data(object):

    def __init__(self):
        self.precision = 10  # Decimal points of accuracy.
        self._bytes = 0

#     # Saving some space with lambdas:
#     megabytes = property(lambda self: self._bytes / (1000 ** 2), lambda self, value:
#                   setattr(self, '_bytes', value * (1000 ** 2)))

    @property
    def bits(self):
        return format_num(self._bytes * 8, self.precision)

    @bits.setter
    def bits(self, value):
        self._bytes = value / 8

    @property
    def bytes(self):
        "8 bits"
        return format_num(self._bytes, self.precision)

    @bytes.setter
    def bytes(self, value):
        self._bytes = value

    @property
    def kilobytes(self):
        "1000 bytes, kB or KB"
        return format_num(self._bytes / 1000, self.precision)

    @kilobytes.setter
    def kilobytes(self, value):
        self._bytes = value * 1000

    @property
    def megabytes(self):
        "1000^2 bytes, MB"
        return format_num(self._bytes / (1000 ** 2), self.precision)

    @megabytes.setter
    def megabytes(self, value):
        self._bytes = value * (1000 ** 2)

    @property
    def gigabytes(self):
        "1000^3 bytes, GB"
        return format_num(self._bytes / (1000 ** 3), self.precision)

    @gigabytes.setter
    def gigabytes(self, value):
        self._bytes = value * (1000 ** 3)

    @property
    def terrabytes(self):
        "1000^4 bytes, TB"
        return format_num(self._bytes / (1000 ** 4), self.precision)

    @terrabytes.setter
    def terrabytes(self, value):
        self._bytes = value * (1000 ** 4)

    @property
    def petabytes(self):
        "1000^5 bytes, PB"
        return format_num(self._bytes / (1000 ** 5), self.precision)

    @petabytes.setter
    def petabytes(self, value):
        self._bytes = value * (1000 ** 5)

    @property
    def kibibytes(self):
        "1024 bytes, KiB or KB"
        return format_num(self._bytes / 1024, self.precision)

    @kibibytes.setter
    def kibibytes(self, value):
        self._bytes = value * 1024

    @property
    def mebibytes(self):
        "1024^2 bytes, MiB"
        return format_num(self._bytes / (1024 ** 2), self.precision)

    @mebibytes.setter
    def mebibytes(self, value):
        self._bytes = value * (1024 ** 2)

    @property
    def gibibytes(self):
        "1024^3 bytes, GiB"
        return format_num(self._bytes / (1024 ** 3), self.precision)

    @gibibytes.setter
    def gibibytes(self, value):
        self._bytes = value * (1024 ** 3)

    @property
    def tebibytes(self):
        "1024^4 bytes, TiB"
        return format_num(self._bytes / (1024 ** 4), self.precision)

    @tebibytes.setter
    def tebibytes(self, value):
        self._bytes = value * (1024 ** 4)

    @property
    def pebibytes(self):
        "1024^5 bytes, PiB"
        return format_num(self._bytes / (1024 ** 5), self.precision)

    @pebibytes.setter
    def pebibytes(self, value):
        self._bytes = value * (1024 ** 5)


class Length(object):

    def __init__(self):
        self.precision = 4  # Decimal points of accuracy.
        self._meters = 0

    @property
    def millimeters(self):
        return format_num(self._meters * 1000, self.precision)

    @millimeters.setter
    def millimeters(self, value):
        self._meters = value / 1000

    @property
    def centimeters(self):
        return format_num(self._meters * 100, self.precision)

    @centimeters.setter
    def centimeters(self, value):
        self._meters = value / 100

    @property
    def meters(self):
        return format_num(self._meters, self.precision)

    @meters.setter
    def meters(self, value):
        self._meters = value

    @property
    def kilometers(self):
        return format_num(self._meters / 1000, self.precision)

    @kilometers.setter
    def kilometers(self, value):
        self._meters = value * 1000

    @property
    def inches(self):
        return format_num(self._meters * 39.37007874, self.precision)

    @inches.setter
    def inches(self, value):
        self._meters = value / 39.37007874

    @property
    def feet(self):
        return format_num(self._meters * 3.280839895, self.precision)

    @feet.setter
    def feet(self, value):
        self._meters = value / 3.280839895

    @property
    def yards(self):
        return format_num(self._meters * 1.0936132983, self.precision)

    @yards.setter
    def yards(self, value):
        self._meters = value / 1.0936132983

    @property
    def miles(self):
        return format_num(self._meters * 0.00062137119224, self.precision)

    @miles.setter
    def miles(self, value):
        self._meters = value / 0.00062137119224


class Volume(object):

    def __init__(self):
        # NOTE: maybe pass decplaces as an argument instead of keeping it here.
        self.precision = 4  # Decimal points of accuracy.
        self._liters = 0

    @property
    def milliliters(self):
        return format_num(self._liters * 1000, self.precision)

    @milliliters.setter
    def milliliters(self, value):
        self._liters = value / 1000

    @property
    def centiliters(self):
        return format_num(self._liters * 100, self.precision)

    @centiliters.setter
    def centiliters(self, value):
        self._liters = value / 100

    @property
    def liters(self):
        return format_num(self._liters, self.precision)

    @liters.setter
    def liters(self, value):
        self._liters = value

    @property
    def kiloliters(self):
        return format_num(self._liters / 1000, self.precision)

    @kiloliters.setter
    def kiloliters(self, value):
        self._liters = value * 1000

    @property
    def ounces(self):
        return format_num(self._liters * 33.814022701, self.precision)

    @ounces.setter
    def ounces(self, value):
        self._liters = value / 33.814022701

    @property
    def pints(self):
        return format_num(self._liters * 2.1133764189, self.precision)

    @pints.setter
    def pints(self, value):
        self._liters = value / 2.1133764189

    @property
    def gallons(self):
        return format_num(self._liters * 0.26417205236, self.precision)

    @gallons.setter
    def gallons(self, value):
        self._liters = value / 0.26417205236

    @property
    def barrels(self):
        return format_num(self._liters * 0.0083864143603, self.precision)

    @barrels.setter
    def barrels(self, value):
        self._liters = value / 0.0083864143603


class Weight(object):

    def __init__(self):
        # NOTE: maybe pass decplaces as an argument instead of keeping it here.
        self.precision = 4  # Decimal points of accuracy.
        self._kilograms = 0

    @property
    def milligrams(self):
        return format_num(self._kilograms * 1000000, self.precision)

    @milligrams.setter
    def milligrams(self, value):
        self._kilograms = value / 1000000

    @property
    def grams(self):
        return format_num(self._kilograms * 1000, self.precision)

    @grams.setter
    def grams(self, value):
        self._kilograms = value / 1000

    @property
    def kilograms(self):
        return format_num(self._kilograms, self.precision)

    @kilograms.setter
    def kilograms(self, value):
        self._kilograms = value

    @property
    def tons(self):
        return format_num(self._kilograms / 1000, self.precision)

    @tons.setter
    def tons(self, value):
        self._kilograms = value * 1000

    @property
    def drams(self):
        return format_num(self._kilograms * 564.3833912, self.precision)

    @drams.setter
    def drams(self, value):
        self._kilograms = value / 564.3833912

    @property
    def ounces(self):
        return format_num(self._kilograms * 35.27396195, self.precision)

    @ounces.setter
    def ounces(self, value):
        self._kilograms = value / 35.27396195

    @property
    def pounds(self):
        "lbs"
        return format_num(self._kilograms * 2.2046226218, self.precision)

    @pounds.setter
    def pounds(self, value):
        self._kilograms = value / 2.2046226218

    @property
    def ustons(self):
        return format_num(self._kilograms * 0.0011023113109, self.precision)

    @ustons.setter
    def ustons(self, value):
        self._kilograms = value / 0.0011023113109


if __name__ == "__main__":
    w = Weight()
    w.kilograms = 1
    print w.kilograms, w.tons, w.drams, w.ounces, w.pounds, w.ustons
