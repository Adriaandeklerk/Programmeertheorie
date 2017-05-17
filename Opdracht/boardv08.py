# version 0.08
# min_value is the minimum value of all houses on the board

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as PLT
import random

# gets max width and length variables in half meters
MAXWIDTH =  160 * 2
MAXLENGTH = 180 * 2

# global variables
x = 0
houses = {}
board = []
minimum = 0
smallhouseinfo = {}
midhouseinfo = {}
bighouseinfo = {}

def min_val():
    x = houses
    # base values of each home, SH = family, MH = bungalow, BH = maison
    MHValue = 399000
    SHValue = 285000
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


def score(repititions):
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
    print Value_AB
    return best_conf


def value():
    # free space between blocks
    FreeSmall = 20
    FreeMid = 50
    FreeBig = 17

    # gets the amount of small, medium and large homes from global variable X
    Small = 60.0 / 100
    Mid = 25.0 / 100
    Big = 15.0 / 100
    Smallhome = int(x * Small)
    Middlehome = int(x * Mid)
    Bighome = int(x * Big)

    # determins the value of the homes with added free space
    #NSmall = smallhouseinfo['value'] + (smallhouseinfo['value increase'] * FreeSmall)
    houseworth = smallhouseinfo['Value'] * Smallhome + midhouseinfo['Value'] \
        * Middlehome + bighouseinfo['Value'] * Bighome

    freeworth = smallhouseinfo['value increase'] * FreeSmall + midhouseinfo['value increase'] \
        * FreeMid + bighouseinfo['value increase'] * FreeBig

    #NMid = midhouseinfo['value'] + (midhouseinfo['value increase'] * FreeMid)
    #NBig = bighouseinfo['value'] + (bighouseinfo['value increase'] * FreeBig)

    # sums the new values up
    #value = (NSmall * Smallhome) + (NMid * Middlehome) + (NBig * Bighome)

    # returns the value
    totalworth = houseworth + freeworth
    return totalworth


def generate_configuration():

    # info containing the amount of houses to place
    small = houses['familyhomes']
    middle = houses['bungalows']
    big = houses['maisons']

    # random x,y values to start
    x1 = random.randint(0,MAXWIDTH)
    y1 = random.randint(0,MAXLENGTH)

    # counters for houses
    smallhousecount = 0
    midhousecount = 0
    bighousecount = 0

    while True:
        # if the amount of houses on the board is not the required amount
        # of a specific house, places it on the board
        while bighousecount != big:
            x2 = x1 + bighouseinfo['width']
            y2 = y1 + bighouseinfo['length']

            # if the width of the house from x1 is bigger than the width of
            # the array, generate a new number
            while x2 >= MAXWIDTH:
                x1 = random.randint(0, MAXWIDTH)
                x2 = x1 + bighouseinfo['width']

            # if the width of the house from y1 is bigger than the width of
            # the array, generate a new number
            while y2 >= MAXLENGTH:
                y1 = random.randint(0, MAXLENGTH)
                y2 = y1 + bighouseinfo['length']

            # checks if ANY of the values in the x,y positions is not 0,
            # of where the house is to be placed, if so generate new x,y positions
            if (board[y1:y2,x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            else:
                # places houses and increases counter by 1
                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] ==0, 3)
                bighousecount += 1

        while midhousecount != middle:
            x2 = x1 + midhouseinfo['width']
            y2 = y1 + midhouseinfo['length']

            # if the width of the house from x1 is bigger than the width of
            # the array, generate a new number
            while x2 >= MAXWIDTH:
                x1 = random.randint(0, MAXWIDTH)
                x2 = x1 + midhouseinfo['width']

            # if the width of the house from y1 is bigger than the width of
            # the array, generate a new number
            while y2 >= MAXLENGTH:
                y1 = random.randint(0, MAXLENGTH)
                y2 = y1 + midhouseinfo['length']

            # checks if ANY of the values in the x,y positions is not 0,
            # of where the house is to be placed, if so generate new x,y positions
            if (board[y1:y2,x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + midhouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + midhouseinfo['length']

            else:
                # places houses and increases counter by 1
                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] ==0, 2)
                midhousecount += 1

        while smallhousecount != small:
            x2 = x1 + smallhouseinfo['width']
            y2 = y1 + smallhouseinfo['length']

            # if the width of the house from x1 is bigger than the width of
            # the array, generate a new number
            while x2 >= MAXWIDTH:
                x1 = random.randint(0, MAXWIDTH)
                x2 = x1 + smallhouseinfo['width']

            # if the width of the house from y1 is bigger than the width of
            # the array, generate a new number
            while y2 >= MAXLENGTH:
                y1 = random.randint(0, MAXLENGTH)
                y2 = y1 + smallhouseinfo['length']

            # checks if ANY of the values in the x,y positions is not 0,
            if (board[y1:y2,x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + smallhouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + smallhouseinfo['length']

                # of where the house is to be placed, if so generate new x,y positions
            else:
                # places houses and increases counter by 1
                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] ==0, 1)
                smallhousecount += 1
        else:
            break

        freespace(board)

        return board
        return freespace

def freespace(board):
    # define variables for amount of meters free space for each type
    smallworth = 0
    midworth = 0
    bigworth = 0

    x1
    y1

    num_zero = (y == 0).all():

    # if there is a 0 on the board count the amount of meters free space
    for 0 in range MAXWIDTH:
        for 0 in range MAXHEIGHT:
            if (board[y1:y2,x1:x2] = 0).any():
                # if 0 belongs to a small house, count free space
                if 1:
                    smallworth += 1
                # if 0 belongs to mid house, count free space
                elif 2:
                    midworth += 1
                # if 0 belongs to a big house, count free space
                elif 3:
                    bigworth += 1

    return smallworth, midworth, bigworth

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


def houseamount():

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
    # generates and saves an image
    img = PLT.imshow(board, interpolation='nearest')
    img.set_cmap('Accent')
    PLT.axis('off')
    PLT.savefig('map.png', bbox_inches='tight')
    #PLT.show()


def main():

    print "Amount of houses, 20, 40 or 60 variant?"
    # wants user input if that is equal to 20, 40 or 60 it continues
    global x
    x = 0
    while x != 60:
        x = 60 #int(raw_input())
        if x == 20:
            break
        elif x == 40:
            break
        elif x == 60:
            break

    print "How many repititions?"
    repititions = 20 #int(raw_input()

    # inits board
    global board
    board = initboard()

    # gets the amount of each houses
    global houses
    houses = houseamount()

    # gets and sets minimum value
    global minimum
    minimum = min_val()

    global smallhouseinfo
    smallhouseinfo = housing('familyhome')
    global midhouseinfo
    midhouseinfo = housing('bungalow')
    global bighouseinfo
    bighouseinfo = housing('maison')

    # generates a random configuration
    generate_configuration()

    print "Total worth of current composition: "
    print value()
    # shows the board
    image(board)

__init__=main()
