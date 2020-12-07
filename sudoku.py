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

    def get_squares(self, board):
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
        return self.__game_board

    def get_reference_board(self):
        return self.__reference_board

    def get_playing_board(self):
        return self.__playable_game_board

    def generate_board(self):
        self.fill_board(self.__game_board)
        # print(np.matrix(self.__game_board))
        self.remove_numbers('Easy')
        self.__reference_board = copy.deepcopy(self.__playable_game_board)
        # print("now it's ready for play")
        # print(np.matrix(self.__playable_game_board))
        return None

    def fill_board(self, board):
        """
        Attempts to fill a sudoku board. If possible, returns true and the board is 'solved'. If not possible,
        returns false.
        :param board:
        :return:
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
                        if self.is_board_full():
                            if self.fill_board(board):
                                return True
                        else:
                            return True
                break
        board[row][col] = ' '
        return False

    def remove_numbers(self, difficulty='Easy'):
        self.__playable_game_board = copy.deepcopy(self.__game_board)
        board = self.__playable_game_board
        if difficulty == 'Easy':
            empty_size = 25
        elif difficulty == 'Medium':
            empty_size = 35
        else:
            empty_size = 40
        while empty_size > 0:
            random_row = randint(0, 8)
            random_column = randint(0, 8)
            board[random_row][random_column] = ' '
            empty_size -= 1
        return None

    def is_board_full(self):
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
        if self.row_check(num, row, board) and self.column_check(num, col, board):
            square_list = self.get_squares(board)
            if self.square_check(num, row, col, square_list):
                return True
        return False

    def row_check(self, num, row, board):
        if num in board[row]:
            return False
        return True

    def column_check(self, num, col, board):
        for x in range(9):
            if num == board[x][col]:
                return False
        return True

    def square_check(self, number, row, col, square_dict):
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





    def get_board_state(self, num, row, col, arg_board):
        board = copy.deepcopy(arg_board)
        board[row][col] = num
        if self.fill_board(board):
                return True
        else:
            return False

class Game:
    def __init__(self):
        self.__window = pygame.display.set_mode(WINDOW_SIZE)
        self.__board = Board()
        self.__playing_board = []
        self.__reference_board = []
        self.__win_state = False

    def set_win_state(self, state):
        self.__win_state = state

    def set_playing_board(self, board):
        self.__playing_board = board
        return

    def set_reference_board(self, board):
        self.__reference_board = board
        return

    def get_current_window(self):
        return self.__window

    def print_board(self):
        print(np.matrix(self.__playing_board))
        return None


    def draw_grid_lines(self, window):
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
        cellValue = CELLFONT.render('%s' % (number), True, color)
        rect = cellValue.get_rect()
        rect.topleft = (y_cord, x_cord)
        self.__window.blit(cellValue, rect)
        return None

    def enter_number(self, number, y_cord, x_cord):
        x = int(x_cord / CELL_SIZE)
        y = int(y_cord / CELL_SIZE)
        reference_board = self.__reference_board
        board = self.__playing_board
        if (reference_board[x][y] == ' ') and self.__board.is_valid_placement(x, y, number, board):
            if self.__board.get_board_state(number, x, y, board):
                finished = True
                board[x][y] = number
                for row in range(9):
                    for col in range(9):
                        if board[row][col] == ' ':
                            finished = False
                if finished:
                    print("board full")
        return None


    def select_cell(self, x, y):
        cell_x = ((x * 9) / WIDTH) * CELL_SIZE
        cell_y = ((y * 9) / HEIGHT) * CELL_SIZE
        pygame.draw.rect(self.__window, BLUE, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 5)
        return None

    def refresh_screen(self):
        window = self.get_current_window()
        window.fill(WHITE)
        self.fill_grid()
        self.draw_grid_lines(window)
        return None

    def play_game(self):
        self.__board.generate_board()
        pygame.display.set_caption("Sudoku Game")
        window = self.get_current_window()
        self.set_playing_board(self.__board.get_playing_board())
        self.set_reference_board(self.__board.get_reference_board())
        self.print_board()

        current_selection = [0, 0]
        window.fill(WHITE)
        self.fill_grid()
        self.draw_grid_lines(window)
        self.select_cell(0, 0)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


                key_pressed = pygame.key.get_pressed()
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

                elif key_pressed[pygame.K_3]:
                    self.refresh_screen()
                    self.enter_number(3, current_selection[0], current_selection[1])
                    self.select_cell(current_selection[0], current_selection[1])

                elif key_pressed[pygame.K_4]:
                    self.refresh_screen()
                    self.enter_number(4, current_selection[0], current_selection[1])
                    self.select_cell(current_selection[0], current_selection[1])

                elif key_pressed[pygame.K_5]:
                    self.refresh_screen()
                    self.enter_number(5, current_selection[0], current_selection[1])
                    self.select_cell(current_selection[0], current_selection[1])

                elif key_pressed[pygame.K_6]:
                    self.refresh_screen()
                    self.enter_number(6, current_selection[0], current_selection[1])
                    self.select_cell(current_selection[0], current_selection[1])

                elif key_pressed[pygame.K_7]:
                    self.refresh_screen()
                    self.enter_number(7, current_selection[0], current_selection[1])
                    self.select_cell(current_selection[0], current_selection[1])

                elif key_pressed[pygame.K_8]:
                    self.refresh_screen()
                    self.enter_number(8, current_selection[0], current_selection[1])
                    self.select_cell(current_selection[0], current_selection[1])

                elif key_pressed[pygame.K_9]:
                    self.refresh_screen()
                    self.enter_number(9, current_selection[0], current_selection[1])
                    self.select_cell(current_selection[0], current_selection[1])

                # if key_pressed[pygame.K_RETURN]:
                # print("enter pressed")

            pygame.display.update()
            GAMECLOCK.tick(300)

    def user_actions(self):
        pass


def main():
    game = Game()
    game.play_game()


if __name__ == "__main__":
    main()




