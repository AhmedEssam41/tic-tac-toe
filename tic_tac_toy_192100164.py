import tkinter as tk
from tkinter import messagebox
from collections import deque
import time

# Constants
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '

# Function to check if a player has won
def check_winner(board, player):
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]) or \
           all([board[j][i] == player for j in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or \
       all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

# Check if the board is full
def is_board_full(board):
    return all([board[i][j] != EMPTY for i in range(3) for j in range(3)])

# Get possible moves
def get_possible_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]

# Apply a move to the board
def apply_move(board, move, player):
    new_board = [row[:] for row in board]
    new_board[move[0]][move[1]] = player
    return new_board

# Depth First Search (DFS)
def dfs(board, depth, player):
    if check_winner(board, PLAYER_X):
        return -10 + depth  # High negative value for losing
    if check_winner(board, PLAYER_O):
        return 10 - depth  # High positive value for winning
    if is_board_full(board):
        return 0  # Draw (neutral)

    possible_moves = get_possible_moves(board)
    if player == PLAYER_X:
        best_value = float('inf')  # Minimize for opponent (X is minimizing player)
        for move in possible_moves:
            new_board = apply_move(board, move, PLAYER_X)
            value = dfs(new_board, depth + 1, PLAYER_O)
            best_value = min(best_value, value)
    else:
        best_value = float('-inf')  # Maximize for player (O is maximizing player)
        for move in possible_moves:
            new_board = apply_move(board, move, PLAYER_O)
            value = dfs(new_board, depth + 1, PLAYER_X)
            best_value = max(best_value, value)

    return best_value

# Breadth First Search (BFS)
def bfs(board, player):
    queue = deque([(board, player)])
    visited = set()
    visited.add(str(board))

    while queue:
        current_board, current_player = queue.popleft()

        if check_winner(current_board, PLAYER_X):
            return -10
        if check_winner(current_board, PLAYER_O):
            return 10
        if is_board_full(current_board):
            return 0

        possible_moves = get_possible_moves(current_board)
        for move in possible_moves:
            new_board = apply_move(current_board, move, current_player)
            if str(new_board) not in visited:
                visited.add(str(new_board))
                queue.append((new_board, PLAYER_X if current_player == PLAYER_O else PLAYER_O))

    return 0

# Uniform Cost Search (UCS)
def ucs(board, player):
    queue = deque([(board, 0, player)])
    visited = set()
    visited.add(str(board))

    while queue:
        current_board, cost, current_player = queue.popleft()

        if check_winner(current_board, PLAYER_X):
            return -10 + cost
        if check_winner(current_board, PLAYER_O):
            return 10 - cost
        if is_board_full(current_board):
            return 0

        possible_moves = get_possible_moves(current_board)
        for move in possible_moves:
            new_board = apply_move(current_board, move, current_player)
            if str(new_board) not in visited:
                visited.add(str(new_board))
                queue.append((new_board, cost + 1, PLAYER_X if current_player == PLAYER_O else PLAYER_O))

    return 0

# Find the best move based on the selected algorithm
def find_best_move(board, player, algorithm):
    best_value = float('-inf') if player == PLAYER_O else float('inf')
    best_move = None
    possible_moves = get_possible_moves(board)

    # Start time tracking
    start_time = time.time()

    for move in possible_moves:
        new_board = apply_move(board, move, player)

        if algorithm == 'DFS':
            move_value = dfs(new_board, 0, PLAYER_X if player == PLAYER_O else PLAYER_X)
        elif algorithm == 'BFS':
            move_value = bfs(new_board, PLAYER_X if player == PLAYER_O else PLAYER_X)
        elif algorithm == 'UCS':
            move_value = ucs(new_board, PLAYER_X if player == PLAYER_O else PLAYER_X)

        if player == PLAYER_O and move_value > best_value:
            best_value = move_value
            best_move = move
        elif player == PLAYER_X and move_value < best_value:
            best_value = move_value
            best_move = move

    # Calculate execution time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Time and space complexity information (approximations)
    time_complexity_label = "Time Complexity: O(b^d)"
    space_complexity_label = "Space Complexity: O(b^d)"

    # Update labels in the GUI with the time and complexity
    time_label.config(text=f"Elapsed Time: {elapsed_time:.4f} seconds")
    complexity_label.config(text=f"{time_complexity_label} | {space_complexity_label}")

    return best_move

# Create a new game instance
def new_game():
    global board
    board = [[EMPTY] * 3 for _ in range(3)]
    update_board()

# Update the board in the GUI
def update_board():
    for i in range(3):
        for j in range(3):
            btn = buttons[i][j]
            btn.config(text=board[i][j], state=tk.NORMAL if board[i][j] == EMPTY else tk.DISABLED)

# Handle button click (Player Move)
def player_move(i, j):
    if board[i][j] == EMPTY:
        board[i][j] = PLAYER_X
        update_board()

        if check_winner(board, PLAYER_X):
            messagebox.showinfo("Game Over", "Player X Wins!")
            disable_buttons()
            return
        elif is_board_full(board):
            messagebox.showinfo("Game Over", "It's a Draw!")
            return
        
        # Now let the AI make its move
        ai_move()

# AI Move (Based on selected algorithm)
def ai_move():
    selected_algorithm = algorithm_var.get()
    best_move = find_best_move(board, PLAYER_O, selected_algorithm)
    if best_move:
        i, j = best_move
        board[i][j] = PLAYER_O
        update_board()

        if check_winner(board, PLAYER_O):
            messagebox.showinfo("Game Over", "Player O (AI) Wins!")
            disable_buttons()
        elif is_board_full(board):
            messagebox.showinfo("Game Over", "It's a Draw!")

# Disable all buttons after the game ends
def disable_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state=tk.DISABLED)

# Create the main GUI window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Create a 3x3 grid of buttons
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text=EMPTY, width=10, height=3, font=('Arial', 24),
                                  command=lambda i=i, j=j: player_move(i, j))
        buttons[i][j].grid(row=i, column=j)

# Create a new game button
new_game_button = tk.Button(root, text="New Game", font=('Arial', 14), command=new_game)
new_game_button.grid(row=3, column=0, columnspan=3)

# Create a dropdown to select algorithm
algorithm_var = tk.StringVar(value="DFS")  # Default algorithm
algorithm_menu = tk.OptionMenu(root, algorithm_var, "DFS", "BFS", "UCS")
algorithm_menu.grid(row=4, column=0, columnspan=3)

# Create labels for time and complexity
time_label = tk.Label(root, text="Elapsed Time: 0.0000 seconds", font=('Arial', 10))
time_label.grid(row=5, column=0, columnspan=3)

complexity_label = tk.Label(root, text="Time Complexity: O(b^d) | Space Complexity: O(b^d)", font=('Arial', 10))
complexity_label.grid(row=6, column=0, columnspan=3)

# Initialize game
new_game()

# Start the Tkinter event loop
root.mainloop()
