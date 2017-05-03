class Housing(object):
    """Different housing models

    Attributes:
        name: Name of housing type.
        size: Size of housing in m2.
        price: Price per housing unit.
        total_space: Necessary space around each housing unit.
        metervalue: Added relative value per extra meter space.
        width: Width of the housing type.
        length: Length of housing type.
    """
    def __init__(self, name, size, price, free_space, metervalue, width, length):
        """Returns a new Housing object"""
        self.name = name
        self.size = size
        self.price = price
        self.free_space = free_space
        self.metervalue = metervalue
        self.width = width
        self.length = length

    def displayHousing(self):
        print "Housing type: ", self.name, ", Total size: ", self.size, ", \
        Price per unit:", self.price, "Free space: ", self.free_space, ", \
        Added value per meter free space: ", self.metervalue, ", Width: ", \
        self.width, ", Length: ", self.length

familyhome = Housing("familyhome", 64, 285000, 2, 3, 8, 8)
bungalow = Housing("bungalow", 75, 399000, 3, 4, 10, 7.5)
maison = Housing("maison", 115.5, 610000, 6, 6, 11, 10.5)

familyhome.displayHousing()
