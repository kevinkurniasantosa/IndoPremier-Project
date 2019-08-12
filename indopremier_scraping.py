from bs4 import BeautifulSoup
import time
import logging
import re
import urllib
import requests
import os
import csv
from datetime import date
import string
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

print('import success')

main_url = 'https://www.indopremier.com/ipotfund/listreksadana.php'

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=chrome_options)
driver.get(main_url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
wait = WebDriverWait(driver, 10)

table_container = wait.until(lambda driver: driver.find_element_by_xpath("//table[@id='fundSelectorAll']"))
list_fund = table_container.find_element_by_tag_name('tbody').find_elements_by_xpath("//tr[@role='row']")

print('Num of Funds: ' + str(len(list_fund)))

for x in range(len(list_fund)):
	# driver.find_element_by_xpath("//div[@role='feed']/div[{}]/div[1]/div[3]/div[1]/div[2]/div[3]/div[1]/div[2]/div/a[@class='_5dec _xcx']".format(loop))).click()
    # Fund Name
    fund_name = driver.find_element_by_xpath("//table[@id='fundSelectorAll']/tbody/tr[{}]/td[@class='text-left fundname all sorting_1']".format(x)).text.strip()
    print(fund_name)

    print(driver.find_element_by_xpath("//table[@id='fundSelectorAll']/tbody/tr[{}]/td[@class='text-left fundname all sorting_1']".format(x)).text.strip())
    








# Sucorinvest Maxi
# Sucorinvest Flexi Fund
# Sucorinvest Equity Fund
# Sucorinvest Sharia Equity Fund
# Shinhan Balance Fund
# Simas Saham Unggulan
# Premier ETF Sri-Kehati
# Prospera Balance
# Simas Syariah Unggulan
# Prospera Saham SMC
