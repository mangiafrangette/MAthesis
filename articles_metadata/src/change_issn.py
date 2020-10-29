import json
import os

files_list = [
    "../data/json_files/my_schema/ms_Zeitschrift_für_digitale_Geisteswissenschaften.json",

]
for file in files_list:
    with open(file, "r", encoding="utf-8") as f:
        json_file = json.load(f)
        for article in json_file:
            for author in article["authors"]:
                if author["affiliation"] is not None:    
                    if type(author["affiliation"]) is not list:
                        author["affiliation"] = [author["affiliation"]]
        with open(file, "w", encoding="utf-8") as fd:
            json.dump(json_file, fd)
        