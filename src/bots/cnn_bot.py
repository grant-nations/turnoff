from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from src.bots.news_bot import NewsBot
import datetime
import re
import time
from typing import List, Dict


class CNNBot(NewsBot):

    def __init__(self):
        super().__init__("CNN")

    def get_articles(self) -> List[Dict[str, str]]:
        """
        Get the articles from the CNN US section

        :return: list of dictionaries with source, title, subtitle, and text
        """

        current_date = datetime.datetime.now()
        year = current_date.year
        month = f"{current_date.month:02d}"  # Zero-padded month (e.g. 06, 07, ...)
        day = f"{current_date.day:02d}"  # Zero-padded day (e.g. 01, 02, ...)

        today_pattern = rf"/{year}/{month}/{day}/.*"

        options = Options()
        options.set_preference('javascript.enabled', False)
        driver = webdriver.Firefox(options=options)

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

        # get the content of each page
        for page in today_pages:
            time.sleep(2)  # don't wake up the CNN weblorbs
            driver.get(page)

            headline = driver.find_element(by=By.CLASS_NAME, value="headline")

            title = headline.find_element(by=By.TAG_NAME, value="h1").text

            article = driver.find_element(by=By.TAG_NAME, value="article")
            article_body = article.find_element(by=By.CLASS_NAME, value="body")
            paragraphs = article_body.find_elements(by=By.TAG_NAME, value="p")

            paragraphs_text = [p.text for p in paragraphs]

            article_text = '\n'.join(paragraphs_text)

            articles.append({
                'source': self.name,
                'title': title,
                'subtitle': "",  # NOTE: CNN articles don't have subtitles
                'text': article_text
            })

        driver.quit()

        return articles
