import pygame, sys
from pygame.locals import *
from random import randint, shuffle
import numpy as np
import copy

pygame.init()
# win = pygame.display.set_mode((500,500))
# pygame.display.set_caption("Test")
GAMECLOCK = pygame.time.Clock()
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
BLUE = (0, 0, 240)

# Fonts
CELLFONT = pygame.font.Font('freesansbold.ttf', 55)

SCALE = 5
BASE_SIZE = 81
WIDTH = int(BASE_SIZE * SCALE)
HEIGHT = int(BASE_SIZE * SCALE)
WINDOW_SIZE = (WIDTH, HEIGHT)
SECTION_SIZE = int((BASE_SIZE * SCALE) / 3)
CELL_SIZE = int(SECTION_SIZE / 3)

# Old Window Display Dimensions
"""
WIDTH = 540
HEIGHT = 540
MARGIN = 30
WINDOW_SIZE = (WIDTH, HEIGHT)
SECTION_SIZE = 180
CELL_SIZE = 60

"""


class Board:
    def __init__(self):
        self.__game_board = [[' ' for _ in range(9)] for _ in range(9)]
        self.__reference_board = []
        self.__playable_game_board = []
        self.__square_dict = {}
        self.__solution_count = 0


    def get_squares(self, board):
        """
        Given a 9x9 board, returns the squares for that board.
        :param board: 9x9 Sudoku board
        :return: Dict of squares for a 9x9 sudoku board
        """
        # simply use list comprehension to build dict values for 3x3 grids. (9 in total)
        square_dict = {
            # top squares
            'square1': [board[n][0:3] for n in range(0, 3)],
            'square2': [board[n][3:6] for n in range(0, 3)],
            'square3': [board[n][6:9] for n in range(0, 3)],
            # middle squares
            'square4': [board[n][0:3] for n in range(3, 6)],
            'square5': [board[n][3:6] for n in range(3, 6)],
            'square6': [board[n][6:9] for n in range(3, 6)],
            # bottom squares
            'square7': [board[n][0:3] for n in range(6, 9)],
            'square8': [board[n][3:6] for n in range(6, 9)],
            'square9': [board[n][6:9] for n in range(6, 9)]
        }
        return square_dict

    def get_board(self):
        """
        Returns the base game board for a given Board instance (no values removed)
        :return: Filled out board for game
        """
        return self.__game_board

    def get_reference_board(self):
        """
        When playing a game, returns the reference board for that game (values removed, no user input)
        :return: Reference board for game
        """
        return self.__reference_board

    def get_playing_board(self):
        """
        While playing a game, returns the current board being played on (values removed + user input)
        :return: Board in play for game
        """
        return self.__playable_game_board

    def generate_board(self, difficulty):
        """
        Creates a solved 9x9 sudoku board and stores it as the base game board, removes a number of values from the board
        and uses the resulting board as the reference/playing boards
        :return:
        """
        self.__game_board = [[' ' for _ in range(9)] for _ in range(9)]
        self.fill_board(self.__game_board)
        # print(np.matrix(self.__game_board))
        self.remove_numbers(difficulty)
        self.__reference_board = copy.deepcopy(self.__playable_game_board)
        # print("now it's ready for play")
        # print(np.matrix(self.__playable_game_board))
        return None

    def fill_board(self, board):
        """
        Recursively attempts to solve a given board (if board is empty, builds out a filled solution.
        If possible, returns true and the board is 'solved'. If not possible,
        returns false.
        :param board: board to be filled
        :return: No return
        """
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # for each cell in the grid
        for cell in range(0, 81):
            # set appropriate row and col
            row = cell // 9
            col = cell % 9
            # if that cell is empty
            if board[row][col] == ' ':
                # shuffle numbers
                shuffle(numbers)
                for number in numbers:
                    # iterate through our numbers until we find one that is valid
                    if self.is_valid_placement(row, col, number, board):
                        # if valid place it there
                        board[row][col] = number
                        # while there are empty cells left
                        if self.next_empty():
                            # recursively call and fill
                            if self.fill_board(board):
                                # if fillable on that recursive path, return true
                                return True
                        else:
                            # base case - no more empty cells after this
                            return True
                break
        board[row][col] = ' '
        # not fillable, we return false
        return False

    def solver(self, board):
        """
        Recursively attempts to solve a given board (if board is empty, builds out a filled solution.
        If possible, returns true and the board is 'solved'. If not possible,
        returns false.
        :param board: board to be filled
        :return: No return
        """
        # same as above, just with a counter. For some reason, whenever I included
        # self__solution_count += 1 in the above, it didn't work. I have no idea why.
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for cell in range(0, 81):
            row = cell // 9
            col = cell % 9
            if board[row][col] == ' ':
                for number in numbers:
                    if self.is_valid_placement(row, col, number, board):
                        board[row][col] = number

                        if self.next_empty(board):
                            if self.solver(board):
                                return True
                        else:
                            self.__solution_count += 1
                            return True
                break
        board[row][col] = ' '
        return False

    def solve_outside_board(self, board):
        """
        Takes a 9x9 sudoku board as input and r uns it through the solver member function
        :param board: board to be solved
        :return: Solved board
        """
        self.solver(board)
        return board

    def remove_numbers(self, difficulty):
        """
        Removes values from a solved sudoku board.
        :param difficulty:
        :return:
        """
        self.__playable_game_board = copy.deepcopy(self.__game_board)
        empty_num = 0
        board = self.__playable_game_board
        if difficulty == 1:
            empty_size = 32
        elif difficulty == 2:
            empty_size = 42
        elif difficulty == 3:
            empty_size = 50
        else:
            empty_size = 20
        while empty_size > 0:
            random_row = randint(0, 8)
            random_column = randint(0, 8)
            other_row = int(8-random_row)
            other_column = int(8-random_column)
            # make a test board copy
            test_board = copy.deepcopy(board)
            # remove value at random row and column. In addition, if parallel value on the opposite side of the board
            # is still active, remove that one as well.
            if test_board[random_row][random_column] != ' ':
                test_board[random_row][random_column] = ' '
                self.__solution_count = 0
                self.solver(test_board)
                # if, after running solver, there is only one solution found
                # we are safe to remove that value. Otherwise, check next value
                if self.__solution_count == 1:
                    board[random_row][random_column] = ' '
                    empty_size -= 1
            # make another test board copy
            test_board = copy.deepcopy(board)
            if test_board[other_row][other_column] != ' ':
                test_board[other_row][other_column] = ' '
                self.__solution_count = 0
                self.solver(test_board)
                # if, after running solver, there is only one solution found
                # we are safe to remove that value. Otherwise, check next value
                if self.__solution_count == 1:
                    board[other_row][other_column] = ' '
                    empty_size -= 1
                    empty_num += 1
        return None

    def next_empty(self, board=None):
        """
        Check for recursive function. Returns coords or None depending on state of board.
        :return: None if no empty values remain, otherwise the coords of an empty cell/True
        """
        if board is None:
            board = self.get_board()
        coords = []
        for row in range(9):
            for column in range(9):
                if board[row][column] == ' ':
                    coords.append(row)
                    coords.append(column)
                    return coords
        return

    def is_valid_placement(self, row, col, num, board):
        """
        Checks to see if it would be valid to place a given num in a given row/col of a board.
        Calls row_check, column_check, and square_check
        :param row: row coordinate of the cell to potentially enter the number
        :param col: col coordinate of the cell to potentially enter the number
        :param num: number to be potentially entered
        :param board: board that the number will be entered on
        :return:
        """
        if self.row_check(num, row, board) and self.column_check(num, col, board):
            # get the square list dictionary for use in the square validity check
            square_list = self.get_squares(board)
            if self.square_check(num, row, col, square_list):
                return True
        return False

    def row_check(self, num, row, board):
        """
        Checks to see if a number is valid for that row.
        :param num: Number to be entered
        :param row: Row that the number would be entered on
        :param board: Board that the row exists on
        :return: True if its valid, otherwise False.
        """
        # if its in the row, return false
        if num in board[row]:
            return False
        return True

    def column_check(self, num, col, board):
        """
        Checks to see if a number is valid for that column
        :param num: Number to be entered
        :param col: Column that the number would be entered in
        :param board: Board that the column exists on
        :return: True if its valid, otherwise False.
        """
        for x in range(9):
            if num == board[x][col]:
                return False
        return True

    def square_check(self, number, row, col, square_dict):
        """
        Checks to see if a number is valid for its square.
        :param number: Number to be entered
        :param row: Row coordinate of the cell the number would be entered in
        :param col: Column coordinate of the cell the number would be entered in
        :param square_dict: Dictionary of squares for a given board
        :return: True if its valid for the square, otherwise False.
        """
        if col < 3:
            if row < 3:
                square = square_dict['square1']
            elif row < 6:
                square = square_dict['square4']
            else:
                square = square_dict['square7']
            # one of the middle three squares
        elif col < 6:
            if row < 3:
                square = square_dict['square2']
            elif row < 6:
                square = square_dict['square5']
            else:
                square = square_dict['square8']
            # one of the right three squares
        else:
            if row < 3:
                square = square_dict['square3']
            elif row < 6:
                square = square_dict['square6']
            else:
                square = square_dict['square9']
        if number in (square[0] + square[1] + square[2]):
            return False
        else:
            return True


