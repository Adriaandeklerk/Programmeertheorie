# version 0.13
# min_value is the minimum value of all houses on the board
# random water generation and building placement
# more refined building placement
# fixed generating configuration
# fixed watershape to be a ratio between 1 and 4 instead of 1:4

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as PLT
import random, math, time, datetime
import scipy
import scipy.spatial

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

smallhouses = []
middlehouses = []
bighouses = []
myset = set()


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
    rep = repititions

    # sets the best value to the minimum value of all houses combined
    best_val = minimum

    # sets the best configuration as non-existent
    best_conf = None

    # itterates over the repititions, generating a configuration for each configuration
    # attempts to hill climb, hoping for an increase in value every itteration
    # and if the value of the result is better than the old best value(minium to min_value)
    # it sets the best value to that new best value and sets the configuration to that configuration
    for i in range(rep):
        A = generate_configuration()
        AB = hill_climbing(A) # -> is to return the free space atleast, so the value function
                              # can determin the score
        Value_AB = value(A, B, C)
        if Value_AB > best_val:
            best_val = Value_AB
            best_conf = AB # -> needs to have the configuration too

    # returns the best configuration
    return best_conf


def value():
    # free space between blocks
    #freesmall/mid/big is the free space between houses

    distancevalue = []
    distance = []
    distances = []

    #iterate over each small house
    for i in smallhouses:
        # store coordinates of each house
        x1 = i["x"]["x1"]
        x2 = i["x"]["x2"]
        y1 = i["y"]["y1"]
        y2 = i["y"]["y2"]
        f = 1
        
        #ensure that you don't look outside of the board
        while x1>f and y1>f and (y2+f)<MAXLENGTH and (x2+f)<MAXWIDTH:
            # if not all numbers found in this part of the board are zero check if they are '4' (is water)
            if not (board[(x1-f):(x1-1),y1-f:y2+f] == 0).all():
                # if it's a 4 continue expanding
                if (board[(x1-f):(x1-1),y1-f:y2+f] == 4).any():
                    print("succes")
                # else store the distancevalue for this house and break
                else:
                    distancevalue.append(f-1)
                    print "f = ", f
                    break
            # do the same for the other directions of the house
            if not (board[(x2+1):(x2+f),y1-f:y2+f] == 0).all():
                if (board[(x2+1):(x2+f),y1-f:y2+f] == 4).any():
                    print("jeej")
                else:
                    distancevalue.append(f-1)
                    print "g = ", f
                    break
            if not (board[x1-f:x2+f,(y1-1):(y1-f)] == 0).all():
                if (board[x1-f:x2+f,(y1-1):(y1-f)] == 4).any():
                    print("ja")
                else:
                    distancevalue.append(f-1)
                    print "h = ", f
                    break
            if not (board[x1-f:x2+f,(y2+1):(y2+f)] == 0).all():
                if (board[x1-f:x2+f,(y2+1):(y2+f)] == 4).any():
                    print("ja")
                else:
                    distancevalue.append(f-1)
                    print "i = ", f
                    break
            # increase the distance each iteration by 1
            else:
                f += 1

    sumincrease = 0

    for j in distancevalue:
        sumincrease += (j*(smallhouseinfo['value increase']))

    print(sumincrease)
    distances = open("distances.txt", "w")
    for i in distancevalue:
        print>>distances, i

    print(distancevalue)


    #    D2 = D/2
    #    FreeSmall += D2

    #print(bighouses)


    #print(FreeSmall)

    # determins the value of the homes with added free space
    #NSmall = smallhouseinfo['Value'] + (smallhouseinfo['value increase'] * FreeSmall)
    #NMid = midhouseinfo['Value'] + (midhouseinfo['value increase'] * FreeMid)
    #NBig = bighouseinfo['Value'] + (bighouseinfo['value increase'] * FreeBig)

    #print (NSmall)
    # sums the new values up
    #value = (NSmall * houses['familyhomes']) + (NMid * houses['bungalows']) + (NBig * houses['maisons'])

    #print value
    # returns the value
    #return value
    # determins the value of the homes with added free space


