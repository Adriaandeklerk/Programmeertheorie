class Housing(object):
    """Different housing models

    Attributes:
        name: Name of housing type.
        size: Size of housing in m2.
        price: Price per housing unit.
        space: Necessary space around each housing unit.
        metervalue: Added relative value per extra meter space.
    """
    def __init__(self, name, size, price, space, metervalue):
        """Returns a new Housing object"""
        self.name = name
        self.size = size
        self.price = price
        self.space = space
        self.metervalue = metervalue

familyhome = Housing("familyhome", 64, 285000, 2, 3)
bungalow = Housing("bungalow", 75, 399000, 3, 4)
maison = Housing("maison", 115.5, 610000, 6, 6)
