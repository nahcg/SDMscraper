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
browser.get("https://shop.shoppersdrugmart.ca/Shop/L%E2%80%99Or%C3%A9al-Paris/c/L%27OREAL?sort=trending&page=0")
time.sleep(3)
soup = BeautifulSoup(browser.page_source, 'lxml')

link = []

while True:
    try:
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
        browser.find_element(By.XPATH,"//ul[@class='plp__paginationNav__tl-xo']/li[3]/button[@class='lds__button plp__activePage__1Py_J plp__listItemBtn__1mEJZ']")
        soup = BeautifulSoup(browser.page_source, 'lxml')
        links = browser.find_elements(By.XPATH, "//div[@class='plp__productResultsBody__3f9qv']/a")
        for l in links:
            link.append(l.get_attribute("href"))
        break

    except NoSuchElementException:

        soup = BeautifulSoup(browser.page_source, 'lxml')
        links = browser.find_elements(By.XPATH, "//div[@class='plp__productResultsBody__3f9qv']/a")
        for l in links:
            link.append(l.get_attribute("href"))

        click = browser.find_element(By.XPATH,"//button[@class='lds__button plp__pageDirect__3mIJR' and @data-testid='pagination-button-right']").click()  


links = pd.DataFrame(link)
links.to_csv('links.csv', encoding='utf-8-sig')

p_final = []
u_final = []
n_final = []
pr_final = []
reg_final = []


for i in link:
    browser.get(i)
    time.sleep(1)
    prods = []
    upc = []
    names = []
    prices = []
    regprices = []

    products = browser.find_elements(By.XPATH, "//div[@class='plp__chipWrapper__2OEZ- plp__colorChip__3X8o-']/button")
    products2 = browser.find_elements(By.XPATH, "//label[@class='plp__label__OdGJu plp__sizeChipLabel__2-sdZ']/input")
    products3 = browser.find_element(By.XPATH, "//div[@class='plp__productInfo__13I0m']//h1[@class='plp__pageHeading__zUcEq plp__productName__2Ci77 plp__productName__1evR8']").get_attribute("innerHTML")
    if len(products) != 0:
        for p in products:
            prods.append(p.get_attribute("value"))
    elif len(products2) != 0:
        for p in products2:
            prods.append(p.get_attribute("value"))
    else:
        products3 = browser.find_element(By.XPATH, "//div[@class='plp__productInfo__13I0m']//h1[@class='plp__pageHeading__zUcEq plp__productName__2Ci77 plp__productName__1evR8']").get_attribute("innerHTML")
        prods.append(products3)
       

    upcs = browser.find_elements(By.XPATH, "//div[@class='plp__chipWrapper__2OEZ- plp__colorChip__3X8o-']/button")
    upcs2 = browser.find_elements(By.XPATH, "//label[@class='plp__label__OdGJu plp__sizeChipLabel__2-sdZ']/input")
    upcs3 = browser.find_element(By.XPATH, "//p[@class='plp__body__3TvTa']").get_attribute("innerHTML")
    if len(upcs) != 0:
        for u in upcs:
            upc.append(u.get_attribute("id"))
    elif len(upcs2) != 0:
        for u in upcs2:
            upc.append(u.get_attribute("id"))
    else:
        upcs3 = browser.find_element(By.XPATH, "//p[@class='plp__body__3TvTa']").get_attribute("innerHTML")
        upc.append(upcs3)
        
    name = browser.find_element(By.XPATH, "//h1[@class='plp__pageHeading__zUcEq plp__productName__2Ci77 plp__productName__1evR8']").get_attribute("innerHTML")
    names = [name for i in range(len(upc))]

    price = browser.find_element(By.XPATH, "//p[@data-testid='price-container']").get_attribute("innerHTML")
    s = re.search("(?(?=[0-9,\.]+\s)([0-9,\.]+(\s..\s)\$[0-9,\.]+)|[0-9,\.]+)", price).group()
    prices = [s for i in range(len(upc))]

    try:
        regprice = browser.find_element(By.XPATH, "//span[@class='plp__priceStrikeThrough__2MAlQ plp__price__325EX plp__strikeThrough__2ay0z']").get_attribute("innerHTML")
        regprices.append(regprice)
    except NoSuchElementException:
        regprices.append("NaN")
        
    p_final.extend(prods)
    u_final.extend(upc)
    n_final.extend(names)
    pr_final.extend(prices)
    reg_final.extend(regprices)
    
            
df1 = pd.DataFrame(p_final)
df2 = pd.DataFrame(u_final)
df3 = pd.DataFrame(n_final)
df4 = pd.DataFrame(pr_final)
df5 = pd.DataFrame(reg_final)

df1 = df1.stack().apply(html.unescape).unstack()
df2 = df2.stack().apply(html.unescape).unstack()
df3 = df3.stack().apply(html.unescape).unstack()
df4 = df4.stack().apply(html.unescape).unstack()
df5 = df5.stack().apply(html.unescape).unstack()

df1.to_csv('loreal1.csv', encoding='utf-8-sig')
df2.to_csv('loreal2.csv', encoding='utf-8-sig')
df3.to_csv('loreal3.csv', encoding='utf-8-sig')
df4.to_csv('loreal4.csv', encoding='utf-8-sig')
df5.to_csv('loreal5.csv', encoding='utf-8-sig')
