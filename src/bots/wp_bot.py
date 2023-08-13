from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from src.bots.bot import Bot
import datetime
import re
import time
from typing import List, Dict, Tuple


class WPBot(Bot):

    def __init__(self):
        super().__init__("Washington Post")

    def get_articles(self) -> Tuple[List[Dict[str, str]],
                                    List[Dict[str, str]]]:
        """
        Get the articles from the Washington Post

        :return: Tuple:
            list of dictionaries with title, subtitle, and text of each article
            list of dictionaries with failed pages and their exceptions
        """

        current_date = datetime.datetime.now()
        year = current_date.year
        month = f"{current_date.month:02d}"  # Zero-padded month (e.g. 06, 07, ...)
        day = f"{current_date.day:02d}"  # Zero-padded day (e.g. 01, 02, ...)

        today_pattern = rf".*/{year}/{month}/{day}/.*"

        options = Options()
        options.set_preference('javascript.enabled', False)
        driver = webdriver.Firefox(options=options)

        us_url = 'https://www.washingtonpost.com'

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

        # remove opinion pages
        # TODO:
        for page in today_pages:
            print(page)

        # list of dictionaries with title, article summary, and paragraph text
        articles = []

        # list of failed pages and their exceptions
        failed_pages = []

        # get the content of each page
        for page in today_pages:
            try:
                time.sleep(2)  # don't wake up the Washington Post caterpillars
                driver.get(page)

                title = driver.find_element(by=By.TAG_NAME, value="h1").text

                subtitle = ""
                try:
                    subtitle = driver.find_element(by=By.TAG_NAME, value="h2").text
                except:
                    pass

                article = driver.find_element(by=By.TAG_NAME, value="article")
                paragraphs = article.find_elements(by=By.TAG_NAME, value="p")

                paragraphs_text = [p.text for p in paragraphs]

                article_text = '\n'.join(paragraphs_text)

                articles.append({
                    'title': title,
                    'subtitle': subtitle,
                    'text': article_text
                })
            except Exception as e:
                failed_pages.append({
                    'page': page,
                    'exception': str(e)
                })

        driver.quit()

        return articles, failed_pages
