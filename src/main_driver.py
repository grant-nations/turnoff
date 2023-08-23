"""
This file is the main driver for the project. It runs all of the bots, gets the article scores, summarizes the top articles,
and posts the tweet. It is the only file that needs to be run to get the tweet posted, and is what is run by the bash script
as a cron job.
"""

from src.news_bot_driver import run_bots
from src.open_ai_driver import get_article_scores, summarize_top_articles, write_tweet_from_summaries
from src.tweet_driver import post_tweet

run_bots()
get_article_scores()
summarize_top_articles()
write_tweet_from_summaries()
post_tweet()
