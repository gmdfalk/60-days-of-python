from __future__ import division

# TODO: Number systems conversion, Temperature


class Data(object):

    def __init__(self):
        self.decplaces = 10  # Decimal points of accuracy.
        self._bytes = 0

    @property
    def bits(self):
        return round(self._bytes * 8, self.decplaces)

    @bits.setter
    def bits(self, value):
        self._bytes = value / 8

    @property
    def bytes(self):
        "8 bits"
        return round(self._bytes, self.decplaces)

    @bytes.setter
    def bytes(self, value):
        self._bytes = value

    @property
    def KB(self):
        "1000 bytes, kB or KB"
        return round(self._bytes / 1000, self.decplaces)

    @KB.setter
    def KB(self, value):
        self._bytes = value * 1000

    @property
    def MB(self):
        "1000^2 bytes, MB"
        return round(self._bytes / (1000 ** 2), self.decplaces)

    @MB.setter
    def MB(self, value):
        self._bytes = value * (1000 ** 2)

    @property
    def GB(self):
        "1000^3 bytes, GB"
        return round(self._bytes / (1000 ** 3), self.decplaces)

    @GB.setter
    def GB(self, value):
        self._bytes = value * (1000 ** 3)

    @property
    def TB(self):
        "1000^4 bytes, TB"
        return round(self._bytes / (1000 ** 4), self.decplaces)

    @TB.setter
    def TB(self, value):
        self._bytes = value * (1000 ** 4)

    @property
    def PB(self):
        "1000^5 bytes, PB"
        return round(self._bytes / (1000 ** 5), self.decplaces)

    @PB.setter
    def PB(self, value):
        self._bytes = value * (1000 ** 5)

    @property
    def KiB(self):
        "1024 bytes, KB or KiB"
        return round(self._bytes / 1024, self.decplaces)

    @KiB.setter
    def KiB(self, value):
        self._bytes = value * 1024

    @property
    def MiB(self):
        "1024^2 bytes, MiB"
        return round(self._bytes / (1024 ** 2), self.decplaces)

    @MiB.setter
    def MiB(self, value):
        self._bytes = value * (1024 ** 2)

    @property
    def GiB(self):
        "1024^3 bytes, GiB"
        return round(self._bytes / (1024 ** 3), self.decplaces)

    @GiB.setter
    def GiB(self, value):
        self._bytes = value * (1024 ** 3)

    @property
    def TiB(self):
        "1024^4 bytes, TiB"
        return round(self._bytes / (1024 ** 4), self.decplaces)

    @TiB.setter
    def TiB(self, value):
        self._bytes = value * (1024 ** 4)

    @property
    def PiB(self):
        "1024^5 bytes, PiB"
        return round(self._bytes / (1024 ** 5), self.decplaces)

    @PiB.setter
    def PiB(self, value):
        self._bytes = value * (1024 ** 5)


class Length(object):

    def __init__(self):
        self.decplaces = 4  # Decimal points of accuracy.
        self._meters = 0

    @property
    def millimeters(self):
        return round(self._meters * 1000, self.decplaces)

    @millimeters.setter
    def millimeters(self, value):
        self._meters = value / 1000

    @property
    def centimeters(self):
        return round(self._meters * 100, self.decplaces)

    @centimeters.setter
    def centimeters(self, value):
        self._meters = value / 100

    @property
    def meters(self):
        return round(self._meters, self.decplaces)

    @meters.setter
    def meters(self, value):
        self._meters = value

    @property
    def kilometers(self):
        return round(self._meters / 1000, self.decplaces)

    @kilometers.setter
    def kilometers(self, value):
        self._meters = value * 1000

    @property
    def inches(self):
        return round(self._meters * 39.3701, self.decplaces)

    @inches.setter
    def inches(self, value):
        self._meters = value / 39.3701

    @property
    def feet(self):
        return round(self._meters * 3.28084, self.decplaces)

    @feet.setter
    def feet(self, value):
        self._meters = value / 3.28084

    @property
    def yards(self):
        return round(self._meters * 1.09361, self.decplaces)

    @yards.setter
    def yards(self, value):
        self._meters = value / 1.09361

    @property
    def miles(self):
        return round(self._meters * 0.000621371, self.decplaces)

    @miles.setter
    def miles(self, value):
        self._meters = value / 0.000621371


class Volume(object):

    def __init__(self):
        # NOTE: maybe pass decplaces as an argument instead of keeping it here.
        self.decplaces = 4  # Decimal points of accuracy.
        self._liters = 0

    @property
    def milliliters(self):
        return round(self._liters * 1000, self.decplaces)

    @milliliters.setter
    def milliliters(self, value):
        self._liters = value / 1000

    @property
    def centiliters(self):
        return round(self._liters * 100, self.decplaces)

    @centiliters.setter
    def centiliters(self, value):
        self._liters = value / 100

    @property
    def liters(self):
        return round(self._liters, self.decplaces)

    @liters.setter
    def liters(self, value):
        self._liters = value

    @property
    def kiloliters(self):
        return round(self._liters / 1000, self.decplaces)

    @kiloliters.setter
    def kiloliters(self, value):
        self._liters = value * 1000

    @property
    def ounces(self):
        return round(self._liters * 33.8140227, self.decplaces)

    @ounces.setter
    def ounces(self, value):
        self._liters = value / 33.8140227

    @property
    def pints(self):
        return round(self._liters * 2.11337642, self.decplaces)

    @pints.setter
    def pints(self, value):
        self._liters = value / 2.11337642

    @property
    def gallons(self):
        return round(self._liters * 0.26417205, self.decplaces)

    @gallons.setter
    def gallons(self, value):
        self._liters = value / 0.26417205

    @property
    def barrels(self):
        return round(self._liters * 0.00838641436, self.decplaces)

    @barrels.setter
    def barrels(self, value):
        self._liters = value / 0.00838641436


if __name__ == "__main__":
    d = Data()