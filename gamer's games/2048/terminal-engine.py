# 2048 terminal engine
# It might feel sick to have 2048 on the humble terminal, but it is a fun challenge.

import os
import random
import copy

cells = [[0,0,0,0],
         [0,0,0,0],
         [0,0,0,0],
         [0,0,0,0]]
previous = ' '

_errors1 = [" Entered X                ", " Command X is invalid     ", 
            " Move didn't change board ", " Game over!               ", 
            " You won!                 ", " Please enter Y or N!     ", 
            " Quitting now?            "]
_inputs1 = [" Enter a command: _       \b\b\b\b\b\b\b\b", " Press to replay(Y/N): _  \b\b\b",
            " Press to quit(Q): _       \b\b\b\b\b\b\b"]
error_code = 0
input_code = 0

# basic terminal functions

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def boards_equal(b1, b2):
    return all(b1[i] == b2[i] for i in range(4))

def error_message(code):
    global previous
    if len(previous) != 1:
        previous = '?'
    else:
        if previous not in 'WASDQI':
            previous = '?'
    return _errors1[code].replace('X', previous)

# game mechanics functions
def pop_random():
    """Pop a random number into a random blank cell, and return True if successful."""
    global cells
    blanks = check_blanks()
    if blanks:
        i, j = random.choice(blanks)
        cells[i][j] = 2 if random.random() < 0.9 else 4
        return True
    return False

def reset_game():
    """Reset the game to the initial state."""
    global cells, previous
    cells = [[0, 0, 0, 0] for _ in range(4)]
    previous = ' '
    # pop_random()

def compress_and_merge(line):
    """Compresses non-zero values and merges adjacent equal numbers."""
    line = [num for num in line if num != 0]
    for i in range(len(line) - 1):
        if line[i] == line[i + 1]:
            line[i] *= 2
            line[i + 1] = 0
    line = [num for num in line if num != 0]
    return line + [0] * (4 - len(line))

# quitting functions

def quit_display():
    print("Quitting application.")
    clear_screen()
    exit(0)

def quit_confirm():
    '''Confirm if the user wants to quit.'''
    global error_code, input_code
    error_code = 6
    input_code = 1
    display()
    while True:
        confirm = input().strip().upper()
        if confirm == 'Y':
            error_code = 0
            input_code = 0
            break
        elif confirm == 'N':
            quit_display()
        else:
            error_code = 5
            input_code = 1
            display()

def welcome_quit():
    clear_screen
    print(f"----- WELCOME:{num_to_unit(2048)} -----")
    print(" ------------------------ ")
    print(" Use W (up), S (down), \n" \
          " A (left), D (right) to \n" \
          " move tiles.")
    print(" I for instructions.")
    print(f" Try to reach {num_to_unit(2048)}!    ")
    to_quit = input(" y to quit (pls not):     \b\b\b\b\b").strip().upper()
    if to_quit == 'Y':
        quit_display()

# game state functions

def check_won():
    """Check if the player has won."""
    global cells
    for row in cells:
        if 2048 in row:
            return True
    return False

def check_game_over():
    if check_blanks():
        return False  # There are still empty spaces
    for i in range(4):
        for j in range(4):
            if i < 3 and cells[i][j] == cells[i+1][j]:
                return False
            if j < 3 and cells[i][j] == cells[i][j+1]:
                return False
    return True

def operation_possible(before):
    global previous, cells, error_code, input_code
    if not boards_equal(before, cells):
        pop_random()
        error_code = 0
    else:
        error_code = 2
    # Always check game over, even if no tiles moved
    if check_game_over():
        error_code = 3
        input_code = 1
        display()
        return 1
    else:
        return 0

def check_blanks():
    '''Output the places where they are blank.'''
    global cells
    blanks = []
    for i in range(4):
        for j in range(4):
            if cells[i][j] == 0:
                blanks.append((i, j))
    return blanks

def num_to_unit(num):
    # ANSI background (bg) and foreground (fg) color codes
    colors = {
        0:     ('\033[48;5;250m', '\033[38;5;240m'),  # Light gray bg, dark text
        2:     ('\033[48;5;245m', '\033[38;5;15m'),   # Gray bg, **white text**
        4:     ('\033[48;5;131m', '\033[38;5;15m'),   # Maroon bg
        8:     ('\033[48;5;196m', '\033[38;5;15m'),   # Red
        16:    ('\033[48;5;202m', '\033[38;5;15m'),   # Orange
        32:    ('\033[48;5;226m', '\033[38;5;0m'),    # Yellow (black text)
        64:    ('\033[48;5;220m', '\033[38;5;0m'),    # Gold
        128:   ('\033[48;5;154m', '\033[38;5;0m'),    # Lime
        256:   ('\033[48;5;34m',  '\033[38;5;15m'),   # Green
        512:   ('\033[48;5;51m',  '\033[38;5;0m'),    # Cyan
        1024:  ('\033[48;5;33m',  '\033[38;5;15m'),   # Blue
        2048:  ('\033[48;5;129m', '\033[38;5;15m'),   # Purple
    }

    bg, fg = colors.get(num, ('\033[48;5;235m', '\033[38;5;15m'))  # fallback
    reset = '\033[0m'
    return f"{bg}{fg}[{str(num).rjust(4)}]{reset}"

