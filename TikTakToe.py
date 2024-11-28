# Copyright (C) Muhammad Essam Abelaziz | Saturday 28 October
#
# If you intend to use, modify, or redistribute this code for educational purposes, you are required to
# provide attribution by prominently displaying the following information in your project:
#
# Original code by Muhammad Essam Abdelaziz
# git@github.com:Coderation/Tic-Tac-Toe-Project-with-6-Uniform-Search-Methods-for-ILLUSTRATIVE-PURPOSES.git

#_________________________________________________________________________________________________________#

# These lines import the necessary modules to
# create the game interface, display messages, and use data structures for the AI algorithms.
import tkinter as tk
from tkinter import messagebox
import random
from collections import deque
from queue import PriorityQueue


# This defines the TicTacToe class, which represents the Tic-Tac-Toe game.
class TicTacToe:
    def __init__(self):
        # This creates a tkinter window with the title "Tic Tac Toe."
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        # The variable current_player keeps track of the current player (either 'X' or 'O'). 'X' starts the game.
        self.current_player = 'X'
        # board is a list that represents the game board. It's initialized with 9 spaces, one for each cell in the Tic-Tac-Toe grid.
        self.board = [' ' for _ in range(9)]
        # This creates a list of buttons, one for each cell in the Tic-Tac-Toe grid.
        # The buttons start with blank text and have the on_button_click function bound to them.
        self.buttons = [tk.Button(self.window, text=' ', font=('normal', 20), width=6, height=2,
                                 command=lambda i=i: self.on_button_click(i)) for i in range(9)]

        # ai_option is initialized to None and will store the chosen AI algorithm for the opponent.
        self.ai_option = None  # Stores the chosen AI algorithm

        # Add buttons for selecting AI options
        # ***
        # These buttons are for the user to choose which AI algorithm they want to play against.
        # Each button has a text label and a corresponding function to set the ai_option attribute.
        # ***
        self.bfs_button = tk.Button(self.window, text='Play against BFS AI', command=self.choose_bfs)
        self.dfs_button = tk.Button(self.window, text='Play against DFS AI', command=self.choose_dfs)
        self.bidirectional_button = tk.Button(self.window, text='Play against Bidirectional AI', command=self.choose_bidirectional)
        self.ucs_button = tk.Button(self.window, text='Play against UCS AI', command=self.choose_ucs)
        self.dls_button = tk.Button(self.window, text='Play against DLS AI', command=self.choose_dls)
        self.iddfs_button = tk.Button(self.window, text='Play against IDDFS AI', command=self.choose_iddfs)

        # This code organizes the buttons in a 3x3 grid layout, mimicking the Tic-Tac-Toe board.
        for button in self.buttons:
            button.grid(row=self.buttons.index(button) // 3, column=self.buttons.index(button) % 3)

        # These lines place the AI option buttons below the game board.
        self.bfs_button.grid(row=3, column=0)
        self.dfs_button.grid(row=3, column=1)
        self.bidirectional_button.grid(row=3, column=2)
        self.ucs_button.grid(row=4, column=0)
        self.dls_button.grid(row=4, column=1)
        self.iddfs_button.grid(row=4, column=2)
        
        # Initially, all the buttons (both game buttons and AI option buttons) are disabled.
        self.disable_buttons()

        # Initially, all the buttons (both game buttons and AI option buttons) are disabled.
        self.window.mainloop()

    # This 'on_button_click' function is called when a button on the Tic Tac Toe board is clicked.
    # The button is identified by its 'index'
    def on_button_click(self, index):
        # It first checks if the clicked cell on the board is empty (marked with a space character).
        if self.board[index] == ' ':
            # If the cell is empty, it updates the board with the current player's symbol (either 'X' or 'O')
            self.board[index] = self.current_player
            # Updates the text on the clicked button.
            self.buttons[index]['text'] = self.current_player
            # It then checks if the current player has won by calling the check_winner function, which will be explained later.
            if self.check_winner(self.current_player):
              # If the current player has won, it calls the end_game function with a message indicating the winner.
              self.end_game(self.current_player + " wins!")
              # If there is no winner and no empty cells left on the board, it's a draw, and it calls the end_game function with a draw message.
            elif ' ' not in self.board:
              self.end_game("It's a draw!")
            # If the game is not over,
            else:
                # it switches the current player from 'X' to 'O' or vice versa to allow the AI to make its move.
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                # If the current player is 'O' after the switch,
                if self.current_player == 'O':
                    #  it triggers the make_pc_move function for the AI to make its move.
                    self.make_pc_move()

    # All these functions below 'choose_searchalgorithmname'
    # simply sets the AI algorithm to be used and enable buttons to make selections for the AI's move
    def choose_bfs(self):
        self.ai_option = 'BFS'
        self.enable_buttons()

    def choose_dfs(self):
        self.ai_option = 'DFS'
        self.enable_buttons()

    def choose_bidirectional(self):
        self.ai_option = 'Bidirectional'
        self.enable_buttons()

    def choose_ucs(self):
        self.ai_option = 'UCS'
        self.enable_buttons()
    
    def choose_dls(self):
        self.ai_option = 'DLS'
        self.enable_buttons()

    def choose_iddfs(self):
        self.ai_option = 'IDDFS'
        self.enable_buttons()

    # This function is responsible for making the AI move based on the selected AI algorithm (self.ai_option)
    # It checks which AI algorithm is selected
    # ('BFS', 'DFS', 'Bidirectional', 'UCS', 'DLS', 'IDDFS') and calls the respective function to determine the best move for the AI.
    def make_pc_move(self):
        if self.ai_option == 'BFS':
            best_move = self.bfs()
        elif self.ai_option == 'DFS':
            best_move = self.dfs()
        elif self.ai_option == 'Bidirectional':
            best_move = self.bidirectional()
        elif self.ai_option == 'UCS':
            best_move = self.ucs()
        elif self.ai_option == 'DLS':
            best_move = self.dls()
        elif self.ai_option == 'IDDFS':
            best_move = self.iddfs()
        # If the AI option is not selected (None),
        # it raises a ValueError to indicate that the AI option should be chosen before the AI can make a move.
        else:
            raise ValueError("AI option not selected")
        # Finally, it triggers the 'on_button_click' function with the 'best_move',
        # causing the AI to make its move on the game board.
        self.on_button_click(best_move)

    # This function checks if a player (either 'X' or 'O') has won the game.
    def check_winner(self, player):
        # It defines the possible win combinations in a list called win_combinations,
        # where each combination is represented as a tuple of indices.
        win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        # It iterates through these win combinations and checks if all the cells in any of the combinations are marked with the given player symbol.
        # If so, it returns True, indicating a win.
        for combo in win_combinations:
            if all(self.board[i] == player for i in combo):
                return True
            # If no win combination is found, it returns False.
        return False

    # This function is called when the game is over, whether there is a winner or it's a draw.
    def end_game(self, result):
        for button in self.buttons:
            # It disables all the buttons on the game board by setting their state to tk.DISABLED, making them unclickable.
            button.config(state=tk.DISABLED)
        # It also disables the AI option selection buttons (bfs_button, dfs_button, etc.) to prevent further AI selections.
        self.bfs_button.config(state=tk.DISABLED)
        self.dfs_button.config(state=tk.DISABLED)
        self.bidirectional_button.config(state=tk.DISABLED)
        self.ucs_button.config(state=tk.DISABLED)
        self.dls_button.config(state=tk.DISABLED)
        self.iddfs_button.config(state=tk.DISABLED)
        # It displays a message box with information about the game result using tk.messagebox.showinfo, with the message specified in the result parameter.
        tk.messagebox.showinfo("Game Over", result)
        # Finally, it quits the game window using self.window.quit() to close the game.
        self.window.quit()

    # This function is responsible for enabling the game board buttons and disabling the AI option selection buttons.
    def enable_buttons(self):
        for button in self.buttons:
            # It iterates through all the buttons in self.buttons and sets their state to tk.NORMAL, making them clickable again
            button.config(state=tk.NORMAL)
        # It also disables the AI option selection buttons to prevent the player from selecting AI algorithms while the game is in progress.
        self.bfs_button.config(state=tk.DISABLED)
        self.dfs_button.config(state=tk.DISABLED)
        self.bidirectional_button.config(state=tk.DISABLED)
        self.ucs_button.config(state=tk.DISABLED)
        self.dls_button.config(state=tk.DISABLED)
        self.iddfs_button.config(state=tk.DISABLED)

    # This function is responsible for disabling the game board buttons and enabling the AI option selection buttons.
    def disable_buttons(self):
        # It iterates through all the buttons in self.buttons and sets their state to tk.DISABLED, making them unclickable.
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        # It enables the AI option selection buttons, allowing the player to choose the AI algorithm for the next game.
        self.bfs_button.config(state=tk.NORMAL)
        self.dfs_button.config(state=tk.NORMAL)
        self.bidirectional_button.config(state=tk.NORMAL)
        self.ucs_button.config(state=tk.NORMAL)
        self.dls_button.config(state=tk.NORMAL)
        self.iddfs_button.config(state=tk.NORMAL)

    # Implements Breadth-First Search algorithm
    def bfs(self):
        # This line creates a list of empty cell indices in the self.board list.
        # It uses a list comprehension -a concise way of creating lists from the ones that already exist-
        # to iterate through the board and finds all indices with an empty space (' ').
        empty_cells = [i for i, val in enumerate(self.board) if val == ' ']
        #  Initializes a variable best_move to store the best move found.
        best_move = None
        # loop is used to simulate making a move (placing 'O') for the AI player in each empty cell and checking if it's a winning move.
        # If a winning move is found, it updates 'best_move' with that move.
        # After each simulation, the board is reset to its previous state.
        # Iterates through the empty cells.
        for move in empty_cells:
            # Simulates the AI move by placing 'O' in the current cell.
            self.board[move] = 'O'
            # Calls the check_winner method to check if this move results in a win for 'O'. 
            if self.check_winner('O'):
                # # If it does, best_move is updated with the current cell index.
                best_move = move
            self.board[move] = ' '  # Resets the board to its original state by emptying the cell.
        if best_move is not None:
            return best_move
        
        # The code then repeats the above process but simulates moves for 'X' instead of 'O'.
        #  It checks if any move by 'X' results in a win, and if so, it updates best_move
        for move in empty_cells:
            self.board[move] = 'X'
            if self.check_winner('X'):
                best_move = move
            self.board[move] = ' '  # Reset the board
            # Finally, the code checks if best_move has been updated during the process. 
            # If it has (meaning a winning move was found for 'O' or 'X'), it returns the best move.
            # If not, it returns a random move from the list of empty cells.
        if best_move is not None:
            return best_move
        # This random choice is a fallback in case no immediate winning move is found
        return random.choice(empty_cells)


    # This dfs function implements a Depth-First Search (DFS) algorithm for making a move in the Tic Tac Toe game. 
    # It explores the game tree by simulating moves and checking for winning conditions. Here's an explanation of the code:
    def dfs(self):
        # This line creates a list of empty cell indices in the self.board. It uses a list comprehension to iterate through the board and finds all indices with an empty space (' ').
        empty_cells = [i for i, val in enumerate(self.board) if val == ' ']
        # Initializes a variable best_move to store the best move found.
        best_move = None
        # The following loop is used to simulate making a move (placing 'O') for the AI player in each empty cell and checking if it's a winning move.
        # If a winning move is found, it updates best_move with that move.
        # After each simulation, the board is reset to its previous state.
        # Iterates through the empty cells.
        for move in empty_cells:
            # Simulates the AI move by placing 'O' in the current cell.
            self.board[move] = 'O'
            # Calls the check_winner method to check if this move results in a win for 'O'.
            if self.check_winner('O'):
                # If it does, best_move is updated with the current cell index.
                best_move = move
            self.board[move] = ' '  # Resets the board to its original state by emptying the cell. 
        if best_move is not None:
            return best_move
        
        # The code then repeats the above process but simulates moves for 'X' instead of 'O'.
        # It checks if any move by 'X' results in a win, and if so, it updates best_move.
        for move in empty_cells:
            self.board[move] = 'X'
            if self.check_winner('X'):
                best_move = move
            self.board[move] = ' '  # Reset the board
        # Finally, the code checks if best_move has been updated during the process.
        # If it has (meaning a winning move was found for 'O' or 'X'), it returns the best move.
        if best_move is not None:
            return best_move
        # If not, it returns a random move from the list of empty cells. This random choice is a fallback in case no immediate winning move is found.
        return random.choice(empty_cells)

    def bidirectional(self):
        #  'empty_cells' = Is a list comprehension that finds all empty cells on the Tic Tac Toe board.
        # It enumerates the board, collecting the index i and the value val, and selects only those cells where val is a space character (representing an empty cell).
        # This prepares a list of tuples where each tuple contains the index of an empty cell and the value (which will always be a space character).
        # **ENUMERATE: allows you to keep track of the number of iterations (loops) in a loop. Ex: Fruites example and loops giving index to each item in list.
        # Gives list of tuples**
        empty_cells = [(i, val) for i, val in enumerate(self.board) if val == ' ']
        #  Is initialized as None and will be used to store the best move found during the algorithm.
        # Initially, there is no best move.
        best_move = None
        # This loop iterates through the empty_cells, where each element is a tuple containing the index move
        # and the value ('X' and 'O' which is ignored with the _ placeholder). Within the loop:
        for move, _ in empty_cells:
            # The code sets the move as 'O' to simulate a possible move by the 'O' player
            self.board[move] = 'O'
            # It then checks if 'O' has won with this move using the check_winner method.
            # If it has,
            if self.check_winner('O'):
                # The code returns move as the best move found so far, indicating that 'O' should make this move.
                self.board[move] = ' '
                return move
            # After the check, the board state is reset to empty by setting self.board[move] to ' ' to explore the next possible move.
            self.board[move] = ' '

        # This part is similar to the previous loop, but it simulates possible moves by the 'X' player and checks if 'X' can win.
        # If a winning move for 'X' is found, it returns that move.
        # This loop looks for a winning move by 'X'.
        for move, _ in empty_cells:
            self.board[move] = 'X'
            if self.check_winner('X'):
                self.board[move] = ' '
                return move
            self.board[move] = ' '

        # If neither 'O' nor 'X' can win with their next move, or if the list of empty cells is empty (indicating a draw situation),
        # the code returns a random move from the list of empty cells.
        # This is a fallback when neither player can win immediately, and the code selects a random move to continue the game.
        return random.choice([i for i, _ in empty_cells])
    
    # Depth-Limited Search algorithm for selecting the best move for the computer player ('O') in Tic-Tac-Toe.
    def dls(self):
        # Find indices of empty cells on the board
        empty_cells = [i for i, val in enumerate(self.board) if val == ' ']
        best_move = None
        best_cost = float('-inf') # Initialize the best cost to negative infinity

        # Iterate through each empty cell
        for move in empty_cells:
            # Try placing 'O' in the current empty cell
            self.board[move] = 'O'
            # Use DLS search to find the cost of the move with a depth limit of 0
            cost = self.dls_search('X', 0)  # Start with a depth limit of 0
            # Undo the move to simulate backtracking
            self.board[move] = ' '

            # Update the best move and cost if the current move has a higher cost
            if cost > best_cost:
                best_cost = cost
                best_move = move

        # Return the best move for the computer player ('O')
        return best_move

    def dls_search(self, player, depth_limit):
         # Check if 'O' has won
        if self.check_winner('O'):
            return -1
        # Check if 'X' has won
        if self.check_winner('X'):
            return 1
        # Check if the board is full or the depth limit is reached
        if ' ' not in self.board or depth_limit == 0:
            return 0

        # Find indices of empty cells on the board
        empty_cells = [i for i, val in enumerate(self.board) if val == ' ']
         # Initialize the best cost based on whether it's 'O' or 'X' turn
        best_cost = float('-inf') if player == 'O' else float('inf')

         # Iterate through each empty cell
        for move in empty_cells:
            # Try placing the current player's symbol in the empty cell
            self.board[move] = player
            # Recursively call DLS search for the next player with a decreased depth limit
            cost = self.dls_search('O' if player == 'X' else 'X', depth_limit - 1)
             # Undo the move to simulate backtracking
            self.board[move] = ' '

             # Update the best cost based on the player's turn
            if player == 'O':
                best_cost = max(best_cost, cost)
            else:
                best_cost = min(best_cost, cost)

        # Return the best cost for the current player's move
        return best_cost


    def ucs(self):
        # Find all empty cells and their indices
        empty_cells = [(i, val) for i, val in enumerate(self.board) if val == ' ']
         # Initialize variables to track the best move and its cost
        best_move = None
        best_cost = float('inf')

        # Iterate through each empty cell to evaluate potential moves
        for move, _ in empty_cells:
             # Make a hypothetical move for player 'O'
            self.board[move] = 'O'
            # Evaluate the cost of this move using UCS search with minimizing 'X'
            cost = self.ucs_search('X')
            # Undo the hypothetical move
            self.board[move] = ' '

            # Update the best move if the current cost is better
            if cost < best_cost:
                best_cost = cost
                best_move = move

        # Return the best move found
        return best_move

    def ucs_search(self, player):
        # Check for game over conditions
        if self.check_winner('O'):
            return -1  # Player 'O' wins, and we're minimizing, so cost is -1
        if self.check_winner('X'):
            return 1  # Player 'X' wins, and we're minimizing, so cost is 1
        if ' ' not in self.board:
            return 0  # It's a draw, and the cost is 0

        # Find all empty cells and their indices
        empty_cells = [(i, val) for i, val in enumerate(self.board) if val == ' ']
        # Initialize the best cost depending on whether we're maximizing or minimizing
        best_cost = float('inf') if player == 'O' else -float('inf')

        # Iterate through each empty cell to evaluate potential moves
        for move, _ in empty_cells:
            # Make a hypothetical move for the current player
            self.board[move] = player
            # Recursively call UCS search to evaluate the cost of the move
            cost = self.ucs_search('O' if player == 'X' else 'X')
            # Undo the hypothetical move
            self.board[move] = ' '

            # Update the best cost based on whether we're maximizing or minimizing
            if player == 'O':
                best_cost = min(best_cost, cost)
            else:
                best_cost = max(best_cost, cost)

        # Return the best cost found for the current player
        return best_cost

    def iddfs(self):
        # Set the maximum depth to explore the entire board
        max_depth = 9 
         # Iterate through depths from 1 to max_depth
        for depth in range(1, max_depth + 1):
            # Perform IDDFS search with the current depth
            best_move = self.iddfs_search(self.current_player, depth)
            # If a valid move is found at the current depth, return it
            if best_move is not None:
                return best_move

    def iddfs_search(self, player, depth):
         # Check for game over conditions or reaching the specified depth
        if self.check_winner('O'):
            return -1 # Player 'O' wins, and we're minimizing, so cost is -1
        if self.check_winner('X'):
            return 1  # Player 'X' wins, and we're minimizing, so cost is 1
        if ' ' not in self.board or depth == 0:
            return 0  # It's a draw, or maximum depth reached, and the cost is 0

        # Find indices of empty cells
        empty_cells = [i for i, val in enumerate(self.board) if val == ' ']
        # Initialize best_cost and best_move based on whether we're maximizing or minimizing
        best_cost = float('-inf') if player == 'O' else float('inf')
        best_move = None

        # Iterate through each empty cell to evaluate potential moves
        for move in empty_cells:
            # Make a hypothetical move for the current player
            self.board[move] = player
             # Recursively call IDDFS search with decreased depth
            cost = self.iddfs_search('O' if player == 'X' else 'X', depth - 1)
              # Undo the hypothetical move
            self.board[move] = ' '

             # Update the best_cost and best_move based on whether we're maximizing or minimizing
            if player == 'O':
                if cost > best_cost:
                    best_cost = cost
                    best_move = move
            else:
                if cost < best_cost:
                    best_cost = cost
                    best_move = move

        # Return the best_move found at the current depth
        return best_move

if __name__ == '__main__':
    TicTacToe()
