#!/usr/bin/env python

import scrapy

class BlockSpider(scrapy.spiders.Spider):

    name = "tagspider"

    def start_requests(self):

        urls = ['https://blockchain.info/tags?filter=2','https://blockchain.info/tags?filter=16','https://blockchain.info/tags?filter=8','https://blockchain.info/tags?filter=4']

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):
    
        addresstags = response.xpath("//body[@class='opaque-nav']/div[@class='container pt-100']/table[@class='table table-striped']/tbody/tr")

        for addresstag in addresstags:

            address_tag = addresstag.xpath("td")

            yield {
                'address':
                    address_tag[0].xpath("a/text()").extract_first().strip(), 
                'tag': 
                    address_tag[1].xpath("span[@class='tag']/text()").extract_first().strip(),
                'link':
                    address_tag[2].xpath("a/text()").extract_first().strip(),
                'verified': 
                    address_tag[3].xpath("img/@src").extract_first().strip().split('/')[2].split('_')[0] == "red",
          }

        next_page = None
        
        try:
            next_page=response.xpath("//body[@class='opaque-nav']/div[@class='container pt-100']/div[@class='center']/ul[@class='pagination']/li[@class='next ']/a/@href").extract_first().strip()
        except:
            pass

        if next_page is not None:
            current_url = response.request.url
            next_page_url = current_url.split('?')[0] + next_page
            yield scrapy.Request(response.urljoin(next_page_url))
            
