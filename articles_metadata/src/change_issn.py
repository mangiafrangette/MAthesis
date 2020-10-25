import json
import os

files_list = [
    "../data/json_files/my_schema/ms_Journal_of_Cultural_Analytics.json",

]
for file in files_list:
    with open(file, "r", encoding="utf-8") as f:
        json_file = json.load(f)
        for article in json_file:
            article["ISSN"] = [
        {
            "value": "2371-4549",
            "type": "electronic"
        }
    ]
        with open(file, "w", encoding="utf-8") as fd:
            json.dump(json_file, fd)
        