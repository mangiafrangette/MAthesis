import scrapy
import csv
import os
import json

# DSH SPIDER
class ArticlesSpider(scrapy.Spider):
    name = "affiliations"
    def start_requests(self):      
        with open("../../../../data/json_files/my_schema/ms_CF_Digital_Studies__Le_champ_numérique.json", "r", encoding="utf-8") as f:
                articles = json.load(f)
                for article in articles:
                    url = article["url"]
                    yield scrapy.Request(url=url, callback=self.parse, meta={"id": article["identifier"]["string_id"]})
                    # parse scrapy data
    def parse(self, response): 
        # le champ                
        authors = response.xpath('//meta[@name="citation_author"]/@content').getall()
        authors_institutions = response.xpath('//meta[@name="citation_author_institution"]/@content').getall()

        author_dicts_list = []
        for index1, author in enumerate(authors):
            for index2, institution in enumerate(authors_institutions):
                if index1 == index2:
                    names = author.split()
                    if len(names) == 2:
                        author_dict = {
                                'given': names[0],
                                'family' : names[1],
                                'affiliation' : [institution]
                                }
                        author_dicts_list.append(author_dict)
                    else:
                        author_dict = {
                                'given': author,
                                'family' : None,
                                'affiliation' : [institution]
                                }
                        author_dicts_list.append(author_dict)
        yield {
            "string_id": response.meta["id"],
            "authors": author_dicts_list
        } 


       