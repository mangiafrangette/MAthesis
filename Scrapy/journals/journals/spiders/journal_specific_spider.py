import scrapy
import csv
import os
import json

# DSH SPIDER
class ArticlesSpider(scrapy.Spider):
    name = "dsh"
    def start_requests(self):      
        """ filename = "../../../../articles_metadata/data/json_files/my_schema/ms_DSH.json" 
        with open(filename, "r", encoding="utf-8") as f:
            articles = json.load(f)
            for article in articles: """
        url = "http://dx.doi.org/10.1093/llc/fqaa027"
        #yield scrapy.Request(url=url, callback=self.parse, meta={"id": article["identifier"]["string_id"]})
        yield scrapy.Request(url=url, callback=self.parse)
    
    # parse scrapy data
    def parse(self, response): 
        url = response.url
        abstract = response.xpath('//section[@class="abstract"]').get()
        
        yield {
        "string_id": url,
        "abstract": abstract
    }



# JOCCH SPIDER
""" class ArticlesSpider(scrapy.Spider):
    name = "jocch"
    def start_requests(self):      
        filename = "../../../../articles_metadata/data/json_files/my_schema/ms_JOCCH.json" 
        with open(filename, "r", encoding="utf-8") as f:
            articles = json.load(f)
            for article in articles:
                url = article["url"]
                yield scrapy.Request(url=url, callback=self.parse, meta={"id": article["identifier"]["string_id"]})
    
    # parse scrapy data
    def parse(self, response): 
        url = response.url
        abstract = response.xpath('//div[@class="abstractSection abstractInFull"]').get()
        
        yield {
        "url": url,
        "abstract": abstract
    } """


                    
    
            

    
