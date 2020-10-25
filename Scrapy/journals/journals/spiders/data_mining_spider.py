import scrapy
import csv
import os
import json

class ArticlesSpider(scrapy.Spider):
    name = "data_mining"
    def start_requests(self):
        urls = [
            "https://hal.archives-ouvertes.fr/hal-02280013v2",
            "http://arxiv.org/abs/1912.05082v3",
            "https://hal.archives-ouvertes.fr/hal-02520508v3",
            "https://hal.archives-ouvertes.fr/hal-01913435v3",
            "https://hal.archives-ouvertes.fr/hal-01915730v2",
            "https://hal.archives-ouvertes.fr/hal-02109972v2",
            "https://hal.archives-ouvertes.fr/hal-02513038v2",
            "http://arxiv.org/abs/1602.08715v2",
            "https://hal.archives-ouvertes.fr/hal-01671592v1",
            "https://hal.archives-ouvertes.fr/hal-01283638v2",
            "https://hal.archives-ouvertes.fr/hal-01281266v2",
            "https://hal.archives-ouvertes.fr/hal-01528092v2",
            "https://hal.archives-ouvertes.fr/hal-01287195v4",
            "https://hal.archives-ouvertes.fr/halshs-01543050v2",
            "https://hal.archives-ouvertes.fr/hal-01294158v2",
            "https://hal.archives-ouvertes.fr/hal-01265297v2",
            "http://arxiv.org/abs/1602.08844v2",
            "http://arxiv.org/abs/1603.01597v2",
            "http://arxiv.org/abs/1602.08657v2",
            "https://hal.archives-ouvertes.fr/hal-01276243v3",
            "https://hal.archives-ouvertes.fr/hal-01279493v2",
            "http://arxiv.org/abs/1603.01207v1",
            "https://hal.archives-ouvertes.fr/halshs-01557447v1",
            "https://hal.archives-ouvertes.fr/hal-01371751v3",
            "https://hal.archives-ouvertes.fr/halshs-01532877v2",
            "https://hal.archives-ouvertes.fr/hal-01294591v2",
            "https://hal.archives-ouvertes.fr/hal-01645124v2",
            "https://hal.archives-ouvertes.fr/hal-01280627v4",
            "https://hal.archives-ouvertes.fr/hal-01282568v4",
            "https://hal.archives-ouvertes.fr/hal-01759191v2",
            "https://hal.archives-ouvertes.fr/hal-01762730v5",
            "https://hal.archives-ouvertes.fr/hal-01466986v2",
            "https://hal.archives-ouvertes.fr/hal-01458216v1",
            "https://hal.archives-ouvertes.fr/hal-01456090v2",
            "https://hal.archives-ouvertes.fr/hal-01443713v1",
            "https://hal.archives-ouvertes.fr/hal-01466986v1",
            "http://arxiv.org/abs/1312.6675v2",
            "http://arxiv.org/abs/1402.2003v2",
            "https://hal.archives-ouvertes.fr/hal-00919370v3",
            "http://arxiv.org/abs/1312.5817v3",
            "http://arxiv.org/abs/1312.4617v2",
            "http://arxiv.org/abs/1311.5401v2",
            "https://hal.archives-ouvertes.fr/hal-01024985v4",
            "http://arxiv.org/abs/1010.0803v3",
            "http://arxiv.org/abs/1405.3539v3",
            "https://hal.archives-ouvertes.fr/hal-01279493v2",
            "http://arxiv.org/abs/1808.10685v3",
            "https://hal.archives-ouvertes.fr/hal-02154122v2",
            "https://hal.archives-ouvertes.fr/hal-02324617v2",
            "http://arxiv.org/abs/2001.01863v7",
            "http://arxiv.org/abs/1807.04892v4",
            "https://hal.archives-ouvertes.fr/hal-01981922v3",
            "http://arxiv.org/abs/1801.00912v3"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    # parse scrapy data
    def parse(self, response): 
        url = response.url
        affiliations = None
        issue = None
        issn_value = None
        issn_type = None
        publisher = None
        keywords = None
        volume = None
        if "https://arxiv.org" in url:
            id_scheme = "arXiv"
            string_id = response.xpath('//meta[@name="citation_arxiv_id"]/@content').get()
            abstract = response.xpath('//*[@id="abs"]/blockquote').get()
            article_title = response.xpath('//*[@id="abs"]/h1').get()
            # no affiliation anywhere
            authors = response.xpath('//meta[@name="citation_author"]/@content"]').getall()            
            date =  response.xpath('//meta[@name="citation_date"]/@content').get()
        else:
            id_scheme = "hal"
            string_id = response.xpath('//meta[@name="DC.identifier"][2]/@content').get()
            abstract = response.xpath('//div[@class="abstract-content"]').get()
            article_title = response.xpath('//h1[@class="title"]').get()
            authors = response.xpath('//meta[@name="citation_author"]/@content').getall()
            affiliation = response.xpath('meta[@name="citation_author_institution"]').getall()   
            date =  response.xpath('//meta[@name="citation_online_date"]/@content').get()
            keywords = response.xpath('//meta[@name="citation_keywords"]/@content').getall()
            volume = response.xpath('//meta[@name="citation_volume"]/@content').get()

        yield {
        "url": url,
        "identifier": {
            "string_id": string_id,
            "id_scheme": id_scheme
        },
        "abstract": abstract,
        "article_title": article_title,
         "authors": [
        {
        'given': author,
        'family' : "",
        'affiliation' : []
        }
        for author in authors
        ], 
        "publisher": publisher,
        "date": date,
        "keywords": keywords,
        "journal_title": "Journal of Data Mining & Digital Humanities",
        "volume": volume,
        "issue": issue,
        "ISSN": [
            {
                "value": issn_value,
                "type": issn_type
            }
        ]
    }


                    
    
            

    
