import json
import os

# 2011-06-29T16:36:57Z
path = "../data/json_files/my_schema"
files_list = [
    "ms_CF_Humanist_Studies_&_the_Digital_Age.json",
    "ms_CF_Digital_Studies__Le_champ_numérique.json",
    "ms_CF_Journal_of_the_Text_Encoding_Initiative.json",
    "ms_CF_Umanistica_Digitale.json",
    


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
        