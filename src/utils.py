import random
import tiktoken
import datetime
import re

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


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string.

    Example: num_tokens_from_string("tiktoken is great!", "cl100k_base") -> 4
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_current_date_string(separator="_"):
    current_date = datetime.datetime.now()
    year = current_date.year
    month = f"{current_date.month:02d}"  # Zero-padded month (e.g. 06, 07, ...)
    day = f"{current_date.day:02d}"  # Zero-padded day (e.g. 01, 02, ...)

    today = f"{year}{separator}{month}{separator}{day}"

    return today


def get_yesterday_date_string(separator="_"):
    current_date = datetime.datetime.now()
    year = current_date.year
    month = f"{current_date.month:02d}"  # Zero-padded month (e.g. 06, 07, ...)
    day = f"{(current_date.day - 1):02d}"  # Zero-padded day (e.g. 01, 02, ...)

    today = f"{year}{separator}{month}{separator}{day}"

    return today


def get_score_from_text(text):
    numbers = re.findall(r'\d+', text)  # Find all numbers in the string
    if numbers:
        lowest_number = min(map(int, numbers))  # Convert to integers and find the lowest
        return lowest_number
    else:
        return -1  # Return None if no numbers are found


def remove_hashtags(tweet):
    # Use regular expression to find and remove hashtags
    cleaned_tweet = re.sub(r'#\w+', '', tweet)
    return cleaned_tweet.strip()


def remove_quotations(input_string):
    cleaned_string = input_string.replace('"', '').replace("'", "")
    return cleaned_string
