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

def parse_and_write(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    #ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    path_to_find = {
        "url": None, 
        "identifier": {'string_id': None, 'id_scheme': None}, 
        "abstract": './/body', 
        "article_title": './/titleStmt/title', 
        "authors": './/docAuthor', 
        "given": './/name',   
        "affiliation": './/titlePart[@type="affil"]',
        "publisher": None, 
        "date": './/revisionDesc//date', 
        "keywords": './/keywords', 
        "journal_title": None, "volume": None, "issue": None, "ISSN": [ { "value": None, "type": None } ] 
    }

    final_dict = {
        "url": None, 
        "identifier": {'string_id': None, 'id_scheme': None}, "abstract": "", 
        "article_title": "", "authors": [], "publisher": None, "date": "", "keywords": [], "journal_title": "ADHO Conference Abstracts", "volume": None, "issue": None, "ISSN": [ { "value": None, "type": None }] 
    }

    # find values and write to dict
    for key, value in path_to_find.items():
        if type(value) is str:

            # KEYWORDS
            if key == "keywords":
                for element in root.find(value).itertext():
                    final_dict[key].append(remove_spaces(element))
                    # clean empty keywords
                if " " or "\n" in final_dict[key]:
                    keywords_set = set(final_dict[key])
                    if " " in final_dict[key]:
                        keywords_set.remove(" ")
                    if "\n" in final_dict[key]:
                        keywords_set.remove("\n")
                    final_dict[key] = list(keywords_set)
                    
            # AUTHORS
            elif key == "authors":
                authors_list = root.findall(value)
                index = 0
                for author in authors_list:
                    author_dict = {
                            "given": "",
                            "family": "",
                            "affiliation": []
                        }
                    #print(final_dict["article_title"])
                    for element in author.find(path_to_find['given']).itertext():
                        author_dict["given"] += remove_spaces(element)
                      
                    affiliation = root.findall(path_to_find['affiliation'])[index]
                    current_aff_string = ""
                    for element in affiliation.itertext():
                        current_aff_string += remove_spaces(element)
                    author_dict["affiliation"].append(current_aff_string)    
                    index += 1
                    final_dict["authors"].append(author_dict)
                    #print(final_dict["authors"])
                
            # abstract
            elif key == "abstract":
                
                if root.find(value) == None:
                    for element in root.find('.//body').itertext():
                        final_dict[key] += remove_spaces(element)
                else:
                    for element in root.find(value).itertext():
                        final_dict[key] += remove_spaces(element)
            
            # DATE 
            elif key == "date":
                if root.find(value) is not None:
                    final_dict[key] = root.find(value).attrib['value']
                    
                    

            # other keys 
            elif key != "given" and key != "family" and key != "affiliation" and key != "keywords" and key != "abstract" and key != "date":   
                for element in root.find(value).itertext():
                    final_dict[key] += remove_spaces(element)
    #print(final_dict)
    return(final_dict)

def write_new_json():
    # Create list of files to pass as input to the function and call the function
    path = '../data/adho_conferences/2007'
    # comment the following from 114 to 119 for one file test
    folder = os.fsencode(path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.xml'): # whatever file types you're using...
            filenames.append(filename)

    #for testing without writing
    """ for file_xml in filenames:
        parse_and_write(f'{path}/{file_xml}') """

    # Create the final json file
    with open(f"../data/adho_conferences/ms_ADHO_2007.json", "w", encoding="utf-8") as fd:
        fd.write("[")
        # comment 125-127 and uncomment the following for one file test
        for file_xml in filenames: 
            json.dump(parse_and_write(f'{path}/{file_xml}'), fd, ensure_ascii=False)
            fd.write(",")
        fd.write("]")

write_new_json()           
        

    
