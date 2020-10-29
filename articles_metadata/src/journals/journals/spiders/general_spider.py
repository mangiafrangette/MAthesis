import scrapy
import csv
import os
import json

class ArticlesSpider(scrapy.Spider):
    name = "testini"
    def start_requests(self):
        path = '../../../../articles_metadata/data/json_files/my_schema'
        folder = os.fsencode(path)
        for file in os.listdir(folder):
            # entra nel file
            filename = os.fsdecode(file)
        
            with open(f'{path}/{filename}', "r", encoding="utf-8") as f:
                articles = json.load(f)
                for article in articles:
                    url = article["url"]
                    yield scrapy.Request(url=url, callback=self.parse, meta={"id": article["identifier"]["string_id"]})
    # parse scrapy data
    def parse(self, response):                 
        if response.xpath('//meta[@name="citation_abstract"]/@content').get() is not None:
            scraped_abstract = response.xpath('//meta[@name="citation_abstract"]/@content').get()
        else: 
            scraped_abstract = response.xpath('//meta[@name="DC.Description"]/@content').get()
        yield {
            "string_id": response.meta["id"],
            "abstract": scraped_abstract
        } 


        # write to document?
        """ with open("testini.json", "r", encoding="utf-8") as fd:
            for abstract in fd: 
                    article["abstract"] = abstract """

                    
    
            

    
