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
        for brand in ['Louis Vuitton']:
            self.directoryname=brand.replace(" ","")
            os.chdir(owd)
            if not os.path.exists(self.directoryname):
                os.makedirs(self.directoryname)
            os.chdir(self.directoryname)
            if not os.path.exists(self.directoryname+"catalogue.csv"):
                append_list_as_row(self.directoryname+"catalogue.csv",["Brand", "ItemCode","URL","Title","Price(WON)","Time"])
            self.branddirect = brand.replace(" ","+").lower()
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            options.add_argument('--headless')
            #2) Need to path to where ever your chrome is located,
            self.driver = webdriver.Chrome("/usr/local/share/chromedriver", options=options)
            self.base_url = "https://www.feelway.com/list.php?f_key_goods="+self.branddirect+'&goods_page=1#self'
            self.verificationErrors = []
            self.accept_next_alert = True

    def test_sel(self):
        folderpath='/home/a/Desktop/github/clothingscrapers/feelwayscrapper/'+self.directoryname+"/"
        owd=os.getcwd()
        owd
        os.chdir(owd)
        driver = self.driver
        driver.get(self.base_url)
        htmlcheck=[driver.page_source]
        greaterhtml=[]
        itemlinks=[]
        pageitemsoup = BeautifulSoup(driver.page_source, 'lxml')
        pagesection=pageitemsoup.find_all('div',{'style' : 'text-align: center'})
        if "Total" in str(pagesection):
            lastpage=(pagesection[0].getText().split()[-2])
        else:
            lastpage=(pagesection[0].getText().split()[-1])
        for page in range(1,int(lastpage)+1):
            self.base_url="https://www.feelway.com/list.php?f_key_goods="+self.branddirect+'&goods_page='+str(page)+'#self'
            driver = self.driver
            driver.get(self.base_url)
            WebDriverWait(driver, 1)
            pageitemsoup = BeautifulSoup(driver.page_source, 'lxml')
            linktagsdiv=pageitemsoup.find_all('div',{'class' : 'realtime-products'})[0]
            thelinks=linktagsdiv.find_all('a',{'class' : 'newA'})
            for itematag in thelinks:
                itemlinks.append(itematag['data-url'])
        for itemurl in itemlinks:
            spliturl=itemurl.split("_")
            splithtml=spliturl[-1].split('.')
            itemcode=splithtml[-2]
            if not os.path.exists(folderpath+itemcode):
                ax=0
                descriptionis="N/A"

                os.makedirs(folderpath+itemcode)
                driver = self.driver
                delay = 3
                base_url = "https://www.feelway.com/"+itemurl
                print(base_url)
                driver.get(base_url)
                WebDriverWait(driver, 2)
                item_soup = BeautifulSoup(driver.page_source,'lxml')
                titlesoup=item_soup.findAll('div',{'class' : 'kbo-product-title'})[0].getText().strip()
                pricesoup=item_soup.findAll('p',{'class' : 'discount'})[0]
                theprice=pricesoup.findAll('em')[0].getText().strip()
                append_list_as_row(folderpath+self.directoryname+"catalogue.csv",[self.branddirect.replace("+"," "), itemcode, base_url,titlesoup,theprice,datetime.datetime.now()])
                imagearea=item_soup.findAll('div',{'class' : 'kbo-product-image-wrapper'})[0]
                theimages=imagearea.findAll('img')
                imageurls=[]
                for eachimage in theimages:
                    imageurls.append(str(eachimage['src'][2:]))
                for clothingimage in imageurls:
                    print(clothingimage)
                    splitimage=clothingimage.split('/')
                    try:
                        urllib.request.urlretrieve('https://'+str(clothingimage), str(splitimage[-1]))
                        shutil.move(os.getcwd()+'/'+splitimage[-1], os.getcwd()+'/'+itemcode+'/'+splitimage[-1])
                    except UnicodeEncodeError:
                        pass


if __name__ == "__main__":
    unittest.main()
