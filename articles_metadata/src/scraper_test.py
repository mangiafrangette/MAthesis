import scrapy
import csv
import os
import json


# entra nella directory, entra nel file, entra nell'articolo
path = '../data/json_files/my_schema'
folder = os.fsencode(path)
for file in os.listdir(folder):
    # entra nel file
    filename = os.fsdecode(file)
    with open(f'{path}/{filename}', "r", encoding="utf-8") as f:
        articles = json.load(f)
        for article in articles:
            url = article["url"]
            print(url)
        
