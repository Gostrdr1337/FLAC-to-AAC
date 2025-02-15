import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def color_to_readable(color_code):
    if color_code.startswith("\033[38;2;"):
        parts = color_code[7:-1].split(";")
        return f"#{int(parts[0]):02X}{int(parts[1]):02X}{int(parts[2]):02X}"
    color_map = {
        "\033[94m": "Blue",
        "\033[92m": "Green",
        "\033[93m": "Yellow",
        "\033[91m": "Red",
        "\033[96m": "Default"
    }
    return color_map.get(color_code, "Unknown")
