import json
import xmltodict
from lxml import etree
import xml.etree.ElementTree as ET
from django.utils.html import strip_tags
import re
import os

def find_elements(tree, paths_dict):
    elements_dict = dict()
    for key, value in paths_dict.items():
        elements_dict[key] = tree.find(value)
    return elements_dict

def remove_tags(tree, elements_dict):
    for element in elements_dict.values():
        if element is not None:
            etree.strip_tags(element, '*')
    return tree

def get_string_dict(tree, elements_dict):
    strings_dict = dict()
    for key, element in elements_dict.items():
        if element is None:
            strings_dict[key] = None
        else:
            strings_dict[key] = element.text
    return strings_dict

def remove_spaces(string):
    return re.sub(r'\n\s+', ' ', string)

def parse_and_write(file_path):
    parser = etree.XMLParser(remove_comments=True)
    # Parse the xml file so that it can be manipulated
    parsed_xml = etree.parse(file_path, parser=parser) 

    # Define path of elements of interest
    abstract_path = './/{http://www.tei-c.org/ns/1.0}body'
    title_path = './/{http://www.tei-c.org/ns/1.0}title'
    authors_path = './/{http://www.tei-c.org/ns/1.0}author'
    author_name = './/{http://www.tei-c.org/ns/1.0}forename'
    author_family = './/{http://www.tei-c.org/ns/1.0}surname'
    author_affiliation = './/{http://www.tei-c.org/ns/1.0}affiliation'
    date_path = './/{http://www.tei-c.org/ns/1.0}date'
    publisher_path = './/{http://www.tei-c.org/ns/1.0}publisher'
    #volume_path = './/{http://www.tei-c.org/ns/1.0}idno[@type="volume"]'
    #issue_path = './/{http://www.tei-c.org/ns/1.0}idno[@type="issue"]'
    #keywords = [keyword_element.text for keyword_element in parsed_xml.findall(keywords_path)]

    # Create list with path of elements (to be cleaned and added to final json)
    paths_dict = {
        'abstract': abstract_path,
        'article_title': title_path,
        'date': date_path,
        'publisher': publisher_path,
        #'keywords': keywords_path,
        #'volume': volume_path,
        #'issue': issue_path
        }

    # Call function to search into the xml Tree the elements' paths specified in paths_dict
    elements_dict = find_elements(parsed_xml, paths_dict)

    cleaned_tree = remove_tags(parsed_xml, elements_dict)

    strings_dict = get_string_dict(cleaned_tree, elements_dict)

    for key, value in strings_dict.items():
            if value is None:
                strings_dict[key] = None
            else:
                strings_dict[key] = remove_spaces(value)


    author_elements = parsed_xml.findall(authors_path)
    authors_list = [
        {
        'given': None if author.find(author_name) is None else author.find(author_name).text,
        #'family' : [len(author.findall(author_family)), [family.text for family in author.findall(author_family)]],
        'family': None if author.find(author_family) is None else author.find(author_family).text,
        #'affiliation' : [affiliation.text for affiliation in author.findall(author_affiliation)]
        'affiliation': None if author.find(author_affiliation) is None else author.find(author_affiliation).text
        }
        for author in author_elements
        ]

    # Create python dict and append metadata text following my schema
    python_dict = dict()
    python_dict['url'] = None
    python_dict['identifier'] = {'string_id': None, 'id_scheme': None}
    for key, value in strings_dict.items():
            python_dict[key] = strings_dict[key]
    python_dict["date"] = re.findall("^.*(?=T)", python_dict["date"])[0]
    python_dict['authors'] = authors_list
    #   python_dict['publisher'] = 
    #python_dict['keywords'] = [keyword_element.text for keyword_element in parsed_xml.findall(keywords_path)]
    #python_dict['keywords'] = None if parsed_xml.find(keywords_path) is None else parsed_xml.find(keywords_path).text
     python_dict['keywords'] = None
    python_dict['journal_title'] = "ADHO Conference"
    python_dict['volume'] = None
    python_dict['issue'] = None
    python_dict['ISSN'] = [
                {
                    "value": None,
                    "type": None
                }
            ]
    return(python_dict)

def write_new_json():
    # Create list of files to pass as input to the function and call the function
    path = '../data/xml_files/adho_conferences/adho_papers'
    # comment the following from 114 to 119 for one file test
    """ folder = os.fsencode(path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.xml'): # whatever file types you're using...
            filenames.append(filename) """

    # Create the final json file
    with open(f"../data/json_files/no_country_dataset/ms_ADHO_Conference.json", "w", encoding="utf-8") as fd:
        fd.write("[")
        # comment 125-127 and uncomment the following for one file test
        """ for file_xml in filenames: 
            json.dump(parse_and_write(f'{path}/{file_xml}'), fd, ensure_ascii=False)
            fd.write(",") """
        json.dump(parse_and_write(f'{path}/WILMS_Lotte_Bridging_the_Gap_between_the_National_Libra.xml'), fd, ensure_ascii=False)
        fd.write(",")
        fd.write("]")

file_path = "../data/xml_files/adho_conferences/adho_papers/WILMS_Lotte_Bridging_the_Gap_between_the_National_Libra.xml"

write_new_json()