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


browser=webdriver.Chrome()
time.sleep(2)
browser.set_page_load_timeout(60000)
soup = BeautifulSoup(browser.page_source, 'lxml')

link = []
with open('C:\\Users\\H513527\\AppData\\Local\\Programs\\Python\\Python310\\sdmlinks3pagesc.csv', newline='') as inputfile:
    csvreader = csv.reader(inputfile)
    next(csvreader)
    for row in csvreader:
        link.append(row[1])

p_final = []
u_final = []
n_final = []
b_final = []
pr_final = []
s_final = []
reg_final = []


for i in link:
    browser.get(i)
    time.sleep(1.5)
    prods = []
    upc = []
    names = []
    brands = []
    prices = []
    sizes = []
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
        upcs3 = re.search('(?<=#).*', upcs3)
        upcs3 = upcs3.group(0)
        upc.append(upcs3)
        
    name = browser.find_element(By.XPATH, "//h1[@class='plp__pageHeading__zUcEq plp__productName__2Ci77 plp__productName__1evR8']").get_attribute("innerHTML")
    names = [name for i in range(len(upc))]

    brand = browser.find_element(By.XPATH, "//div[@class='plp__productInfo__13I0m']/p[@class='plp__brandName__8MSID']/a").get_attribute("innerHTML")
    brands = [brand for i in range(len(upc))]
    
    size = browser.find_element(By.XPATH, "//div[@class='plp__container__wxmKh']//p[@class='plp__variantName__tiEnh']").get_attribute("innerHTML")
    sizes = [size for i in range(len(upc))]

    price = browser.find_element(By.XPATH, "//p[@data-testid='price-container']").get_attribute("innerHTML")
    s = re.search("(?(?=[0-9,\.]+\s)([0-9,\.]+(\s..\s)\$[0-9,\.]+)|[0-9,\.]+)", price).group()
    prices = [s for i in range(len(upc))]

    try:
        regprice = browser.find_element(By.XPATH, "//span[@class='plp__priceStrikeThrough__2MAlQ plp__price__325EX plp__strikeThrough__2ay0z']").get_attribute("innerHTML")
        regprices = [regprice for i in range(len(upc))]
    except NoSuchElementException:
        regprices = ["NaN" for i in range(len(upc))]

    p_final.extend(prods)
    u_final.extend(upc)
    n_final.extend(names)
    b_final.extend(brands)
    pr_final.extend(prices)
    s_final.extend(sizes)
    reg_final.extend(regprices)
    
            
df1 = pd.DataFrame(n_final)
df2 = pd.DataFrame(s_final)
df3 = pd.DataFrame(p_final)
df4 = pd.DataFrame(b_final)
df5 = pd.DataFrame(pr_final)
df6 = pd.DataFrame(reg_final)
df7 = pd.DataFrame(u_final)

df1 = df1.stack().apply(html.unescape).unstack()
df2 = df2.stack().apply(html.unescape).unstack()
df3 = df3.stack().apply(html.unescape).unstack()
df4 = df4.stack().apply(html.unescape).unstack()
df5 = df5.stack().apply(html.unescape).unstack()
df6 = df6.stack().apply(html.unescape).unstack()
df7 = df7.stack().apply(html.unescape).unstack()

frames = [df1, df2, df3, df4, df5, df6, df7]

result = pd.concat(frames, axis=1, join = "inner")

result.to_csv('sdmoutput1page5.csv', encoding='utf-8-sig')
