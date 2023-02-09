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
soup = BeautifulSoup(browser.page_source, 'lxml')

link = []
with open('C:\\Users\\H513527\\AppData\\Local\\Programs\\Python\\Python310\\wellmakeuplinks.csv', newline='') as inputfile:
    csvreader = csv.reader(inputfile)
    next(csvreader)
    for row in csvreader:
        link.append(row[1])

b_final = []
n_final = []
d_final = []
curr_final = []
reg_final = []


for i in link:
    browser.get(i)
    time.sleep(1)
    brand = []
    name = []
    desc = []
    currprice = []
    regprice = []

    brands = browser.find_elements(By.XPATH, "//div[@class='col-xs-12 product-info__mobileheading']/a")
    for b in brands:
        brand.append(b.get_attribute("innerHTML"))

    names = browser.find_elements(By.XPATH, "//div[@class='col-xs-12 product-info__mobileheading']/span")
    for n in names:
        name.append(n.get_attribute("innerHTML"))

    descs = browser.find_elements(By.XPATH, "//div[@class='product-info__heading']/p[@class='product-info__subtitle']/span[2]")
    for d in descs:
        desc.append(d.get_attribute("innerHTML"))

    prices = browser.find_elements(By.XPATH, "//div[@class='col-xs-12 product-info__mobileheading']/div[@class='product-info__price']/p[@class='price']")
    prices2 = browser.find_elements(By.XPATH, "//div[@class='col-xs-12 product-info__mobileheading']/div[@class='product-info__price']/p[@class='price old_price']")
    prices3 = browser.find_elements(By.XPATH, "//div[@class='col-xs-12 product-info__mobileheading']/div[@class='product-info__price']/p[@class='price new_price']")
    if len(prices) != 0:
        for p in prices:
            currprice.append(p.get_attribute("innerHTML"))
            regprice.append(p.get_attribute("innerHTML"))
    elif len(prices2) != 0:
        for q in prices2:
            currprice.append(q.get_attribute("innerHTML"))
    elif len(prices3) !=0:
        for r in prices3:
            regprice.append(r.get_attribute("innerHTML"))

    b_final.extend(brand)
    n_final.extend(name)
    d_final.extend(desc)
    curr_final.extend(currprice)
    reg_final.extend(regprice)
            
df1 = pd.DataFrame(b_final)
df2 = pd.DataFrame(n_final)
df3 = pd.DataFrame(d_final)
df4 = pd.DataFrame(curr_final)
df5 = pd.DataFrame(reg_final)

df1 = df1.stack().apply(html.unescape).unstack()
df2 = df2.stack().apply(html.unescape).unstack()
df3 = df3.stack().apply(html.unescape).unstack()
df4 = df4.stack().apply(html.unescape).unstack()
df5 = df5.stack().apply(html.unescape).unstack()

frames = [df1, df2, df3, df4, df5]

result = pd.concat(frames, axis=1, join = "inner")

result.to_csv('welltest.csv', encoding='utf-8-sig')
