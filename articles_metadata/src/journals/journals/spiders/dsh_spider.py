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
        authors = response.xpath('//meta[@name="citation_author"]').getall()
        authors_institutions = response.xpath('//meta[@name="citation_author_institution"]').getall()

        author_dicts_list = []
        for index1, author in enumerate(authors):
            for index2, institution in enumerate(authors_institutions):
                if index1 == index2:
                    author_dict = {
                            'given': author,
                            'family' : "",
                            'affiliation' : [institution]
                            }
                    author_dicts_list.append(author_dict)                 
        
        yield {
        "string_id": url,
        "abstract": abstract,
        "authors": author_dicts_list
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


                    
    
            

    
