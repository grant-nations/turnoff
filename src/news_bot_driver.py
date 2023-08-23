"""
This file contains the driver for the news bots that scrape articles from news sites.
"""

from src.utils import print_green, print_red, CHECK_MARK, get_current_date_string
from src.news_bots.nyt_bot import NYTBot
from src.news_bots.fox_bot import FoxBot
from src.news_bots.cnn_bot import CNNBot
from src.news_bots.wp_bot import WPBot
import json
import os


def run_bots():
    """
    Run all of the bots and save the data to JSON files.
    """

    # | Create bots |
    # V             V

    bots = [
        NYTBot(),
        FoxBot(),
        CNNBot(),
        WPBot()
    ]

    # | Create directories for today's data |
    # V                                     V

    today = get_current_date_string()

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

            all_articles.append({
                "source": bot.name,
                "articles": articles
            })

            all_failed_pages.append({
                "source": bot.name,
                "failed_pages": failed_pages
            })

        except Exception as e:
            print_red(e)
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
