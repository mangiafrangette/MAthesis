import json
import os

def to_my_schema(path, file_name):
    with open(f'{path}/{file_name}', "r", encoding="utf-8") as f:
        input_schema = json.load(f)
        with open(f"../data/json_files/my_schema_{file_name}", "a", encoding="utf-8") as fd:
            fd.write("[")
            for key, value in input_schema.items():
                identifier = value["ID"]
                authors = value["author"]
                abstract = value["abstract"]
                title = value["title"]
                date = value["year"]
                publisher = value["publisher"]
                journal_title = value["journal"]
                keywords = []
                volume = value["volume"]
                issue = value["number"]
                ISSN = value["issn"]

                    # creating my schema
                python_dict = dict()
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
                # devo fare tipo enumerate(keys per le virgole)
                json.dump(python_dict, fd)
                #if index<len(datacite_schema)-1:
                fd.write(",")
        fd.write("]")
                

path = '../data/json_files'
file_name = 'Computers_and_the_Humanities.json'

to_my_schema(path, file_name)    
