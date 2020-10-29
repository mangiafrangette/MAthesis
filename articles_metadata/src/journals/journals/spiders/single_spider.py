import scrapy
import csv
import os
import json

class ArticlesSpider(scrapy.Spider):
    name = "get_abstracts"
    def start_requests(self):      
        filename = "../../../../data/json_files/my_schema/ms_CF_Journal_of_the_Text_Encoding_Initiative.json" 
        with open(filename, "r", encoding="utf-8") as f:
            articles = json.load(f)
            for article in articles:
                url = article["url"]
                yield scrapy.Request(url=url, callback=self.parse, meta={"id": article["identifier"]["string_id"]})
    # parse scrapy data
    def parse(self, response):                 
        #if response.xpath('//meta[@name="citation_abstract"]/@content').get() is not None:
        #    scraped_abstract = response.xpath('//meta[@name="citation_abstract"]/@content').get()
        #else: 
        # scraped_abstract = response.xpath('//meta[@name="dc.Description"]/@content').get()
        # digital philology
        #scraped_abstract = response.xpath('//div[@class="abstract"]/p').getall()
        # le champ numerique
        # scraped_abstract = response.xpath('//div[@class="authors"][2]/p').get()
        # Digitális_Bölcsészet
        # scraped_abstract = response.xpath('//div[@class="authors"][2]/p').get()
        # Frontiers in DH
        # scraped_abstract = response.xpath('//*[@id="article"]/div/div[2]/main/div/div/div/div[2]/p').get()
        # humanist_Studies
        # scraped_abstract = response.xpath('//*[@id="articleAbstract"]/div').get()
        # international_curation
        # scraped_abstract = response.xpath('//div[@class="item abstract"]').get()
        # international_humanities
        # scraped_abstract = response.xpath('//div[@id="Abs1-content"]/p').get()
        # cultural_analytics
        # scraped_abstract = response.xpath('//meta[@name="citation_abstract"]/@content').get()
        # japanese
        # scraped_abstract = response.xpath('//p[@class="global-para-14"]').get()
        # tei
        scraped_abstract = response.xpath('//p[@class="resume"]').get()
        
        yield {
            "string_id": response.meta["id"],
            "abstract": scraped_abstract
        } 


        # write to document?
        """ with open("testini.json", "r", encoding="utf-8") as fd:
            for abstract in fd: 
                    article["abstract"] = abstract """

                    
    
            

    
