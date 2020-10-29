import json
import os

def add_scraped_affiliations(my_schema_file, scrapy_affiliations):
    with open(my_schema_file, "r", encoding="utf-8") as f:
        articles = json.load(f)
    with open(scrapy_affiliations, "r", encoding="utf-8") as g: 
        scrapy_affiliations = json.load(g)
        for article in articles:
            for affiliation in scrapy_affiliations:
                if article["identifier"]["string_id"] == affiliation["string_id"]:
                    for author1 in article["authors"]:
                        for author2 in affiliation["authors"]:
                            if author1["given"] in author2["given"]: 
                                author1["affiliation"] = author2["affiliation"]
                                with open(my_schema_file, "w", encoding="utf-8") as fd:
                                    json.dump(articles, fd)


add_scraped_affiliations("../data/json_files/my_schema/ms_Digital_Medievalist.json", "../data/json_files/scraped_affiliations/aff_digital_medievalist.json")
