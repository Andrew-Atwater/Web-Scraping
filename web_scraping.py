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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd

service = Service(executable_path = "/chromedriver/chromedriver-win64")
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")

driver = webdriver.Chrome(service = service, options = options)
url = "https://scholar.google.com/scholar?as_ylo=2023&q=machine+learning&hl=en&as_sdt=0,20"
driver.get(url)
time.sleep(5)

scroll_pause_time = 10

screen_height = driver.execute_script("return window.screen.height;")

i = 1
while True: #scroll function
    driver.execute_script("window.scrollTo(0, {screen_height} * {i});").format( #setting up window size, scroll speed
        screen_height = screen_height, i = i
    )
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    if ((screen_height*i > scroll_height) or (i > 20)):
        break

def scrapePage():
    rows = []

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.gs_ri"))
    )

    cards = driver.find_elements(By.CSS_SELECTOR, "div.gs_ri")
    for c in cards:
        try:
            title_el = c.find_element(By.CSS_SELECTOR, "h3.gs_rt")
            title = title_el.text.strip()
        except Exception:
            title = ""

        try:
            pubinfo_el = c.find_element(By.CSS_SELECTOR, "div.gs_a")
            pubInfo = pubinfo_el.text.strip()
        except Exception:
            pubInfo = ""

        citedBy = 0
        try:
            footer_links = c.find_elements(By.CSS_SELECTOR, ".gs_fl a")
            for a in footer_links:
                t = a.text.strip()
                if t.startswith("Cited by"):
                    m = re.search(r"Cited by\s+(\d+)", t)
                    if m:
                        citedBy = int(m.group(1))
                    else:
                        citedBy = 0
                    break
        except Exception:
            pass

        rows.append(
            {
                "title" : title,
                "publication_info" : pubInfo,
                "cited_by" : citedBy,
            }
        )
    return rows
