import random

CHECK_MARK = "\u2713"


def print_color(text, color_code, end='\n', flush=False):
    print(f"\033[{color_code}m{text}\033[0m", end=end, flush=flush)


def print_red(text, end='\n', flush=False):
    print_color(text, "31", end=end, flush=flush)


def print_green(text, end='\n', flush=False):
    print_color(text, "32", end=end, flush=flush)


def print_yellow(text, end='\n', flush=False):
    print_color(text, "33", end=end, flush=flush)


def print_blue(text, end='\n', flush=False):
    print_color(text, "34", end=end, flush=flush)


def print_magenta(text, end='\n', flush=False):
    print_color(text, "35", end=end, flush=flush)


def print_cyan(text, end='\n', flush=False):
    print_color(text, "36", end=end, flush=flush)


def random_failure_message():
    failure_messages = [
        "Oops, the hamster powering our server fell asleep.",
        "Looks like a squirrel chewed through the internet cables.",
        "The gremlins are at it again, causing technical mischief.",
        "Code machine broke.",
        "A black hole temporarily swallowed our data.",
        "An alien invasion disrupted our systems. They love memes!",
        "A glitch in the matrix caused a system malfunction.",
        "Collision between quantum strings caused singularity.",
        "The quantum flux capacitor overheated and caused a meltdown.",
        "We accidentally spilled glitter on the servers, and chaos ensued.",
    ]

    return random.choice(failure_messages)


def month_to_number(month_string):
    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12
    }

    lowercase_month = month_string.lower()

    if lowercase_month in months:
        return months[lowercase_month]
    else:
        raise ValueError("Invalid month string")



def is_month_name(input_string):
    months = [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december"
    ]
    
    return input_string.lower() in months