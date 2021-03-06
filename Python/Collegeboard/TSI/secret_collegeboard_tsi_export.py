#!/bin/python
# ===========================================================
# Created By: Richard Barrett
# Organization: DVISD
# DepartmenT: Data Services
# Purpose: Test Score & 3rd Party Website Data Pull Automation
# Date: 01/20/2020
# ===========================================================

import selenium
import shutil
import xlsxwriter
import os
import unittest
import requests
import subprocess
import getpass
import platform
import logging
import time 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 
from datetime import date

decrypt = "gpg --output secrets_test.json --decrypt secrets.gpg" 

if os.path.exists("secrets.gpg"):
      returned_value = subprocess.call(decrypt, shell=True)
else:
        print("The file does not exist")
            
import json
with open('secrets_test.json','r') as f:
      config = json.load(f)

# Definitions
# find_elements_by_name
# find_elements_by_xpath
# find_elements_by_link_text
# find_elements_by_partial_link_text
# find_elements_by_tag_name
# find_elements_by_class_name
# find_elements_by_css_selector

# System Variables
today = date.today()
date = today.strftime("%m/%d/%Y")
node = platform.node()
system = platform.system()
username = getpass.getuser()
version = platform.version()
current_directory = os.getcwd()

# URL Variables 
login_url = 'https://www.accuplacer.org/'
redirect_url = 'https://www.accuplacer.org/api/home.html#/'
reports_scheduler_url = 'https://www.accuplacer.org/api/home.html#/reportScheduler'
custom_reports_url = 'https://www.accuplacer.org/api/home.html#/customReports'

# Check for Version of Chrome

# Options 
#options = webdriver.ChromeOptions() 
#options.add_argument("download.default_directory=current_directory", "--headless")

# WebDriver Path for System
if platform.system() == ('Windows'):
    browser = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\chromedriver.exe")
elif platform.system() == ('Linux'):
    browser = webdriver.Chrome(executable_path='/home/rbarrett/Drivers/Google/Chrome/chromedriver_linux64/chromedriver')
elif platform.system() == ('Darwin'):
    browser = webdriver(executable_path='~/Drivers/Google/Chrome/chromedriver_mac64/chromedriver')
else:
    print("Are you sure you have the Selenium Webdriver installed in the correct path?")
      
# Parent URL
browser.get("https://www.accuplacer.org")

# Credentials NEEDS UNIT TEST
username = browser.find_element_by_id("login")
password = browser.find_element_by_id("password")
username.send_keys(config['user']['name'])
password.send_keys(config['user']['password'])

# UI Container Handle for Notifications Window that Pops Up. 

# Authentication submit.click()
# For XPATH = //*[@id='loginContainer']/form/footer/button
element = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='loginContainer']/form/footer/button")))
element.click();
print("Logging into Collegeboard Accuplacer System!")

# Navigate to Report
element = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Reports")))
element.click();

element = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Custom Reports")))
element.click();
print("Custom Reports Navigation Selected...")

# Make the Report
# Step 1 - Click Dropdown Menu and Load Current Year Query
element = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='loadSavedQueryCustomReport']/option[text()='All TSI Scores 2020']")))
element.click();
print("Current Year Query has been selected...")

# Step 2 - Create and Load Dynamic Name for Custom Report with System Call to $Date Dependent on OS in Format of TSI_SCORES_$YEAR_$DATE_LAST_RUN
# Powershell Variable = $(Get-Date -Format "yyyy")
# Linux & Mac Variable = $(date +%F)
# Element XPATH = //*[@id="reportDescriptionCustomReport"]
description = browser.find_element_by_id('reportDescriptionCustomReport')
description.send_keys("NameNeedsFormatting")
print("Report has been named and staged for submission...")

# Step 3 - Filter by Criteria
# Click Plus Button on Index(1)
element = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='rptSearchCollapsible']/div[2]/div[1]/h3/a/i[1]")))
element.click();

# Click Calendar Icon
# Element XPATH = //*[@id='collapseFour-1']/div/fieldset/import-date-select/div[1]/div[3]/div/span/button/i
element = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='collapseFour-1']/div/fieldset/import-date-select/div[1]/div[3]/div/span/button/i")))
element.click();
print("Calendar Selection being made...")

# Click Today Button on Calendar
# Element XPATH = //*[@id='collapseFour-1']/div/fieldset/import-date-select/div[1]/div[3]/div/ul/li[2]/span/button[1]
element = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='collapseFour-1']/div/fieldset/import-date-select/div[1]/div[3]/div/ul/li[2]/span/button[1]")))
element.click();
time.sleep(2)
print("Date is selected as current date...")

#NEED TO PUT AN IF FUNCION AND UNIT TEST FOR SESSION TIMEOUTS!!!
#browser.get("https://www.accuplacer.org/api/home.html#/customReports")
#Download the report
# Click Submit Button
element = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='rptSearchCollapsible']/div[5]/div/button")))
element.click();
print("Query submission successful!")

# Click Download Button
# Element XPATH = //*[@id='rptd']/div[2]/a
element = WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='rptd']/div[2]/a")))
element.click();
print("Download button was pressed!")

# NEED TO PUT AN IF FUNCION AND UNIT TEST FOR SESSION TIMEOUTS!!!
# Quit the Webbrowser
time.sleep(5)

# Delete the Encrypted File
if os.path.exists("secrets_test.json"):
  os.remove("secrets_test.json")
  print("The file was removed and everything is clean!")
else:
  print("The file does not exist")

print("The download was successfull!")
browser.quit()

# Format Downloaded File to District Specifications
