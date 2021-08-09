
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Optionscon
import time
import urllib.request
# import argh
import csv
import json
import os
import pandas as pd
import numpy as np

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36')]
urllib.request.install_opener(opener)

driver = webdriver.Chrome(r"C:\Users\Katya\Documents\GitHub\SF-Project\chromedriver.exe")
driver.get('https://steamcommunity.com/app/526870/reviews/?p=1&browsefilter=mostrecent')
content = driver.find_element_by_id('AppHubCards')

html = driver.find_element_by_tag_name('html')


# review_template = {
#     'date': 'review_date',
#     'text': 'review_text',
#     'hours_played': 'hours_played',
#     'recommended': 'recommended',
#     'received_free': 'received_free'
# }

temp_list = []

scrolls = 1


for scroll in range(scrolls):
    page_num = scroll + 1
    
    page_name = 'page' + str(page_num)
    page = content.find_element_by_id(page_name)
    
    rows = page.find_elements_by_class_name('apphub_CardRow')
    html.send_keys(Keys.END)
    
    for row in rows:
        
        cards = driver.find_elements_by_class_name('apphub_UserReviewCardContent')
    
        for card in cards:
            
            # top header
            header = card.find_element_by_class_name('reviewInfo')
            
            #review content box
            review_content = card.find_element_by_class_name('apphub_CardTextContent')
            
            try: 
                received_free = review_content.find_element_by_class_name('received_compensation').text
            except Exception as e:
                received_free = '0'
                pass 
        
            finally: 
                review_date = review_content.find_element_by_class_name('date_posted').text
                review_text: str = review_content.text
                hours_played: str = header.find_element_by_class_name('hours').text
                recommended: str = header.find_element_by_class_name('title').text
            
            print(review_date, review_text, hours_played, '\n')
            
            table_dict = {
                'date': review_date,
                'text': review_text,
                'hours_played': hours_played,
                'recommended': recommended,
                'received_free': received_free,
            }

            temp_list.append(table_dict)
            df = pd.DataFrame(temp_list)
            
            df.to_csv(r"C:\Users\Katya\Documents\GitHub\SF-Project\scraped_data.csv")
            # # review_df = pd.DataFrame({
            #     'date': review_date,
            #     'text': review_text,
            #     'hours_played': hours_played,
            #     'recommended': recommended,
            #     'received_free': received_free,
            # # }, index=[0])


            
# pd.DataFrame(review_df, index=[]).to_csv(page_name + '.csv')
driver.close()

