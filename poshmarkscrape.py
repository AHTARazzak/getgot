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

def checkpage(pageurl):
    thispage=1
    start=True
    while start:
        url=pageurl+str(thispage)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        values = {'name' : names.get_full_name(),
            'location' : 'Northampton',
            'language' : 'Python' }
        headers = { 'User-Agent' : user_agent }
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')
        req = Request(url, headers=headers)
        the_page = urlopen(req).read()
        pageitemsoup = BeautifulSoup(the_page, 'lxml')
        finalpage=pageitemsoup.findAll('button',attrs = {'class' : 'btn btn--pagination'})[-2]
        lastpage=int(str(finalpage).split()[-2])+1
        thepage=pageitemsoup.findAll('button',attrs = {'class' : 'btn btn--pagination bg--light-gray fw--med'})
        inpage=int(str(thepage).split()[-2])
        if inpage!=lastpage:
            start = True
            thispage+=1
        else:
            start= False
    return(thispage)

def getthebrand(labels):
    page=1
    directoryname=brand.replace(" ","")
    labelcheck=brand.replace(" ","-")
    os.chdir(owd)
    if not os.path.exists(directoryname):
        os.makedirs(directoryname)
    os.chdir(directoryname)
    if not os.path.exists(directoryname+"catalogue.csv"):
        append_list_as_row(directoryname+"catalogue.csv",["Site", "Brand", "ItemCode","URL","Price","Type", "Title","Availability","Material", "Colour", "Size", "Model", "Description", "Condition","Time"])
    branddirect = brand.replace(" ","%20").lower()
    for i in range(1,checkpage("https://poshmark.com/search?query="+branddirect+"&type=listings&max_id=")+1):
        url="https://poshmark.com/search?query="+branddirect+"&type=listings&max_id="+str(i)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        values = {'name' : names.get_full_name(),
            'location' : 'Northampton',
            'language' : 'Python' }
        headers = { 'User-Agent' : user_agent }
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')
        req = Request(url, headers=headers)
        the_page = urlopen(req).read()
        pageitemsoup = BeautifulSoup(the_page, 'lxml')
        theurls=[]
        itemurls=[]
        links=pageitemsoup.findAll('a',attrs = {'href' : True,'class' : True})
        for link in links:
            if '/listing/' in str(link['href']):
                theurls.append(link['href'])
        for itemurl in theurls:
            if (labelcheck in itemurl) or (labelcheck.upper() in itemurl):
                findurl='https://poshmark.com'+itemurl
                itemurls.append(findurl)
        for item in itemurls:
            spliturl=item.split("-")
            itemcode=spliturl[-1]
            if not os.path.exists("poshmark_"+itemcode):
                os.makedirs("poshmark_"+itemcode)
                item_req = Request(item, headers=headers)
                item_page = urlopen(item_req).read()
                item_soup = BeautifulSoup(item_page, 'lxml')
                theprice=item_soup.findAll('h1')
                thepricetag=str(theprice[-1])
                thepriceis=(thepricetag.split()[1])
                catagories=item_soup.findAll('a',attrs = {'class' : "btn btn--tag tag-details__btn",'href' : True})[-1]
                catagoriesis=(str(catagories['href']).split("/")[-1])
                colour=item_soup.findAll('a',attrs = {'data-et-prop-listing_color' : True,'href' : True})
                if len(colour)>0:
                    colour=colour[0]
                    colouris=(str(colour['data-et-prop-listing_color']))
                else:
                    colouris="N/A"
                size=item_soup.findAll('button',attrs = {'class' : "size-selector__size-option btn btn--tertiary tc--lb fw--bold br--burgundy"})
                if len(size)>0:
                    size=size[0]
                    splitsize=str(size).split()
                    sizeis=splitsize[-2]
                else:
                    sizeis="N/A"
                append_list_as_row(directoryname+"catalogue.csv",["poshmark", brand, "poshmark_"+itemcode,item,str(cc.convert(int(re.findall("\d+", thepriceis)[0]),'USD',thecurrency)) + " "+thecurrency,catagoriesis,"N/A","N/A","N/A",colouris,sizeis,"N/A","N/A","N/A",datetime.datetime.now()])
                carouselli=item_soup.findAll('li',attrs = {'class' : "carousel__item carousel__item",'style' : True})
                for element in carouselli:
                    start=str(element).index("data-src")+10
                    end=str(element).index(" src")-1
                    item_pic_url=(str(element)[start:end])
                    finalimg=item_pic_url.split("/")
                    urllib.request.urlretrieve(str(item_pic_url), str(finalimg[-1]))
                    shutil.move(os.getcwd()+'/'+finalimg[-1], os.getcwd()+'/'+"poshmark_"+itemcode+'/'+finalimg[-1])
                    time.sleep(random.randint(0,2))
getthebrand(brand)
