import numpy as np
import random

COLUMNS = ["a", "b", "c"]


# where the player decides if they want to be noughts or crosses
def noughts_or_crosses():
    '''
    The player decides if they're noughts or crosses if they're playing in
    multiplayer.
    '''

    VALID_NOUGHTS_ANSWERS = [
        "noughts", "naughts", "nought", "naught", "n", "o", "0"
    ]
    VALID_CROSSES_ANSWERS = [
        "crosses", "cross", "cross's", "c", "x"
    ]

    o_or_x_input = input(
        "\n"
        "Do you want to be noughts or crosses?\n"
        "Noughts goes first.\n"
        "> "
    ).lower()

    if o_or_x_input in VALID_NOUGHTS_ANSWERS:
        nought_or_cross = 1
    elif o_or_x_input in VALID_CROSSES_ANSWERS:
        nought_or_cross = 4
    else:
        print("Please enter a valid input")
        return noughts_or_crosses()
    return nought_or_cross


# prints the contents of the array as text-format
def print_array(board_array):
    '''
    Turns the array into a printable board format that is seen by the player.
    '''

    # board templates
    TOP_BOTTOM_ROW = "       |     |     "
    MID_ROW = "  _____|_____|_____\n       |     |     "
    CELL_BASE = "  -  "  # the "-" is replaced depending on symbol

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
            cell = CELL_BASE.replace("-", " ")
        elif board_array[row][column] == 1:
            cell = CELL_BASE.replace("-", "O")
        else:
            cell = CELL_BASE.replace("-", "X")

        final_cell_list.append(cell)

    #  assembling the printable board
    board_print = (
        f"    a     b     c  "
        f"\n{TOP_BOTTOM_ROW}\n"
        f"1 {final_cell_list[0]}|{final_cell_list[1]}|{final_cell_list[2]}"
        f"\n{MID_ROW}\n"
        f"2 {final_cell_list[3]}|{final_cell_list[4]}|{final_cell_list[5]}"
        f"\n{MID_ROW}\n"
        f"3 {final_cell_list[6]}|{final_cell_list[7]}|{final_cell_list[8]}"
        f"\n{TOP_BOTTOM_ROW}"
    )
    print(board_print)


def human_cell_chooser(board_array, player_character):
    '''
    Turns the "b3" format of a user input into a coordinates tuple (1,2).
    It then calls the update array function to place the mark on the board.
    '''

    if player_character == 1:
        player_symbol = "NOUGHTS"
    else:
        player_symbol = "CROSSES"

    inputted_cell = input(
        f"{player_symbol}: which cell do you want to put your mark in? Example: b3\n> "
    ).lower()

    xn = inputted_cell.strip().lower()
    xn_split = [x for x in xn]

    if len(xn_split) > 2:  # seeing if user has inputted more than two characters
        return human_cell_chooser(
            input("Please input only two characters\n> ").lower()
        )

    column = xn_split[0]
    if column == "a":
        column = 0
    elif column == "b":
        column = 1
    elif column == "c":
        column = 2
    else:  # if first character is anything except a, b, or c
        return human_cell_chooser(
            input("Please input a valid column letter (a, b, c)\n> ").lower()
        )

    try:
        row = int(xn_split[1]) - 1
        if row > 2:  # seeing if number is below 3
            return human_cell_chooser(
                input("Please input a valid row number (1, 2, 3)\n> ").lower()
            )
    except ValueError:  # seeing if second character is a number
        return human_cell_chooser(
            input("Please input a valid row number (1, 2, 3)\n> ").lower()
        )

    coord = (row, column)

    update_array(board_array, coord, player_character, human=True)


# updates the controller array from input provided by the user
def update_array(board_array, coord, player_character, human=True):
    '''
    Updates the array. Based on either AI or human moves.
    '''

    if human:

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
    Output is a tuple of coordinates (row, column).

    This coordinate is the empty one in the row/column/diagonal that has two
    marks of the same type in it already.
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


def game_end_detector(board_array, player_character, player, multiplayer):
    '''
    Returns False if the game should stop, and True if it should continue
    This is decided on whether there is a three-in-a-row or draw or not.
    Different end-game messages depending on whether single or multiplayer.
    '''

    game_end = False

    # column three in a row
    count = 0
    for col in board_array.T:
        if np.sum(col) == 3 or np.sum(col) == 12:
            game_end = True
        else:
            count += 1

    # row three in a row
    count = 0
    for row in board_array:
        if np.sum(row) == 3 or np.sum(row) == 12:
            game_end = True
        else:
            count += 1

    # diagonal three in a row
    if (
        board_array[0][0] + board_array[1][1] + board_array[2][2] == 3 or
        board_array[0][0] + board_array[1][1] + board_array[2][2] == 12 or

        board_array[0][2] + board_array[1][1] + board_array[2][0] == 3 or
        board_array[0][2] + board_array[1][1] + board_array[2][0] == 12
    ):
        game_end = True

    if np.sum(board_array) == 21:
        print("It's a draw.")
        return False

    if not game_end:
        return True
    else:
        if multiplayer:
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
        else:
            if player_character == 1:
                print("Noughts win!")
            else:
                print("Crosses win!")


VALID_YES_ANSWERS = ["yes", "y", "ye", "yess"]
VALID_NO_ANSWERS = ["no", "n", "noo", ]
VALID_SP_ANSWERS = [
    "sp", "singleplayer", "single player", "single-player", "spp", "ssp",
    "sspp"
]
VALID_MP_ANSWERS = [
    "mp", "multiplayer", "multi player", "multi-player", "mpp", "mmp",
    "mmpp"
]


game_on = True

print("Welcome to Noughts and Crosses!")

valid_response = False
while not valid_response:
    single_or_multi = input(
        "Do you want to play in singleplayer or multiplayer? sp/mp\n> "
    ).lower()
    if single_or_multi in VALID_SP_ANSWERS:
        singleplayer = True
        valid_response = True
    elif single_or_multi in VALID_MP_ANSWERS:
        singleplayer = False
        valid_response = True
    else:
        print(single_or_multi)
    # else repeat loop


# SINGLEPLAYER
while game_on and singleplayer:

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
            board_array, player_character, player=True, multiplayer=True
        )

        if game_running:
            ai_go(board_array, player_character)
            game_running = game_end_detector(
                board_array, player_character, player=False, multiplayer=True
            )

    valid_response = False
    while not valid_response:
        play_again = input("Do you want to play again? y/n\n> ").lower()
        if play_again in VALID_YES_ANSWERS:
            game_on = True
            valid_response = True
        elif play_again in VALID_NO_ANSWERS:
            print("Thank you for playing!")
            game_on = False
            valid_response = True
        else:
            valid_response = False


# MULTIPLAYER
while game_on and not singleplayer:

    board_array = np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])

    game_running = True

    while game_running:

        human_cell_chooser(board_array, player_character=1)
        game_running = game_end_detector(
            board_array, player_character=1, player=True, multiplayer=False
        )

        if game_running:
            human_cell_chooser(board_array, player_character=4)
            game_running = game_end_detector(
                board_array, player_character=4, player=True,
                multiplayer=False
            )

    valid_response = False
    while not valid_response:
        play_again = input("Do you want to play again? y/n\n> ").lower()
        if play_again in VALID_YES_ANSWERS:
            game_on = True
            valid_response = True
        elif play_again in VALID_NO_ANSWERS:
            print("Thank you for playing!")
            game_on = False
            valid_response = True
        else:
            valid_response = False
