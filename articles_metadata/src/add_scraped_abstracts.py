import json
import os

def add_scraped_abstracts(my_schema_file, scrapy_abstracts):
    with open(my_schema_file, "r", encoding="utf-8") as f:
        articles = json.load(f)
    with open(scrapy_abstracts, "r", encoding="utf-8") as g: 
        scrapy_abstracts = json.load(g)
        for article in articles:
            for abstract in scrapy_abstracts:
                if article["identifier"]["string_id"] == abstract["url"]:
                    article["abstract"] = abstract["abstract"]
                    with open(my_schema_file, "w", encoding="utf-8") as fd:
                        json.dump(articles, fd)


add_scraped_abstracts("../data/json_files/my_schema/ms_JOCCH.json", "../data/json_files/scraped_abstracts/scrapy_jocch.json")
