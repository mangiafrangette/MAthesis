import json
import os

def count_json_objects(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        articles_list = json.load(f)
        null_articles = []      
        for article in articles_list:
            string_article = json.dumps(article)
            if not(article) or "404" in string_article:
                null_articles.append(article)
        total_articles = len(articles_list)
        non_null_articles = total_articles - len(null_articles) 
    return total_articles, non_null_articles
        
# list of json paths 
path = '../data/json_files/datacite_api'
folder = os.fsencode(path)
filenames = []
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith('.json'): # whatever file types you're using...
        filenames.append(filename)

# create counter
counter = 0
# call function for each json file
for file_name in filenames:
    total_articles, non_null_articles = count_json_objects(f'{path}/{file_name}')
    with open('../non_null_articles.md', 'a', encoding='utf-8') as g:
        g.write(f'# {file_name}\n non-null articles: {non_null_articles}\n total articles: {total_articles}\n')
    counter += non_null_articles

#count_json_objects('../data/json_files/Umanistica_Digitale_crossref_metadata.json')