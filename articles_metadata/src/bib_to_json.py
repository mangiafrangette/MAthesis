import bibtexparser
import json
import os

def bib_to_json():
    
    path = '../data/bibtex_files'
    for file_name in os.listdir(path):

        with open(f'{path}/{file_name}', encoding="utf-8") as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        with open(f'../data/json_files/{file_name.replace(".bib",".json")}', "w", encoding="utf-8") as json_file:
            json.dump(bib_database.entries_dict, json_file)

bib_to_json()


