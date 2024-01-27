import numpy as np
import random

COLUMNS = ["a", "b", "c"]


# where the player decides if they want to be noughts or crosses
def noughts_or_crosses():
    o_or_x_input = input(
        "\n"
        "Do you want to be noughts or crosses?\n"
        "Noughts goes first.\n"
        "> "
    ).lower()

    if o_or_x_input == "noughts" or o_or_x_input == "nought":
        nought_or_cross = 1
    elif o_or_x_input == "crosses" or o_or_x_input == "cross":
        nought_or_cross = 4
    else:
        print("Please enter a valid input")
        return noughts_or_crosses()
    return nought_or_cross


# prints the contents of the array as text-format
def print_array(board_array):

    cell_base = "  -  "  # default cell format
    final_cell_list = []

    counter = 0
    for n in range(9):

        # figuring out where in the array the cell is
        column = counter % 3
        row = int(round(counter / 3, 0))
        if column == 2:
            row -= 1
        counter += 1

        if board_array[row][column] == 0:
            cell = cell_base.replace("-", " ")
        elif board_array[row][column] == 1:
            cell = cell_base.replace("-", "O")
        else:
            cell = cell_base.replace("-", "X")

        final_cell_list.append(cell)

    #  assembling the printable board
    top_bottom_row = "       |     |     "
    mid_row = "  _____|_____|_____\n       |     |     "
    board_print = (
        f"    a     b     c  "
        f"\n{top_bottom_row}\n"
        f"1 {final_cell_list[0]}|{final_cell_list[1]}|{final_cell_list[2]}"
        f"\n{mid_row}\n"
        f"2 {final_cell_list[3]}|{final_cell_list[4]}|{final_cell_list[5]}"
        f"\n{mid_row}\n"
        f"3 {final_cell_list[6]}|{final_cell_list[7]}|{final_cell_list[8]}"
        f"\n{top_bottom_row}"
    )
    print(board_print)


def human_cell_chooser(board_array, player_character):
    '''
    Turns the "b3" format of a user input into a coordinates tuple (1,2).
    It then calls the update array function to place the mark on the board.
    '''

    inputted_cell = input(
        "Which cell do you want to put your mark in? Example: b3\n> ")

    xn = inputted_cell.strip().lower()
    xn_split = [x for x in xn]

    if len(xn_split) > 2:  # seeing if user has inputted more than two characters
        return human_cell_chooser(input("Please input only two characters\n> "))

    column = xn_split[0]
    if column == "a":
        column = 0
    elif column == "b":
        column = 1
    elif column == "c":
        column = 2
    else:  # if first character is anything except a, b, or c
        return human_cell_chooser(input("Please input a valid column letter (a, b, c)\n> "))

    try:
        row = int(xn_split[1]) - 1
        if row > 2:  # seeing if number is below 3
            return human_cell_chooser(input("Please input a valid row number (1, 2, 3)\n> "))
    except ValueError:  # seeing if second character is a number
        return human_cell_chooser(input("Please input a valid row number (1, 2, 3)\n> "))

    coord = (row, column)

    update_array(board_array, coord, player_character, human=True)


# updates the controller array from input provided by the user
def update_array(board_array, coord, player_character, human=True):

    if human == True:

        if board_array[coord[0]][coord[1]] != 0:
            print("You can only select an empty cell!")
            return human_cell_chooser(board_array, player_character)
        else:
            board_array[coord[0]][coord[1]] = player_character

    else:
        if board_array[coord[0]][coord[1]] != 0:
            return True
        else:
            if player_character == 1:
                board_array[coord[0]][coord[1]] = 4
            else:
                board_array[coord[0]][coord[1]] = 1

    print_array(board_array)


