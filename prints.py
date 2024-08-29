def print_colored(text, color, end="\n"):  # Add end parameter with default value "\n"
    colors = {
        "white": "\033[97m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "red": "\033[91m",
        "orange": "\033[33m",
        "pink": "\033[95m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "end": "\033[0m",
    }
    print(f"{colors.get(color, colors['white'])}{text}{colors['end']}", end=end)  # Pass end to print

def printBoard(board):
    print_colored("Board: ", "yellow")
    if not board:
        print_colored("Empty", "green", end=" ")
    for piece in board:
        print_colored(f"[{piece[0]}|{piece[1]}]", "green", end=" ")
    print("")