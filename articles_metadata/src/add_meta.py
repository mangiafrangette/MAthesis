import json
import os

files_list = [
    "../data/json_files/my_schema/ms_Digital_Medievalist copy.json",
]
for file in files_list:
    with open(file, "r", encoding="utf-8") as f:
        json_file = json.load(f)
        for article in json_file:
            """ article["journal_title"] = "International Journal for Digital Art History" """
            article["url"] = f'http://dx.doi.org/{article["identifier"]["string_id"]}'
            
        with open(file, "w", encoding="utf-8") as fd:
            json.dump(json_file, fd)
        