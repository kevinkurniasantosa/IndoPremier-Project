from bs4 import BeautifulSoup
import time
import logging
import re
import urllib
import requests
import os
import csv
from datetime import datetime
import string
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pygsheets

print('import success')

today_date = datetime.now().strftime('%m/%d/%Y').lstrip("0").replace(" 0", " ")
main_url = 'https://www.indopremier.com/ipotfund/listreksadana.php'
nab = []

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=chrome_options)
driver.get(main_url)

def scraping_indopremier():
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        wait = WebDriverWait(driver, 10)

        table_container = wait.until(lambda driver: driver.find_element_by_xpath("//table[@id='fundSelectorAll']"))
        list_fund = table_container.find_element_by_tag_name('tbody').find_elements_by_xpath("//tr[@role='row']")

        print('Scraping IndoPremier(mutual funds) for ' + today_date)
        print('Num of Funds: ' + str(len(list_fund)))
        print('-----------------------------')
        time.sleep(1.5)

        for x in range(len(list_fund)):
            if x == 238:
                break

            # Fund Name
            fund_name = driver.find_element_by_xpath("//table[@id='fundSelectorAll']/tbody/tr[{}]/td[@class='text-left fundname all sorting_1']/a".format(x+1)).text.strip()
            print(fund_name)
            if fund_name == 'Sucorinvest Maxi':
                nab_sm = driver.find_element_by_xpath("//table[@id='fundSelectorAll']/tbody/tr[{}]/td[@class='text-right min-desktops']".format(x+1)).text.strip()
            elif fund_name == 'Sucorinvest Flexi Fund':
                nab_sf = driver.find_element_by_xpath("//table[@id='fundSelectorAll']/tbody/tr[{}]/td[@class='text-right min-desktops']".format(x+1)).text.strip()
            elif fund_name == 'Sucorinvest Equity Fund':
                nab_se = driver.find_element_by_xpath("//table[@id='fundSelectorAll']/tbody/tr[{}]/td[@class='text-right min-desktops']".format(x+1)).text.strip()
            elif fund_name == 'Sucorinvest Sharia Equity Fund':
                nab_ss = driver.find_element_by_xpath("//table[@id='fundSelectorAll']/tbody/tr[{}]/td[@class='text-right min-desktops']".format(x+1)).text.strip()
            elif fund_name == 'Shinhan Balanced Fund':
                nab_sb = driver.find_element_by_xpath("//table[@id='fundSelectorAll']/tbody/tr[{}]/td[@class='text-right min-desktops']".format(x+1)).text.strip()
            elif fund_name == 'Simas Saham Unggulan':
                nab_su = driver.find_element_by_xpath("//table[@id='fundSelectorAll']/tbody/tr[{}]/td[@class='text-right min-desktops']".format(x+1)).text.strip()
            elif fund_name == 'Premier ETF Sri-Kehati':
                nab_pe = driver.find_element_by_xpath("//table[@id='fundSelectorAll']/tbody/tr[{}]/td[@class='text-right min-desktops']".format(x+1)).text.strip()
            elif fund_name == 'Prospera Balance':
                nab_pb = driver.find_element_by_xpath("//table[@id='fundSelectorAll']/tbody/tr[{}]/td[@class='text-right min-desktops']".format(x+1)).text.strip()
            elif fund_name == 'Simas Syariah Unggulan':
                nab_su2 = driver.find_element_by_xpath("//table[@id='fundSelectorAll']/tbody/tr[{}]/td[@class='text-right min-desktops']".format(x+1)).text.strip()
            elif fund_name == 'Prospera Saham SMC':
                nab_ps = driver.find_element_by_xpath("//table[@id='fundSelectorAll']/tbody/tr[{}]/td[@class='text-right min-desktops']".format(x+1)).text.strip() 
                
        nab.append(nab_sm)
        nab.append(nab_sf)
        nab.append(nab_se)
        nab.append(nab_ss)
        nab.append(nab_sb)
        nab.append(nab_su)
        nab.append(nab_pe)
        nab.append(nab_pb)
        nab.append(nab_su2)
        nab.append(nab_ps)

        print('Result NAB(' + today_date + '): ' + str(nab))

        # Write to Google Sheet
        write_to_gsheet(nab_sm, nab_sf, nab_se, nab_ss, nab_sb, nab_su, nab_pe, nab_pb, nab_su2, nab_ps)
    except Exception as err:
        print('Error: ' + str(err))

def write_to_gsheet(nab_sm, nab_sf, nab_se, nab_ss, nab_sb, nab_su, nab_pe, nab_pb, nab_su2, nab_ps):
    try:
        num_of_sheets = 10  # Very important
        gsheet_url = 'https://docs.google.com/spreadsheets/d/1G19TmvJ9fYY0aRnzFq54-HsV1EiA7RgQChbp9qCShz4/edit?ts=5bb0e404#gid=1172999628'
        gsheet_sheet = [
                        'Sucor Maxi Fund', 
                        'Sucor Flexi Fund', 
                        'Sucor Equity Fund', 
                        'Sucor Sharia Eq', 
                        'Shinhan Balanced Fund', 
                        'Simas saham unggulan', 
                        'Premier ETF Sri-Kehati',         
                        'Prospera Balance', 
                        'Siham shariah unggulan', 
                        'Prospera Saham SMC'
                        ]
        gsheet_credential = 'kevin_client_service.json'
                                                        
        gc = pygsheets.authorize(service_file=gsheet_credential)
        wb = gc.open_by_url(gsheet_url)

        for y in range(num_of_sheets): # 0 - 9
            print('---------------------')
            sheet = wb.worksheet_by_title(gsheet_sheet[y])

            # Get last row
            val = filter(None, sheet.get_col(2))
            num_of_rows = len(val) + 1
            print('Num of rows in ' + gsheet_sheet[y] + ': ' + str(num_of_rows))
                
            for row in reversed(range(num_of_rows+1)): # 229 - 0
                if sheet.cell('B' + str(row)).value == today_date:
                    print('Write NAB in ' + gsheet_sheet[y])
                    sheet.update_value('C' + str(row), nab[y]) # v2.0.1
                    break
    except Exception as err:
        print('Error in write_gsheet: ' + str(err))

if __name__ == '__main__':
    scraping_indopremier()