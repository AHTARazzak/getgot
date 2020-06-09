from selenium import webdriver
from bs4 import BeautifulSoup
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from urllib.request import Request, urlopen
import urllib.parse
import sys
import os
import csv
import random
import datetime
from csv import writer

import unittest, time, re

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

class Sel(unittest.TestCase):
    def setUp(self):
        owd=os.getcwd()
        owd
        #1) include more brands if you want, spelling and composition is important ['Damir Doma']
        #CAN ONLY DO ONE BRAND AT A TIME
        for brand in ['Rick Owens']:
            directoryname=brand.replace(" ","")
            os.chdir(owd)
            if not os.path.exists(directoryname):
                os.makedirs(directoryname)
            os.chdir(directoryname)
            if not os.path.exists(directoryname+"catalogue.csv"):
                append_list_as_row(directoryname+"catalogue.csv",["Brand", "ItemCode","URL","Price(EUR)","Size","Time"])
            branddirect = brand.replace(" ","%20").lower()
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            options.add_argument('--headless')
            #2) Need to path to where ever your chrome is located,
            self.driver = webdriver.Chrome("/usr/local/share/chromedriver", chrome_options=options)
            self.driver.implicitly_wait(30)
            self.base_url = "https://sobump.com/search?q="+branddirect
            self.verificationErrors = []
            self.accept_next_alert = True
    def test_sel(self):
        #3) Need to path to the directory your running the code from for whatever brand
        folderpath='/home/a/Desktop/clothingscrapers/sobumpscrapper/RickOwens/'
        owd=os.getcwd()
        owd
        os.chdir(owd)
        driver = self.driver
        delay = 3
        driver.get(self.base_url)
        htmlcheck=[driver.page_source]
        for i in range(1,1000):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            htmlcheck.append(driver.page_source)
            if htmlcheck[-1] == htmlcheck[-2]:
                break
            html_source=htmlcheck[-1]
        soup=BeautifulSoup(html_source, 'lxml')
        itemlinks=[]
        for a in soup.find_all('a',href=True):
            if "><img" in str(a):
                start_index=str(a).index("href=")
                end_index=str(a).index("<img")
                itemlinks.append("https://sobump.com"+str(a)[start_index+6:end_index-2])
        itemlinks=itemlinks[1:]
        #print(len(itemlinks))
        for item in itemlinks:
            spliturlslash=item.split("/")
            splitlasthyphen=spliturlslash[-1].split("-")
            itemcode=splitlasthyphen[0]
            itemtitle=item[item.index("-")+1:]
            if not os.path.exists(folderpath+itemcode):
                os.makedirs(folderpath+itemcode)
                user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                headers = { 'User-Agent' : user_agent }
                item_req = Request(item, headers=headers)
                item_page = urlopen(item_req).read()
                item_soup = BeautifulSoup(item_page, 'lxml')
                theprice=item_soup.findAll('div',attrs = {'class' : "product-sale-price"})[-1].contents
                thepriceis=(theprice[0][1:])
                thesize=item_soup.findAll('span',attrs = {'class' : "product-size"})
                if len(thesize)>0:
                    thesize=thesize[-1].contents
                    thesizeis=(thesize[0])
                else:
                    thesizeis="N/A"
                    #4) Need to change brand name of CSV to whatever the brand is without space following format from Line X
                append_list_as_row(folderpath+'RickOwens'+"catalogue.csv",[splitlasthyphen[1]+splitlasthyphen[2], itemcode,item,thepriceis,thesizeis,datetime.datetime.now()])
                carouselimg=item_soup.findAll('div',attrs = {'class' : "image-gallery-image"})
                for element in carouselimg:
                    item_pic_url=element.findChildren()[0]['src']
                    finalimg=item_pic_url.split("/")
                    urllib.request.urlretrieve(str(item_pic_url), str(finalimg[-1]))
                    shutil.move(folderpath+finalimg[-1],folderpath+itemcode+'/'+finalimg[-1])
                    time.sleep(random.randint(0,2))
if __name__ == "__main__":
    unittest.main()
