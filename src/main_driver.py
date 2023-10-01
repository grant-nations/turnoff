from src.news_bot_driver import run_bots
from src.open_ai_driver import get_article_scores, summarize_top_articles, write_tweet_from_summaries
from src.tweet_driver import post_tweet

run_bots()
get_article_scores()
summarize_top_articles()
write_tweet_from_summaries()
post_tweet()
