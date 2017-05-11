# version 0.04
# min_value is the minimum value of all houses on the board

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as PLT
import random

# gets max width and length variables in half meters
MAXWIDTH =  160 * 2
MAXLENGTH = 180 * 2


def min_val(houses):
    x = houses
    # base values of each home, SH = family, MH = bungalow, BH = maison
    SHValue = 285000
    MHValue = 399000
    BHValue = 610000

    Small = x['familyhomes']
    Mid = x['bungalows']
    Big = x['maisons']

    # calulation of the minimum value of all homes
    minvalue = (Small * SHValue) + (Mid * MHValue) + (Big * BHValue)

    return minvalue


def initboard():

    # initializes a numpy array for the board
    board = np.zeros(shape=(MAXLENGTH, MAXWIDTH))
    # returns the initialized board
    return board

def score(minimum, repititions):

    # sets the amount of repititions
    repititions = repititions

    # sets the best value to the minimum value of all houses combined
    best_val = minimum

    # sets the best configuration as non-existent
    best_conf = None

    # itterates over the repititions, generating a configuration for each configuration
    # attempts to hill climb, hoping for an increase in value every itteration
    # and if the value of the result is better than the old best value(minium to min_value)
    # it sets the best value to that new best value and sets the configuration to that configuration
    for i in range(repititions):
        A = generate_configuration()
        AB = hill_climbing(A) # -> is to return the free space atleast, so the value function
                              # can determin the score
        Value_AB = value(A, B, C)
        if Value_AB > best_val:
            best_val = Value_AB
            best_conf = AB # -> needs to have the configuration too

    # returns the best configuration
    return best_conf


def value(A, B, C):
    # free space between blocks
    FreeSmall = A
    FreeMid = B
    FreeBig = C

    # retrieves housing info
    SH = housing('familyhome')
    MH = housing('bungalow')
    BH = housing('maison')

    # gets the amount of small, medium and large homes from global variable X
    Small = 60.0 / 100
    Mid = 25.0 / 100
    Big = 15.0 / 100
    Smallhome = int(x * Small)
    Middlehome = int(x * Mid)
    Bighome = int(x * Big)

    # determins the value of the homes with added free space
    NSmall = SH['value'] + (SH['value increase'] * FreeSmall)
    NMid = MH['value'] + (MH['value increase'] * FreeMid)
    NBig = BH['value'] + (BH['value increase'] * FreeBig)

    # sums the new values up
    value = (NSmall * Smallhome) + (NMid * Middlehome) + (NBig * Bighome)

    # returns the value
    return value


def generate_configuration(houses,board):

    # info containing the amount of houses to place
    houses = houses
    small = houses['familyhomes']
    middle = houses['bungalows']
    big = houses['maisons']

    # house information contains width and length
    smallinfo = housing('familyhome')
    midinfo = housing('bungalow')
    biginfo = housing('maison')

    # random x,y values to start
    x1 = random.randint(0,MAXWIDTH)
    y1 = random.randint(0,MAXLENGTH)

    smallhousecount = 0
    midhousecount = 0
    bighousecount = 0

    while True:
        if smallhousecount != small:
            x2 = x1 + smallinfo['width']
            y2 = y1 + smallinfo['length']
            while x2 >= MAXWIDTH:
                x1 = random.randint(0, MAXWIDTH)
                x2 = x1 + smallinfo['width']

            while y2 >= MAXLENGTH:
                y1 = random.randint(0, MAXLENGTH)
                y2 = y1 + smallinfo['length']

            if (board[y1:y2,x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + smallinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + smallinfo['length']
            else:
                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] ==0, 1)
                smallhousecount += 1

        elif midhousecount != middle:
            x2 = x1 + middleinfo['width']
            y2 = y1 + middleinfo['length']
            while x2 >= MAXWIDTH:
                x1 = random.randint(0, MAXWIDTH)
                x2 = x1 + middleinfo['width']

            while y2 >= MAXLENGTH:
                y1 = random.randint(0, MAXLENGTH)
                y2 = y1 + middleinfo['length']

            if (board[y1:y2,x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + 4
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + 4
            else:
                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] ==0, 2)
                midhousecount += 1

        elif bighousecount != big:
            x2 = x1 + biginfo['width']
            y2 = y1 + biginfo['length']
            while x2 >= MAXWIDTH:
                x1 = random.randint(0, MAXWIDTH)
                x2 = x1 + biginfo['width']

            while y2 >= MAXLENGTH:
                y1 = random.randint(0, MAXLENGTH)
                y2 = y1 + biginfo['length']

            if (board[y1:y2,x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + biginfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + biginfo['length']
            else:
                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] ==0, 3)
                bighousecount += 1
        else:
            break

        return board

def hill_climbing(A):

    # stuck here too

    best_value = min_val(x)
    best_conf = None
    for conf in [something](A):
        val = value(conf)
        if best_val > val:
            best_conf = conf
            best_val = val

    if best_conf > value(A):
        return A
    return hill_climbing(best_conf)


def housing(housename):

    # returns a dict containing the house type, surface area, value, free space,
    # value increase per meter of free space, length and width
    if housename == 'familyhome':
        return{
               "Housetype":"familyhome","Surface Area":64,
               "Value":285000, "Free space":2,
               "value increase":8550, "length":24,
               "width":24
               }

    elif housename == 'bungalow':
        return{
               "Housetype":"bungalow","Surface Area":75,
               "Value":399000, "Free space":3,
               "value increase":15960, "length":32,
               "width":27
               }

    elif housename == 'maison':
        return{
               "Housetype":"maison","Surface Area":115.5,
               "Value":610000, "Free space":6,
               "value increase":36600, "length":46,
               "width":45
               }


def houseamount(x):

    # determins the amount of each type of house
    Small = 60.0 / 100
    Mid = 25.0 / 100
    Big = 15.0 / 100

    # gets the amount of each home
    Smallhome = int(x * Small)
    Middlehome = int(x * Mid)
    Bighome = int(x * Big)

    # returns a dict with each amount of home
    return {
            "familyhomes":Smallhome,
            "bungalows": Middlehome,
            "maisons": Bighome
            }


def image(board):

    img = PLT.imshow(board, interpolation='nearest')
    img.set_cmap('hot')
    PLT.axis('off')
    PLT.show()
    PLT.savefig('map.png', bbox_inches='tight')


def main():

    print "Amount of houses, 20, 40 or 60 variant?"
    x = 20

    # wants user input if that is equal to 20, 40 or 60 it continues
    while x != 20:
        x = int(raw_input())
        if x == 20:
            break
        elif x == 40:
            break
        elif x == 60:
            break

    print "How many repititions?"
    repititions = 20 #int(raw_input())

    # inits board
    board = initboard()
    # gets the amount of each houses
    houses = houseamount(x)
    minimum = min_val(houses)
    generate_configuration(houses, board)
    image(board)

__init__=main()
