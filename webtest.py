from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import csv
import json
import os
import pandas as pd
import numpy as np
import re 
from datetime import datetime
from openpyxl import Workbook
import csv

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36')]
urllib.request.install_opener(opener)

driver = webdriver.Chrome(r"C:\Users\Katya\Documents\GitHub\SF-Project\chromedriver.exe")
driver.get('https://steamcommunity.com/app/526870/reviews/?p=1&browsefilter=mostrecent')
content = driver.find_element_by_id('AppHubCards')

html = driver.find_element_by_tag_name('html')

# OUR GAME ID: currently, set to Satisfactory
game_id = 526870

template = 'https://steamcommunity.com/app/{}/reviews/?browsefilter=mostrecent'
template_with_language = 'https://steamcommunity.com/app/{}/reviews/?browsefilter=mostrecent&filterLanguage=english'
url = template_with_language.format(game_id)

driver.get(url)

# get current position of y scrollbar
last_position = driver.execute_script("return window.pageYOffset;")

reviews = []
review_ids = set()
running = True

while running:
    # get cards on the page
    cards = driver.find_elements_by_class_name('apphub_Card')

    for card in cards[-20:]:  # only the tail end are new cards

        # gamer profile url
        profile_url = card.find_element_by_xpath('.//div[@class="apphub_friend_block"]/div/a[2]').get_attribute('href')

        # steam id
        steam_id = profile_url.split('/')[-2]
        
        # check to see if I've already collected this review
        if steam_id in review_ids:
            continue
        else:
            review_ids.add(steam_id)

        # username
        user_name = card.find_element_by_xpath('.//div[@class="apphub_friend_block"]/div/a[2]').text

        # language of the review
        date_posted = card.find_element_by_xpath('.//div[@class="apphub_CardTextContent"]/div').text
        review_content = card.find_element_by_xpath('.//div[@class="apphub_CardTextContent"]').text.replace(date_posted,'').strip()    

        # review length
        review_length = len(review_content.replace(' ', ''))    

        # recommendation
        thumb_text = card.find_element_by_xpath('.//div[@class="reviewInfo"]/div[2]').text
        thumb_text    

        # amount of play hours
        play_hours = card.find_element_by_xpath('.//div[@class="reviewInfo"]/div[3]').text
        play_hours    

        # save review
        review = (steam_id, profile_url, review_content, thumb_text, review_length, play_hours, date_posted)
        reviews.append(review)    
        
    # attempt to scroll down thrice.. then break
    scroll_attempt = 0

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")    
        time.sleep(2)
        curr_position = driver.execute_script("return window.pageYOffset;")
        
        if curr_position == last_position:
            scroll_attempt += 1
            time.sleep(2)
            
            if curr_position >= 3:
                running = False
                break
        else:
            last_position = curr_position
            break  # continue scraping the results
        
    #TO DO: condition when "See More Content" button appears
driver.find_element_by_xpath('.//*[@id="GetMoreContentBtn"]/a').click()
# shutdown the web driver
driver.close()

# save the file to a CSV file
today = datetime.today().strftime('%Y%m%d')   
with open(f'Steam_Reviews_{game_id}_{today}.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['SteamId', 'ProfileURL', 'ReviewText', 'Review', 'ReviewLength(Chars)', 'PlayHours', 'DatePosted'])
    writer.writerows(reviews)

