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

brand="Rick Owens"
owd=os.getcwd()
owd
branddirect = brand.replace(" ","+")
os.chdir(owd)
if not os.path.exists(branddirect):
    os.makedirs(branddirect)
os.chdir(branddirect)
getpagebrand=brand.replace(" ",".20")
class mericareSpider(scrapy.Spider):
    name="mercariscraper"
    #start_urls=['https://aucfan.com/search1/q-'+thebrandsearch+'/s-mix/']
    def start_requests(self):
        yield scrapy.Request("https://www.mercari.com/jp/search/?keyword="+branddirect, self.parse,dont_filter=True)
    def parse(self,response):
        itemcode=[]
        # proceed to other pages of the listings
        avaliablepages = response.xpath('//li[contains(@class, "pager-cell")]').getall()
        if len(avaliablepages)>2:
            breaklines=avaliablepages[1].split("\n")
            #print(breaklines[1][breaklines[1].index('href')+6:breaklines[1].index('">')])
            #print(breaklines[1][breaklines[1].index('">')+2:breaklines[1].index("</a")])
        for page_url in response.xpath('//figure[contains(@class, "items-box-photo")]/img').extract():
            itemcode.append(page_url[page_url.index("photos/")+7:page_url.index("_1")])
        nodupitems=list(dict.fromkeys(itemcode))
        #print(nodupitems)
        for item in nodupitems:
            fullurl="https://www.mercari.com/jp/items/"+item
            pageurl=response.urljoin(fullurl)
            yield scrapy.Request(url=pageurl, callback=self.parse)
            if not os.path.exists(item):
                os.makedirs(item)
            if not os.path.exists(branddirect+'check.txt'):
                os.mknod(branddirect+'check.txt')
            with open(branddirect+'check.txt','r+') as checkf:
                if item not in checkf.read():
                    checkf.write(item+"\n")
                    theimages = response.xpath('//div[contains(@class, "owl-item-inner")]/img').getall()
                    [urllib.request.urlretrieve(itempic[itempic.find("data-src=")+10:itempic.find(".jpg")+4],itempic[itempic.find("/photos/")+8:itempic.find(".jpg")+4]) for itempic in theimages]
                    #time.sleep(3)
                    [shutil.move(os.getcwd()+'/'+str(itempic[itempic.find("/photos/")+8:itempic.find(".jpg")+4]), os.getcwd()+'/'+item+'/'+str(itempic[itempic.find("/photos/")+8:itempic.find(".jpg")+4])) for itempic in theimages]
                    theprice = response.xpath('//div[contains(@class, "item-price-box text-center")]/span').getall()
                    if len(theprice)>0:
                        theprincebox=theprice[0]
                        theprice=theprincebox[theprincebox.find('">')+3:theprincebox.find("</")]
                    elif len(theprice)<1:
                        theprice="N/A"
                    theboxall= response.xpath('//div[contains(@class, "item-main-content clearfix")]/table/tr/td').getall()
                    thetypeline=theboxall[1].split('\n')[3]
                    thetype=thetypeline[thetypeline.index("/i>")+4:thetypeline.index("</div")]
                    thebrandline=theboxall[2].split('\n')[3]
                    thesizeall=theboxall[3]
                    thesize=thesizeall[4:thesizeall.index("</td>")]
                    checksale=response.xpath('//div[contains(@class, "item-photo")]').getall()
                    for sale in checksale:
                        if "item-sold-out-badge" in sale:
                            sold='SOLD'
                        else:
                            sold="AVAILABLE"
                    yield {
                    'Brand' : thebrandline.strip(),
                    'ItemCode' : item,
                    'URL' : fullurl,
                    'Price' : theprice,
                    'Size' : thesize,
                    'Type' : thetype,
                    'Status' : sold
                    }
                    #themeta = response.xpath('//head/meta[contains(@name, "description")]').getall()
                    #metatxt=themeta[0][themeta[0].find("content=")+9:themeta[0].find('">')]
                    #print(metatxt)
                    #print(themeta[0])
                    #print(translator.translate(metatxt,src='ja',dest='en'))
            checkf.close()
