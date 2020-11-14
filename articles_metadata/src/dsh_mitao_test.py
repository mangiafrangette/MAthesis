import json
import os
from basic_operations import *

def create_abstract_txt(file_path):
    counter = 0
    with open(file_path, "r", encoding="utf-8") as file:
        all_articles = json.load(file) 
    #each abstract is a document
        for article in all_articles:
            counter += 1
            with open(f'../data/test_DSH_abstracts/{counter}.txt', 'w', encoding='utf-8') as g:
                g.write(article["abstract"])

file_path = "../data/json_files/complete_dataset/ms_DSH_filled_aff.json"
create_abstract_txt(file_path)