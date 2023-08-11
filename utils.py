def print_color(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def print_red(text):
    print_color(text, "31")

def print_green(text):
    print_color(text, "32")

def print_yellow(text):
    print_color(text, "33")

def print_blue(text):
    print_color(text, "34")

def print_magenta(text):
    print_color(text, "35")

def print_cyan(text):
    print_color(text, "36")