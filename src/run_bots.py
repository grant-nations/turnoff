# This file runs all of the bots and saves the data to JSON files.
#
# TODO: 
#  - Add more bots
#  - Fix text encoding issues
#  - Add this script to a cron job
#  - Run articles through GPT-4
#  - Post output to Twitter
#   
#  - Run bots in parallel
#  - Add logging

from src.utils import print_green, print_red, CHECK_MARK, random_failure_message
from src.bots.nyt_bot import NYTBot
from src.bots.fox_bot import FoxBot
from src.bots.cnn_bot import CNNBot
from src.bots.wp_bot import WPBot
import json
import datetime
import os

# | Create bots |
# V              V

bots = [
    NYTBot(),
    FoxBot(),
    CNNBot(),
    WPBot()
]

# | Create directories for today's data |
# V                                     V

current_date = datetime.datetime.now()
year = current_date.year
month = f"{current_date.month:02d}"  # Zero-padded month (e.g. 06, 07, ...)
day = f"{current_date.day:02d}"  # Zero-padded day (e.g. 01, 02, ...)

today = f"{year}_{month}_{day}"

articles_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", today)
if not os.path.exists(articles_path):
    os.makedirs(articles_path, exist_ok=True)
articles_path = os.path.join(articles_path, "articles.json")

failed_pages_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", today)
if not os.path.exists(failed_pages_path):
    os.makedirs(failed_pages_path, exist_ok=True)
failed_pages_path = os.path.join(failed_pages_path, "failed_pages.json")

failed_sites_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", today)
if not os.path.exists(failed_sites_path):
    os.makedirs(failed_sites_path, exist_ok=True)
failed_sites_path = os.path.join(failed_sites_path, "failed_sites.json")

# | Get articles from each site |
# V                             V

all_articles = []
all_failed_pages = []
failed_sites = []

for bot in bots:
    try:
        print(f"Getting articles from {bot.name}...\n")

        articles, failed_pages = bot.get_articles()

        print(f"{len(articles)} articles collected")

        for article in articles:
            print_green(  CHECK_MARK, end="", flush=True)
            print(f" {article['title']}")

        for failed_page in failed_pages:
            print_red("  X", end="", flush=True)
            print(f" {failed_page['page']}")

        all_articles.append({
            "source": bot.name,
            "articles": articles
        })

        all_failed_pages.append({
            "source": bot.name,
            "failed_pages": failed_pages
        })

    except Exception as e:
        print_red(random_failure_message())
        print(f"{e}")
        failed_sites.append({
            "source": bot.name,
            "exception": str(e)
        })

    finally:
        print("----------------------------------------\n")

# | Save data to JSON files |
# V                         V

with open(articles_path, "w") as f:
    json.dump(all_articles, f, indent=2)

with open(failed_pages_path, "w") as f:
    json.dump(all_failed_pages, f, indent=2)

with open(failed_sites_path, "w") as f:
    json.dump(failed_sites, f, indent=2)
