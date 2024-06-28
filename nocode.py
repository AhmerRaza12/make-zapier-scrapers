from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
import requests
import os
import pandas
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
import pandas as pd
import csv
from dotenv import load_dotenv

Options = webdriver.ChromeOptions()
Options.add_argument('--no-sandbox')
Options.add_argument('--disable-dev-shm-usage')
Options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
Options.add_argument('--start-maximized')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=Options)

# read the urls from nocode_links.txt file
with open('nocode_links.txt', 'r') as file:
    urls = file.read().splitlines()
data_list= []
def extract_data():
    try:
        for url in urls:
            driver.get(url)
            time.sleep(2)
            link_of_page = driver.current_url
            integration_name = driver.find_element(By.TAG_NAME, "h1").text
            try:
                integration_description = driver.find_element(By.XPATH, "//p[@class='integration-bio']").text
            except:
                integration_description = ''
            try:
                integration_link = driver.find_element(By.XPATH,"//a[@class='link']").get_attribute('href')
            except:
                integration_link = ''
            try:
                integration_image_xpath = driver.find_element(By.XPATH,"//div[@class='header-integration']//div[@class='integration-circle']")
                integration_image = integration_image_xpath.value_of_css_property('background-image')
                integration_image = integration_image.split('url("')[1].split('")')[0]
            except:
                integration_image = ''
            try:
                integration_templates = driver.find_elements(By.XPATH,"//a[@class='expect-card w-inline-block']")
                for template in integration_templates:
                        try:
                            template_name = driver.execute_script("return arguments[0].innerText", template)
                        except Exception as e:
                            print(f"An error occured while getting the template name: {str(e)}")
                            break 
                        template_link = template.get_attribute('href')
                        data = {
                            'Integration Name': integration_name,
                            'Integration Description': integration_description,
                            'Integration Link': integration_link,
                            'Integration Image': integration_image,
                            'Template Name': template_name,
                            'Template Link': template_link,
                            'Link of Page': link_of_page
                            }
                        print(data)
                        data_list.append(data)
            except:
                data = {
                    'Integration Name': integration_name,
                    'Integration Description': integration_description,
                    'Integration Link': integration_link,
                    'Integration Image': integration_image,
                    'Template Name': '',
                    'Template Link': '',
                    'Link of Page': link_of_page
                    }
                print(data)
                data_list.append(data)

    except:
        pass
     
    finally: 
        driver.quit()

    return data_list


data = extract_data()
df = pd.DataFrame(data)

df.to_csv('nocode_data.csv', index=False,encoding='utf-8-sig')

