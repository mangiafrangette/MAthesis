import os
import json

# This file was run to get digital scholarship in the humanities data through a service called proxies api. 

filename = "../data/json_files/my_schema/ms_DSH.json"
with open(filename, "r", encoding="utf-8") as f:
    articles = json.load(f)
    for index, article in enumerate(articles):
        url = article["url"]
        output_file_name = f'dsh{index}.xml'
        os.system(f'curl "http://api.proxiesapi.com/?auth_key=b0bbd56ab84d8fb27d722c27d323a9c5_sr98766_ooPq87&url={url}" -o {output_file_name}')