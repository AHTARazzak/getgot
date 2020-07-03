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
                append_list_as_row(self.directoryname+"catalogue.csv",["Brand", "ItemCode","URL","Price(EUR)","Size","Colour","Material","Condition","Description","Time"])
            self.branddirect = brand.replace(" ","+").lower()
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            options.add_argument('--headless')
            #2) Need to path to where ever your chrome is located,
            self.driver = webdriver.Chrome("/usr/local/share/chromedriver", chrome_options=options)
            self.base_url = "https://thenextcloset.com/items?button=&number_of_items=60&page=1&search="+self.branddirect
            self.verificationErrors = []
            self.accept_next_alert = True

    def test_sel(self):
        folderpath='/home/a/Desktop/github/clothingscrapers/thenextclosetscrapper/'+self.directoryname+"/"
        owd=os.getcwd()
        owd
        os.chdir(owd)
        driver = self.driver
        driver.get(self.base_url)
        htmlcheck=[driver.page_source]
        greaterhtml=[]
        itemlinks=[]
        getlastpage_soup=BeautifulSoup(driver.page_source, 'lxml')
        thepagnation=getlastpage_soup.findAll("span", {"class": "page-number"})
        self.lastpage=(thepagnation[0].getText().split()[-1].strip())
        for page in range(1,int(self.lastpage)+1):
            driver = self.driver
            delay = 3
            base_url = "https://thenextcloset.com/items?button=&number_of_items=60&page="+str(page)+"&search="+self.branddirect
            driver.get(base_url)
            WebDriverWait(driver, delay)
            for i in range(1,1000):
                print(i)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                htmlcheck.append(driver.page_source)
                if htmlcheck[-1] == htmlcheck[-2]:
                    break
                greaterhtml.append(htmlcheck[-1])
        for productpage in greaterhtml:
            soup=BeautifulSoup(productpage, 'lxml')
            for product in soup.findAll("div", {"data-testid": "product-card-wrapper"}):
                for thea in product.find_all('a',href=True):
                    itemlinks.append(thea['href'])
        for eachitem in itemlinks:
            if self.branddirect.replace("+","-") in eachitem:
                spliturlslash=eachitem.split("/")
                itemcode=spliturlslash[-1]
                if not os.path.exists(folderpath+itemcode):
                    os.makedirs(folderpath+itemcode)
                    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                    headers = { 'User-Agent' : user_agent }
                    item_req = Request("https://thenextcloset.com/"+eachitem, headers=headers)
                    item_page = urlopen(item_req).read()
                    item_soup = BeautifulSoup(item_page, 'lxml')
                    theprice=str(item_soup.findAll('div',attrs = {'id' : "current-price"})[-1].contents[-1])
                    if "</span" in theprice:
                        finalprice=theprice[theprice.index("€"):theprice.index("</span")].replace(".","")
                    else:
                        finalprice=theprice.replace(".","")
                    thesize=str(item_soup.findAll('div',attrs = {'class' : "size-color-row"})[-1])
                    splithesize=thesize.split("\n")
                    for divtag in splithesize:
                        if "Maat" in divtag:
                            cutsize=divtag[divtag.index('Maat:'):divtag.index('</p')]
                            finalsize=(cutsize.split()[-1])
                        if "Conditie:" in divtag:
                            thecondition=divtag[divtag.index('Conditie:')+9:divtag.index('</p')]
                            finalcondition=(thecondition.strip())
                    thebox=str(item_soup.findAll('dd',attrs = {'class' : "flex flex--stacked"})[-1])
                    splithebox=thebox.split("\n")
                    for eachdescp in splithebox:
                        if "OMSCHRIJVING" in eachdescp:
                            description=eachdescp[eachdescp.index('-20px">')+7:]
                        if 'KLEUR' in eachdescp:
                            colouris=eachdescp[eachdescp.index('KLEUR')+51:eachdescp.index('ITEM NUMMER')-34]
                    thematerial=item_soup.findAll('p',attrs = {'id' : "materiaal"})[-1].contents[-1]
                    append_list_as_row(folderpath+self.directoryname+"catalogue.csv",[self.branddirect.replace("+"," "), itemcode,"https://thenextcloset.com/"+eachitem,finalprice[1:],finalsize,colouris,thematerial,finalcondition,description,datetime.datetime.now()])
                    carouselimg=item_soup.findAll('ul',attrs = {'class' : "uk-slideshow-items"})[0]
                    carouselimgnest=carouselimg.findAll('a',attrs = {'href' : True})
                    for item_pic_url in carouselimgnest:
                        finalimg=str(item_pic_url['href']).split("/")
                        urllib.request.urlretrieve(str(item_pic_url['href']), str(finalimg[-1]))
                        shutil.move(folderpath+finalimg[-1],folderpath+itemcode+'/'+finalimg[-1])

if __name__ == "__main__":
    unittest.main()
