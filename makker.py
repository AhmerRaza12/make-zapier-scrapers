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


links = set()
def get_links():
    with open('makker.com_links.txt', 'r') as file:
        urls = file.read().splitlines()
    try:
        for url in urls:
            driver.get(url)
            time.sleep(2)     
            while True:
                try:
                    load_more=driver.find_element(By.XPATH,"//a[.='Charger plus']")
                    driver.execute_script("arguments[0].scrollIntoView();", load_more)
                    time.sleep(1)
                    load_more.click()
                    time.sleep(1)
                except NoSuchElementException:
                    break
                except ElementNotInteractableException:
                    print("No more templates to load")
                    break
                except Exception as e:
                    print(f"An errror occured while clicking the next page button :  {str(e)}")
                    pass
            
            links_xpath = driver.find_elements(By.XPATH, "//a[@class='w-inline-block']")
            print(f"In url:{url} found total templates: {len(links_xpath)}")
            for link in links_xpath:
                links.add(link.get_attribute('href'))
                print(link.get_attribute('href'))
            
    except Exception as e:
        print(f"An error occured while getting the links : {str(e)}")
    return links


with open('makker.com_template_links.txt', 'r') as file:
    urls = file.read().splitlines()


def scrape_data():
    data_list=[]
   
    for url in urls:
        try:

            driver.get(url)
            time.sleep(2)
            page_link = url
            template_name = driver.find_element(By.XPATH, "//h3[@class='smaller-h1 _16mt']").text
            template_description = driver.find_element(By.XPATH, "//div[@class='_16mt']").text
            template_tools_xpath = driver.find_elements(By.XPATH,"//div[@class='included-tools w-dyn-item']")
            # get the tools used in the template by joining them with ','
            template_tools = ', '.join([tool.text for tool in template_tools_xpath])
            template_img_links = driver.find_elements(By.XPATH,"//div[@class='included-tools w-dyn-item']//div[@class='icon-cube_container smaller-cube']//img")
            try:
                make_redirect_link = driver.find_element(By.XPATH,"(//a[.='Cloner le scenario'])[1]").get_attribute('href')
            except:
                make_redirect_link = " "
            img_links = '\n'.join([img.get_attribute('src') for img in template_img_links])
            data={
                'Template Name':template_name,
                'Template Description':template_description,
                'Tools Used in Template':template_tools,
                'Images ':img_links,
                'Link of Page':page_link,
                'Make.com Redirect Link': make_redirect_link   
            }
            print(data)
            data_list.append(data)
        except Exception as e:
            print(f"An error occured while getting the url : {str(e)}")
            pass
    return data_list


blog_post_data =[]
def get_blog():
    try:
        driver.get("https://www.makkers.fr/blog")
        time.sleep(2)
        blog_posts_xpath = driver.find_elements(By.XPATH,"//a[@class='blog-card w-inline-block']")
        for blog_post in blog_posts_xpath:
            blog_post.click()
            time.sleep(4)
            Link_of_page = driver.current_url
            blog_image_div = driver.find_element(By.XPATH,"//div[@class='article-image']")
            # get the style attribute of the div and extract the url of the image
            blog_image = re.search(r'url\((.*?)\)', blog_image_div.get_attribute('style')).group(1)
            blog_title  = driver.find_element(By.TAG_NAME,"h1").text
            blog_date_posted = driver.find_element(By.XPATH,"//div[@class='space-right-small grey-text _12ml']").text
            blog_read_time = driver.find_element(By.XPATH,"//div[@class='space-right-tiny grey-text _12ml']").text
            blog_author_name = driver.find_element(By.XPATH," //div[@class='grey-text _16ml']").text
            blog_author_image_div = driver.find_element(By.XPATH,"//div[@class='author-picture_container']")
            blog_author_image = re.search(r'url\((.*?)\)', blog_author_image_div.get_attribute('style')).group(1)
            blog_content = driver.find_element(By.TAG_NAME,"article").text
            blog_data = {
                'Blog Title':blog_title,
                'Date Posted':blog_date_posted,
                'Read Time':blog_read_time,
                'Author Name':blog_author_name,
                'Author Image':blog_author_image,
                'Content':blog_content,
                'Link of Page':Link_of_page,
                'Blog Image':blog_image
            }
            blog_post_data.append(blog_data)
            driver.back()
            time.sleep(1)

    except Exception as e:
        print(f"An error occured while getting the blog posts : {str(e)}")
        pass
        
    return blog_post_data


if __name__ == '__main__':
    total_links=get_links()
    print(f"Total links found: {len(total_links)}")
    # add the links to the file makker.com_template_links.txt
    with open('makker.com_template_links.txt', 'w') as file:
        for link in total_links:
            file.write(link + '\n')
    data=scrape_data()
    df = pd.DataFrame(data)
    df.to_csv('makker.com_templates.csv', mode='a', header=True, index=False,encoding='utf-8')
    print(df)
    blogs=get_blog()
    df = pd.DataFrame(blogs)
    df.to_csv('makker.com_blogs.csv', mode='a', header=True, index=False,encoding='utf-8')
    print(df)