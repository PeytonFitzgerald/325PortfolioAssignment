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
        print(self.__game_board)
        self.__game_board = [[' ' for _ in range(9)] for _ in range(9)]
        print(self.__game_board)
        if difficulty == 1:
            difficulty = 'Easy'
        elif difficulty == 2:
            difficulty = 'Medium'
        else:
            difficulty = 'Hard'
        print(difficulty)
        self.fill_board(self.__game_board)
        print("above just filled")
        print(self.__game_board)
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
        for cell in range(0, 81):
            row = cell // 9
            col = cell % 9
            if board[row][col] == ' ':
                shuffle(numbers)
                for number in numbers:
                    if self.is_valid_placement(row, col, number, board):
                        board[row][col] = number
                        if self.next_empty():
                            if self.fill_board(board):
                                return True
                        else:
                            return True
                break
        board[row][col] = ' '
        return False

    def solver(self, board):
        """
        Recursively attempts to solve a given board (if board is empty, builds out a filled solution.
        If possible, returns true and the board is 'solved'. If not possible,
        returns false.
        :param board: board to be filled
        :return: No return
        """
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for cell in range(0, 81):
            row = cell // 9
            col = cell % 9
            if board[row][col] == ' ':
                for number in numbers:
                    if self.is_valid_placement(row, col, number, board):
                        board[row][col] = number

                        if self.next_empty():
                            if self.solver(board):
                                return True
                        else:
                            self.__solution_count += 1
                            return True
                break
        board[row][col] = ' '
        return False

    def remove_numbers(self, difficulty):
        """
        Removes values from a solved sudoku board.
        :param difficulty:
        :return:
        """
        self.__playable_game_board = copy.deepcopy(self.__game_board)
        print(self.__game_board)
        empty_num = 0
        board = self.__playable_game_board
        if difficulty == 'Easy':
            empty_size = 36
        elif difficulty == 'Medium':
            empty_size = 42
        else:
            empty_size = 46

        empty_size = 1
        while empty_size > 0:
            print(np.matrix(board))
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
                    print(empty_size)
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
        """
            if board[random_row][random_column] != ' ':
                board[random_row][random_column] = ' '
                if board[random_row][random_column] != ' ':
                    board[8 - random_row][8 - random_column] = ' '
                    empty_size -= 2
                else:
                    empty_size -= 1
        """
        return None

    def next_empty(self):
        """
        Check for recursive function. Returns coords or None depending on state of board.
        :return: None if no empty values remain, otherwise the coords of an empty cell/True
        """
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
        for small_x_line in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(window, GREY, (small_x_line, 0), (small_x_line, HEIGHT))
        for small_y_line in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(window, GREY, (0, small_y_line), (WIDTH, small_y_line))

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
                    color = BLACK
                else:
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
            print('1')
            # if self.__board.is_valid_placement(number, x, y, board):
            if 1 == 1:
                print('2')
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
        window = self.get_current_window()
        window.fill(BLUE)

    def new_game(self):
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
        #window = self.get_current_window()
        self.print_board()

        self.refresh_screen()

        current_selection = [0, 0]
        self.select_cell(0, 0)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


                key_pressed = pygame.key.get_pressed()

                if self.__win_state:
                    self.display_victory()
                    if key_pressed[pygame.K_RETURN]:
                        self.set_win_state(False)
                        self.new_game()
                        self.refresh_screen()
                else:

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

                    elif key_pressed[pygame.K_1]:
                        self.refresh_screen()
                        self.enter_number(1, current_selection[0], current_selection[1])
                        self.select_cell(current_selection[0], current_selection[1])

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
                    # print("enter pressed")

            pygame.display.update()
            GAMECLOCK.tick(60)


def main():
    difficulties = [1, 2, 3]
    difficulty = 1
    no_input = True
    while no_input:
        difficulty = int(input("What difficulty, type 1 for easy, 2 for medium, 3 for hard"))
        if difficulty in difficulties:
            no_input = False
        else:
            print("Invalid input. Please enter either '1', '2', or '3'")
            print('\n')
    game = Game()
    game.set_difficulty(difficulty)
    game.play_game()


if __name__ == "__main__":
    main()




