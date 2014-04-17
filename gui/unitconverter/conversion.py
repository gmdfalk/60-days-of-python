from __future__ import division


class Length(object):

    def __init__(self):
        self.precision = 4  # Decimal points of accuracy.
        self._meters = 0

    @property
    def millimeters(self):
        return round(self._meters * 1000, self.precision)

    @millimeters.setter
    def millimeters(self, value):
        self._meters = value / 1000

    @property
    def centimeters(self):
        return round(self._meters * 100, self.precision)

    @centimeters.setter
    def centimeters(self, value):
        self._meters = value / 100

    @property
    def meters(self):
        return round(self._meters, self.precision)

    @meters.setter
    def meters(self, value):
        self._meters = value

    @property
    def kilometers(self):
        return round(self._meters / 1000, self.precision)

    @kilometers.setter
    def kilometers(self, value):
        self._meters = value * 1000

    @property
    def inches(self):
        return round(self._meters * 39.3701, self.precision)

    @inches.setter
    def inches(self, value):
        self._meters = value / 39.3701

    @property
    def feet(self):
        return round(self._meters * 3.28084, self.precision)

    @feet.setter
    def feet(self, value):
        self._meters = value / 3.28084

    @property
    def yards(self):
        return round(self._meters * 1.09361, self.precision)

    @yards.setter
    def yards(self, value):
        self._meters = value / 1.09361

    @property
    def miles(self):
        return round(self._meters * 0.000621371, self.precision)

    @miles.setter
    def miles(self, value):
        self._meters = value / 0.000621371


class Volume(object):

    def __init__(self):
        # NOTE: maybe pass precision as an argument instead of keeping it here.
        self.precision = 4  # Decimal points of accuracy.
        self._liters = 0

    @property
    def milliliters(self):
        return round(self._liters * 1000, self.precision)

    @milliliters.setter
    def milliliters(self, value):
        self._liters = value / 1000

    @property
    def centiliters(self):
        return round(self._liters * 100, self.precision)

    @centiliters.setter
    def centiliters(self, value):
        self._liters = value / 100

    @property
    def liters(self):
        return round(self._liters, self.precision)

    @liters.setter
    def liters(self, value):
        self._liters = value

    @property
    def kiloliters(self):
        return round(self._liters / 1000, self.precision)

    @kiloliters.setter
    def kiloliters(self, value):
        self._liters = value * 1000

    @property
    def ounces(self):
        return round(self._liters * 33.814, self.precision)

    @ounces.setter
    def ounces(self, value):
        self._liters = value / 33.814

    @property
    def pints(self):
        return round(self._liters * 2.11338, self.precision)

    @pints.setter
    def pints(self, value):
        self._liters = value / 2.11338

    @property
    def gallons(self):
        return round(self._liters * 0.264172, self.precision)

    @gallons.setter
    def gallons(self, value):
        self._liters = value / 0.264172

    @property
    def barrels(self):
        return round(self._liters * 0.00838641436, self.precision)

    @barrels.setter
    def barrels(self, value):
        self._liters = value / 0.00838641436


if __name__ == "__main__":
    v = Volume()
    v.liters = 1
    print v.gallons
