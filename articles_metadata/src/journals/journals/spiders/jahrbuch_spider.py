import scrapy
import csv
import os
import json

# DSH SPIDER
class ArticlesSpider(scrapy.Spider):
    name = "zeit"
    def start_requests(self):      
        urls = [
            "http://dx.doi.org/10.17175/sb004_006a" ,
             "http://dx.doi.org/10.17175/sb004_011",
            "http://dx.doi.org/10.17175/2019_005",
            "http://dx.doi.org/10.17175/sb003_012",
            "http://dx.doi.org/10.17175/2019_008",
            "http://dx.doi.org/10.17175/2020_001",
            "http://dx.doi.org/10.17175/2020_003",
            "http://dx.doi.org/10.17175/sb004_004",
            "http://dx.doi.org/10.17175/sb004_001",
            "http://dx.doi.org/10.17175/sb004_010",
            "http://dx.doi.org/10.17175/sb004_009",
            "http://dx.doi.org/10.17175/sb004_008",
            "http://dx.doi.org/10.17175/2019_002",
            "http://dx.doi.org/10.17175/2016_012",
            "http://dx.doi.org/10.17175/sb004_005",
            "http://dx.doi.org/10.17175/2019_003",
            "http://dx.doi.org/10.17175/sb004_003",
            "http://dx.doi.org/10.17175/2018_002",
            "http://dx.doi.org/10.17175/2018_003",
            "http://dx.doi.org/10.17175/2018_004",
            "http://dx.doi.org/10.17175/sb004_002",
            "http://dx.doi.org/10.17175/sb004_013",
            "http://dx.doi.org/10.17175/sb004_007",
            "http://dx.doi.org/10.17175/sb004_012",
            "http://dx.doi.org/10.17175/sb003_002",
            "http://dx.doi.org/10.17175/sb003_014",
            "http://dx.doi.org/10.17175/sb003_004",
            "http://dx.doi.org/10.17175/sb003_010",
            "http://dx.doi.org/10.17175/sb003_011",
            "http://dx.doi.org/10.17175/sb003_013",
            "http://dx.doi.org/10.17175/sb002_009",
            "http://dx.doi.org/10.17175/sb002_007",
            "http://dx.doi.org/10.17175/sb002_003",
            "http://dx.doi.org/10.17175/sb002_006",
            "http://dx.doi.org/10.17175/sb002_005",
            "http://dx.doi.org/10.17175/sb002_004",
            "http://dx.doi.org/10.17175/sb002_001",
            "http://dx.doi.org/10.17175/sb003_003",
            "http://dx.doi.org/10.17175/sb003_003",
            "http://dx.doi.org/10.17175/sb003_001",
            "http://dx.doi.org/10.17175/2016_010",
            "http://dx.doi.org/10.17175/2017_002",
            "http://dx.doi.org/10.17175/2017_003",
            "http://dx.doi.org/10.17175/2017_005",
            "http://dx.doi.org/10.17175/2017_006",
            "http://dx.doi.org/10.17175/2018_001",
            "http://dx.doi.org/10.17175/sb002_002",
            "http://dx.doi.org/10.17175/sb002_010",
            "http://dx.doi.org/10.17175/sb002_008",
            "http://dx.doi.org/10.17175/sb001_023",
            "http://dx.doi.org/10.17175/sb001_016",
            "http://dx.doi.org/10.17175/2016_002",
            "http://dx.doi.org/10.17175/2016_003",
            "http://dx.doi.org/10.17175/2016_004",
            "http://dx.doi.org/10.17175/2016_006",
            "http://dx.doi.org/10.17175/2016_009",
            "http://dx.doi.org/10.17175/2016_011",
            "http://dx.doi.org/10.17175/sb001_021",
            "http://dx.doi.org/10.17175/sb001_014",
            "http://dx.doi.org/10.17175/sb001_006",
            "http://dx.doi.org/10.17175/sb001_015",
            "http://dx.doi.org/10.17175/sb001_017",
            "http://dx.doi.org/10.17175/sb001_018",
            "http://dx.doi.org/10.17175/sb001_008",
            "http://dx.doi.org/10.17175/sb001_007",
            "http://dx.doi.org/10.17175/sb001_020",
            "http://dx.doi.org/10.17175/sb001_009",
            "http://dx.doi.org/10.17175/sb001_013",
            "http://dx.doi.org/10.17175/sb001_002",
            "http://dx.doi.org/10.17175/sb001_010",
            "http://dx.doi.org/10.17175/sb001_019",
            "http://dx.doi.org/10.17175/sb001_003",
            "http://dx.doi.org/10.17175/sb001_004",
            "http://dx.doi.org/10.17175/sb001_001" 
        ]
        for url in urls:
        #yield scrapy.Request(url=url, callback=self.parse, meta={"id": article["identifier"]["string_id"]})
            yield scrapy.Request(url=url, callback=self.parse)
    
    # parse scrapy data
    def parse(self, response): 
        url = response.url
        id_scheme = "DOI"
        string_id = response.xpath('//div[@id="info1"]/p[1]').get()
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

                    
    
            

    
