import sys
import copy

# datestamp: 1/19/2021
# set the max height and width that the board can be and how many players and how many we need in a row player 1 is human and player 2 is the ai.
maxHeight = 30
maxWidth = 30
minheight = 4
minwidth = 4
maxdepth = 3
ai = 2
player = 1

# for each slot you can play, do the algorithm for that slot,
# then take all the outputs from each slot and return what the player or ai would choose based on the outputs.

# function that returns a value for the state of the game that is passed into it.
# should be biased towards having more pieces in the middle of the board and having more pieces towards the bottom
def positionscore(board):
    score = 0
    temp = 0
    col = 0
    rown = 0
    weight = 0
    for row in board:
        for piece in row:
            temp = 0
            weight = 0
            if piece == ai:
                temp = temp + 100
            elif piece == player:
                temp = temp - 100
            score = score + temp
            weight = abs((col + 1) - (width - col))
            score = score + ((temp / (weight + 1)) * rown + 1)
            col = col + 1
        col = 0
        rown = rown + 1
    return score


def openrow(board, col):
    for r in range(height):
        if board[r][col] != 0:
            return r - 1
    return height - 1

# here is where i will try to implement the algorithm
def minimax(board, depth, turn):

    # first check if its won
    if checkBoard(board, turn) == True:
        if turn == ai:
            return 99999
        else:
            return -99999


    # this is where we will evaluate the game board (only if its at the bottom of the tree)
    if depth == maxdepth:
        return positionscore(board)

    # set the turn to the other player
    if turn == player:
        turn = ai
        best = -999999
    else:
        turn = player
        best = 99999
    # get the valid slots that aren't filled up
    openslots = validslots(board)

    # we are going to go down those paths and make an array with the outputs of going down each of those paths
    for slot in openslots:
        row = openrow(board, slot)
        boardcopy = copy.deepcopy(board)
        place(boardcopy, row, slot, turn)
        score = minimax(boardcopy, depth + 1, turn)
        # if its the ai turn
        if turn == ai:
            if score >= best:
                best = score
        # if its the humans turn
        elif turn == player:
            if score <= best:
                best = score
    return best


# function to get the all of the valid slots that you can play in and returns the slots in an array
def validslots(board):
    openslots = []
    slotnum = 0
    for pos in board[0]:
        if pos == 0:
            openslots.append(slotnum)
        slotnum = slotnum + 1
    return openslots

# check the state of the game function, will only check if the player that is inputted has won and not if any other player had won.
# will return true if that player has won, will return false if they didn't win.
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



def place(board, row, col, turn):
	board[row][col] = turn

# function for printing the board
def printboard(board):
        # print the board with titles above each column
        for i in range(width):
            print(i + 1, end = " ")
        # then print a newline character
        print()

        # print each row in the board and put a newlince character after printing each row
        for row in board:
            for i in range(width):
                print(row[i], end = " ")
            print()

height = 6
width = 7


# get the width and height from the user
#while True:
#    height = input("Height of board: ")
#    if height.isdecimal() == True:
#        if int(height) <= maxHeight and int(height) >= minheight:
#            height = int(height)
#            break
#        else:
#            print("Try something smaller or bigger")

#while True:
#    width = input("Width of board: ")
#    if width.isdecimal() == True:
#        if int(width) <= maxWidth and int(width) >= minwidth:
#            width = int(width)
#            break
#        else:
#            print("Try something smaller or bigger")



# generate the board that is a 2d array
game = [[0 for i in range(width)] for j in range(height)]

while True:

    # set it to the players turn and print the board
    turn = 1
    printboard(game)

    # get the players move
    while True:
        move = input("player" + str(turn) + "'s move: ")
        if move.isdecimal() == True:
            move = int(move) - 1
            if move >= 0 and move < width:
                if game[0][move] > 0:
                    print("You can't place here")
                else:
                    move = int(move)
                    break
            else:
                print("error: not in range")

    # update the game board with the persons move
    row = openrow(game, move)
    place(game, row, move, turn)

    # see if the player has won
    if checkBoard(game, turn) == True:
        printboard(game)
        print("Player " + str(turn) + " Wins")
        sys.exit(0)

    # now we will make the ai run for the next turn
    # get the outputs from every slot that you can play
    allmoves = validslots(game)

    turn = ai


    best = (-9999, 0)
    for slot in allmoves:
        row = openrow(game, slot)
        gamecopy = copy.deepcopy(game)
        place(gamecopy, row, slot, turn)
        val = minimax(gamecopy, 0, 2)
        if val >= best[0]:
            best = (val, slot)

    print("best for first layer:", end = "")
    print(best)

    row = openrow(game, best[1])
    # update the board to play those values
    place(game, row, best[1], turn)

    # now we check if the ai won
    if checkBoard(game, turn) == True:
        printboard(game)
        print("The computer has won")
        sys.exit(0)

    # bug: the ai will play the first column if there is no other better move, but if the first colomn is full then it will print an error
