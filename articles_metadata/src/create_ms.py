import scrapy
import csv
import os
import json

filename = "../data/json_files/full_list_of_ids.json" 
with open(filename, "r", encoding="utf-8") as f:
    journals = json.load(f)
    articles_dicts_list = []
    for journal in journals:
        if "Jahr" in journal["journal_title"]:
            for url in journal["research_articles"]:
                article = {
                        "url": url,
                        "identifier": {
                        "string_id": None,
                        "id_scheme": None
                    },
                    "abstract": None,
                    "article_title": None,
                    "authors": [
                        {
                            "given": None,
                            "family": None,
                            "affiliation": [None]
                        }
                    ],
                    "publisher": None,
                    "date": None,
                    "keywords": None,
                    "journal_title": None,
                    "volume": None,
                    "issue": None,
                    "ISSN": [
                        {
                            "value": None,
                            "type": None
                        }
                    ]
                }
                articles_dicts_list.append(article)
            with open("ms_Jahrbuch_für_Computerphilologie.json", "w",encoding="utf-8") as fd:
                json.dump(articles_dicts_list, fd)
