from bs4 import BeautifulSoup 
from selenium import webdriver
import pandas as pd
import time
import csv
import regex as re
import html
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')

browser=webdriver.Chrome()

link = []
with open('C:\\Users\\callm\\Desktop\\scraper\\3pagelinksmckesson.csv', newline='') as inputfile:
    csvreader = csv.reader(inputfile)
    next(csvreader)
    for row in csvreader:
        link.append(row[1])

l_final = []

for i in link:
    browser.get(i)
    time.sleep(4)
    soup = BeautifulSoup(browser.page_source, 'lxml')

    hrefs2 = []
    
    while True:
        try:
            hrefs3 = []
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
            browser.find_element(By.XPATH,"//ul[@class='plp__paginationNav__tl-xo']/li[3]/button[@class='lds__button plp__activePage__1Py_J plp__listItemBtn__1mEJZ']")
            soup = BeautifulSoup(browser.page_source, 'lxml')
            links = browser.find_elements(By.XPATH, "//div[@class='plp__productResultsBody__3f9qv']/a")
            time.sleep(2)
            for l in links:
                hrefs3.append(l.get_attribute("href"))

            hrefs2.extend(hrefs3)
            
            break

        except NoSuchElementException:

            hrefs = []
            soup = BeautifulSoup(browser.page_source, 'lxml')
            links2 = browser.find_elements(By.XPATH, "//div[@class='plp__productResultsBody__3f9qv']/a")
            time.sleep(2)
            for z in links2:
                hrefs.append(z.get_attribute("href"))
            time.sleep(2)
            
            hrefs2.extend(hrefs)
            time.sleep(1)
            
            findclick = browser.find_element(By.XPATH,"//button[@class='lds__button plp__pageDirect__3mIJR' and @data-testid='pagination-button-right']")
            browser.execute_script("arguments[0].click();", findclick)

    
    l_final.extend(hrefs2)

links = pd.DataFrame(l_final)
links.to_csv('sdmlinks3pagestest.csv', encoding='utf-8-sig')
