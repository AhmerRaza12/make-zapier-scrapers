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
# Options.add_argument('--headless=new')


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=Options)
# links = set()

# def get_links():
#     try:
#         driver.get('https://www.make.com/en/integrations?community=1&verified=1')
#         time.sleep(2)
#         try:
#             cookie_banner_close_btn = driver.find_element(By.XPATH, "//button[@class='onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon']")
#             if cookie_banner_close_btn.is_displayed():
#                 cookie_banner_close_btn.click()
#                 time.sleep(2)
#         except NoSuchElementException:
#             pass
#         app_div = driver.find_element(By.XPATH, "(//div[@class='SearchCommonStyles_resultsWrapper__ZF0xF']//div[@class='SearchCommonStyles_currentItems__YO7iP SearchCommonStyles_small__9k9X9'])[2]")
#         while True:
#             try:
#                 load_more = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='primary-outline SearchCommonStyles_loadMore__9u7hH']")))
#                 driver.execute_script("arguments[0].scrollIntoView();", load_more)
#                 time.sleep(1)
#                 driver.execute_script("arguments[0].click();", load_more)
#                 time.sleep(3)    
#             except TimeoutException:
#                 print("No more 'Load More' button found.")
#                 break
#             except Exception as e:
#                 print(f"An error occurred while clicking 'Load More' button: {str(e)}")
    
#         WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//a[@class='AppCard_appCard__gSGNN AppCard_appCardSmall__5ueCV AppCard_appCardFullWidth__0j8Vt']")))
#         links_xp = app_div.find_elements(By.XPATH, ".//a[@class='AppCard_appCard__gSGNN AppCard_appCardSmall__5ueCV AppCard_appCardFullWidth__0j8Vt']")
#         for link in links_xp:
#             href = link.get_attribute('href')
#             links.add(href)
        
#     except NoSuchElementException as e:
#         print(f"Element not found: {str(e)}")
 
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
    
#     finally:
#         driver.quit()  
    
#     return links

# all_links = get_links()
# print("The number of unique links found are:", len(all_links))
# def save_links_to_file(links_set):
#     file_path = os.path.join(os.getcwd(), 'make.com_links.txt')
    
#     # Write links to file
#     with open(file_path, 'w') as file:
#         for link in links_set:
#             file.write(link + '\n')
    
#     print(f"Saved {len(links_set)} unique links to {file_path}")
# save_links_to_file(all_links)


# read the links from the file links.txt and store them in a list
def read_links_from_file():
    links = []
    file_path = os.path.join(os.getcwd(), 'make.com_links.txt')
    with open(file_path, 'r') as file:
        links = file.readlines()
    
    return links

links = read_links_from_file()

