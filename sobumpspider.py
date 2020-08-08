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
from currency_converter import CurrencyConverter

cc = CurrencyConverter()

brandnamefile = open("thebrand.txt", "r+")
brand = brandnamefile.read()

chromepathfile = open("chromepath.txt", "r+")
chromepath = chromepathfile.read().strip()

tocurrencyfile = open("currency.txt", "r+")
thecurrency = tocurrencyfile.read().strip()

def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)

class Sel(unittest.TestCase):
    def setUp(self):
        owd=os.getcwd()
        owd
        directoryname=brand.replace(" ","")
        os.chdir(owd)
        if not os.path.exists(directoryname):
            os.makedirs(directoryname)
        os.chdir(directoryname)
        if not os.path.exists(directoryname+"catalogue.csv"):
            append_list_as_row(directoryname+"catalogue.csv",["Site", "Brand", "ItemCode","URL","Price","Type", "Title","Availability","Material", "Colour", "Size", "Model", "Description", "Condition","Time"])
        branddirect = brand.replace(" ","%20").lower()
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chromepath, options=options)
        self.driver.implicitly_wait(30)
        self.base_url = "https://sobump.com/search?q="+branddirect
        self.verificationErrors = []
        self.accept_next_alert = True
    def test_sel(self):
        brand='Rick Owens'
        owd=os.getcwd()
        folderpath=owd+"/"
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
        for item in itemlinks:
            spliturlslash=item.split("/")
            splitlasthyphen=spliturlslash[-1].split("-")
            itemcode=splitlasthyphen[0]
            try:
                itemtitle=item[item.index("-")+1:]
            except ValueError:
                itemtitle=item
            if not os.path.exists(folderpath+"sobump_"+itemcode):
                os.makedirs(folderpath+"sobump_"+itemcode)
                user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                headers = { 'User-Agent' : user_agent }
                item_req = Request(item, headers=headers)
                item_page = urlopen(item_req).read()
                item_soup = BeautifulSoup(item_page, 'lxml')
                try:
                    theprice=item_soup.findAll('div',attrs = {'class' : "product-sale-price"})[-1].contents
                    thepriceis=(theprice[0][1:])
                except IndexError:
                    pass
                thesize=item_soup.findAll('span',attrs = {'class' : "product-size"})
                if len(thesize)>0:
                    thesize=thesize[-1].contents
                    thesizeis=(thesize[0])
                else:
                    thesizeis="N/A"
                append_list_as_row(folderpath+brand.replace(" ","")+"catalogue.csv",["sobump",splitlasthyphen[1]+splitlasthyphen[2], "sobump_"+itemcode,item,str(cc.convert(int(re.findall("\d+", thepriceis)[0]),'GBP',thecurrency)) + " "+thecurrency,"N/A","N/A","N/A","N/A","N/A",thesizeis,"N/A","N/A","N/A",datetime.datetime.now()])
                carouselimg=item_soup.findAll('div',attrs = {'class' : "image-gallery-image"})
                for element in carouselimg:
                    item_pic_url=element.findChildren()[0]['src']
                    finalimg=item_pic_url.split("/")
                    urllib.request.urlretrieve(str(item_pic_url), str(finalimg[-1]))
                    shutil.move(folderpath+finalimg[-1],folderpath+"sobump_"+itemcode+'/'+finalimg[-1])
                    time.sleep(random.randint(0,2))
if __name__ == "__main__":
    unittest.main()
