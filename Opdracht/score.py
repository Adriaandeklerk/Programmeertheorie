# Begin van de score functie

import scipy
import scipy.spatial

def value():
    # free space between blocks
    #freesmall/mid/big is the free space between houses

    #FreeSmall, FreeMid and FreeBig should be the total free space in square meters
    FreeSmall =
    smallhouses = {}

    # PSEUDOCODE
    for i in smallhouses:
        Z = smallhouses[i]
        D = scipy.spatial.distance.cdist(Z,Z)
        
        #Euclidische ruimte formule, neemt twee coordinaten en een input array en berekent de afstand tussen de 2 punten
        D_euc = scipy.spatial.distance.seuclidean(x1, x2, board)

        print(D)
        print(Z)
        # zet afstand om naar hele meters
        D2 = D / 2
        # afronden naar beneden
        #
        # vrijstand voor kleine huizen, hoeken ontbreken nog!
        FreeSmall += D2 * 32
    for i in midhouses:
        Z = midhouses[i]
        D = scipy.spatial.distance.cdist(Z,Z)
        D2 = D / 2
        FreeMid += D2 * 35

    for i in bighouses:
        Z = bighouses[i]
        D = scipy.spatial.distance.cdist(Z,Z)
        D2 = D / 2
        FreeBig += D2 * 43

    # determins the value of the homes with added free space
    NSmall = smallhouseinfo['value'] + (smallhouseinfo['value increase'] * FreeSmall)
    NMid = midhouseinfo['value'] + (midhouseinfo['value increase'] * FreeMid)
    NBig = bighouseinfo['value'] + (bighouseinfo['value increase'] * FreeBig)

    # sums the new values up
    value = (NSmall * houses['familyhomes']) + (NMid * houses['bungalows']) + (NBig * houses['maisons'])

    # returns the value
    return value

