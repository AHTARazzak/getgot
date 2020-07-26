#import scrapy
#from googletrans import Translator

#brands=["rick owens"]
#for brand in brands:
#    fixedbrand=brand.replace(" ",".20")
    
#start_url='https://aucfan.com/search1/q-'+fixedbrand+'/s-mix/?shipping=all&o=p1&location=0'
class aucfanSpider(scrapy.Spider):
    name="okay"
    start_urls=['https://aucfan.com/search1/q-rick.20owens/s-mix/?shipping=all&o=p1&location=0']
    def parse(self, response):
        # proceed to other pages of the listings
        for page_url in response.xpath('//a[contains(@class, "hdLink")]/@href').extract():
            page_url = response.urljoin(page_url)
            yield scrapy.Request(url=page_url, callback=self.parse)

        # extract the torrent items
        for tr in response.css('table.lista2t tr.lista2'):
            tds = tr.css('td')
            link = tds[1].css('a')[0]
            yield {
                'title' : link.css('::attr(title)').extract_first(),
                'url' : response.urljoin(link.css('::attr(href)').extract_first()),
                'date' : tds[2].css('::text').extract_first(),
                'size' : tds[3].css('::text').extract_first(),
                'seeders': int(tds[4].css('::text').extract_first()),
                'leechers': int(tds[5].css('::text').extract_first()),
                'uploader': tds[7].css('::text').extract_first(),
            }
