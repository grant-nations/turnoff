from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bots.news_bot import NewsBot
import re
import time
from typing import List, Dict

class FoxBot(NewsBot):

    def __init__(self):
        super().__init__("Fox")

    def get_articles(self) -> List[Dict[str, str]]:
        """
        Get the articles from the Fox News US section

        :return: list of dictionaries with source, title, subtitle, and text
        """

        today_pattern = r"(\d+)\s+(hour|hours|min|mins|minute|minutes)\s+ago"

        options = Options()
        options.set_preference('javascript.enabled', False)
        driver = webdriver.Firefox(options=options)

        base_url = 'https://foxnews.com'
        us_url = base_url + '/us'

        driver.get(us_url)

        driver.implicitly_wait(1)

        today_pages = []

        # get the main content div
        main_content = driver.find_element(by=By.CLASS_NAME, value="main-content")

        # the main content div contains articles (FIND THEM)
        main_articles = main_content.find_elements(by=By.TAG_NAME, value="article")

        # each article has a time stamp (FIND IT)
        for article in main_articles:
            article_time = article.find_element(by=By.CLASS_NAME, value="time").text
            if article_time and re.search(today_pattern, article_time):
                # if the time stamp is today, then add the article to the list of today's articles
                title = article.find_element(by=By.CLASS_NAME, value="title")
                a_tag = title.find_element(by=By.TAG_NAME, value="a")
                href = a_tag.get_attribute("href")
                today_pages.append(href)

        # remove duplicates (not likely)
        today_pages = list(set(today_pages))

        # list of dictionaries with title, article summary, and paragraph text
        articles = []

        # get the content of each page
        for page in today_pages:
            time.sleep(2)  # don't wake up the fox
            driver.get(page)

            article = driver.find_element(by=By.CLASS_NAME, value="main-content")

            title = article.find_element(by=By.CLASS_NAME, value="headline").text
            subtitle = article.find_element(by=By.CLASS_NAME, value="sub-headline").text

            article_body = article.find_element(by=By.CLASS_NAME, value="article-body")
            paragraphs = article_body.find_elements(by=By.TAG_NAME, value="p")

            article_text = ""

            for p in paragraphs:
                # skip the "strong" tags (they're links to other articles)
                if not p.find_elements(by=By.TAG_NAME, value="strong"):
                    article_text += p.text + "\n"

            articles.append({
                'source': "Fox",
                'title': title,
                'subtitle': subtitle,
                'text': article_text
            })

        driver.quit()

        return articles
