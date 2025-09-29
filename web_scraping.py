#Author: Andrew Atwater
#COS482 Homework 1, problem 1: Web Scraping
#9/29/2025
"""
In this task, you will scrape the Google Scholar pages for articles related to machine learning
published since year 2023:
https://scholar.google.com/scholar?as_ylo=2023&q=machine+learning&hl=en&as_sdt=0,20
The above link will take you to the first page of the Google Scholar search results using the
keyword “machine learning” and specifying the years of publication to be 2023 or later. However,
there are more than one page of search results.
Your task is to scrape all pages of the above search results, and collect the following information
about each article: title, publication information (including authors, publication venue, year, and
publisher), and the number of times the article has been cited by other articles. You should
construct a Pandas’ dataframe to hold the above information for each article. Your dataframe
should look like: (see homework)
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

service = Service(executable_path = "/chromedriver/chromedriver-win64")
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")

driver = webdriver.Chrome(service = service, options = options)

driver.get("https://scholar.google.com/scholar?as_ylo=2023&q=machine+learning&hl=en&as_sdt=0,20")
time.sleep(5)

scroll_pause_time = 10

screen_height = driver.execute_script("return window.screen.height;")

i = 1
while True:
    driver.execute_script("window.scrollTo(0, {screen_height} * {i});").format(
        screen_height = screen_height, i = i
    )
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    if ((screen_height*i > scroll_height) or (i > 20)):
        break