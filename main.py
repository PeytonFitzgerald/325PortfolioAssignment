from random import randint, shuffle
import numpy as np

def create_board(num):
    board = [['' for _ in range(num)] for _ in range(num)]
    print(np.matrix(board))
    board_size = num^2
    num_options = []

    for opt in range(0,num):
        num_options.append(opt)
    options_size = len(num_options)
    for n in range(0,num^2):
        x = n//options_size
        y = n%options_size
        if board[x][y]=='':
            for opt in num_options:
                
        
    
    # board = [[random.random() for i in range(sudoku_number)] for j in range(sudoku_number)]
    return board
    # [[0 for x in range(maxCap+1)] for _ in range(num_items+1)]
def main():
    sudo_size = int(input("Enter the N dimension for the sudoko board (e.g., \"9\" for a 9x9 board): "))
    game_board = create_board(sudo_size)
    
 


if __name__ == "__main__":
    main()