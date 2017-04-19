# version 0.01
# does not account for surface water
# does not account for different houses, uses basic 8x8 houses
# only accounts for the 20 house varient, singles (12 houses)

# Define blank list
board = []
width =  160
length = 180
hw = (4)
hl = (3)

for row in range(hl):
  # Append a blank list to each row cell
  board.append([])
  for column in range(hw):
    # Assign [] to each row
    board[row].append('[x]')

# Function will print board with whitespace inbetween
def print_board(board):
  for row in board:
    print " ".join(row)

print_board(board)
print "vrijstand breedte =", length / hw, "meter"
print "vrijstand length =", length / hl, "meter"
print "remainder width =", width % 10, "meter",  hw, "houses"
print "remainder length =", length % 10, "meter",  hl, "houses"
print "totaal aantal huizen =", hl * hw
print ((hw * hl) * 285000) + (( length / hw) * 8550), 'euro'
print (hw * hl) * 285000, "basisprijs"