class Game:
    def __init__(self):
        self.__window = pygame.display.set_mode(WINDOW_SIZE)
        self.__board = Board()
        self.__playing_board = []
        self.__reference_board = []
        self.__difficulty = 1
        self.__win_state = False
        self.__cheated = False
        self.__win_image = pygame.image.load("win.png")

    def set_win_state(self, state):
        """
        Sets the win state for a given game
        :param state:
        :return: None
        """
        self.__win_state = state

    def set_difficulty(self, difficulty):
        self.__difficulty = difficulty

    def set_playing_board(self, board):
        """
        Sets the playing board for a given game (which the user actually enters values in)
        :param board: board to use as a basis for creation of the playing board
        :return: None
        """
        self.__playing_board = board
        return

    def set_reference_board(self, board):
        """
        Sets the reference board for a given game - copy of the playing board before any inputs are made.
        :param board: Board to use as a basis for creation of the reference board.
        :return: None
        """
        self.__reference_board = board
        return

    def get_current_window(self):
        """
        Gets the current window being used by pygame to display the sudoku game.
        :return: Current pygame window
        """
        return self.__window

    def print_board(self):
        """
        Uses np.matrix to print out the playing board in the console
        :return: None - prints to console
        """
        print(np.matrix(self.__playing_board))
        return None

    def draw_grid_lines(self, window):
        """
        Draws a 9x9 grid unto a pygame window
        :param window: Current pygame window
        :return: None
        """
        # 1x1 Cell grid lines
        for small_x_line in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(window, GREY, (small_x_line, 0), (small_x_line, HEIGHT))
        for small_y_line in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(window, GREY, (0, small_y_line), (WIDTH, small_y_line))

        # 3x3 square grid lines
        for big_x_line in range(0, WIDTH, SECTION_SIZE):
            pygame.draw.line(window, BLACK, (big_x_line, 0), (big_x_line, HEIGHT))
        for big_y_line in range(0, HEIGHT, SECTION_SIZE):
            pygame.draw.line(window, BLACK, (0, big_y_line), (WIDTH, big_y_line))
        return None

    def fill_grid(self):
        """
        Draws onto the current pygame window the contents of the game's current playing board
        :return:None
        """
        board = self.__playing_board
        for x in range(9):
            for y in range(9):
                cell_val = board[x][y]
                if board[x][y] == self.__reference_board[x][y]:
                    # color clues black
                    color = BLACK
                else:
                    # color user inputs blue
                    color = BLUE
                if cell_val != ' ':
                    self.fill_cell(cell_val, (x * CELL_SIZE), (y * CELL_SIZE), color)
                    pygame.display.update()

    def fill_cell(self, number, x_cord, y_cord, color):
        """

        :param number: Number to be entered into a cell
        :param x_cord: x coordinate in the window where the number should be drawn
        :param y_cord: y coordinate in the window where the number should be drawn
        :param color: Color that the number should be drawn with
        :return: None
        """
        # use x_cord and y_cord as reference to the location on the screen a given
        # cell is being rendered. Then, render that cell value appropriately on the window
        cellValue = CELLFONT.render('%s' % (number), True, color)
        rect = cellValue.get_rect()
        rect.topleft = (y_cord, x_cord)
        self.__window.blit(cellValue, rect)
        return None

    def clear_number(self, y_cord, x_cord):
        """
        Clears a number from a given location in the window (essentailly makes a given cell in the grid white)
        :param y_cord:
        :param x_cord:
        :return:
        """
        # divide the x/y coordinates that were passed by cell_size to get the actual row/column for indexing the
        # playing board array
        x = int(x_cord / CELL_SIZE)
        y = int(y_cord / CELL_SIZE)
        if self.__reference_board[x][y] == ' ':
            # only clear numbers that the user has entered, not clues
            board = self.__playing_board
            board[x][y] = ' '


    def enter_number(self, number, y_cord, x_cord):
        """
        Given a number, adds it to the current playing board if it is valid to place it in the given locaiton
        :param number: Number to be entered onto the board
        :param y_cord: y coordinate of the number to be entered on the board (coordinate in the game window)
        :param x_cord: x coordinate of the number to be entered on the board (coordinate in the game window)
        :return: None
        """
        x = int(x_cord / CELL_SIZE)
        y = int(y_cord / CELL_SIZE)
        reference_board = self.__reference_board
        board = self.__playing_board
        if (reference_board[x][y] == ' ') and self.__board.is_valid_placement(x, y, number, board):
            # if self.__board.is_valid_placement(number, x, y, board):
            if 1 == 1:
                finished = True
                board[x][y] = number
                for row in range(9):
                    for col in range(9):
                        if board[row][col] == ' ':
                            finished = False
                if finished:
                    self.set_win_state(True)
                    print("You Won! Board is solved.")
        return None


    def select_cell(self, x, y):
        """
        Draws a rectangle around a given that the user is currently selecting in the window
        :param x: x coordinate in the window of the cell to be selected
        :param y: y coordinate in the window of the cell to be selected
        :return: None
        """
        cell_x = ((x * 9) / WIDTH) * CELL_SIZE
        cell_y = ((y * 9) / HEIGHT) * CELL_SIZE
        pygame.draw.rect(self.__window, BLUE, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 5)
        return None

    def cheat(self):
        """"""
        """Calls on the Board class's fill method to instantly fill a given board"""
        pygame.time.delay(1000)
        self.__board.solve_outside_board(self.__playing_board)
        self.__cheated = True


    def refresh_screen(self):
        """
        Refereshes the content of the current game window. Fills it with white, fills the grid based on the game board,
        and draws grid lines.
        :return: None
        """
        window = self.get_current_window()
        window.fill(WHITE)
        self.fill_grid()
        self.draw_grid_lines(window)
        return None

    def display_victory(self):
        """
        Displays the victory image on the screen
        """
        window = self.get_current_window()
        window.fill(WHITE)
        self.__window.blit(self.__win_image, (WIDTH*.15, HEIGHT*.005))

    def new_game(self):
        """
        Starts a new game. Creates a new board based on the game object's current difficulty.
        """
        self.__board.generate_board(self.__difficulty)
        self.set_playing_board(self.__board.get_playing_board())
        self.set_reference_board(self.__board.get_reference_board())

    def play_game(self):
        """
        Playing method of the game class. Contains the pygame code to actually run the game / refresh screen / update
        board based on user inputs
        :return: None
        """
        self.new_game()
        pygame.display.set_caption("Sudoku Game")
        window = self.get_current_window()

        self.refresh_screen()

        current_selection = [0, 0]
        self.select_cell(0, 0)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


                key_pressed = pygame.key.get_pressed()

                if self.__cheated:
                    if key_pressed[pygame.K_RETURN]:
                        self.__cheated = False
                        self.__win_state = True

                elif self.__win_state:
                    self.display_victory()
                    # check for difficulty repeat
                    if key_pressed[pygame.K_RETURN]:
                        # screen to display if user has filled out the board. If they press enter, the game begins again
                        self.set_win_state(False)
                        self.new_game()
                        self.refresh_screen()
                        current_selection = [0, 0]

                    # check if user wants to try another difficulty
                    if key_pressed[pygame.K_0]:
                        self.set_difficulty(0)
                        self.set_win_state(False)
                        self.new_game()
                        self.refresh_screen()
                        current_selection = [0, 0]

                    if key_pressed[pygame.K_1]:
                        self.set_difficulty(1)
                        self.set_win_state(False)
                        self.new_game()
                        self.refresh_screen()
                        current_selection = [0, 0]

                    if key_pressed[pygame.K_2]:
                        self.set_difficulty(2)
                        self.set_win_state(False)
                        self.new_game()
                        self.refresh_screen()
                        current_selection = [0, 0]

                    if key_pressed[pygame.K_3]:
                        self.set_difficulty(3)
                        self.set_win_state(False)
                        self.new_game()
                        self.refresh_screen()
                        current_selection = [0, 0]



                else:

                    # ----------------------
                    # General movement keys. Moves the blue rectangle signifying the users selected cell based on
                    # the arrow key entered
                    # current_selection[0] is the x coord, current_selection[1] is the y coord
                    # ------------------------
                    if key_pressed[pygame.K_LEFT]:
                        movement = current_selection[0] - CELL_SIZE
                        if movement < 0:
                            pass
                        else:
                            current_selection[0] = movement
                        self.refresh_screen()
                        self.select_cell(current_selection[0], current_selection[1])

                    if key_pressed[pygame.K_RIGHT]:
                        movement = current_selection[0] + CELL_SIZE
                        if movement > (WIDTH - CELL_SIZE):
                            pass
                        else:
                            current_selection[0] = movement
                        self.refresh_screen()
                        self.select_cell(current_selection[0], current_selection[1])

                    elif key_pressed[pygame.K_UP]:
                        movement = current_selection[1] - CELL_SIZE
                        if movement < 0:
                            pass
                        else:
                            current_selection[1] = movement
                        self.refresh_screen()
                        self.select_cell(current_selection[0], current_selection[1])

                    elif key_pressed[pygame.K_DOWN]:
                        movement = current_selection[1] + CELL_SIZE
                        if movement > (HEIGHT - CELL_SIZE):
                            pass
                        else:
                            current_selection[1] = movement
                        self.refresh_screen()
                        self.select_cell(current_selection[0], current_selection[1])

                    # -------------
                    # For each of the below, if a number is entered, update the game's board to reflect it's been
                    # entered if it was valid, and then refresh the screen accordingly
                    # -------------

                     # if '1' pressed
                    elif key_pressed[pygame.K_1]:
                        self.refresh_screen()
                        self.enter_number(1, current_selection[0], current_selection[1])
                        self.select_cell(current_selection[0], current_selection[1])

                    # if '2' pressed
                    elif key_pressed[pygame.K_2]:
                        self.refresh_screen()
                        self.enter_number(2, current_selection[0], current_selection[1])
                        self.select_cell(current_selection[0], current_selection[1])

                    # if '3' pressed
                    elif key_pressed[pygame.K_3]:
                        self.refresh_screen()
                        self.enter_number(3, current_selection[0], current_selection[1])
                        self.select_cell(current_selection[0], current_selection[1])

                    # if '4' pressed
                    elif key_pressed[pygame.K_4]:
                        self.refresh_screen()
                        self.enter_number(4, current_selection[0], current_selection[1])
                        self.select_cell(current_selection[0], current_selection[1])

                    # if '5' pressed
                    elif key_pressed[pygame.K_5]:
                        self.refresh_screen()
                        self.enter_number(5, current_selection[0], current_selection[1])
                        self.select_cell(current_selection[0], current_selection[1])

                    # if '6' pressed
                    elif key_pressed[pygame.K_6]:
                        self.refresh_screen()
                        self.enter_number(6, current_selection[0], current_selection[1])
                        self.select_cell(current_selection[0], current_selection[1])

                    # if '7' pressed
                    elif key_pressed[pygame.K_7]:
                        self.refresh_screen()
                        self.enter_number(7, current_selection[0], current_selection[1])
                        self.select_cell(current_selection[0], current_selection[1])

                    # if '8' pressed
                    elif key_pressed[pygame.K_8]:
                        self.refresh_screen()
                        self.enter_number(8, current_selection[0], current_selection[1])
                        self.select_cell(current_selection[0], current_selection[1])

                    # if '9' pressed
                    elif key_pressed[pygame.K_9]:
                        self.refresh_screen()
                        self.enter_number(9, current_selection[0], current_selection[1])
                        self.select_cell(current_selection[0], current_selection[1])

                    # if 'Esc' pressed
                    elif key_pressed[pygame.K_ESCAPE]:
                        self.clear_number(current_selection[0], current_selection[1])
                        self.refresh_screen()
                        self.select_cell(current_selection[0], current_selection[1])
                    # if key_pressed[pygame.K_RETURN]:

                    elif key_pressed[pygame.K_s]:
                        self.cheat()
                        self.refresh_screen()
                        self.select_cell(current_selection[0], current_selection[1])
                        cheated = True

            pygame.display.update()
            GAMECLOCK.tick(60)


def main():
    difficulties = ['0', '1', '2', '3']
    difficulty = 1
    no_input = True
    while no_input:
        difficulty = input("What difficulty? Type 0 for super easy puzzles. Or, you can type 1 for easier puzzles, 2 for normal puzzles, or 3 for harder puzzles")
        if difficulty in difficulties:
            no_input = False
        else:
            print("Invalid input. Please enter either '0', '1', '2', or '3'")
            print('\n')
    difficulty = int(difficulty)
    print('\n')
    print('\n')
    print('\n')
    print('\n')
    print("Generating game, if the window doesn't pop up automatically please look at your task bar at the bottom of the screen")
    print('\n')
    print('Game Instructions (also in README)')
    print("Use arrow keys to move around the grid.")
    print("Type a number to enter a number into an empty grid cell")
    print("Clear a grid cell by pressing the escape key. NOTE: You cannot clear a cell with a black colored number")
    print("Press 'S' at any time to cheat and instantly solve the board.) Afterwards, press Enter at any time to see the win screen and then start a new game")
    game = Game()
    game.set_difficulty(difficulty)
    game.play_game()

if __name__ == "__main__":
    main()




