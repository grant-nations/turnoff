from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import datetime
import re
import time

current_date = datetime.datetime.now()
year = current_date.year
month = f"{current_date.month:02d}"  # Zero-padded month (e.g. 06, 07, ...)
day = f"{current_date.day:02d}"  # Zero-padded day (e.g. 01, 02, ...)

today_pattern = rf"/{year}/{month}/{day}/.*"

options = Options()
options.set_preference('javascript.enabled', False)
driver = webdriver.Firefox(options=options)

base_url = 'https://www.nytimes.com'
us_url = base_url + '/section/us'

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

# list of dictionaries with title, article summary, and paragraph text
articles = []

# get the content of each page
for page in today_pages:
    time.sleep(2)  # don't wake up the NYT
    driver.get(page)

    article = driver.find_element(by=By.TAG_NAME, value="article")

    title = article.find_element(by=By.TAG_NAME, value="h1").text
    summary = article.find_element(by=By.ID, value="article-summary").text
    article_body = article.find_element(by=By.NAME, value="articleBody")
    paragraphs = article_body.find_elements(by=By.TAG_NAME, value="p")

    article_text = '\n'.join([p.text for p in paragraphs])

    print("----------------------------------")
    print(f"Title: {title}")
    print(f"subtitle: {summary}")
    print(f"Text: {article_text}")
    print("----------------------------------\n")

    articles.append({
        'title': title,
        'subtitle': summary,
        'text': article_text
    })


driver.quit()
