import json
import os

def add_scraped_abstracts(my_schema_file, scrapy_abstracts):
    
    with open(my_schema_file, "w", encoding="utf-8") as f:
        articles = json.load(f)
    with open(scrapy_abstracts, "r", encoding="utf-8") as g: 
        scrapy_abstracts = json.load(g)
        for article in articles:
            for abstract in scrapy_abstracts:
                if article["identifier"]["string_id"] == abstract["string_id"]:
                    article["abstract"] = abstract["abstract"]



add_scraped_abstracts("../data/json_files/my_schema/my_schema_c_Digital_Medievalist.json", "../data/json_files/my_schema/scrapy_abstracts_requests.json")

""" path = '../data/json_files/my_schema'
folder = os.fsencode(path)
for file in os.listdir(folder):
    my_schema_file = f'{path}/{os.fsdecode(file)}'
    scraped_file = "../data/json_files/my_schema/scrapy_abstracts_requests.json"
    add_scraped_abstracts(my_schema_file, scraped_file) """
