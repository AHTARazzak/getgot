#need to redo in selenium

from requests_html import HTMLSession
import sys
import urllib.request, urllib.error, urllib.parse
import webbrowser
from bs4 import BeautifulSoup
import pyautogui
import time
import requests
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

thebrands=['Rick Owens']
owd=os.getcwd()
owd
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def adjustbrandname(brands):
    editbrands=[]
    for brand in brands:
        editbrand=brand.replace(" ","+")
        editbrands.append(editbrand.lower())
    return editbrands

def getalllinks(brandname,thepage):
    url=mpurl+'/q/'+str(brandname.replace(" ","+").lower())+"/p/"+str(thepage)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    values = {'name' : names.get_full_name(),
        'location' : 'Northampton',
        'language' : 'Python' }
    headers = { 'User-Agent' : user_agent }
    req = Request(url, headers=headers)
    the_page = urlopen(req).read()
    pageitemsoup = BeautifulSoup(the_page, 'lxml')
    linktags=pageitemsoup.find_all('a',{'class' : 'mp-Listing-coverLink'})
    for alinks in linktags:
        linklist.append(alinks.get('href'))
    return(linklist)

#getalllinks('Rick Owens',1)

def getgetpagerange(brandname):
    checkpage=True
    thepage=1
    while checkpage:
        url=mpurl+'/q/'+str(brandname.replace(" ","+").lower())+"/p/"+str(thepage)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        values = {'name' : names.get_full_name(),
            'location' : 'Northampton',
            'language' : 'Python' }
        headers = { 'User-Agent' : user_agent }
        req = Request(url, headers=headers)
        the_page = urlopen(req).read()
        pageitemsoup = BeautifulSoup(the_page, 'lxml')
        pagesection=[eachtag for eachtag in pageitemsoup.find_all('span',{'class' : 'mp-PaginationControls-pagination-pageList'})[0]]
        if "<span>" not in str(pagesection[-1]):
            thepage+=1
            print(thepage)
        else:
            return thepage
            checkpage=False

for thebrand in adjustbrandname(thebrands):
    mpurl='https://www.marktplaats.nl'
    linklist=[]
    os.chdir(owd)
    if not os.path.exists(thebrand):
        os.makedirs(thebrand)
    os.chdir(thebrand)
    if not os.path.exists(thebrand+"catalogue.csv"):
        append_list_as_row(thebrand+"catalogue.csv",["Brand", "ItemCode","URL","ItemName","Price(YEN)","Availability","Time","Material", "Colour", "Size", "Model", "Description", "Condition"])
    for page in range(1,getgetpagerange(thebrand)+1):
        allthelinks=getalllinks(thebrand,page)
    owd=os.getcwd()
    owd
    for itemurl in allthelinks:
        spliturl=itemurl.split("/")
        itemcode=spliturl[-1]
        if not os.path.exists(itemcode):
            ax=0
            lengthis="N/A"
            bx=0
            colouris="N/A"
            cx=0
            conditionis="N/A"
            dx=0
            sizeis="N/A"
            ex=0
            os.makedirs(itemcode)
            user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
            values = {'name' : names.get_full_name(),
                'location' : 'Northampton',
                'language' : 'Python' }
            headers = { 'User-Agent' : user_agent }
            item_req = Request(mpurl+itemurl, headers=headers)
            #item_req1 = requests.get(mpurl+itemurl, timeout=(3.05, 27))
            print(item_req)
            #print(item_req1)
            #requests.get('https://github.com', timeout=(3.05, 27))
            item_page = urlopen(item_req).read()
            time.sleep(3)
            item_soup = BeautifulSoup(item_page, 'lxml')
            thedescription=item_soup.findAll('div',{'id' : 'vip-ad-description'})[0].text
            thetitle=item_soup.find_all('h1',{'class' : 'title'})[0].text
            theprice=item_soup.find_all('span',{'class' : 'price'})[0].text
            formarea=item_soup.find_all('table',{'class' : 'first-column attribute-table single-value-attributes'})
            if len(formarea)>0:
                itemrow=[eachtag for eachtag in formarea[0].find_all('tr')[0]]
                if 'Lengte' in itemrow[1]:
                    ax=1
                    lengthis=itemrow[-2].text
                    print(lengthis)
                if ax==0:
                    lengthis="N/A"
                if 'Kleur' in itemrow[1]:
                    bx=1
                    colouris=itemrow[-2].text
                    print(colouris)
                if bx==0:
                    colouris="N/A"
                if 'Conditie' in itemrow[1]:
                    cx=1
                    conditionis=itemrow[-2].text
                    print(colouris)
                if cx==0:
                    conditionis="N/A"
                if 'Maat' in itemrow[1]:
                    dx=1
                    sizeis=itemrow[-2].text
                    print(sizeis)
                if dx==0:
                    sizeis="N/A"
            allimages=item_soup.find_all('div',{'class' : 'carousel-viewport'})
            print(allimages)
            '''
            liiages=allimages.find_all('a')
            thetimeis=datetime.datetime.now()
            imageurls=[]
            for imagetag in liiages:
                imagestr=str(imagetag)
                imageurls.append("https://shop.kind.co.jp"+imagestr[imagestr.index("href=")+6:imagestr.index("rel=")-2])
            for clothingimage in imageurls:
                splitimage=clothingimage.split('/')
                urllib.request.urlretrieve(str(clothingimage), str(splitimage[-1]))
                shutil.move(os.getcwd()+'/'+splitimage[-1], os.getcwd()+'/'+itemcode+'/'+splitimage[-1])
            ax=1
            bx=1
            cx=1
            dx=1
            ex=1
            fx=1
            gx=1
            append_list_as_row(thebrand+"catalogue.csv",[brandis, itemcode,itemurl,titleis,priceis,availabilityis,thetimeis,materialis,colouris,sizeis,modelis,descriptionis,conditionis])
            print(itemcode)
'''
