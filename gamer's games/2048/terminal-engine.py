# 2048 terminal engine
# It might feel sick to have 2048 on the humble terminal, but it is a fun challenge.

import os
import random
import copy
import math

cells = [[0,0,0,0],
         [0,0,0,0],
         [0,0,0,0],
         [0,0,0,0]]
previous = ' '

_errors1 = [" Entered X                     ", " Command X is invalid          ", 
            " Move didn't change board      ", " Game over!                    ", 
            " You won!                      ", " Please enter Y or N!          ", 
            " Quitting now?                 "]
_inputs1 = [" Enter a command: _             \b\b\b\b\b\b\b\b\b\b\b\b\b", " Press to continue(Y/N): _     \b\b\b\b\b\b",
            " Press to quit(Q): _            \b\b\b\b\b\b\b\b\b\b\b\b"]
# ------------------------------- 
# Replay/Continue/Exit(R/C/E):
#
error_code = 0
input_code = 0

# settings
settings = {
    "colors": (True, "Colours"),
    "easy": (True, "Easy mode"),
    "unlimited": (False, "Unlimited mode")
}

num_to_settings = ["colors", "easy", "unlimited"]

# easy mode variables
EASY_min=2
EASY_max=2

# basic terminal functions

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def boards_equal(b1, b2) -> bool:
    return all(b1[i] == b2[i] for i in range(4))

def error_message(code) -> str:
    global previous
    if len(previous) != 1:
        previous = '?'
    else:
        if previous not in 'WASDQI':
            previous = '?'
    return _errors1[code].replace('X', previous)

def on_off(bl) -> bool:
    if bl: return 'on '
    else: return 'off'

# game mechanics functions
def pop_random() -> bool:
    """Pop a random number into a random blank cell, and return True if successful."""
    global cells
    blanks = check_blanks()
    if blanks:
        i, j = random.choice(blanks)
        if settings['easy']:
            cells[i][j] = 2 ** random.randint(int(math.log2(EASY_min)), int(math.log2(EASY_max)))
        else:
            cells[i][j] = 2 if random.random() < 0.9 else 4
        return True
    return False

def reset_game() -> None:
    """Reset the game to the initial state."""
    global cells, previous, EASY_max, EASY_min
    cells = [[0, 0, 0, 0] for _ in range(4)]
    previous = ' '
    EASY_min=2
    EASY_max=2
    # pop_random()

def compress_and_merge(line) -> list:
    """Compresses non-zero values and merges adjacent equal numbers."""
    line = [num for num in line if num != 0]
    for i in range(len(line) - 1):
        if line[i] == line[i + 1]:
            line[i] *= 2
            line[i + 1] = 0
    line = [num for num in line if num != 0]
    return line + [0] * (4 - len(line))

def reset_min_max() -> None:
    """Reset the EASY_min and EASY_max values based on current cells."""
    global EASY_min, EASY_max, cells
    _min=68719476736; _max=0
    for i in cells:
        for j in i:
            if j==0: continue
            _min=min(_min, j)
            _max=max(_max, j)
    _max = max(_max//2, 2)
    EASY_max=_max
    EASY_min=_min

# quitting functions

def quit_display() -> None:
    "Quit."
    print("Quitting application.")
    clear_screen()
    exit(0)

def quit_confirm(i=0) -> None:
    '''Confirm if the user wants to quit.'''
    global error_code, input_code
    error_code = 6
    input_code = i+1
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

def welcome_quit() -> None:
    clear_screen()
    print(f"-------- WELCOME: {num_to_unit(2048)} --------")
    print( " ------------------------------- ")
    print()
    print( "         S for settings          ")
    print( "       I for instructions        ")
    print( )
    print(f"      Try to reach {num_to_unit(2048)}!      ")
    print()
    to_quit = input(" y to quit (pls not):            "+"\b"*12).strip().upper()
    if to_quit == 'Y':
        quit_display()

# game state functions

def check_won() -> bool:
    """Check if the player has won."""
    global cells
    for row in cells:
        if 2048 in row:
            return True
    return False

def check_game_over() -> bool:
    "Check if the game is over."
    if check_blanks():
        return False  # There are still empty spaces
    for i in range(4):
        for j in range(4):
            if i < 3 and cells[i][j] == cells[i+1][j]:
                return False
            if j < 3 and cells[i][j] == cells[i][j+1]:
                return False
    return True

def operation_possible(before) -> int:
    "Check if an operation is possible."
    global previous, cells, error_code, input_code
    # Always check game over, even if no tiles moved
    if check_game_over():
        error_code = 3
        input_code = 1
        display()
        return 1
    if not boards_equal(before, cells):
        pop_random()
        error_code = 0
    else:
        error_code = 2
    return 0

def check_blanks() -> list:
    '''Output the places where they are blank.'''
    global cells
    blanks = []
    for i in range(4):
        for j in range(4):
            if cells[i][j] == 0:
                blanks.append((i, j))
    return blanks

def num_to_unit(num) -> str:
    """
    Colour and format a number for display.
    If settings 'colors' is off, return a plain string.
    """
    global settings
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
        2048:  ('\033[48;5;20m',  '\033[38;5;15m'),
        4096:  ('\033[48;5;127m', '\033[38;5;15m'),   # Purple
        8192:  ('\033[38;5;52m',  '\033[38;5;15m')
    }
    if not settings['colors']:
        return f"[{str(num).rjust(4)}]"
    bg, fg = colors.get(num, ('\033[48;5;235m', '\033[38;5;15m'))  # fallback
    reset = '\033[0m'
    if num>10000:
        num = {
            16384: "16K",
            32768: "32K",
            65536: "65K",
            131072: "131K",
            262144: "262K",
            524288: "524K",
            1048576: "1M",
            2097152: "2M",
            4194304: "4M",
            8388608: "8M",
            16777216: "16M",
            33554422: "33M",
            67108864: "67M",
            134217728: "134M",
            268435456: "268M",
            536870912: "536M",
            1073741824: "1B",
            2147483648: "2B",
            4294967296: "4B",
            8589934592: "8B",
            17179869184: "17B",
            34359738368: "34B",
            68719476736: "68B"
        } [num]
    return f"{bg}{fg}[{str(num).rjust(4)}]{reset}"