# this is important for the AI to be able to block the player
# if sum of row/column is 2 (1*2) or 8 (4*2), then there are two 1s or 4s in
# the column
def two_in_row_detector(board_array):
    '''
    Output is a tuple which looks like (x, y, row, column).

    x is what type of two in a row it is. If it's a row, x=0 -- column = 1,
    diagonal L-R (down and right) = 2, diagonal R-L = 3

    y is which character has the two in a row. Noughts = 1, Crosses = 4

    Row/column is the free slot (i.e. 0 on the array)

    '''

    # finds the coordinate of the empty cell in a two-in-a-row
    def coord_finder(primary_axis):
        secondary_axis_count = 0
        for cell in primary_axis:
            if cell == 0:
                return secondary_axis_count
            secondary_axis_count += 1

    # column two in a row
    col_count = 0
    for col in board_array.T:
        if np.sum(col) == 2 or np.sum(col) == 8:

            row = coord_finder(col)

            return (row, col_count)

        else:
            col_count += 1

    # row two in a row
    row_count = 0
    for row in board_array:
        if np.sum(row) == 2 or np.sum(row) == 8:

            col = coord_finder(row)
            return (row_count, col)

        else:
            row_count += 1

    # diagonal two in a row
    if (
        board_array[0][0] + board_array[1][1] + board_array[2][2] == 2 or
        board_array[0][0] + board_array[1][1] + board_array[2][2] == 8
    ):
        if board_array[0][0] == 0:
            return (0, 0)
        elif board_array[1][1] == 0:
            return (1, 1)
        else:
            return (2, 2)

    elif (
        board_array[0][2] + board_array[1][1] + board_array[2][0] == 2 or
        board_array[0][2] + board_array[1][1] + board_array[2][0] == 8
    ):
        if board_array[0][2] == 0:
            return (0, 2)
        elif board_array[1][1] == 0:
            return (1, 1)
        else:
            return (2, 0)

    return None


def ai_go(board_array, player_character):
    '''
    If there is a two in a row, the AI will place there. Either to block the
    player, or to win with a three in a row.

    Otherwise, the AI will choose a random point to put a mark in.
    '''

    coord = two_in_row_detector(board_array)
    if coord != None:
        update_array(
            board_array, coord, player_character, human=False
        )
    else:
        randomly_choosing = True

        while randomly_choosing:
            row = random.randint(0, 2)
            column = random.randint(0, 2)
            coord = (row, column)

            randomly_choosing = update_array(
                board_array, coord, player_character, human=False
            )


def three_in_row_detector(board_array):
    '''
    True if there is a three in a row, False if not. 
    '''

    # column three in a row
    count = 0
    for col in board_array.T:
        if np.sum(col) == 3:
            return True
        elif np.sum(col) == 12:
            return True
        else:
            count += 1

    # row three in a row
    count = 0
    for row in board_array:
        if np.sum(row) == 3:
            return True
        elif np.sum(row) == 12:
            return True
        else:
            count += 1

    # diagonal three in a row
    if (
        board_array[0][0] + board_array[1][1] + board_array[2][2] == 3 or
        board_array[0][0] + board_array[1][1] + board_array[2][2] == 12 or

        board_array[0][2] + board_array[1][1] + board_array[2][0] == 3 or
        board_array[0][2] + board_array[1][1] + board_array[2][0] == 12
    ):
        return True

    return False


def game_end_detector(board_array, player_character, player):
    '''Returns False if the game should stop, and True if it should continue'''
    game_end = three_in_row_detector(board_array)

    if np.sum(board_array) == 21:
        print("It's a draw.")
        return False

    if not game_end:
        return True
    else:
        if player:
            if player_character == 1:
                print("Noughts win! Congratulations!")
            else:
                print("Crosses win! Congratulations!")
        else:
            if player_character == 1:
                print("Sorry, Crosses win.")
            else:
                print("Sorry, Noughts win.")
        return False


game_on = True

print("Welcome to Noughts and Crosses!")

while game_on:

    board_array = np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])

    player_character = noughts_or_crosses()

    game_running = True

    if player_character == 4:
        ai_go(board_array, player_character)
    else:
        print_array(board_array)

    while game_running:

        human_cell_chooser(board_array, player_character)
        game_running = game_end_detector(
            board_array, player_character, player=True)

        if game_running:
            ai_go(board_array, player_character)
            game_running = game_end_detector(
                board_array, player_character, player=False)

    valid_response = False
    while not valid_response:
        play_again = input("Do you want to play again? y/n\n> ")
        if play_again == "y":
            game_on = True
            valid_response = True
        elif play_again == "n":
            print("Thank you for playing!")
            game_on = False
            valid_response = True
        else:
            valid_response = False