def watershape():
    maxarea = MAXLENGTH * MAXWIDTH # gets max area of the array
    wsa = 0.2 * maxarea # water surface area
    minwidth = 1#int(MAXWIDTH / 100)
    while True:
        awt = wsa / random.randint(1,4) # average water tile, determins how many water tiles should exist
        number = int(wsa / awt) # gets the random interger back for later
        width = random.randint(minwidth, int(MAXWIDTH / number)) #generates a random width between 1/50th and 1/xth(max=4) of the width
        length = int(awt / width)
        if int(width / length) >= 1 and int(width / length) <= 4 or int(length / width) >= 1 and int(length / width) <= 5:
            break

    return {"tiles":number, 'x':width, 'y':length}


def generate_configuration():

    # info containing the amount of houses to place
    small = houses['familyhomes']
    middle = houses['bungalows']
    big = houses['maisons']

    water = watershape()
    # random x,y values to start
    x1 = random.randint(0,MAXWIDTH)
    y1 = random.randint(0,MAXLENGTH)

    # counters for houses
    smallhousecount = 0
    midhousecount = 0
    bighousecount = 0
    watercount = 0
    counter = 0
    #bighouses = 0

    timeout = time.time() + 5
    #timeout2 = datetime.time() + datetime.timedelta(seconds=5)
    #print timeout2

    bighousecorner = int(math.sqrt((bighouseinfo['Free space']**2) + bighouseinfo['Free space']**2))
    midhousecorner = int(math.sqrt((midhouseinfo['Free space']**2) + midhouseinfo['Free space']**2))
    smallhousecorner = int(math.sqrt((smallhouseinfo['Free space']**2) + smallhouseinfo['Free space']**2))

    while time.time() < timeout:

        # if the amount of houses on the board is not the required amount
        # of a specific house, places it on the board

        while watercount != water['tiles'] and time.time() <= timeout:
            x2 = x1 + water['x']
            y2 = y1 + water['y']

            # if the width of the house from x1 is bigger than the width of
            # the array, generate a new number
            while x2 >= MAXWIDTH:
                x1 = random.randint(0, MAXWIDTH)
                x2 = x1 + water['x']

            # if the width of the house from y1 is bigger than the width of
            # the array, generate a new number
            while y2 >= MAXLENGTH:
                y1 = random.randint(0, MAXLENGTH)
                y2 = y1 + water['y']

            if (board[y1:y2,x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + water['x']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + water['y']

            else:
                # places houses and increases counter by 1
                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] ==0, 4)
                watercount += 1

        while bighousecount != big and time.time() <= timeout:
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

            if (board[y1:y2,x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            elif (board[(y1 - bighouseinfo['Free space']):(y2 + bighouseinfo['Free space']),x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            elif (board[y1:y2,(x1 - bighouseinfo['Free space']):(x2 + bighouseinfo['Free space'])] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            elif (board[(y1 - bighousecorner):(y2 + bighousecorner), (x1 - bighousecorner):(x2 + bighousecorner)] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            # checks if ANY of the values in the x,y positions is not 0,
            # of where the house is to be placed, if so generate new x,y positionsk
            else:
                # places houses and increases counter by 1
                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] ==0, 3)
                bighousecount += 1
                info = {"id": counter, "x":{"x1" : x1, "x2" : x2}, "y":{"y1" : y1, "y2" : y2}}
                bighouses.append((info))
                counter += 1

        while midhousecount != middle and time.time() <= timeout:

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

            elif (board[(y1 - midhouseinfo['Free space']):(y2 + midhouseinfo['Free space']),x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            elif (board[y1:y2,(x1 - midhouseinfo['Free space']):(x2 + midhouseinfo['Free space'])] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            elif (board[(y1 - midhousecorner):(y2 + midhousecorner), (x1 - midhousecorner):(x2 + midhousecorner)] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            elif (board[(y1 - bighouseinfo['Free space']):(y2 + bighouseinfo['Free space']), x1:x2] == 3).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            elif (board[(y1 - bighouseinfo['Free space']):(y2 + bighouseinfo['Free space']), x1:x2] == 3).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            elif (board[(y1 - bighousecorner):(y2 + bighousecorner), (x1 - bighousecorner):(x2 + bighousecorner)] == 3).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']
            else:
                # places houses and increases counter by 1
                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] ==0, 2)
                midhousecount += 1
                info = {"id": counter, "x":{"x1" : x1, "x2" : x2}, "y":{"y1" : y1, "y2" : y2}}
                middlehouses.append((info))
                counter += 1

        while smallhousecount != small and time.time() <= timeout:
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

            elif (board[(y1 - smallhouseinfo['Free space']):(y2 + smallhouseinfo['Free space']),x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            elif (board[y1:y2,(x1 - smallhouseinfo['Free space']):(x2 + smallhouseinfo['Free space'])] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            elif (board[(y1 - smallhousecorner):(y2 + smallhousecorner), (x1 - smallhousecorner):(x2 + smallhousecorner)] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            elif (board[(y1 - bighouseinfo['Free space']):(y2 + bighouseinfo['Free space']), x1:x2] == 3).any() or (board[(y1 - midhouseinfo['Free space']):(y2 + midhouseinfo['Free space']), x1:x2] == 2).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            elif (board[(y1 - bighouseinfo['Free space']):(y2 + bighouseinfo['Free space']), x1:x2] == 3).any() or (board[y1:y2, (x1 - midhouseinfo['Free space']):(x2 + midhouseinfo['Free space'])] == 2).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            elif (board[(y1 - bighousecorner):(y2 + bighousecorner), (x1 - bighousecorner):(x2 + bighousecorner)] == 3).any() or (board[(y1 - midhousecorner):(y2 + midhousecorner), (x1 - midhousecorner):(x2 + midhousecorner)] == 2).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + bighouseinfo['width']
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + bighouseinfo['length']

            # of where the house is to be placed, if so generate new x,y positions
            else:
                # places houses and increases counter by 1
                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] ==0, 1)
                smallhousecount += 1

                info = {"id": counter, "x":{"x1" : x1, "x2" : x2}, "y":{"y1" : y1, "y2" : y2}}
                smallhouses.append((info))
                counter += 1

        else:
            smallhomestext = open("testsmallhouses.txt", "w")
            allhomes = open("allhomes.txt", "w")
            for i in smallhouses:
                print>>smallhomestext, i
                print>>allhomes, i
            middlehomestext = open("testmiddlehouses.txt", "w")
            for i in middlehouses:
                print>>middlehomestext, i
                print>>allhomes, i
            bighomestext = open("testbighouses.txt", "w")
            for i in bighouses:
                print>>bighomestext, i
                print>>allhomes, i

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
               "Value":285000, "Free space":4,
               "value increase":(8550 / 2), "length":(8 * 2),
               "width":(8 * 2)
               }

    elif housename == 'bungalow':
        return{
               "Housetype":"bungalow","Surface Area":75,
               "Value":399000, "Free space":6,
               "value increase":(15960 / 2), "length":(10 * 2),
               "width":int((7.5 * 2))
               }

    elif housename == 'maison':
        return{
               "Housetype":"maison",
               "Value":610000, "Free space":(6 * 2),
               "value increase":(36600 / 2), "length":(11 * 2),
               "width":int((10.5 * 2))
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

def start_generator():
    print "terraforming board"
    global board
    board = initboard()
    print "generating configuration"
    generate_configuration()


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
    #generate_configuration()
    start_generator()
    # shows the board
    value()
    image(board)


__init__=main()