# display functions

def display() -> None:
    """Display the current state of the game."""
    global cells, error_code, input_code, _inputs1, EASY_min, EASY_max
    clear_screen()
    print(f"---------- PLAY:{num_to_unit(2048)} ----------")
    print(" ------------------------------- ")
    if settings['easy']:
        #print(EASY_min, EASY_max)
        easy_list = [
            " MIN: ",
            num_to_unit(EASY_min),
            " MAX: ",
            num_to_unit(EASY_max)
        ]
    else:
        easy_list = ["    " for i in range(4)]
    for i in range(4):
        row = cells[i]
        print(' '+''.join(num_to_unit(num) for num in row)+'|'+easy_list[i]+' ')
    if (error_code == 4 or error_code == 3):
        input_code = 1
    print()
    print(_errors1[error_code])
    print(_inputs1[input_code], end='', flush=True)

def display_rules() -> None:
    '''Display the rules of the game.'''
    clear_screen()
    #print(" ------------------------------- ")
    print(f"--------- RULES: {num_to_unit(2048)} ---------")
    print(" ------------------------------- ")
    print(''' Instructions: S=down, D=right,  
 A=left, W=up, E=exit game       
 Q = quit application,           
 I = instructions                

 Press Enter to continue         \b\b\b\b\b\b\b\b\b''', end="")
    input()

def home() -> None:
    '''Return to the home screen.'''
    clear_screen()
    print()
    command = ''
    while command != 'E':
        clear_screen()
        #print(" ------------------------------- ")
        print(f"-------- WELCOME: {num_to_unit(2048)} --------")
        print( " ------------------------------- ")
        print()
        print( "         S for settings          ")
        print( "       I for instructions        ")
        print( )
        print(f"      Try to reach {num_to_unit(2048)}!      ")
        print()
        command = input(" Enter E to start: _             \b\b\b\b\b\b\b\b\b\b\b\b\b\b").strip().upper()
        if command == 'I':
            display_rules()
        elif command == 'S':
            set_settings()
        elif command == 'Q':
            welcome_quit()

def set_settings() -> None:
    "GUI for Settings"
    global settings
    selected=0
    _inp = ""
    select_icon = lambda x: "<-" if x==selected else "  "
    def show_setting(x: int):
        setting_key = num_to_settings[x]
        item = settings[setting_key][1]
        whitespace = (16-len(item)) * ' '
        return "  "+item+": "+on_off(settings[setting_key][0])+whitespace+select_icon(x)
    while _inp!='C':
        clear_screen()
        #print(" ------------------------------- ")
        print(f"-------- SETTINGS:{num_to_unit(2048)} --------")
        print(" ------------------------------- ")
        print(show_setting((selected + len(settings) - 1) % len(settings)))
        print(show_setting(selected))
        print(show_setting((selected + 1) % len(settings)))
        print(" S to scroll, T to toggle,       \n" \
              " C to confirm                    ")
        print()
        cmd = input(" Enter a command...              "+"\b"*8).strip().upper()
        if cmd=="S":
            selected = (selected + 1) % len(settings)
        elif cmd=="T":
            setting_key = num_to_settings[selected]
            settings[setting_key] = tuple([not settings[setting_key][0], settings[setting_key][1]])
        elif cmd=="C":
            _inp = 'C'
            
# in-game loop

def main() -> int:
    """Main game loop."""
    global previous, cells, error_code, input_code, settings
    input_code = 0
    error_code = 0
    pop_random()  # Start with a random number
    while True:
        reset_min_max()
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
            quit_confirm(1)
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
        if check_won() and not settings['unlimited'][0]:
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
