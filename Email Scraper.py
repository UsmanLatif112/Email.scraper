# Imports 

import re
import time, csv
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
 
#  Make csv to save Scraped Data

def make_csv(filename: str, data, new=True):
    """make a csv file with the given filename
    and enter the data
    """
    mode = "w" if new else "a"
    with open(filename, mode, newline="") as f:
        f.writelines(data)


make_csv("Email Data.csv", "Email Data from Websites\n", new=True)
make_csv("Email Data.csv", "city;Business Name;Address;Website;Phone#;Email\n", new=False)

# Start webdriver_manager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('disable-notifications')
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()

# Login With facebook account

urll = "https://web.facebook.com/login"
driver.get(urll)
actions = ActionChains(driver)
actions.send_keys(Keys.ENTER).perform()
time.sleep(1)
User_name = "turgutjutt668@gmail.com"
Pass_word = "Word@123"
username = driver.find_element(By.XPATH, "//*[@id='email']")
for char in User_name:
    username.send_keys(char)
    time.sleep(0.3)
passwrod = driver.find_element(By.XPATH, "//*[@id='pass']")
for char in Pass_word:
    passwrod.send_keys(char)
    time.sleep(0.3)
time.sleep(1)
login =  driver.find_element(By.XPATH, "//*[@id='loginbutton']").click()
time.sleep(1)
driver.execute_script("window.stop();")
time.sleep(2)

# Get values from csv file & execute one by one in webdriver

with open("Website.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        value1 = row[0]
        value2 = row[1]
        value3 = row[2]
        value4 = row[3]
        value5 = row[4]
                         
        try:
            
    #  Start scraping emails from websites

        # Open website if website have email

            url = f"http://{value4}"
            driver.get(url)
            print(f"URL: {url}")
            time.sleep(1)
            sources = driver.page_source
            matches = re.findall(r'href="mailto:([^"]*)"', sources)
            detail = ""
            for match in matches:
                print(match)
                if match not in detail:
                    detail += f"{match};"
                make_csv("Email Data.csv", f"{value1};{value2};{value3};{value4};{value5};{detail}\n", new=False)
                break
    
    # If website dont have email check facebook icon on website 
    
        # if website have facebook open it new tab
            
            if not matches:
                if "//www.facebook.com" in sources:
                    print("facebook")
                    facebook = driver.find_element(By.XPATH, "//a[contains(@href, '//www.facebook.com')]")
                    facebook_link = facebook.get_attribute("href")
                    time.sleep(3)
                    driver.execute_script(f"window.open('{facebook_link}', '_blank');")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.execute_script("window.stop();")
                    time.sleep(5)
                    
                    # Check Email on facebook page with href tag 
                     
                    sourcess = driver.page_source
                    time.sleep(2)
                    matchxs = re.findall(r'href="mailto:([^"]*)"', sourcess)
                    detaile = ""
                    for matchs in matchxs:
                        print(matchs)
                        time.sleep(2)
                        if matchs not in detail:
                            detaile += f"{matchs};"
                        make_csv("Email Data.csv", f"{value1};{value2};{value3};{value4};{value5};{detaile}\n", new=False)
                        break
                    driver.execute_script("window.close();")
                    time.sleep(2)
                    driver.switch_to.window(driver.window_handles[-1])
                    
                # if email not found with href tag check with regular expression 
                
                if not matchxs:
                    sourcexs = driver.page_source
                    time.sleep(2)
                    pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
                    sourcexx = "<html>...</html>"
                    emails = pattern.findall(sourcexs)
                    emaill = ""
                    for email in emails:
                        print(email)
                        if email not in emaill:
                            emaill += f"{email};"
                        make_csv("Email Data.csv", f"{value1};{value2};{value3};{value4};{value5};{emaill}\n", new=False)
                        break
                    driver.execute_script("window.close();")
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[-1])
                
                # If email also not found with regular expression then print Email not found
                
                if not emails:
                    make_csv("Email Data.csv", f"{value1};{value2};{value3};{value4};{value5};Email Not Found\n", new=False)

# If Email not found on website and on facebook print emial not found
  
        except:
           make_csv("Email Data.csv", f"{value1};{value2};{value3};{value4};{value5};Email Not Found\n", new=False)    
        time.sleep(1)

driver.quit()