# display functions
def display():
    """Display the current state of the game."""
    global cells, error_code, input_code, _inputs1
    clear_screen()
    print(f"------ PLAY: {num_to_unit(2048)} ------")
    print(" ------------------------ ")
    for row in cells:
        print(' '+''.join(num_to_unit(num) for num in row)+' ')
    if (error_code == 4 or error_code == 3):
        input_code = 1
    print(error_message(error_code))
    print(_inputs1[input_code], end='', flush=True)

def display_rules():
    '''Display the rules of the game.'''
    clear_screen()
    print(f"------ RULES:{num_to_unit(2048)} ------")
    print(" ------------------------ ")
    print(''' Instructions: S = down, 
 D = right,  A = left,
 W = up, E = exit game
 Q = quit application,
 I = instructions
 Press Enter to continue''', end="")
    input()

def home():
    '''Return to the home screen.'''
    clear_screen()
    print()
    command = ''
    while command != 'E':
        clear_screen()
        print(f"----- WELCOME:{num_to_unit(2048)} -----")
        print(" ------------------------ ")
        print(" Use W (up), S (down), \n" \
              " A (left), D (right) to \n" \
              " move tiles.")
        print(" I for instructions.")
        print(f" Try to reach {num_to_unit(2048)}!    ")
        command = input(" Enter E to start: _      \b\b\b\b\b\b\b").strip().upper()
        if command == 'I':
            display_rules()
        if command == 'Q':
            welcome_quit()

# main game loop
def main():
    """Main game loop."""
    global previous, cells, error_code, input_code
    input_code = 0
    error_code = 0
    pop_random()  # Start with a random number
    while True:
        display()
        command = input().strip().upper()
        if command == 'W':
            previous = 'W'
            before = copy.deepcopy(cells)

            column_based_cells = [[cells[j][i] for j in range(4)] for i in range(4)]
            for i in range(4):
                new_col = compress_and_merge(column_based_cells[i])
                for j in range(4):
                    column_based_cells[i][j] = new_col[j]
            cells = [[column_based_cells[j][i] for j in range(4)] for i in range(4)]
            if operation_possible(before):
                return 1
        elif command == 'S':
            previous = 'S'
            before = copy.deepcopy(cells)
            column_based_cells = [[cells[j][i] for j in range(4)] for i in range(4)]
            for i in range(4):
                reversed_col = column_based_cells[i][::-1]
                new_col = compress_and_merge(reversed_col)
                column_based_cells[i] = new_col[::-1]
            cells = [[column_based_cells[j][i] for j in range(4)] for i in range(4)]
            if operation_possible(before):
                return 1
        elif command == 'A':
            previous = 'A'
            before = copy.deepcopy(cells)
            for i in range(4):
                cells[i] = compress_and_merge(cells[i])
            if operation_possible(before):
                return 1
        elif command == 'D':
            previous = 'D'
            before = copy.deepcopy(cells)
            for i in range(4):
                reversed_row = cells[i][::-1]
                new_row = compress_and_merge(reversed_row)
                cells[i] = new_row[::-1]
            if operation_possible(before):
                return 1
        elif command == 'E':
            print("Exiting the game.")
            return 0
        elif command == 'Q':
            quit_confirm()
            error_code = 0
            continue
        elif command == 'I':
            display_rules()
            error_code = 0
            continue
        else:
            previous = command
            error_code = 1
            continue
        if check_won():
            error_code = 4
            input_code = 1
            display()
            return 1

# program loop
if __name__ == "__main__":
    while True:
        home()
        while True:
            reset_game()
            status = main()
            if status == 0:
                break
            input_code = 1
            display()
            quit_choice = True
            while True:
                choice = input().strip().upper()
                if choice == 'N':
                    print("Thanks for playing!")
                    print()
                    break
                elif choice == 'Y':
                    quit_choice = False
                    break
                elif choice == 'Q':
                    exit(0)
                elif choice == 'I':
                    display_rules()
                    display()     
                else:
                    error_code = 5
                    input_code = 1
                    display()
            if quit_choice:
                break
