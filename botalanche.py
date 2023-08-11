from utils import print_green, print_red
from bots.nyt_bot import NYTBot
from bots.fox_bot import FoxBot

bots = [
    NYTBot(),
    FoxBot()
]

all_articles = []

for bot in bots:
    try:
        print(f"Getting articles from {bot.name}...", end="", flush=True)

        articles = bot.get_articles()

        print_green(" GOOD\n")
        print("Articles:")
        for article in articles:
            print("-> " + article["title"])
        print()

        all_articles.extend(articles)
    except Exception as e:
        print_red(" NOT GOOD")
        print(f"{e}")