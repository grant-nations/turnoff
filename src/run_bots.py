from src.utils import print_green, print_red
from src.bots.nyt_bot import NYTBot
from src.bots.fox_bot import FoxBot
from src.bots.cnn_bot import CNNBot

bots = [
    # NYTBot(),
    # FoxBot(),
    CNNBot()
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