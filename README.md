$ python3 sudoku.py
    1. **YOU WILL NEED TO INSTALL PYGAME AND ANACONDA (NUMPY AND OTHERS) TO RUN THIS ON YOUR MACHINE**

        - If running anaconda, this is as simple as running the anaconda terminal and typing
            pip install pygame

        - Otherwise, check the following resources:
            https://www.pygame.org/wiki/GettingStarted
            You can also look at the repl.it host at https://repl.it/@PeytonFitzgeral/325Portfolio#main.py
            However, it was often buggy for me on this website and often wouldn't start/register keyboard inputs
            properly when moving around the grid. If using replit, you'll need to play around with the pygame window
            size to actually work within the browser. Sometimes replit makes it too small.

    2. Run the game by typing "python3 sudoku.py" or "python sudoku.py" in the terminal, or by
       opening it and running via an IDE.

    3. The game begins with terminal input prompts. You will be asked to select a difficulty. Enter
       '0' for super easy, '1' for easy, '2' for intermediate, and '3' for hard. After making this selection,
       a pygame window will open (sometimes you need to look for it on your taskbar at the bottom of the screen.)


    4. A pygame window will open up that allows you to play the game. To navigate the sudoku grid,
       use your arrow keys ('Up' key to move up, 'Down' key to move down, 'Left' key to move left, and
       'Right' key to move right. When you want to enter a number into an empty cell, simply press that number
       on your keyboard. Numbers that you have entered are colored blue, numbers that were present originally are colored black.


    5.  ************IMPORTANT******
       To erase a blue number, simply select its cell and then press 'escape'.

       To exit a game, simply press 'X' in the top right corner of the screen (or close repl.it tab.)

       To instantly solve a game,  press 'S' to view the solved board, and then 'enter' to start a new game.
                *************VERY IMPORTANT LIMITATION DISCLAIMER***************
                If a solution wasn't possible given your inputs at the time of cheating, the cells will not fill in
                and you won't be able to delete or enter new numbers.

       After winning (or cheating), you will be shown a victory screen. Press enter to play again with the same difficulty,
       or use '1' '2' '3' or '4' to select one of the difficulties described on screen/in the beginning on the terminal.


       Press enter to proceed to the victory screen and then reset.