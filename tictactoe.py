from tkinter import *
import random

def is_winner(board, player):
    # Check rows
    for row in range(3):
        if all(board[row][col]['text'] == player for col in range(3)):
            return True
    
    # Check columns
    for col in range(3):
        if all(board[row][col]['text'] == player for row in range(3)):
            return True
    
    # Check diagonals
    if all(board[i][i]['text'] == player for i in range(3)):
        return True
    if all(board[i][2-i]['text'] == player for i in range(3)):
        return True
    
    return False

def is_board_full(board):
    return all(board[row][col]['text'] != "" for row in range(3) for col in range(3))

def get_empty_cells(board):
    return [(row, col) for row in range(3) for col in range(3) if board[row][col]['text'] == ""]

def minimax(board, depth, is_maximizing):
    if is_winner(board, "O"):
        return 1
    if is_winner(board, "X"):
        return -1
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for row, col in get_empty_cells(board):
            board[row][col]['text'] = "O"
            score = minimax(board, depth + 1, False)
            board[row][col]['text'] = ""
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row, col in get_empty_cells(board):
            board[row][col]['text'] = "X"
            score = minimax(board, depth + 1, True)
            board[row][col]['text'] = ""
            best_score = min(score, best_score)
        return best_score

def ai_move():
    if check_winner() is False:  # Only make a move if the game isn't over
        best_score = float('-inf')
        best_move = None
        
        for row, col in get_empty_cells(buttons):
            buttons[row][col]['text'] = "O"
            score = minimax(buttons, 0, False)
            buttons[row][col]['text'] = ""
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        if best_move:
            row, col = best_move
            buttons[row][col]['text'] = "O"
            
            if check_winner() is False:
                player = "X"
                label.config(text=(player + " turn"))
            elif check_winner() is True:
                label.config(text=("O wins"))
                show_game_over("O wins!")
            elif check_winner() == "Tie":
                label.config(text=("Tie!"))
                show_game_over("It's a Tie!")

def show_game_over(message):
    # Create a new window for game over
    game_over_window = Toplevel(window)
    game_over_window.title("Game Over")
    game_over_window.geometry("300x200")
    
    # Center the window
    game_over_window.transient(window)
    game_over_window.grab_set()
    
    # Add message
    Label(game_over_window, text=message, font=('consolas', 20)).pack(pady=20)
    
    # Add new game button
    Button(game_over_window, text="New Game", font=('consolas', 15),
           command=lambda: [game_over_window.destroy(), new_game()]).pack(pady=10)
    
    # Add quit button
    Button(game_over_window, text="Quit", font=('consolas', 15),
           command=window.quit).pack(pady=10)

def next_turn(row, column):
    global player
    if buttons[row][column]['text'] == "" and check_winner() is False:
        buttons[row][column]['text'] = player

        if check_winner() is False:
            if empty_spaces() == 0:
                label.config(text="Tie!")
                show_game_over("It's a Tie!")
            else:
                player = players[1] if player == players[0] else players[0]
                label.config(text=(player + " turn"))
                
                # If it's AI's turn, make the move
                if player == "O":
                    window.after(500, ai_move)  # Add a small delay for better UX
        elif check_winner() is True:
            label.config(text=(player + " wins"))
            show_game_over(player + " wins!")
        elif check_winner() == "Tie":
            label.config(text=("Tie!"))
            show_game_over("It's a Tie!")

def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            buttons[row][0].config(bg="green")
            buttons[row][1].config(bg="green")
            buttons[row][2].config(bg="green")
            return True
        
    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != "":
            buttons[0][column].config(bg="green")
            buttons[1][column].config(bg="green")
            buttons[2][column].config(bg="green")
            return True
        
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        buttons[0][0].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][2].config(bg="green")
        return True
    
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        buttons[0][2].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][0].config(bg="green")
        return True
    
    if empty_spaces() == 0:
        return "Tie"
    
    return False

def empty_spaces():
    spaces = 9
    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] != "":
                spaces -= 1
    return spaces

def new_game():
    global player
    player = random.choice(players)
    label.config(text=player + " turn")

    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="", bg="#F0F0F0")

    if player == "O":  # If AI goes first
        window.after(500, ai_move)

window = Tk()
window.title("Tic Tac Toe")
players = ["X", "O"]  # X is human, O is AI
player = random.choice(players)
buttons = [[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]]

# Bind spacebar to new_game function
window.bind('<space>', lambda event: new_game())

label = Label(text=player + " turn", font=('consolas', 40))
label.pack(side="top")

frame = Frame(window)
frame.pack()

for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text="", font=('consolas', 40), width=5, height=2, command=lambda row=row, column=column: next_turn(row, column))
        buttons[row][column].grid(row=row, column=column)

new_game()
window.mainloop()