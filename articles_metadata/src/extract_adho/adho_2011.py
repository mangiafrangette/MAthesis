import json
import xmltodict
from lxml import etree
import xml.etree.ElementTree as ET
from django.utils.html import strip_tags
import re
import os
import copy

def remove_spaces(string):
    return re.sub(r'\n\s+', ' ', string)

# main function

def parse_and_write(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    ns = {'tei': 'http://www.w3.org/1999/xhtml'}
    
    path_to_find = {
        "url": None, 
        "identifier": {'string_id': None, 'id_scheme': None}, "abstract": './/tei:p[@class="noindent"]', 
        "article_title": './/tei:title', "authors": None, "given": None, "family": None, "affiliation": None, "publisher": None, "date": None, "keywords": None, "journal_title": None, "volume": None, "issue": None, "ISSN": [ { "value": None, "type": None } ] 
    }

    final_dict = {
        "url": None, 
        "identifier": {'string_id': None, 'id_scheme': None}, "abstract": "", 
        "article_title": "", "authors": [{
                            "given": "",
                            "family": "",
                            "affiliation": []
                        }], "publisher": None, "date": "2011", "keywords": None, "journal_title": "ADHO Conference Abstracts", "volume": None, "issue": None, "ISSN": [ { "value": None, "type": None }] 
    }

    # find values and write to dict
    for key, value in path_to_find.items():
        if type(value) is str:
            # abstract
            full_txt = ""
            if key == "abstract": 
                abs = root.findall(value, ns)
                #print(abs)
                for element in abs:
                    for txt in element.itertext():
                        #print(txt)
                        full_txt += remove_spaces(txt)
                final_dict[key] = full_txt
                #print(txt)
                    
            # KEYWORDS
            if key == "keywords":
                for element in root.find(value, ns).itertext():
                    final_dict[key].append(remove_spaces(element))
                    # clean empty keywords
                if " " in final_dict[key]:
                    
                    keywords_set = set(final_dict[key])
                    
                    keywords_set.remove(" ")
                    final_dict[key] = list(keywords_set)
                    
            # AUTHORS
            elif key == "authors":
                authors_list = root.findall(value, ns)
                
                for author in authors_list:
                    author_dict = {
                            "given": "",
                            "family": "",
                            "affiliation": []
                        }
                    for element in author.find(path_to_find['given'], ns).itertext():
                        author_dict["given"] += remove_spaces(element)
                    for element in author.find(path_to_find['family'], ns).itertext():
                        author_dict["family"] += remove_spaces(element)
                    for affiliation in author.findall(path_to_find['affiliation'], ns):
                        current_aff_string = ""
                        for element in affiliation.itertext():
                            current_aff_string += remove_spaces(element)
                        author_dict["affiliation"].append(current_aff_string)
                    final_dict["authors"].append(author_dict)

            # other things 
            elif key != "given" and key != "family" and key != "affiliation" and key != "keywords" and key != "abstract":    
                for element in root.find(value, ns).itertext():
                    final_dict[key] += remove_spaces(element)
    #print(final_dict["abstract"])
    #print("\nANOTHER TEXT\n")        
    return(final_dict)


def correct_abstracts(correct_article, dict_to_correct):
    #print(correct_article)
    for article_to_corr in dict_to_correct:
        if article_to_corr["article_title"] == correct_article["article_title"]:
            article_to_corr["abstract"] = correct_article["abstract"]
            return article_to_corr
    """ print("FOLLOWING IS CORRECT")
    print(correct_article["abstract"])
    print("FOLLOWING IS TO CORRECT")
    print(article_to_corr["abstract"]) """
    #print(dict_to_correct)



def write_new_json():
    # Create list of files to pass as input to the function and call the function
    path = '../data/adho_conferences/2011'
    # comment the following from 114 to 119 for one file test
    folder = os.fsencode(path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.xml'): # whatever file types you're using...
            filenames.append(filename)

    # Create the final json file
    with open(f"../data/adho_conferences/ms_ADHO_2011 copy.json", "r", encoding="utf-8") as fg:
        dict_to_correct = json.load(fg)

    with open(f"../data/adho_conferences/ms_ADHO_2011.json", "w", encoding="utf-8") as fd:
        fd.write("[")
        # comment 125-127 and uncomment the following for one file test
        for file_xml in filenames: 
            json.dump(correct_abstracts(parse_and_write(f'{path}/{file_xml}'), dict_to_correct), fd, ensure_ascii=False)
            fd.write(",")
        fd.write("]")            

write_new_json()           
        

    
