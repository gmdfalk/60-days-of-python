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


if __name__ == "__main__":
    L = Length()
    L.centimeters = 100
    print L.millimeters, L.centimeters, L._meters, L.kilometers
    print L.inches, L.feet, L.yards, L.miles
