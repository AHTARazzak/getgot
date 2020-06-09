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
import datetime

brand="Rick Owens"
owd=os.getcwd()
owd

branddirect = brand.replace(" ","")
os.chdir(owd)
if not os.path.exists(branddirect):
    os.makedirs(branddirect)
os.chdir(branddirect)
getpagebrand=brand.replace(" ",".20")
basicurl = 'https://aucfan.com/search1/q-'+getpagebrand.lower()+'/s-mix/?p=1&o=p1&shipping=all'
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
dirtypagelist=pageitemsoup.findAll('ul',attrs = {'class' : "searchPaginationNav"})
dirtypagelist.pop()
cleanpagelist=str(dirtypagelist[0])
pagelistsplit=cleanpagelist.split("\n")
lastpage=pagelistsplit[-3]
lastpagenumber=lastpage[lastpage.index('">')+2:lastpage.index('</a')]
thebrandsearch=brand.replace(" ",".20")
class aucfanSpider(scrapy.Spider):
    name="aucfanscrapper"
    start_urls=['https://aucfan.com/search1/q-'+thebrandsearch+'/s-mix/']
    lastpagenumber=int(lastpagenumber)+1
    def start_requests(self):
        for i in range(self.lastpagenumber):
            yield scrapy.Request('https://aucfan.com/search1/q-'+thebrandsearch.lower()+'/s-mix/?p=%d&o=p1&shipping=all' % i, self.parse,dont_filter=True)
    def parse(self,response):
        # proceed to other pages of the listings
        for page_url in response.xpath('//a[contains(@class, "hdLink")]/@href').extract():
            page_url = response.urljoin(page_url)
            yield scrapy.Request(url=page_url, callback=self.parse)
            #print('okaydone')
            #print("".join(page_url)[-11:-1].replace("/", ""))
            itemcode="".join(page_url)[-11:-1].replace("/", "")
            if not os.path.exists(itemcode):
                os.makedirs(itemcode)
            if not os.path.exists(branddirect+'check.txt'):
                os.mknod(branddirect+'check.txt')
            with open(branddirect+'check.txt','r+') as checkf:
                if itemcode not in checkf.read():
                    checkf.write(itemcode+"\n")
                    checkf.close()
        desctext=response.css('div.colItemsAreaInner p.fSize04.tColor03.btmMgnSet2').getall()
        imagelist=[]
        if brand.lower() in str(desctext).lower():
            for prodimage in response.xpath('//div[contains(@class, "colItemsAreaInner")]//div/div').getall():
              pageurl=response.request.url[-11:-1].replace("/", "")
              if "data-src" in prodimage:
                if (prodimage.index("data-src"))==122:
                    imageurl=prodimage[prodimage.index("data-src")+10:].split()[0][:-1]
                    imagelist.append(imageurl)
            therows=response.xpath('//ul[contains(@class, "itemsCatePath")]/li/a').getall()
            if len(therows)>3:
                thetype=therows[3][therows[3].find('t1">')+4:therows[3].find("</a>")]
                size=therows[4][therows[4].find('t1">')+4:therows[4].find("</a>")]
            else:
                thetype="N/A"
                size="N/A"
            thepricebox=response.xpath('//em[contains(@class, "amount")]').getall()
            price=thepricebox[0][thepricebox[0].find('">')+2:thepricebox[0].find("</em>")]
            yield {
            'Brand' : thebrandsearch,
            'ItemCode' : pageurl,
            'URL' : str(response.request.url),
            'Price(YEN)' : price,
            'Size' : size,
            'Type' : thetype,
            'Time' : datetime.datetime.now(),
            }
                           # print(imageurl)
            nodupimages=list(dict.fromkeys(imagelist))
            #print(nodupimages)
            [urllib.request.urlretrieve(str(image), str(image[image.rfind("/")+1:])) for image in nodupimages]
            time.sleep(2)
            [shutil.move(os.getcwd()+'/'+str(image[image.rfind("/")+1:]), os.getcwd()+'/'+pageurl+'/'+str(image[image.rfind("/")+1:])) for image in nodupimages]
