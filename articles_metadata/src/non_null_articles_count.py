import json
import os
from basic_operations import *

def count_json_objects(file_name):
    articles_list = json_load(file_name) 
    null_articles = []      
    for article in articles_list:
        string_article = json.dumps(article)
        if not(article) or "404" in string_article:
            null_articles.append(article)
    total_articles = len(articles_list)
    non_null_articles = total_articles - len(null_articles) 
    return total_articles, non_null_articles
        
# list of json paths 
dir_path = '../data/json_files/datacite_api'

# create counter
counter = 0
# call function for each json file
for file_name in paths_from_directory(dir_path, ".json"):
    total_articles, non_null_articles = count_json_objects(f'{path}/{file_name}')
    with open('../non_null_articles.md', 'a', encoding='utf-8') as g:
        g.write(f'# {file_name}\n non-null articles: {non_null_articles}\n total articles: {total_articles}\n')
    counter += non_null_articles

#count_json_objects('../data/json_files/Umanistica_Digitale_crossref_metadata.json')