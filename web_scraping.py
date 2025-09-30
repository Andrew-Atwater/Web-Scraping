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

service = Service(executable_path = "/chromedriver/chromedriver-win64")
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")

driver = webdriver.Chrome(service = service, options = options)
url = "https://scholar.google.com/scholar?as_ylo=2023&q=machine+learning&hl=en&as_sdt=0,20"
driver.get(url)
time.sleep(5)

screen_height = driver.execute_script("return window.screen.height;")

def humanSleep(low = 0.5, high = 2.0):
    time.sleep(random.uniform(low, high))

def scroll():
    i = 1
    while True: #scroll function
        driver.execute_script("window.scrollTo(0, {screen_height} * {i});").format( #setting up window size, scroll speed
            screen_height = screen_height, i = i
        )
        i += 1
        humanSleep()
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if (screen_height*i > scroll_height):
            break

def nextPage():
    next_button = driver.find_element(By.XPATH, '//*[@class = "gs_ico gs_ico_nav_next"]')
    try:    
        if next_button:
            driver.execute_script("arguments[0].click();", next_button)
    except Exception:
        pass

def startScrape():
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
        humanSleep()
        try:
            pubinfo_el = c.find_element(By.CSS_SELECTOR, "div.gs_a")
            pubInfo = pubinfo_el.text.strip()
        except Exception:
            pubInfo = ""
        humanSleep()
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
        try:
            scroll()
            humanSleep()
        except Exception:
            humanSleep()
            nextPage()
            humanSleep()
    return rows

def main():
    startScrape()
    driver.close()

if __name__ == "__main__":
    main()