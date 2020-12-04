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
        board_not_ready = True
        # temp generation of board
        board = [[' ' for _ in range(9)] for _ in range(9)]
        board_size = 81
        numbers =[1,2,3,4,5,6,7,8,9]

        while board_not_ready:
            for cell in range(0,81):
                row=cell//9
                col=cell%9
                if board[row][col] == ' ':
                    shuffle(numberList)
                    for number in numbers:
                        if number not in board[row]:
                            if number not in board[col]:
                                
            
            if self.verify_solution(board):
                board_not_ready = False
                
        return board
    
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
        print(self.__board.get_board())
        
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
    game_window.play_game()
    
if __name__ == "__main__":
    main()




