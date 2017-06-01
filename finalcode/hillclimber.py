# Final version of the Hill Climber and Random sampling
# Programmeertheorie
# Case: Amstelhaege
#
# Joren de Goede, Troy Breijaert, Adriaan de Klerk
#

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as PLT
import random, math, time, datetime


# gets max width and length variables in half meters
MAXWIDTH =  160 * 2
MAXLENGTH = 180 * 2

# global variables
x = 0
houses = {}
board = []
minimum = 0

# create dicts to store information of houses
smallhouseinfo = {}
midhouseinfo = {}
bighouseinfo = {}
allhomesinfo = []
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

def hill_climb(allhomesinfo):

    # pick a random house (h)
    h = random.randint(0, x-1)

    # generate random new x and y
    j = random.randint(0, MAXWIDTH)
    k = random.randint(0, MAXLENGTH)

    # calculate the old value
    oldvalue = value()
    values_array = []

    # iterate 2000 times over board
    for i in range(2000):

        # get x and y coordinates of house
        house = allhomesinfo[h]
        x1 = house["x"]["x1"]
        x2 = house["x"]["x2"]
        y1 = house["y"]["y1"]
        y2 = house["y"]["y2"]

        housingtype = house["type"]

        # store random x and y value
        j1 = j
        k1 = k

        # get second x and y value for new house
        j2 = j1 + allhomesinfo[h]["type"]["width"]
        k2 = k1 + allhomesinfo[h]["type"]["length"]

        # check if random coordinates don't exceed boundaries or generate other
        if j1 > MAXWIDTH or j2 > MAXWIDTH:
            j = random.randint(0, MAXWIDTH)
            j1 = j
            j2 = j1 + housingtype["width"]

        if k1 > MAXLENGTH or k2 > MAXLENGTH:
            k = random.randint(0, MAXLENGTH)
            k1 = k
            k2 = k1 + housingtype["length"]

        # place new house on the map and remove the old house
        else:
            info = {"id": h, "x":{"x1" : j1, "x2" : j2}, "y":{"y1" : k1, "y2" : k2}, "type": housingtype}
            np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] == 0, 0)
            allhomesinfo.remove((house))
            np.place(board[k1:k2,j1:j2], board[k1:k2,j1:j2] == int(housingtype["type"]), int(housingtype["type"]))
            allhomesinfo.append((info))

            # calculate new value
            newvalue = value()

            # store all values in array for textfile
            valuesave = oldvalue
            values_array.append((valuesave))

            print(oldvalue)
            print(newvalue)

            # check if new value is better than old value and go on to the next house
            if newvalue > oldvalue:
                oldvalue = newvalue

                j = random.randint(0, MAXWIDTH)
                k = random.randint(0, MAXLENGTH)
                h = random.randint(0, x-1)

            # else restore the old house, remove the new one and go on to the next house
            else:
                np.place(board[k1:k2,j1:j2], board[k1:k2,j1:j2] == 0, 0)
                del allhomesinfo[h]

                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] == int(housingtype["type"]), int(housingtype["type"]))
                info = {"id": h, "x":{"x1" : x1, "x2" : x2}, "y":{"y1" : y1, "y2" : y2}, "type": housingtype}
                allhomesinfo.append((info))

                j = random.randint(0, MAXWIDTH)
                k = random.randint(0, MAXLENGTH)
                h = random.randint(0, x-1)

    # store values in textfile
    s = str(round(time.time() * 1000))
    valuestext = open("values" + s + ".txt", "w")
    for i in values_array:
        print>>valuestext, i

    return oldvalue

