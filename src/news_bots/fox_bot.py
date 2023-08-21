from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from src.news_bots.news_bot import NewsBot
import re
import time
from typing import List, Dict, Tuple
import datetime
from src.utils import month_to_number, is_month_name, print_green, CHECK_MARK, print_red
from selenium.webdriver.firefox.service import Service as FirefoxService


class FoxBot(NewsBot):

    def __init__(self):
        super().__init__("Fox")

    def get_articles(self, verbose: bool = True) -> Tuple[List[Dict[str, str]],
                                                          List[Dict[str, str]]]:
        """
        Get today's articles from Fox

        :return: Tuple:
            list of dictionaries with title, subtitle, and text of each article
            list of dictionaries with failed pages and their exceptions
        """

        today_pattern = r"(\d+)\s+(hour|hours|min|mins|minute|minutes)\s+ago"

        options = Options()
        options.set_preference('javascript.enabled', False)
        options.headless = True
        service = FirefoxService(executable_path="/snap/bin/geckodriver")
        driver = webdriver.Firefox(service=service, options=options)

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
            article_time = article.find_elements(by=By.CLASS_NAME, value="time")
            if article_time:
                article_time = article_time[0].text
                if re.search(today_pattern, article_time):
                    # if the time stamp is today, then add the article to the list of today's articles
                    title = article.find_element(by=By.CLASS_NAME, value="title")
                    a_tag = title.find_element(by=By.TAG_NAME, value="a")
                    href = a_tag.get_attribute("href")
                    today_pages.append(href)
            else:  # no time; this article is probable from today (we will check it later)
                title = article.find_element(by=By.CLASS_NAME, value="title")
                a_tag = title.find_element(by=By.TAG_NAME, value="a")
                href = a_tag.get_attribute("href")
                today_pages.append(href)

        # remove duplicates (not likely)
        today_pages = list(set(today_pages))

        # list of dictionaries with title, article summary, and paragraph text
        articles = []

        # list of dictionaries with failed pages and their exceptions
        failed_pages = []

        # get the content of each page
        for page in today_pages:
            try:
                time.sleep(2)  # don't wake up the fox
                driver.get(page)

                # double check that the page is from today, if not, skip it
                article_time = driver.find_element(by=By.TAG_NAME, value="time").text
                time_elements = article_time.split(" ")

                # sometimes it's "Published April 1, 2021" and sometimes it's "April 1, 2021"
                month_index = 0
                for i in range(len(time_elements)):
                    if is_month_name(time_elements[i]):
                        month_index = i
                        break

                month = month_to_number(time_elements[month_index])  # convert month name to number
                day = int(time_elements[month_index + 1].replace(",", ""))  # remove comma from day
                year = int(time_elements[month_index + 2])

                today = datetime.datetime.today()
                if today.month != month or today.day != day or today.year != year:
                    continue

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
                    'title': title,
                    'subtitle': subtitle,
                    'text': article_text
                })

                if verbose:
                    print_green("  " + CHECK_MARK, end="", flush=True)
                    print(f" {title}")

            except Exception as e:
                failed_pages.append({
                    'page': page,
                    'exception': str(e)
                })

                if verbose:
                    print_red("  X", end="", flush=True)
                    print(f" {page}")

        driver.quit()

        return articles, failed_pages
