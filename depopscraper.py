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
from csv import writer
import datetime
import unittest, time, re

brandnamefile = open("thebrand.txt", "r+")
brand = brandnamefile.read()

chromepathfile = open("chromepath.txt", "r+")
chromepath = chromepathfile.read()

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
        self.base_url = "https://www.depop.com/search/?q="+branddirect
        self.verificationErrors = []
        self.accept_next_alert = True
    def test_sel(self):
        owd=os.getcwd()
        directoryname=brand.replace(" ","")
        folderpath=owd
        owd
        os.chdir(owd)
        driver = self.driver
        delay = 3
        driver.get(self.base_url)
        htmlcheck=[driver.page_source]
        for i in range(1,100):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            htmlcheck.append(driver.page_source)
            if htmlcheck[-1] == htmlcheck[-2]:
                break
            html_source=htmlcheck[-1]
        soup=BeautifulSoup(html_source, 'lxml')
        itemlinks=[]
        nice=soup.findAll('a')
        for a in soup.find_all('a',href=True):
            if "product__item" in str(a):
                start_index=str(a).index("href=")
                end_index=str(a).index("<div")
                itemlinks.append("https://www.depop.com"+str(a)[start_index+6:end_index-2])
        itemlinks=itemlinks[1:]
        for item in itemlinks:
            spliturlslash=item.split("/")
            splitlasthyphen=spliturlslash[-2].split("-")
            itemcode=splitlasthyphen[0]
            if not os.path.exists(folderpath+"/"+"depop_"+itemcode):
                os.makedirs(folderpath+"/"+"depop_"+itemcode)
                user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                headers = { 'User-Agent' : user_agent }
                item_req = Request(item, headers=headers)
                item_page = urlopen(item_req).read()
                item_soup = BeautifulSoup(item_page, 'lxml')
                for theprice in item_soup.findAll('span',attrs = {'class' : True}):
                    if "Pricestyles__DiscountPrice" in str(theprice):
                        thepriceis=str(theprice.contents[0])+str(theprice.contents[-1])
                    elif "Pricestyles__FullPrice" in str(theprice):
                        thepriceis=str(theprice.contents[0])+str(theprice.contents[-1])
                for thesize in item_soup.findAll('td',attrs = {'class' : "TableCell-zjtqe7-0 fxiPRF"}):
                    if "Pricestyles" not in str(thesize):
                        thesizeis=thesize.contents[0]
                    else:
                        thesizeis="N/A"
                append_list_as_row(folderpath+"/"+directoryname+"catalogue.csv",["depop",splitlasthyphen[1]+splitlasthyphen[2], "depop_"+itemcode,item,str(re.findall("\d+", thepriceis)[0])+" (GBP)","N/A", "N/A", "Yes", "N/A","N/A",thesizeis,"N/A","N/A","N/A",datetime.datetime.now()])
                options = webdriver.ChromeOptions()
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--incognito')
                options.add_argument('--headless')
                driver = webdriver.Chrome(chromepath, options=options)
                driver.get(item)
                for i in range(1,20):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    htmlcheck.append(driver.page_source)
                    if htmlcheck[-1] == htmlcheck[-2]:
                        break
                    pic_source=htmlcheck[-1]
                picsoup=BeautifulSoup(pic_source, 'lxml')
                theimages=picsoup.find_all('img',attrs = {'src' : True})
                imageslist=[]
                for eachimage in theimages:
                    if "U" not in eachimage['src']:
                        imageslist.append(eachimage['src'])
                for item_pic_url in imageslist:
                    finalimg=item_pic_url.split("/")
                    urllib.request.urlretrieve(str(item_pic_url), str(finalimg[-2]))
                    shutil.move(folderpath+"/"+finalimg[-2],folderpath+"/"+"depop_"+itemcode+'/'+finalimg[-2])
                    time.sleep(random.randint(0,2))
if __name__ == "__main__":
    unittest.main()
