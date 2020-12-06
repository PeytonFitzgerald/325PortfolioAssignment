import pygame, sys
from pygame.locals import *
from random import randint, shuffle
import numpy as np



pygame.init()
#win = pygame.display.set_mode((500,500))
#pygame.display.set_caption("Test")
GAMECLOCK = pygame.time.Clock()
# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (200,200,200)

# Game Window Display Dimensions
WIDTH = 540
HEIGHT = 540
WINDOW_SIZE = (WIDTH, HEIGHT)
SECTION_SIZE = 180
CELL_SIZE = 60


class Board:
    def __init__(self):
        self.__game_board = self.generate_board()
        
    def generate_board(self):
        """Generates a valid 9x9 sudoku board, and then removes values from it to make sure its ready to play.
         
        Returns:
            No return - stored in self.__game_board
        """        
        board_not_ready = True
        # temp generation of board
        board = [[' ' for _ in range(9)] for _ in range(9)]
        board_size = 81
        numbers =[1,2,3,4,5,6,7,8,9]
        square_dict = {
            # top squares
            'square1': [board[n][0:3] for n in range(0,3)],
            'square2': [board[n][3:6] for n in range(0,3)],
            'square3': [board[n][6:9] for n in range(0,3)],
            # middle squares
            'square4': [board[n][0:3] for n in range(3,6)],
            'square5': [board[n][3:6] for n in range(3,6)],
            'square6': [board[n][6:9] for n in range(3,6)],
            # bottom squares
            'square7': [board[n][0:3] for n in range(6,9)],
            'square8': [board[n][3:6] for n in range(6,9)],
            'square9': [board[n][6:9] for n in range(6,9)]
        }
        while board_not_ready:
            # loop through each cell in the board to give it a value
            for cell in range(0,81):
                # assing appropriate row and col for this cell's iteration
                row=cell//9
                col=cell%9
                
                # make sure it's empty 
                if board[row][col] == ' ':
                    shuffle(numbers)
                    # look through each of the potential numbers, select one that's not in..
                    for number in numbers:
                        # this row...
                        print("number is + " + str(number) + " and its row is " + str(row) + " and its row contents are the following:")
                        print(board[row])
                        if number not in board[row]:
                            # or this column...
                            for x in range(0,9):
                                if number != board[x][col]:
                                    
                                    
                            # one of the three left squares       
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
                            if number not in square:
                                board[row][col] = number
                                        
                                """
                                    if col < 3:
                                        cur_square = [board[cell][0:3]]
                                    elif col < 6:
                                        cur_square = [board[cell][3:6] for cell in range(0,3)]
                                    else:
                                        cur_square = [board[cell][6:9]]
                                """
                                
                                
                                
            
            if self.verify_solution(board) and (' ' not in board):
                print("board legit")
                board_not_ready = False
                return board 
            else("board is not legit, trying again")
            
        
    
    def get_board(self):
        return self.__game_board
    
    def verify_board_state(self):
        pass
    
    def verify_solution(self, board):
        valid = True
        
        if valid:
            return valid
        else:
            return not valid
        
            
    
class Game:
    def __init__(self):
        self.__window = pygame.display.set_mode(WINDOW_SIZE)
        self.__board = Board()
        
    def draw_grid_lines(self, window):
        for small_x_line in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(window, GREY, (small_x_line,0), (small_x_line,HEIGHT))
        for small_y_line in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(window, GREY, (0,small_y_line), (WIDTH, small_y_line))
            
        for big_x_line in range(0, WIDTH, SECTION_SIZE):
            pygame.draw.line(window, BLACK, (big_x_line,0), (big_x_line,HEIGHT))
        for big_y_line in range(0, HEIGHT, SECTION_SIZE):
            pygame.draw.line(window, BLACK, (0,big_y_line), (WIDTH, big_y_line))
        return None
        
    def get_current_window(self):
        return self.__window
        
    def print_board(self):
        print(np.matrix(self.__board.get_board()))
        
    def play_game(self):
        pygame.display.set_caption("Sudoku Game")
        window = self.get_current_window()
        window.fill(WHITE)
        self.draw_grid_lines(window)
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass
            pygame.display.update()
            GAMECLOCK.tick(10)
    
    def user_actions(self):
        pass
    
def main():
    game_window = Game()
    game_window.print_board()
    game_window.play_game()
    
if __name__ == "__main__":
    main()




