import scrapy
import csv
import os
import json

class ArticlesSpider(scrapy.Spider):
    name = "ijhacauthors"
    def start_requests(self):      
        filename = "../../../../data/json_files/my_schema/ms_IJHAC.json" 
        with open(filename, "r", encoding="utf-8") as f:
            articles = json.load(f)
            for article in articles:
                url = article["url"]
                yield scrapy.Request(url=url, callback=self.parse, meta={"id": article["identifier"]["string_id"]})
    # parse scrapy data
    def parse(self, response):                 
        
        publisher = response.xpath('//meta[@name="dc.Publisher"]/@content').get()
        authors = response.xpath('//meta[@name="dc.Creator"]/@content').getall()
        date = response.xpath('//meta[@name="dc.Date"]/@content').getall()

        author_dicts_list = []
        for author in authors:
            names = author.split()
            if len(names) == 2:
                author_dict = {
                        'given': names[0],
                        'family' : names[1],
                        'affiliation' : [None]
                        }
                author_dicts_list.append(author_dict)
            else:
                author_dict = {
                        'given': author,
                        'family' : None,
                        'affiliation' : [None]
                        }
                author_dicts_list.append(author_dict)
        
        yield {
            "string_id": response.meta["id"],
            "authors": author_dicts_list,
            "publisher": publisher,
            "date": date
        } 

# questa cosa poi va scritta sul documento ufficiale! 

                    
    
            

    
