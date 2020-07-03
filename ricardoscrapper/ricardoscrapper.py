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
        for brand in ['Prada']:
            self.directoryname=brand.replace(" ","")
            os.chdir(owd)
            if not os.path.exists(self.directoryname):
                os.makedirs(self.directoryname)
            os.chdir(self.directoryname)
            if not os.path.exists(self.directoryname+"catalogue.csv"):
                append_list_as_row(self.directoryname+"catalogue.csv",["Brand", "ItemCode","URL","Title","Price(CHF)","Description","Time"])
            self.branddirect = brand.replace(" ","%20").lower()
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            options.add_argument('--headless')
            #2) Need to path to where ever your chrome is located,
            self.driver = webdriver.Chrome("/usr/local/share/chromedriver", options=options)
            self.base_url = "https://www.ricardo.ch/de/s/"+self.branddirect+'?next_offset=59&page=1'
            self.verificationErrors = []
            self.accept_next_alert = True

    def test_sel(self):
        folderpath='/home/a/Desktop/github/clothingscrapers/ricardoscrapper/'+self.directoryname+"/"
        owd=os.getcwd()
        owd
        os.chdir(owd)
        driver = self.driver
        driver.get(self.base_url)
        htmlcheck=[driver.page_source]
        greaterhtml=[]
        itemlinks=[]
        pageitemsoup = BeautifulSoup(driver.page_source, 'lxml')
        if "MuiFlatPagination-root jss598" in str(pageitemsoup):
            pagesection=pageitemsoup.find_all('div',{'class' : 'MuiFlatPagination-root jss598'})[0]
            onlypages=pagesection.find_all('a',{'href' : True})
            thepage=(onlypages[-2].findAll(text=True)[0])
        else:
            thepage=int(thepage)
        for page in range(1,int(thepage)+1):
            url="https://www.ricardo.ch/de/s/"+self.branddirect+'?next_offset=59&page='+str(thepage)
            driver = self.driver
            driver.get(self.base_url)
            pageitemsoup = BeautifulSoup(driver.page_source, 'lxml')
            linktags=pageitemsoup.find_all('a',{'class' : 'MuiGrid-root link--2OHFZ MuiGrid-item MuiGrid-grid-xs-6 MuiGrid-grid-sm-4 MuiGrid-grid-md-3'})
            for itematag in linktags:
                itemlinks.append(itematag['href'])
        for itemurl in itemlinks:
            spliturl=itemurl.split("/")
            splithypehn=spliturl[-2].split('-')
            itemcode=splithypehn[-1]
            if not os.path.exists(folderpath+itemcode):
                ax=0
                descriptionis="N/A"
                bx=0
                cx=0
                dx=0
                ex=0
                os.makedirs(folderpath+itemcode)
                driver = self.driver
                delay = 3
                base_url = "https://www.ricardo.ch"+itemurl
                print(base_url)
                driver.get(base_url)
                WebDriverWait(driver, 3)
                item_soup = BeautifulSoup(driver.page_source,'lxml')
                titlesoup=item_soup.findAll('h1',{'class' : 'title--30fKd'})[0].text
                if "jss170 valueprice--23qfn" in str(item_soup):
                    pricesoup=item_soup.findAll('p',{'class' : 'jss170 valueprice--23qfn'})[0].text
                else:
                    pricesoup=item_soup.findAll('p',{'class' : 'jss170 value--2CfaM'})[0].text
                thedescriptiongen=item_soup.findAll('div',{'class' : 'userDescription--1-bzj'})[0]
                thedescription=thedescriptiongen.findAll('p')
                if len(thedescription)>0:
                    ax=1
                    thedescriptionactual=thedescription[0].text
                if ax==0:
                    thedescriptionactual="N/A"
                append_list_as_row(folderpath+self.directoryname+"catalogue.csv",[self.branddirect.replace("+"," "), itemcode, base_url,titlesoup,pricesoup,thedescriptionactual,datetime.datetime.now()])
                imagearea=item_soup.findAll('div',{'role' : 'presentation'})[0]
                theimages=imagearea.findAll('img')
                imageurls=[]
                for eachimage in theimages:
                    imageurls.append(str(eachimage['src']))
                for clothingimage in imageurls:
                    splitimage=clothingimage.split('/')
                    urllib.request.urlretrieve(str(clothingimage), str(splitimage[-2]))
                    shutil.move(os.getcwd()+'/'+splitimage[-2], os.getcwd()+'/'+itemcode+'/'+splitimage[-1])
                    ax=1
                    bx=1
                    cx=1
                    dx=1
                    ex=1
                    fx=1
                    gx=1

if __name__ == "__main__":
    unittest.main()
