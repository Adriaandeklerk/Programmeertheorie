# version 0.03
# does not account for surface water
# does not account for different houses, uses basic 8x8 houses
# only accounts for the 20 house varient, singles (12 houses)
# min_value is the minimum value of all houses on the board

import numpy as np
x = 0
board = []

def min_val(x):

    SHValue = 285000 # value of the smallest home, the family home
    MHValue = 399000 # value of the middle home, the bungalow
    BHValue = 610000 # value of the biggest home, the maison


    Small = 60.0 / 100
    Mid = 25.0 / 100
    Big = 15.0 / 100

    Smallhome = int(x * Small) # amount of familyhomes
    Middlehome = int(x * Mid) # amount of bungalows
    Bighome = int(x * Big) # amount of maisons

    # calulation of the minimum value of all homes
    minvalue = (Smallhome * SHValue) + (Middlehome * MHValue) + (Bighome * BHValue)
    return minvalue

def initboard():

    MAXWIDTH =  160 * 2 # max width of the field in half meters
    MAXLENGTH = 180 * 2 # max length of the field in half meters
    ASA = (MAXWIDTH * MAXLENGTH) * 0.8 # accessible surface area
    RLength = int(ASA / MAXWIDTH) #relative length
    board = np.empty((RLength , MAXWIDTH),dtype=object)

    for row in range(RLength):
        for col in range(MAXWIDTH):
            board[row, col] = 'E'
    return board

def score():

    repititions = 100
    best_val = min_val(x)
    best_conf = None
    for i in range(repititions):
        A = generate_configuration()
        AB = hill_climbing(A)
        Value_AB = value(AB)
        if Value_AB > best_val:
            best_val = Value_AB
            best_conf = AB
    return best_conf

def value(A):
    vrijstand = A

    SHValue = 285000
    MHValue = 399000
    BHValue = 610000


    Small = 60.0 / 100
    Mid = 25.0 / 100
    Big = 15.0 / 100

    Smallhome = int(x * Small)
    Middlehome = int(x * Mid)
    Bighome = int(x * Big)

    NSmall = SHvalue + (0.03 * SHValue) * vrijstand
    NMid = MHValue + (0.03 * MHValue) * vrijstand
    NBig = BHValue + (0.03 * BHValue) * vrijstand
    value = (NSmall * SHValue) + (NMid * MHValue) + (NBig * BHValue)

    return value

def generate_configuration():

    # check if object can fit on x and check if object can fit on y
    houses = houseamount(x)
    small = houses['familyhomes']
    middle = houses['bungalows']
    big = houses['maisons']
    smallinfo = housing('familyhome')
    midinfo = housing('bungalow')
    biginfo = housing('maison')

    xcount = 0
    blue = ''

    for i in board:
        xcount += 1

        if(board[i] - smallinfo['width'] < 0):
            i += 1
        elif(board[i] - smallinfo['width'] >= 0):
            for j in board[i]:
                if(board[i][j] - smallinfo['length'] < 0):
                    j += 1
                elif(board[i][j] - smallinfo['length'] >= 0):
                    blue = 'bob'

    return blue

def hill_climbing(A):

    best_value = 20
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

    # creating dicts containing the key for each housetype
    A = housename

    if A == 'familyhome':
        return{
               "Housetype":"familyhome","Surface Area":64,
               "Value":285000, "Free space":2,
               "value increase":8550, "length":24,
               "width":24
               }

    elif A == 'bungalow':
        return{
               "Housetype":"bungalow","Surface Area":75,
               "Value":399000, "Free space":3,
               "value increase":15960, "length":32,
               "width":27
               }

    elif A == 'maison':
        return{
               "Housetype":"bungalow","Surface Area":115.5,
               "Value":610000, "Free space":6,
               "value increase":36600, "length":46,
               "width":45
               }


def houseamount(x):

        Small = 60.0 / 100
        Mid = 25.0 / 100
        Big = 15.0 / 100

        Smallhome = int(x * Small) # amount of familyhomes
        Middlehome = int(x * Mid) # amount of bungalows
        Bighome = int(x * Big) # amount of maisons
        return {
                "familyhomes":Smallhome,
                "bungalows": Middlehome,
                "maisons": Bighome
                }

def main():
    board = initboard()
    x = 20
    # dit stuk vraagt om input
    #x = int(raw_input())

    #print housing('bungalow')['length'], housing('bungalow')['width'], "in half meters"
    print generate_configuration()

__init__=main()
