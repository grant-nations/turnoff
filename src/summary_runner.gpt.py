"""
This file summarizes the articles collected by the bots. NOTE! This file costs REAL MONEY to run!
"""

import os
import openai
from dotenv import load_dotenv
import src.utils as utils
import json

GPT_MODEL = "gpt-3.5-turbo-16k"


def run_summary():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # | Get today's articles from files |
    # V                                 V

    today = utils.get_current_date_string()
    articles_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", today, "articles.json")

    articles_data = None

    with open(articles_path, "r") as f:
        articles_data = json.load(f)

    # | Summarize the articles |
    # V                        V

    summarized_content = []
    for source_articles in articles_data:
        print(f"Starting on source {source_articles['source']}...")

        # | Summarize the articles from a single source (e.g. CNN) |
        # V                                                        V

        source = source_articles["source"]
        articles = source_articles["articles"]
        summarized_articles_count = 0
        article_index = 0

        while summarized_articles_count < len(articles):
            articles_to_summarize = []
            token_count = 0

            for i in range(article_index, len(articles)):
                article = articles[i]

                article_token_len = 0

                article_token_len += utils.num_tokens_from_string(article["text"])
                article_token_len += utils.num_tokens_from_string(article["title"])

                if article_token_len >= 12000:
                    # this article is too long to be summarized
                    summarized_articles_count += 1
                    article_index += 1
                    continue

                token_count += article_token_len

                if token_count < 12000:
                    # this article can be added to the batch
                    articles_to_summarize.append(article)
                    summarized_articles_count += 1
                    article_index += 1

                    if article_index < len(articles):
                        # there are more articles to summarize
                        continue

                # reaching this point means that the batch is full or there are no more articles to summarize

                # | Send the batch to OpenAI |
                # V                          V

                print(f"    Summarizing {len(articles_to_summarize)} articles from {source}...", end="", flush=True)
                # summarize the articles
                user_str = f"Here's a list of articles from {source}:\n"
                for article in articles_to_summarize:
                    user_str += f"Title: {article['title']}\n"
                    user_str += f"Text: {article['text']}\n\n"

                # the user_str is the prompt for the AI
                user_str += f"Summarize these articles, including only the information that is relevant to the general state of the human world. \
                    If the articles are biased, please remove the bias. Please keep the summary under {2000} words.\n"

                # the messages are the context for the AI; the first message is the AI's role
                messages = [
                    {"role": "system",
                        "content": "You are an educated AI that views the world through the lense of existentialism. \
                            You are employed as a reporter for an AI news agency that reports daily on human affairs."},
                    {"role": "user",
                        "content": user_str}
                ]

                # send the request to OpenAI
                response = openai.ChatCompletion.create(
                    model=GPT_MODEL,
                    messages=messages
                )

                print(" Done.")

                # add the summarized article to the list of summarized articles
                summarized_content.append({
                    "source": source,
                    "summarized_articles": [article["title"] for article in articles_to_summarize],
                    "summary": response["choices"][0]["message"]["content"]
                })

                break

        # we have finished summarizing all of the articles from this source
        print(f"Finished summarizing {len(articles)} articles from {source}.\n")

    # | Save the summarized articles to a file |
    # V                                        V

    summarized_content_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data", today, "summaries.json")

    with open(summarized_content_path, "w") as f:
        json.dump(summarized_content, f, indent=2)


if __name__ == "__main__":
    run_summary()