module_data = []
template_data = []
def get_data(links):
    # for the first 5 links
    for i in range(5):
        try:
            driver.get(links[i])
            time.sleep(2)
            try:
                cookie_banner_close_btn = driver.find_element(By.XPATH, "//button[@class='onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon']")
                if cookie_banner_close_btn.is_displayed():
                    cookie_banner_close_btn.click()
                    time.sleep(2)
            except NoSuchElementException:
                pass
            
            name_of_integration = driver.find_element(By.XPATH, "//h1[@class='h2']").text
            name_of_tool = driver.find_element(By.XPATH, "//div[@class='AppOwnerCard_appOwnerCardHeaderTitle__pF_f4']").text
            link_of_page = driver.current_url
            logo_link = driver.find_element(By.XPATH, "//div[@class='AppOwnerCard_appOwnerCardHeader__PsSIo']//img").get_attribute('src')
            description = driver.find_element(By.XPATH, "//div[@class='body-large DetailsHeader_bodyText__jxP_H DetailsHeader_truncated__GC7Wi']//p").text
            
            try:
                trigger_action_div = driver.find_element(By.XPATH, "//div[@data-cy='TriggersAndActions']")
                
                while True:
                    try:
                        load_more = trigger_action_div.find_element(By.XPATH, ".//button[.='Load More']")
                        driver.execute_script("arguments[0].scrollIntoView();", load_more)
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", load_more)
                        time.sleep(3)    
                    except NoSuchElementException:
                        
                        break
                    except Exception as e:
                        print(f"An error occurred while clicking 'Load More' button: {str(e)}")
                
                module_name = driver.find_elements(By.XPATH, "//div[@class='heading TriggersAndActions_heading__Lq4Mf']")
                module_descp = driver.find_elements(By.XPATH, "//p[@class='caption TriggersAndActions_description__CXki_']")
                module_type = driver.find_elements(By.XPATH, "//div[@class='small TriggersAndActions_integrationType__CeYBw']")
                
                for module in range(len(module_name)):
                    data = {
                        'Name of Integration': name_of_integration,
                        'Name of Tool': name_of_tool,
                        'Link of Page': link_of_page,
                        'Logo Link': logo_link,
                        'Description': description,
                        'Module Name': module_name[module].text,
                        'Module Description': module_descp[module].text,
                        'Module Type': module_type[module].text,
                    }
                    module_data.append(data)
                
            except NoSuchElementException:
                data = {
                    'Name of Integration': name_of_integration,
                    'Name of Tool': name_of_tool,
                    'Link of Page': link_of_page,
                    'Logo Link': logo_link,
                    'Description': description,
                    'Module Name': '',
                    'Module Description': '',
                    'Module Type': '',
                }
                module_data.append(data)

            try:
                template_div = driver.find_element(By.XPATH, "//div[@class='container SimilarTemplatesSearch_templates__g0gC_']")
                
                while True:
                    try:
                        load_more = template_div.find_element(By.XPATH, ".//button[.='Load More']")
                        driver.execute_script("arguments[0].scrollIntoView();", load_more)
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", load_more)
                        time.sleep(3)
                    except NoSuchElementException:
                        
                        break
                    except Exception as e:
                        print(f"An error occurred while clicking 'Load More' button: {str(e)}")
                
                template_name = driver.find_elements(By.XPATH, "//div[@class='h6 TemplateCard_title__R6yVt']")
                template_descp = driver.find_elements(By.XPATH, "//div[contains(@class,'caption TemplateCard_description__SJyOv')]")
                template_link = driver.find_elements(By.XPATH, "//a[@class='TemplateCard_templateCard__DapRM']")
                
                for template in range(len(template_name)):
                    data = {
                        'Name of Integration': name_of_integration,
                        'Name of Tool': name_of_tool,
                        'Link of Page': link_of_page,
                        'Logo Link': logo_link,
                        'Description': description,
                        'Template Name': template_name[template].text,
                        'Template Description': template_descp[template].text,
                        'Template Link': template_link[template].get_attribute('href'),
                    }
                    template_data.append(data)
            
            except NoSuchElementException:
                data = {
                    'Name of Integration': name_of_integration,
                    'Name of Tool': name_of_tool,
                    'Link of Page': link_of_page,
                    'Logo Link': logo_link,
                    'Description': description,
                    'Template Name': '',
                    'Template Description': '',
                    'Template Link': '',
                }
                template_data.append(data)
        
        except Exception as e:
            print(f"An error occurred while processing link {links[i]}: {str(e)}")
            pass

get_data(links)

module_df = pd.DataFrame(module_data, columns=['Name of Integration', 'Name of Tool', 'Link of Page', 'Logo Link', 'Description', 'Module Name', 'Module Description', 'Module Type'])
template_df = pd.DataFrame(template_data, columns=['Name of Integration', 'Name of Tool', 'Link of Page', 'Logo Link', 'Description', 'Template Name', 'Template Description', 'Template Link'])

module_df.to_csv('make.com_module_data.csv', index=False)
template_df.to_csv('make.com_template_data.csv', index=False)
    

