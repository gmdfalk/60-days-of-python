from __future__ import division


class Length(object):

    def __init__(self):
        self.millimeters = 0
        self.centimeters = 0
        self.meters = 0
        self.kilometers = 0
        self.inches = 0
        self.feet = 0
        self.yards = 0
        self.miles = 0

    def from_centimeters(self, cm):
        self.centimeters = cm
        self.meters = 0.999999


