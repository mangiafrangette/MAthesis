import json
import os

def datacite_to_my_schema(path, file_name):
    with open(f'{path}/{file_name}', "r", encoding="utf-8") as f:
        datacite_schema = json.load(f)
        with open(f"../data/json_files/my_schema/my_schema_{file_name}".replace("datacite_original", "d"), "a", encoding="utf-8") as fd:
            fd.write("[")
            for index, article in enumerate(datacite_schema):
                string_article = json.dumps(article)
                if article is not None and "404" not in string_article:
                    identifier = article["data"]["id"]
                    authors = [author for author in article["data"]["attributes"]["author"]]
                    url = article["data"]["attributes"]["url"]
                    abstract = article["data"]["attributes"]["description"]
                    title = article["data"]["attributes"]["title"]
                    date = article["data"]["attributes"]["updated"]
                    publisher = ""
                    journal_title = ""
                    keywords = []
                    volume = ""
                    issue = ""
                    ISSN = []

                    # creating my schema
                    python_dict = dict()
                    python_dict['url'] = url
                    python_dict['identifier'] = {
                        'string_id' : identifier,
                        'id_scheme' : "DOI" 
                        }
                    python_dict['abstract'] = abstract
                    python_dict['article_title'] = title
                    python_dict['authors'] = authors
                    python_dict['publisher'] = publisher
                    python_dict['date'] = date
                    python_dict['keywords'] = keywords
                    python_dict['journal_title'] = journal_title
                    python_dict['volume'] = volume
                    python_dict['issue'] = issue
                    python_dict['ISSN'] = ISSN
                
                    json.dump(python_dict, fd)
                    if index<len(datacite_schema)-1:
                        fd.write(",")
            fd.write("]")
                

# list of json paths 
path = '../data/json_files/datacite_api'
folder = os.fsencode(path)
filenames = []
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    filenames.append(filename)

# call function over all datacite json files
for file_name in filenames:
    datacite_to_my_schema(path, file_name)
    