def value():
    # calculates the values of all houses with free space

    distanceallhouse = []
    housingdict = []
    counter = 0

    # iterate over housing dict
    for i in allhomesinfo:
        x1 = i["x"]["x1"]
        x2 = i["x"]["x2"]
        y1 = i["y"]["y1"]
        y2 = i["y"]["y2"]
        f = 1

        housingdict.append(i)

        # store free space variable depending on housing type
        FS = i["type"]["Free space"]

        # calculate the total free space around each house and append in dict
        # water is also allowed for free space
        while True:
            f += 1
            if (board[(y1-FS-f):(y1-FS-1),x1:x2] != 0).any() and (board[(y1-FS-f):(y1-FS-1),x1:x2] != 4).any():
                info = {"id": counter, "f": f-1, "Value": i["type"]["Value"]}
                counter += 1
                distanceallhouse.append((info))
                break

            if (board[(y2+FS+1):(y2+FS+f),x1:x2] != 0).any() and (board[(y2+FS+1):(y2+FS+f), x1:x2] != 4).any():
                info = {"id": counter, "f": f-1, "Value": i["type"]["Value"]}
                counter += 1
                distanceallhouse.append((info))
                break

            if (board[y1:y2,(x1-FS-f):(x1-FS-1)] != 0).any() and (board[y1:y2,(x1-FS-f):(x1-FS-1)] != 4).any():
                info = {"id": counter, "f": f-1, "Value": i["type"]["Value"]}
                counter += 1
                distanceallhouse.append((info))
                break

            if (board[y1:y2,(x2+FS+1):(x2+FS+f)] != 0).any() and (board[y1:y2,(x2+FS+1):(x2+FS+f)] != 4).any():
                info = {"id": counter, "f": f-1, "Value": i["type"]["Value"]}
                counter += 1
                distanceallhouse.append((info))
                break

            if f >= MAXLENGTH:
                break


        sumofvalue = 0
        j = 0

        # for each house, calculate the total score with base value and value increase based on free space
        for i in distanceallhouse:
            sumofvalue += ((i["f"] * housingdict[j]["type"]["value increase"])) + i["Value"]
            j += 1
    return sumofvalue


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
                info = {"id": counter, "x":{"x1" : x1, "x2" : x2}, "y":{"y1" : y1, "y2" : y2}, "type": bighouseinfo}
                bighouses.append((info))
                allhomesinfo.append((info))
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
                info = {"id": counter, "x":{"x1" : x1, "x2" : x2}, "y":{"y1" : y1, "y2" : y2}, "type": midhouseinfo}
                middlehouses.append((info))
                allhomesinfo.append((info))
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

                info = {"id": counter, "x":{"x1" : x1, "x2" : x2}, "y":{"y1" : y1, "y2" : y2}, "type": smallhouseinfo}
                smallhouses.append((info))
                allhomesinfo.append((info))
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

def housing(housename):

    # returns a dict containing the house type, surface area, value, free space,
    # value increase per meter of free space, length and width
    if housename == 'familyhome':
        return{
               "Housetype":"familyhome","Surface Area":64,
               "Value":285000, "Free space":4,
               "value increase":(8550 / 2), "length":(8 * 2),
               "width":(8 * 2), "type":1
               }

    elif housename == 'bungalow':
        return{
               "Housetype":"bungalow","Surface Area":75,
               "Value":399000, "Free space":6,
               "value increase":(15960 / 2), "length":(10 * 2),
               "width":(7.5 * 2), "type":2
               }

    elif housename == 'maison':
        return{
               "Housetype":"maison","Surface Area":100,
               "Value":610000, "Free space":(6 * 2),
               "value increase":(36600 / 2), "length":(11 * 2),
               "width":(10.5 * 2), "type":3
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
    PLT.show()

def main():
    # set the amount of houses
    global x
    while x != 40:
        x = 60 #int(change amount of houses)
        if x == 20:
            break
        elif x == 40:
            break
        elif x == 60:
            break

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
    start_generator()

    # remove hashes to calculate value of random sample
    #oldvalue = 0
    #oldvalue = value()
    #print("Score found:")
    #print(oldvalue)
    #valueslist = []
    #oldvalue = value()
    #valuessave = ((oldvalue))
    #valueslist.append((valuessave))
    
    # remove hashes to save result in file
    #valuesrandom = open("valuesrandom.txt", "a")
    #for i in valueslist:
    #    print>>valuesrandom, i

    # runs the hill climber 2000 times and gives best value
    oldvalue = 0
    oldvalue = hill_climb(allhomesinfo)
    print("Best score found:")
    print(oldvalue)



    # shows the board
    image(board)


__init__=main()
