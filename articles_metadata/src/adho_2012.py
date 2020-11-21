import json
import xmltodict
from lxml import etree
import xml.etree.ElementTree as ET
from django.utils.html import strip_tags
import re
import os

def remove_spaces(string):
    return re.sub(r'\n\s+', ' ', string)

# main function

## warning: this date is the revision date, there was no publication date... 

def parse_and_write(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    path_to_find = {
        "url": None, 
        "identifier": {'string_id': None, 'id_scheme': None}, "abstract": './/tei:text/tei:body', 
        "article_title": './/tei:titleStmt/tei:title', "authors": './/tei:titleStmt/tei:author', "given": None, "family": None, "name": './/tei:name',"affiliation": './/tei:affiliation', "publisher": './/tei:publicationStmt/tei:publisher', "date": './/tei:revisionDesc/tei:change/tei:date', "keywords": None, "journal_title": None, "volume": None, "issue": None, "ISSN": [ { "value": None, "type": None } ] 
    }

    final_dict = {
        "url": None, 
        "identifier": {'string_id': None, 'id_scheme': None}, "abstract": "", 
        "article_title": "", "authors": [], "publisher": "", "date": "", "keywords": None, "journal_title": "ADHO Conference Abstracts", "volume": None, "issue": None, "ISSN": [ { "value": None, "type": None }] 
    }

    # find values and write to dict
    for key, value in path_to_find.items():
        if type(value) is str:
                              
            # AUTHORS
            if key == "authors":
                authors_list = root.findall(value, ns)
                
                for author in authors_list:
                    author_dict = {
                            "given": "",
                            "family": "",
                            "affiliation": []
                        }
                    for element in author.find(path_to_find['name'], ns).itertext():

                        print(remove_spaces(element).split(",")[1])
                        author_dict["given"] += remove_spaces(element).split(",")[1]
                        author_dict["family"] += remove_spaces(element).split(",")[0]
                    for affiliation in author.findall(path_to_find['affiliation'], ns):
                        current_aff_string = ""
                        for element in affiliation.itertext():
                            current_aff_string += remove_spaces(element)
                        author_dict["affiliation"].append(current_aff_string)
                    final_dict["authors"].append(author_dict)

            # other things 
            elif key != "name" and key != "affiliation":    
                for element in root.find(value, ns).itertext():
                    final_dict[key] += remove_spaces(element)
            
    return(final_dict)

def write_new_json():
    # Create list of files to pass as input to the function and call the function
    path = '../data/adho_conferences/2012'
    # comment the following from 114 to 119 for one file test
    folder = os.fsencode(path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.xml'): # whatever file types you're using...
            filenames.append(filename)

    # Create the final json file
    with open(f"../data/adho_conferences/ms_ADHO_2012.json", "w", encoding="utf-8") as fd:
        fd.write("[")
        # comment 125-127 and uncomment the following for one file test
        for file_xml in filenames: 
            json.dump(parse_and_write(f'{path}/{file_xml}'), fd, ensure_ascii=False)
            fd.write(",")
        fd.write("]")

write_new_json()           
        

    
