import scrapy
import csv
import os
import json
import requests

from stem import Signal
from stem.control import Controller


""" def renew_connection():
    with Controller.from_port(port = 9151) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM) """

class ArticlesSpider(scrapy.Spider):
    name = "dsh"
    def start_requests(self):      
        filename = "../../../../data/json_files/my_schema/ms_DSH.json" 
        with open(filename, "r", encoding="utf-8") as f:
            articles = json.load(f)
            for article in articles[10:15]:
                # renew_connection()
                url = article["url"]
                yield scrapy.Request(url=url, callback=self.parse, meta={"id": article["identifier"]["string_id"]})
        """ url = "http://dx.doi.org/10.1093/llc/fqq027"
        yield scrapy.Request(url=url, callback=self.parse) """
    
    
    # parse scrapy data
    def parse(self, response): 
        abstract = response.xpath('//section[@class="abstract"]').get()
        authors = response.xpath('//meta[@name="citation_author"]/@content').getall()
        authors_institutions = response.xpath('//meta[@name="citation_author_institution"]/@content').getall()

        #get authors and their affiliations
        authors_dicts_list = []
        for index1, author in enumerate(authors):
            for index2, institution in enumerate(authors_institutions):
                if index1 == index2:
                    names = author.split(",")
                    if len(names) == 2:
                        author_dict = {
                                'given': names[1],
                                'family' : names[0],
                                'affiliation' : [institution]
                                }
                        authors_dicts_list.append(author_dict)
                    else:
                        author_dict = {
                                'given': author,
                                'family' : None,
                                'affiliation' : [institution]
                                }
                        authors_dicts_list.append(author_dict)               
        
        yield {
        #"string_id": response.meta["id"],
        "abstract": abstract,
        "authors": authors_dicts_list
    }


                    
    
            

    
