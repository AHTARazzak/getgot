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
                append_list_as_row(self.directoryname+"catalogue.csv",["Brand", "ItemCode","URL","Price(CHF)","Condition","Colour","Material","Size","Time"])
            self.branddirect = brand.replace(" ","%20").lower()
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            options.add_argument('--headless')
            #2) Need to path to where ever your chrome is located,
            self.driver = webdriver.Chrome("/usr/local/share/chromedriver", options=options)
            self.base_url = "https://www.rebelle.com/en/all?page=1&query="+self.branddirect
            self.verificationErrors = []
            self.accept_next_alert = True
    def test_sel(self):
        folderpath='/home/a/Desktop/github/clothingscrapers/rebellescrapper/'+self.directoryname+"/"
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
        lastpage=pageitemsoup.find_all('a',{'class' : '_3yeDnAH9HUyLKOBFx5296d pathActive relatedPathActive'})[-1].contents[0]
        for page in range(1,int(lastpage)+1):
            self.base_url="https://www.rebelle.com/en/all?page="+str(page)+"&query="+self.branddirect
            driver = self.driver
            driver.get(self.base_url)
            WebDriverWait(driver, 2)
            pageitemsoup = BeautifulSoup(driver.page_source, 'lxml')
            linktags=pageitemsoup.find_all('a',{'class' : '_3Uq7-YuHOAvHTHqCD4x-vg'})
            for itematag in linktags:
                itemlinks.append(itematag['href'])
        for itemurl in itemlinks:
            spliturl=itemurl.split("/")
            splithypehn=spliturl[-1].split('-')
            itemcode=splithypehn[-1]
            if not os.path.exists(folderpath+itemcode):
                os.makedirs(folderpath+itemcode)
                driver = self.driver
                base_url = "https://www.rebelle.com"+itemurl
                driver.get(base_url)
                WebDriverWait(driver, 2)
                item_soup = BeautifulSoup(driver.page_source,'lxml')
                theprice=item_soup.find_all('span',{'class' : '_2fWqlm4D_23s24d5No6Fuz textMedium'})[0].getText().split()[0]
                thecondition=item_soup.find_all('td',{'class' : '_39SNMg0X0E1OUlIcuGsKLw textMedium'})[0].getText().split()[0]
                thetable=item_soup.find_all('table',{'class' : 'zJowfpBfx3oZOUysfRPF7'})[0]
                therows=thetable.find_all('td')
                thecolour=therows[7].getText()
                thematerial=therows[9].getText()
                sizetable=item_soup.find_all('table',{'class' : 'zJowfpBfx3oZOUysfRPF7'})[1]
                sizetablerows=sizetable.find_all('td')
                thesize=(sizetablerows[1].getText())
                append_list_as_row(folderpath+self.directoryname+"catalogue.csv",[self.branddirect.replace("%20"," "), itemcode, base_url,theprice,thecondition,thecolour,thematerial,thesize,datetime.datetime.now()])
                imagearea=item_soup.findAll('figure',{'class' : '_2QG9I7JZ5PUZdZBEXww2au greyProductOverlay'})[0]
                theimageitself=imagearea.findAll('img')[0]['src']
                splitimage=theimageitself.split('/')
                urllib.request.urlretrieve(str(theimageitself), str(splitimage[-1]))
                shutil.move(os.getcwd()+'/'+splitimage[-1], os.getcwd()+'/'+itemcode+'/'+splitimage[-1])
if __name__ == "__main__":
    unittest.main()