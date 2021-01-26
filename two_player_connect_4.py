import sys
# set the max height and width that the board can be and how many players and how many we need in a row
maxHeight = 30
maxWidth = 30
minheight = 4
minwidth = 4
players = 2
inarow = 4

# check the state of the game function
def checkBoard(game, turn):

    # first check for horizontal wins we can eliminate checking for a win past a certain point to avoid a segmentation fault
    for row in range(height):
        for col in range(width - 3):
            if game[row][col] == turn and game[row][col + 1] == turn and game[row][col + 2] == turn and game[row][col + 3] == turn:
                return True

    # now we check for vertical wins
    for row in range(height - 3):
        for col in range(width):
            if game[row][col] == turn:
                if game[row][col] == turn and game[row + 1][col] == turn and game[row + 2][col] == turn and game[row + 3][col] == turn:
                    return True

    # now we will check for diagonal wins
    # there are two types of diagonal wins (\ and /) and we need to check for them individually

    # this is how we check for \ wins
    for row in range(height - 3):
        for col in range(width - 3):
            if game[row][col] == turn and game[row + 1][col + 1] == turn and game[row + 2][col + 2] == turn and game[row + 3][col + 3] == turn:
                return True

    # this is how we check for / wins
    for row in range(3, height):
        for col in range(width - 3):
            if game[row][col] == turn and game[row - 1][col + 1] == turn and game[row - 2][col + 2] == turn and game[row - 3][col + 3] == turn:
                return True

    # if we didnt find any 4s in a row
    return False

def printboard():
        # print the board with titles above each column
        for i in range(width):
            print(i + 1, end = " ")
        print()

        for row in board:
            for i in range(width):
                print(row[i], end = " ")
            print()



# get the width and height from the user
while True:
    height = input("Height of board: ")
    if height.isdecimal() == True:
        if int(height) <= maxHeight and int(height) >= minheight:
            height = int(height)
            break
        else:
            print("Try something smaller or bigger")

while True:
    width = input("Width of board: ")
    if width.isdecimal() == True:
        if int(width) <= maxWidth and int(width) >= minwidth:
            width = int(width)
            break
        else:
            print("Try something smaller or bigger")

# generate the board that is a 2d array
board = [[0 for i in range(width)] for j in range(height)]

# set whos turn it is
turn = 1

while True:

    printboard()

    # get the players move
    while True:
        move = input("player" + str(turn) + "'s move: ")
        if move.isdecimal() == True:
            move = int(move) - 1
            if move >= 0 and move < width:
                if board[0][move] > 0:
                    print("You can't place here")
                else:
                    move = int(move)
                    break
            else:
                print("error: not in range")

    # look where to place the piece and place it
    rown = 0
    for row in board:
        if rown == height - 1:
            board[rown][move] = turn
            break
        elif board[rown + 1][move] > 0:
            board[rown][move] = turn
            break
        rown += 1

    if checkBoard(board, turn) == True:
        printboard()
        print("Player " + str(turn) + " Wins")
        sys.exit(0)

    turn += 1
    if turn > players:
        turn = 1
