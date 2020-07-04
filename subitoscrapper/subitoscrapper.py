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
            self.directoryname=brand.replace(" ","")
            os.chdir(owd)
            if not os.path.exists(self.directoryname):
                os.makedirs(self.directoryname)
            os.chdir(self.directoryname)
            if not os.path.exists(self.directoryname+"catalogue.csv"):
                append_list_as_row(self.directoryname+"catalogue.csv",["Brand", "ItemCode","URL","Title","Price(CHF)","Type","Description","Time"])
            self.branddirect = brand.replace(" ","+").lower()
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            options.add_argument('--headless')
            #2) Need to path to where ever your chrome is located,
            self.driver = webdriver.Chrome("/usr/local/share/chromedriver", options=options)
            self.base_url = "https://www.subito.it/annunci-italia/vendita/usato/?q="+self.branddirect+"&o=1"
            self.verificationErrors = []
            self.accept_next_alert = True

    def test_sel(self):
        folderpath='/home/a/Desktop/github/clothingscrapers/subitoscrapper/'+self.directoryname+"/"
        owd=os.getcwd()
        owd
        os.chdir(owd)
        driver = self.driver
        driver.get(self.base_url)
        WebDriverWait(driver, 2)
        htmlcheck=[driver.page_source]
        greaterhtml=[]
        itemlinks=[]
        pageitemsoup = BeautifulSoup(driver.page_source, 'lxml')
        lastpagecont=pageitemsoup.find_all('div',{'class' : 'jsx-3012950973 pagination-container'})[0]
        lastpage=int(lastpagecont.find_all('span')[-1].getText().strip())
        for page in range(1,int(lastpage)+1):
            self.base_url="https://www.subito.it/annunci-italia/vendita/usato/?q="+self.branddirect+"&o="+str(page)
            driver = self.driver
            driver.get(self.base_url)
            WebDriverWait(driver, 2)
            pageitemsoup = BeautifulSoup(driver.page_source, 'lxml')
            linktags=pageitemsoup.find_all('a',{'class' : 'jsx-3924372161 link'})
            for itematag in linktags:
                itemlinks.append(itematag['href'])
        for itemurl in itemlinks:
            spliturl=itemurl.split("/")
            splithdot=spliturl[-1].split('.')
            splithyphen=splithdot[-2].split("-")
            itemcode=splithyphen[-1]
            if not os.path.exists(folderpath+itemcode):
                ax=0
                thetype="N/A"
                os.makedirs(folderpath+itemcode)
                driver = self.driver
                base_url = itemurl
                driver.get(base_url)
                WebDriverWait(driver, 2)
                item_soup = BeautifulSoup(driver.page_source,'lxml')
                thetitle=item_soup.find_all('h1',{'class' : 'classes_sbt-text-atom__2GBat classes_token-h4__3_Swu size-normal classes_weight-semibold__1RkLc ad-info__title'})[0].getText().strip()
                theprice=item_soup.find_all('h4',{'class' : 'classes_sbt-text-atom__2GBat classes_token-h4__3_Swu size-normal classes_weight-semibold__1RkLc classes_price__HmHqw'})[0].getText().strip()
                if "classes_sbt-text-atom__2GBat classes_token-body__1dLNW size-normal classes_weight-book__3zPi1 value jsx-3561725324" in str(item_soup):
                    ax=1
                    thetype=item_soup.find_all('span',{'class' : 'classes_sbt-text-atom__2GBat classes_token-body__1dLNW size-normal classes_weight-book__3zPi1 value jsx-3561725324'})[0].getText().strip()
                if ax==0:
                    thetype="N/A"
                thedescription=item_soup.find_all('p',{'class' : 'classes_sbt-text-atom__2GBat classes_token-body__1dLNW size-normal classes_weight-book__3zPi1 jsx-436795370 description classes_preserve-new-lines__1X-M6'})[0].getText().strip()
                append_list_as_row(folderpath+self.directoryname+"catalogue.csv",[self.branddirect.replace("%20"," "), itemcode, base_url,thetitle,theprice,thetype,thedescription,datetime.datetime.now()])
                imagearea=item_soup.findAll('div',{'class' : 'carousel flickity-enabled is-draggable'})[0]
                allimages=imagearea.findAll('img')
                imageurls=[]
                for eachimage in allimages:
                    if 'src=' in str(eachimage):
                        imageurls.append(eachimage['src'])
                    if 'data-flickity-lazyload=' in str(eachimage):
                        imageurls.append(eachimage['data-flickity-lazyload'])
                for clothingimage in imageurls:
                    splitimage=clothingimage.split('-')
                    urllib.request.urlretrieve(str(clothingimage), str(splitimage[-1]))
                    shutil.move(os.getcwd()+'/'+splitimage[-1], os.getcwd()+'/'+itemcode+'/'+splitimage[-1])
                ax=1

if __name__ == "__main__":
    unittest.main()
