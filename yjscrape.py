from requests_html import HTMLSession
import sys
import urllib.request, urllib.error, urllib.parse
import webbrowser
from bs4 import BeautifulSoup
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
import re
import enchant
import shutil
import pandas as pd
from statistics import mean
import os
from urllib.request import Request, urlopen
import urllib.parse
from collections import OrderedDict
import names
import random
import csv
from csv import writer
import datetime
from currency_converter import CurrencyConverter

cc = CurrencyConverter()

brandnamefile = open("thebrand.txt", "r+")
brand = brandnamefile.read()

chromepathfile = open("chromepath.txt", "r+")
chromepath = chromepathfile.read().strip()

tocurrencyfile = open("currency.txt", "r+")
thecurrency = tocurrencyfile.read().strip()

owd=os.getcwd()
owd
def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)

def getalllinks(brandname,thepage):
    url=yjpurl+str(brandname)+'&exflg=1&b='+str((thepage*50)-50+1)+'&n=50&rc_ng=1'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    values = {'name' : names.get_full_name(),
        'location' : 'Northampton',
        'language' : 'Python' }
    headers = { 'User-Agent' : user_agent }
    req = Request(url, headers=headers)
    the_page = urlopen(req).read()
    pageitemsoup = BeautifulSoup(the_page, 'lxml')
    linktags=pageitemsoup.find_all('a',{'class' : 'Product__imageLink'})
    for itematag in linktags:
        linklist.append(itematag['href'])
    return(linklist)

def getgetpagerange(brandname):
    checkpage=True
    thepage=1
    while checkpage:
        url=yjpurl+str(brandname)+'&exflg=1&b='+str((thepage*50)-50+1)+'&n=50&rc_ng=1'
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        values = {'name' : names.get_full_name(),
            'location' : 'Northampton',
            'language' : 'Python' }
        headers = { 'User-Agent' : user_agent }
        req = Request(url, headers=headers)
        the_page = urlopen(req).read()
        pageitemsoup = BeautifulSoup(the_page, 'lxml')
        pagesection=pageitemsoup.find_all('li',{'class' : 'Pager__list'})
        if "</span>" not in str(pagesection[-2]):
            thepage+=1
        else:
            return thepage
            checkpage=False

thebrand=(brand.replace(" ","+").lower())
yjpurl='https://auctions.yahoo.co.jp/search/search?p='
linklist=[]
os.chdir(owd)
if not os.path.exists(brand.replace(" ","")):
    os.makedirs(brand.replace(" ",""))
os.chdir(brand.replace(" ",""))
if not os.path.exists(brand.replace(" ","")+"catalogue.csv"):
    append_list_as_row(brand.replace(" ","")+"catalogue.csv",["Site", "Brand", "ItemCode","URL","Price","Type", "Title","Availability","Material", "Colour", "Size", "Model", "Description", "Condition","Time"])
for page in range(1,getgetpagerange(thebrand)+1):
    allthelinks=getalllinks(thebrand,page)
owd=os.getcwd()
owd
for itemurl in allthelinks:
    spliturl=itemurl.split("/")
    itemcode=spliturl[-1]
    if not os.path.exists("Y!J_"+itemcode):
        os.makedirs("Y!J_"+itemcode)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        values = {'name' : names.get_full_name(),
            'location' : 'Northampton',
            'language' : 'Python' }
        headers = { 'User-Agent' : user_agent }
        item_req = Request(itemurl, headers=headers)
        item_page = urlopen(item_req).read()
        item_soup = BeautifulSoup(item_page, 'lxml')
        thedescription=item_soup.find_all('dd',{'class' : 'ProductDetail__description'})
        starttime=(thedescription[1].contents[-1])
        endtime=(thedescription[2].contents[-1])
        startingprice=(thedescription[9].contents[-1])
        sellerid=(thedescription[10].contents[-1])
        currentprice=item_soup.find_all('dd',{'class' : 'Price__value'})
        currentpriceis=(currentprice[0].contents[0].replace("\n",""))
        itemtablerows=item_soup.find_all('tr',{'class' : 'ProductTable__row js-postionRight'})
        thecatagories=""
        for eachsection in itemtablerows:
            if "カテゴリ" in str(itemtablerows):
                theli=eachsection.find_all('li')
                for eachli in theli:
                    if "rsec:category" in str(eachli):
                        thea=eachli.find_all('a')
                        for final in thea:
                            thecatagories+=str(final.contents[0])+" "
            if "ブランド" in str(itemtablerows):
                theli=eachsection.find_all('li')
                for eachli in theli:
                    if "rsec:brand" in str(eachli):
                        thea=eachli.find_all('a')
                        thebrandis=thea[0].contents[0]
            else:
                thebrandis="N/A"
            if "状態" in str(itemtablerows):
                theli=eachsection.find_all('li')[0]
                splittheli=str(theli).split()
                theconditionis=splittheli[-2]
        getitemtitle=item_soup.find_all('h1',{'class' : 'ProductTitle__text'})
        thetitleis=(getitemtitle[0].contents[0].replace("\u3000"," "))
        imageurls=[]
        getimagewindow=item_soup.find_all('ul',{'class' : 'ProductImage__thumbnails'})
        if len(getimagewindow)>0:
            getimagewindow=getimagewindow[0]
            windowimages=getimagewindow.find_all('img',{'src':True})
            for theimage in windowimages:
                imageurls.append(theimage['src'])
            for clothingimage in imageurls:
                splitimage=clothingimage.split('/')
                urllib.request.urlretrieve(str(clothingimage), str(splitimage[-1]))
                shutil.move(os.getcwd()+'/'+splitimage[-1], os.getcwd()+'/'+"Y!J_"+itemcode+'/'+splitimage[-1])
        append_list_as_row(brand.replace(" ","")+"catalogue.csv",["Y!J", thebrandis, "Y!J_"+itemcode,itemurl,str(cc.convert(int(re.findall("\d+", currentpriceis)[0]),'JPY',thecurrency))+ " "+thecurrency,thecatagories,thetitleis,starttime,"N/A","N/A","N/A","N/A","N/A",theconditionis,datetime.datetime.now()])
