import scrapy
from googletrans import Translator
import os
import urllib.request, urllib.error, urllib.parse
from urllib.request import Request, urlopen
import urllib.parse
import time
import random
import shutil
import names
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
import datetime

brand="Rick Owens"
owd=os.getcwd()
owd
branddirect = brand.replace(" ","")
os.chdir(owd)
if not os.path.exists(branddirect):
    os.makedirs(branddirect)
os.chdir(branddirect)
getpagebrand=brand.replace(" ","+")
basicurl = 'https://www.kijiji.it/'+getpagebrand.lower()+'/?p=1&entryPoint=sb'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
values = {'name' : names.get_full_name(),
'location' : 'Northampton',
'language' : 'Python' }
headers = { 'User-Agent' : user_agent }
data = urllib.parse.urlencode(values)
data = data.encode('ascii')
req = Request(basicurl, headers=headers)
the_page = urlopen(req).read()
pageitemsoup = BeautifulSoup(the_page, 'lxml')
pagearea=pageitemsoup.find_all('div',{'class' : 'page-count'})[0]
pageareaspan=pagearea.find_all('span')
lastpage=(pageareaspan[-1].contents[0])
class kijijiScrapper(scrapy.Spider):
    name="kijijiscrapper"
    #start_urls=['https://www.kijiji.it/'+getpagebrand.lower()+'/?p=1&entryPoint=sb']
    #for pages in range(1,int(lastpage)+1):
    lastpage=lastpage
    def start_requests(self):
        for pages in range(1,int(self.lastpage)+1):
            yield scrapy.Request('https://www.kijiji.it/-'+str(getpagebrand.lower())+'/?p='+str(pages)+'&entryPoint=sb', self.parse,dont_filter=True)
    def parse(self,response):
        # proceed to other pages of the listings
        for page_url in response.xpath('//li[contains(@class, "item result  gtm-search-result")]/@data-href').extract():
            page_url = response.urljoin(page_url)
            yield scrapy.Request(url=page_url, callback=self.parse)
            itemcode=(page_url.split('/')[-2])
            if not os.path.exists(itemcode):
                os.makedirs(itemcode)
            if not os.path.exists(branddirect+'check.txt'):
                os.mknod(branddirect+'check.txt')
            with open(branddirect+'check.txt','r+') as checkf:
                if itemcode not in checkf.read():
                    checkf.write(itemcode+"\n")
                    checkf.close()
        desctext=response.xpath('//p[contains(@class,"text vip__text-description")]').extract()
        imagelist=[]
        if len(desctext)>0:
            if brand.lower() in desctext[0].lower():
                imagelist=[]
                titletag=response.xpath('//h1[contains(@class,"heading-4 font-weight-regular vip__title")]').extract()
                if len(titletag)>0:
                    findtitle=str(titletag)
                    if "title" in findtitle:
                        titleis=(findtitle[findtitle.index('">')+2:findtitle.index("</h1")][2:].strip()[:-2].strip())
                pricetag=response.xpath('//h2[contains(@class,"heading-4 color-blue-500 font-weight-regular vip__price")]').extract()
                if len(pricetag)>0:
                    findprice=str(pricetag[0])
                    if "€" in findprice:
                        #print(findprice)
                        priceis=(findprice[findprice.index('">')+2:findprice.index("€")].strip())
                imagecarousel=response.xpath('//img[contains(@class,"image-wrap__picture")]').extract()
                if len(imagecarousel)>0:
                    for imagetag in imagecarousel:
                        imagetag=str(imagetag)
                        imagelist.append(imagetag[imagetag.index('src=')+5:imagetag.index('alt=')-2])
                itemcode=str(response.request.url).split("/")[-2]
                yield {
                'Brand' : brand,
                'ItemCode' : itemcode,
                'URL' : str(response.request.url),
                'Title' : titleis,
                'Price(EUR)' : priceis,
                'Time' : datetime.datetime.now(),
                }
                count=0
                for clothingimage in imagelist:
                    splitimage=clothingimage.split('/')
                    urllib.request.urlretrieve(str(clothingimage), str(splitimage[-1]))
                    time.sleep(2)
                    shutil.move(os.getcwd()+'/'+splitimage[-1], os.getcwd()+'/'+itemcode+'/'+str(count)+splitimage[-1])
                    count+=1
