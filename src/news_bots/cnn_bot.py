from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from src.news_bots.news_bot import NewsBot
# import datetime
import re
import time
from typing import List, Dict, Tuple
from src.utils import get_current_date_string

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

class CNNBot(NewsBot):

    def __init__(self):
        super().__init__("CNN")

    def get_articles(self) -> Tuple[List[Dict[str, str]],
                                    List[Dict[str, str]]]:
        """
        Get today's articles from CNN

        :return: Tuple:
            list of dictionaries with title, subtitle, and text of each article
            list of dictionaries with failed pages and their exceptions
        """

        today_pattern = rf"/{get_current_date_string(separator='/')}/.*"

        options = Options()
        options.set_preference('javascript.enabled', False)

        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

        # driver = webdriver.Firefox(options=options)

        us_url = 'https://www.cnn.com/us'

        driver.get(us_url)

        driver.implicitly_wait(1)

        anchor_tags = driver.find_elements(by=By.TAG_NAME, value="a")

        today_pages = []

        for a_tag in anchor_tags:
            href = a_tag.get_attribute("href")
            if href and re.search(today_pattern, href):
                today_pages.append(href)

        # remove duplicates
        today_pages = list(set(today_pages))

        html_pattern = re.compile(r".*\.html$")
        today_pages = [page for page in today_pages if re.search(html_pattern, page)]

        # list of dictionaries with title, article summary, and paragraph text
        articles = []

        # list of dictionaries with failed pages and their exceptions
        failed_pages = []

        # get the content of each page
        for page in today_pages:
            try:
                time.sleep(2)  # don't wake up the CNN weblorbs
                driver.get(page)

                title = driver.find_element(by=By.TAG_NAME, value="h1").text

                article = driver.find_element(by=By.TAG_NAME, value="article")
                article_body = None
                try:
                    article_body = article.find_element(by=By.CLASS_NAME, value="body")
                except:
                    try:
                        article_body = article.find_element(by=By.ID, value="body-text")
                    except Exception as e:
                        raise e
                    
                paragraphs = article_body.find_elements(by=By.TAG_NAME, value="p")

                paragraphs_text = [p.text for p in paragraphs]

                article_text = '\n'.join(paragraphs_text)

                articles.append({
                    'title': title,
                    'subtitle': "",  # NOTE: CNN articles don't have subtitles
                    'text': article_text
                })
            except Exception as e:
                failed_pages.append({
                    'page': page,
                    'exception': str(e)
                })

        driver.quit()

        return articles, failed_pages

if __name__ == "__main__":
    bot = CNNBot()
    articles, failed_pages = bot.get_articles()
    print(articles)
    print(failed_pages)