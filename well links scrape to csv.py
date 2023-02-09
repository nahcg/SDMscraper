from bs4 import BeautifulSoup 
from selenium import webdriver
import pandas as pd
import time
import csv
import regex as re
import html
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


browser=webdriver.Chrome()
browser.get("https://well.ca/categories/makeup_4215.html")
footer = browser.find_element(By.XPATH, "//a[@id='next']")
browser.execute_script("arguments[0].scrollIntoView();", footer)
time.sleep(5)
browser.switch_to.frame("ju_iframe_838978")
browser.find_element(By.XPATH, "//form[@id='justuno_form']/div[@class='design-layer vcenter']/div[@class='frame-container']/div[@class='design-layer vcenter']/div[@class='design-layer-editable']").click()
browser.switch_to.default_content()
time.sleep(1)
link = []

while True:
    try:
        browser.find_element(By.XPATH, "//div[@id='categories_main_content']/div[@id='infscr-loading']/div[@class='content']/div[@style='opacity: 1;']")
        break  
    except NoSuchElementException:
        browser.execute_script("arguments[0].scrollIntoView();", footer)    

soup = BeautifulSoup(browser.page_source, 'lxml')
links = browser.find_elements(By.XPATH, "//div[@class='grid__item col-md-3 col-sm-4 col-xs-6']/div/a")
for l in links:
    link.append(l.get_attribute("href"))

df = pd.DataFrame(link)
df.to_csv("wellmakeuplinks.csv")

