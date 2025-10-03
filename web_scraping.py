#Author: Andrew Atwater
#COS482 Homework 1, problem 1: Web Scraping
#9/29/2025

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
import random

service = Service(executable_path = "C:/chromedriver/chromedriver-win64/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")

driver = webdriver.Chrome(service = service, options = options)
url = "https://scholar.google.com/scholar?as_ylo=2023&q=machine+learning&hl=en&as_sdt=0,20"
driver.get(url)
time.sleep(5)

screen_height = driver.execute_script("return window.screen.height;")

WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.gs_ri"))
    )

def humanSleep(low, high):
    time.sleep(random.uniform(low, high))

def scrollViewport(driver, css_card = "div.gs_ri", step_ratio = 0.95, max_steps = 20, max_idle = 3):
    last_count = -1
    idle = 0
    for _ in range(max_steps):
        cards = driver.find_elements(By.CSS_SELECTOR, css_card)
        count = len(cards)
        if count == last_count:
            idle += 1
        else:
            idle, last_count = 0, count
        
        #check to see if at bottom

        bottom = driver.execute_script(
            "return (window.scrollY + window.innerHeight) >= "
            "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight) -2;"
        )

        if bottom and idle >= max_idle:
            break

        driver.execute_script("window.scrollBy(0, Math.floor(window.innerHeight * arguments[0]));", step_ratio)
        humanSleep(1.0, 1.2)

def nextPage():
    next_button = driver.find_element(By.XPATH, '//*[@class = "gs_ico gs_ico_nav_next"]')
    try:    
        if next_button:
            driver.execute_script("arguments[0].click();", next_button)
            page_num += 1
    except Exception:
        pass

def scrapePage(driver):
    rows = []

    WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.gs_ri"))
    )

    scrollViewport(driver, css_card = "div.gs_ri", step_ratio = 0.95, max_steps = 20, max_idle = 3)

    cards = driver.find_elements(By.CSS_SELECTOR, "div.gs_ri")
    for c in cards:
        try:
            title_el = c.find_element(By.CSS_SELECTOR, "h3.gs_rt")
            title = title_el.text.strip()
        except Exception:
            title = ""
        humanSleep(0.5, 1.2)
        try:
            pubinfo_el = c.find_element(By.CSS_SELECTOR, "div.gs_a")
            pubInfo = pubinfo_el.text.strip()
        except Exception:
            pubInfo = ""
        humanSleep(0.7, 1.5)
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

def startScrape():
    all_rows = []
    page_index = 1

    while page_index <= 50:
        page_rows = scrapePage(driver)
        all_rows.extend(page_rows)

        nextPage()
        page_index += 1

    return all_rows

def main():
    data = startScrape()
    
    frame = pd.DataFrame(data, columns = ["title", "publication_info", "cited_by"])

    #drop whitespace convert citations to ints
    frame["title"] = frame["title"].fillna("").str.strip()
    frame["publication_info"] = frame["publication_info"].fillna("").str.strip()
    frame["cited_by"] = pd.to_numeric(frame.get("cited_by", 0), errors="coerce").fillna(0).astype(int)

    savename = "google_scholar_scrape_ML.csv"
    frame.to_csv(savename, index = False, encoding = "utf-8")

    driver.quit()

if __name__ == "__main__":
    main()