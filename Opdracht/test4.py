import numpy as np
import random
import matplotlib.pyplot as plt

MAXWIDTH = 100
MAXLENGTH = 100

def initboard():
    board = np.zeros(shape=(MAXLENGTH, MAXWIDTH))
    return board

def image(board):
    img = plt.imshow(board, interpolation='nearest')
    img.set_cmap('hot')
    plt.axis('off')
    plt.show()

def main():
    x1 = random.randint(0, MAXWIDTH)
    y1 = random.randint(0, MAXLENGTH)

    board = initboard()
    small = 0.6 * 20
    countsmall = 0
    mid = 0.2 * 20
    countmid = 0
    big = 0.2 * 20
    countbig = 0

    while True:
        if countsmall != small:
            x2 = x1 + 2
            y2 = y1 + 2
            while x2 >= MAXWIDTH:
                x1 = random.randint(0, MAXWIDTH)
                x2 = x1 + 2

            while y2 >= MAXLENGTH:
                y1 = random.randint(0, MAXLENGTH)
                y2 = y1 + 2

            if (board[y1:y2,x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + 2
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + 2
            else:
                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] ==0, 1)
                countsmall += 1

        elif countmid != mid:
            x2 = x1 + 4
            y2 = y1 + 4
            while x2 >= MAXWIDTH:
                x1 = random.randint(0, MAXWIDTH)
                x2 = x1 + 4

            while y2 >= MAXLENGTH:
                y1 = random.randint(0, MAXLENGTH)
                y2 = y1 + 4

            if (board[y1:y2,x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + 4
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + 4
            else:
                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] ==0, 2)
                countmid += 1
        elif countbig != big:
            x2 = x1 + 8
            y2 = y1 + 8
            while x2 >= MAXWIDTH:
                x1 = random.randint(0, MAXWIDTH)
                x2 = x1 + 8

            while y2 >= MAXLENGTH:
                y1 = random.randint(0, MAXLENGTH)
                y2 = y1 + 8

            if (board[y1:y2,x1:x2] != 0).any():
                x1 = random.randint(0, MAXWIDTH -1 )
                x2 = x1 + 8
                y1 = random.randint(0, MAXLENGTH - 1)
                y2 = y2 + 8
            else:
                np.place(board[y1:y2,x1:x2], board[y1:y2,x1:x2] ==0, 3)
                countbig += 1
        else:
            break

    print(board)
    image(board)

__init__=main()
