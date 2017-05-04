# version 0.01
# does not account for surface water
# does not account for different houses, uses basic 8x8 houses
# only accounts for the 20 house varient, singles (12 houses)
# min_value is the minimum value of all houses on the board
import numpy as np

def min_val(x):

    SHValue = 285000
    MHValue = 399000
    BHValue = 610000


    Small = 60.0 / 100
    Mid = 25.0 / 100
    Big = 15.0 / 100

    Smallhome = int(x * Small)
    Middlehome = int(x * Mid)
    Bighome = int(x * Big)

    minvalue = (Smallhome * SHValue) + (Middlehome * MHValue) + (Bighome * BHValue)
    return minvalue

def initboard():

    board = []      # Define blank list
    MAXWIDTH =  160 # max width of the field in meters
    MAXLENGTH = 180 # max length of the field in meters
    ASA = (MAXWIDTH * MAXLENGTH) * 0.8 # accessible surface area
    RLength = int(ASA / MAXWIDTH) #relative length

    for row in range(RLength + 1):
        for col in range(MAXWIDTH + 1):
            board.append({"x":row, "y":col})

    return board

def initboard2():

    MAXWIDTH =  160 # max width of the field in meters
    MAXLENGTH = 180 # max length of the field in meters
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
    return 403

def hill_climbing(A):

    best_value = 20
    best_conf = None
    for conf in range(A):
        val = value(conf)
        if best_val > val:
            best_conf = conf
            best_val = val

    if best_conf > value(A):
        return A
    return hill_climbing(best_conf)


x = 20
# dit stuk vraagt om input
#x = int(raw_input())

#print initboard()[1], initboard()[161]
