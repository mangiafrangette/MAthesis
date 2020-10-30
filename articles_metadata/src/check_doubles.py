import json
import os

files_list = [
    "../data/json_files/my_schema/ms_Digital_Medievalist.json",
]
for file in files_list:
    with open(file, "r", encoding="utf-8") as f:
        json_file = json.load(f)
        output_list = list()
        id_set = set()
        for article in json_file:
            if article["identifier"]["string_id"] not in id_set:
                id_set.add(article["identifier"]["string_id"])
                output_list.append(article)
    with open(file, "w", encoding="utf-8") as fd:
        json.dump(output_list, fd)
        