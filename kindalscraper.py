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

brandnamefile = open("thebrand.txt", "r+")
brand = brandnamefile.read()

owd=os.getcwd()
owd
def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)

def getalllinks(brandname,thepage):
    url=kindurl+str(brandname)+"&p="+str(thepage)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    values = {'name' : names.get_full_name(),
        'location' : 'Northampton',
        'language' : 'Python' }
    headers = { 'User-Agent' : user_agent }
    req = Request(url, headers=headers)
    the_page = urlopen(req).read()
    pageitemsoup = BeautifulSoup(the_page, 'lxml')
    linktags=pageitemsoup.find_all('div',{'class' : 'item'})
    for alinks in linktags:
        theatag=str(alinks.find_all('a')[0])
        linklist.append("https://shop.kind.co.jp"+theatag[theatag.index('href')+6:theatag.find('target')-2])
    return(linklist)

def getgetpagerange(brandname):
    checkpage=True
    thepage=1
    while checkpage:
        url=kindurl+str(brandname)+"&p="+str(thepage)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        values = {'name' : names.get_full_name(),
            'location' : 'Northampton',
            'language' : 'Python' }
        headers = { 'User-Agent' : user_agent }
        req = Request(url, headers=headers)
        the_page = urlopen(req).read()
        pageitemsoup = BeautifulSoup(the_page, 'lxml')
        try:
            pagesection=pageitemsoup.find_all('ul',{'class' : 'pager clearfix'})[0]
            pagesectionli=pagesection.find_all('li')
            if "<em>" not in str(pagesectionli[-1]):
                thepage+=1
            else:
                return thepage
                checkpage=False
        except IndexError:
            thepage=1
            return thepage

thebrand=(brand.replace(" ","+").lower())
kindurl='https://shop.kind.co.jp/item_list/?kw='
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
    itemcode=spliturl[-2]
    if not os.path.exists("kindal_"+itemcode):
        ax=0
        bx=0
        cx=0
        dx=0
        ex=0
        fx=0
        gx=0
        os.makedirs("kindal_"+itemcode)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        values = {'name' : names.get_full_name(),
            'location' : 'Northampton',
            'language' : 'Python' }
        headers = { 'User-Agent' : user_agent }
        item_req = Request(itemurl, headers=headers)
        item_page = urlopen(item_req).read()
        item_soup = BeautifulSoup(item_page, 'lxml')
        formarea=item_soup.find_all('div',{'class' : 'form_area'})[0]
        itemtitle=formarea.find_all('h1')
        brandis=(str(itemtitle)[str(itemtitle).index("</span>")+7:str(itemtitle).index("<br/>")].strip())
        titleis=(str(itemtitle)[str(itemtitle).index("<br/>")+5:str(itemtitle).index("</h1>")].strip())
        priceinfo=formarea.find_all('p',{'class' : 'sp'})[0]
        priceis=(str(priceinfo)[str(priceinfo).index('"sp">')+5:str(priceinfo).index("円")])
        detailarea=item_soup.find_all('p',{'class' : 'style2'})[0]
        detailsplit=str(detailarea).split("<strong>")
        if "/contents/images/soldout_icon.gif" in str(formarea):
            gx=1
            availabilityis="SOLD OUT"
        if gx==0:
            availabilityis="AVAILABLE"
        for detail in detailsplit:
            if "【素材】" in str(detail):
                ax=1
                materialis=(str(detail)[str(detail).index("</strong>")+9:str(detail).index("<br/>")])
            if ax==0:
                materialis="N/A"
            if "【カラー】" in str(detail):
                bx=1
                colouris=(str(detail)[str(detail).index("</strong>")+9:str(detail).index("<br/>")])
            if bx==0:
                colouris="N/A"
            if "【表記サイズ】" in str(detail):
                cx=1
                sizeis=(str(detail)[str(detail).index("</strong>")+9:str(detail).index("<br/>")])
            if cx==0:
                sizeis="N/A"
            if "【製造番号】" in str(detail):
                dx=1
                modelis=(str(detail)[str(detail).index("</strong>")+9:str(detail).index("<br/>")])
            if dx==0:
                modelis="N/A"
            if "【詳細情報】" in str(detail):
                ex=1
                descriptionis=(str(detail)[str(detail).index("</strong>")+9:str(detail).index("<br/>")])
            if ex==0:
                descriptionis="N/A"
            if "【ダメージ】" in str(detail):
                fx=1
                conditionis=(str(detail)[str(detail).index("</strong>")+9:str(detail).index("<br/>")])
            if fx==0:
                conditionis="N/A"
        allimages=item_soup.find_all('div',{'class' : 'image_area'})[0]
        liiages=allimages.find_all('a')
        thetimeis=datetime.datetime.now()
        imageurls=[]
        for imagetag in liiages:
            imagestr=str(imagetag)
            imageurls.append(imagestr[imagestr.index("href=")+6:imagestr.index("rel=")-2])
        for clothingimage in imageurls:
            splitimage=clothingimage.split('/')
            urllib.request.urlretrieve(str(clothingimage), str(splitimage[-1][:splitimage[-1].index(".jpg")+4]))
            shutil.move(os.getcwd()+'/'+str(splitimage[-1][:splitimage[-1].index(".jpg")+4]), os.getcwd()+'/'+"kindal_"+itemcode+'/'+str(splitimage[-1][:splitimage[-1].index(".jpg")+4]))
        ax=1
        bx=1
        cx=1
        dx=1
        ex=1
        fx=1
        gx=1
        append_list_as_row(brand.replace(" ","")+"catalogue.csv",["kindal", brandis, "kindal_"+itemcode,itemurl,str(re.findall("\d+", priceis)[0]) + " (YEN)","N/A",titleis,availabilityis,materialis,colouris,sizeis,modelis,descriptionis,conditionis,thetimeis])
