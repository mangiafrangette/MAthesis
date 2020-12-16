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
    
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    path_to_find = {
        "url": None, 
        "identifier": {'string_id': None, 'id_scheme': None}, 
        "abstract": './/tei:text/tei:body', 
        "article_title": './/tei:titleStmt/tei:title', 
        "authors": './/tei:sourceDesc//tei:author', 
        "given": './/tei:forename', 
        "family": './/tei:surname', 
        "affiliation": './/tei:affiliation/tei:orgName', 
        "publisher": None, 
        "date": None, 
        "keywords": None, 
        "journal_title": None, "volume": None, "issue": None, "ISSN": [ { "value": None, "type": None } ] 
    }

    final_dict = {
        "url": None, 
        "identifier": {'string_id': None, 'id_scheme': None}, "abstract": "", 
        "article_title": "", "authors": [], "publisher": None, "date": "2017", "keywords": None, "journal_title": "ADHO Conference Abstracts", "volume": None, "issue": None, "ISSN": [ { "value": None, "type": None }] 
    }

    # find values and write to dict
    for key, value in path_to_find.items():
        if type(value) is str:
            # KEYWORDS
            if key == "keywords":
                for element in root.find(value, ns).itertext():
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
                authors_list = root.findall(value, ns)
                #print(authors_list)
                
                for author in authors_list:
                    author_dict = {
                            "given": "",
                            "family": "",
                            "affiliation": []
                        }
                    #print(final_dict["article_title"])
                    if author.find(path_to_find['given'], ns) is not None and author.find(path_to_find['family'], ns) is not None:
                        for element in author.find(path_to_find['given'], ns).itertext():
                            author_dict["given"] += remove_spaces(element)
                        for element in author.find(path_to_find['family'], ns).itertext():
                            author_dict["family"] += remove_spaces(element)
                        
                        if author.findall(path_to_find['affiliation'], ns) is not None:
                            for affiliation in author.findall(path_to_find['affiliation'], ns):
                                current_aff_string = ""
                                for element in affiliation.itertext():
                                    current_aff_string += remove_spaces(element)
                                author_dict["affiliation"].append(current_aff_string)

                    final_dict["authors"].append(author_dict)
                    #print(author_dict)

            # abstract
            elif key == "abstract":
                if root.find(value, ns) == None:
                    for element in root.find('.//tei:text/tei:body', ns).itertext():
                        final_dict[key] += remove_spaces(element)
                else:
                    for element in root.find(value, ns).itertext():
                        final_dict[key] += remove_spaces(element)
            
            # DATE 
            elif key == "date":
                if root.find(value, ns) is not None:
                    for element in root.find(value, ns).itertext():
                        final_dict[key] = re.findall("^.*(?=T)", element)[0]
                    

            # other keys 
            elif key != "given" and key != "family" and key != "affiliation" and key != "keywords" and key != "abstract" and key != "date" and key != "authors":   
                for element in root.find(value, ns).itertext():
                    final_dict[key] += remove_spaces(element)
    #print(final_dict)
    return(final_dict)

def write_new_json():
    # Create list of files to pass as input to the function and call the function
    path = '../data/adho_conferences/2017'
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
    with open(f"../data/adho_conferences/ms_ADHO_2017.json", "w", encoding="utf-8") as fd:
        fd.write("[")
        # comment 125-127 and uncomment the following for one file test
        for file_xml in filenames: 
            json.dump(parse_and_write(f'{path}/{file_xml}'), fd, ensure_ascii=False)
            fd.write(",")
        fd.write("]")

write_new_json()           
        

    
