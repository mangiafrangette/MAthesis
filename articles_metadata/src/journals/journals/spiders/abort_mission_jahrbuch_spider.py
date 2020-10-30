import scrapy
import csv
import os
import json

# abort mission...........
class ArticlesSpider(scrapy.Spider):
    name = "jahrbuch"
    def start_requests(self):      
        filename = "../../../../data/json_files/full_list_of_ids.json" 
        with open(filename, "r", encoding="utf-8") as f:
            journals = json.load(f)
            for journal in journals:
                if "Jahr" in journal["journal_title"]:
                    for url in journal["research_articles"]:
                        yield scrapy.Request(url=url, callback=self.parse) 
    
    # parse scrapy data
    def parse(self, response): 
        url = response.url
        id_scheme = None 
        string_id = None
        abstract = response.xpath('//div[@id="abstract_en"]').get()
        article_title = response.xpath('//h1[@class="page-header"]').get()
        authors = response.xpath('//div[@style="margin: 1em 0 1em 0;"]').getall()
        date = response.xpath('//div[@id="info1"]/p[3]').get()
        keywords = response.xpath('//div[@id="info2"]/p[3]').get()
        issue = []
        volume = response.xpath('//div[@id="breadcrumb"]/a[2]').get()
        publisher = []
        
        #get authors and their affiliations
        authors_dicts_list = []
        for index, author_name in enumerate(authors):
            index += 1
            author_meta = response.xpath('//*[@id="author{}"]'.format(index)).get()
            
            print(author_meta)
            author_dict = {
                'given': author_name,
                'family': [],
                'affiliation': author_meta
            }
            authors_dicts_list.append(author_dict)

        yield {
        "url": url,
        "identifier": {
            "string_id": string_id,
            "id_scheme": id_scheme
        },
        "abstract": abstract,
        "article_title": article_title,
        "authors": authors_dicts_list,
        "publisher": publisher,
        "date": date,
        "keywords": keywords,
        "journal_title": "Journal of Data Mining & Digital Humanities",
        "volume": volume,
        "issue": issue,
        "ISSN": [
            {
                "value": [],
                "type": "electronic"
            }
        ]
    }

                    
    
            

    
