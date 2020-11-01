import json
import os

ms_file = "../data/json_files/my_schema/ms_IJHAC.json"
scrapy_file = "../data/json_files/scrapy_ijhac_authors.json"

with open(ms_file, "r", encoding="utf-8") as f:
    my_schema_json = json.load(f)
    with open(scrapy_file, "r", encoding="utf-8") as fd:
        scrapy_file = json.load(fd)
        for article1 in my_schema_json:
            for article2 in scrapy_file:
                if article1["identifier"]["string_id"] == article2["string_id"]:
                    article1["date"] = article2["date"][0]
                    article1["authors"] = article2["authors"]
                    article1["publisher"] = article2["publisher"]
                    
                    with open(ms_file, "w", encoding="utf-8") as g:
                        json.dump(my_schema_json, g)
        