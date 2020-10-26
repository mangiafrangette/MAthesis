import json
import os

def crossref_to_my_schema(path, file_name):
    with open(f'{path}/{file_name}', "r", encoding="utf-8") as f:
        crossref_schema = json.load(f)
        with open(f"../data/json_files/my_schema/ms_{file_name}".replace("crossref_original", ""), "a", encoding="utf-8") as fd:
            fd.write("[")
            for index, article in enumerate(crossref_schema):
                string_article = json.dumps(article)
                if article is not None and "404" not in string_article:
                    identifier = article["DOI"]
                    url = article["URL"]
                    if "author" in article:
                        authors = [author for author in article["author"]]
                    else:
                        authors = []
                    abstract = []
                    title = article["title"][0]
                    date = article["created"]["date-time"]
                    publisher = article["publisher"]
                    journal_title = article["container-title"][0]
                    keywords = []
                    if "volume" in article:
                        volume = article["volume"]
                    else:
                        volume = ""
                    if "issue" in article:
                        issue = article["issue"]
                    else:
                        issue = ""    
                    if "issn-type" in article:
                        ISSN = article["issn-type"]
                    else:
                        ISSN = [
                            {
                                "value": [],
                                "type": []
                            }
                        ]

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
                    if index<len(crossref_schema)-1:
                        fd.write(",")
            fd.write("]")
                

# list of json paths 
path = '../data/json_files/crossref_api'
folder = os.fsencode(path)
""" filenames = []
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    filenames.append(filename) """
filenames = ["CF_Digital_Studies__Le_champ_numérique_crossref_metadata.json",
"CF_Humanist_Studies_&_the_Digital_Age_crossref_metadata.json", 
"CF_Journal_of_the_Text_Encoding_Initiative_crossref_metadata.json"
]

# call function over all crossref json files
for file_name in filenames:
    crossref_to_my_schema(path, file_name)
    
