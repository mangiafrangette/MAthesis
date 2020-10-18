import json
import xmltodict
from lxml import etree
import xml.etree.ElementTree as ET
from django.utils.html import strip_tags
import re
import os

# Removes all unnecessary elements from within relevant elements but keep content
def remove_tags(tree, paths_dict):
    for value in paths_dict.values():
        etree.strip_tags(tree.find(value), '*')
    return tree

# Get string value from elements 
def get_string_dict(tree, paths_dict):
    strings_dict = dict()
    for key, value in paths_dict.items():
        strings_dict[key] = tree.find(value).text
    return strings_dict


# Removes spaces from a string
def remove_spaces(string):
    return re.sub(r'\n\s+', ' ', string)
      

def xml_to_json(file):

    parser = etree.XMLParser(remove_comments=True)
    # Parse the xml file so that it can be manipulated
    parsed_xml = etree.parse(file, parser=parser) 
    
    # Define path of elements of interest
    abstract_path = './/{http://www.digitalhumanities.org/ns/dhq}abstract'
    title_path = './/{http://www.tei-c.org/ns/1.0}title'
    authors_path = './/{http://www.digitalhumanities.org/ns/dhq}authorInfo'
    author_name = './/{http://www.digitalhumanities.org/ns/dhq}author_name'
    author_family = './/{http://www.digitalhumanities.org/ns/dhq}family'
    author_affiliation = './/{http://www.digitalhumanities.org/ns/dhq}affiliation'
    date_path = './/{http://www.tei-c.org/ns/1.0}date'
    # publisher_path = './/{http://www.digitalhumanities.org/ns/dhq}family'
    volume_path = './/{http://www.tei-c.org/ns/1.0}idno[@type="volume"]'
    issue_path = './/{http://www.tei-c.org/ns/1.0}idno[@type="issue"]'
    # keywords_path = './/{http://www.tei-c.org/ns/1.0}keywords[@scheme="#authorial_keywords"]'
    # keywords = [keyword.text for keyword in keywords_list]
    # print(etree.tostring(parsed_xml.find(author_family)))

    # Create list with path of elements (to be cleaned and added to final json)
    paths_dict = {
        'abstract': abstract_path,
        'title': title_path, 
        #'date': date_path,
        # 'publisher': publisher_path,
        #'volume': volume_path,
        #'issue': issue_path
        }

    # Call function to remove tags 
    cleaned_tree = remove_tags(parsed_xml, paths_dict)

    # Create dictionary with strings
    strings_dict = get_string_dict(cleaned_tree, paths_dict)
    
    # Remove spaces from most elements
    for key, value in strings_dict.items():
        print(key)
        strings_dict[key] = remove_spaces(value)

    # Authors information shouldnt need to be cleaned 
    author_elements = parsed_xml.findall(authors_path)
    authors_list = [
        {
        'given': author.find(author_name).text,
        'family' : [len(author.findall(author_family)),[family.text for family in author.findall(author_family)]],
        'affiliation' : [affiliation.text for affiliation in author.findall(author_affiliation)]
        }
        for author in author_elements
        ]


    # Create python dict and append metadata text following my schema
    python_dict = dict()
    for key, value in strings_dict.items():
        python_dict[key] = strings_dict[key]
    python_dict['authors'] = authors_list
#   python_dict['publisher'] = 
    # python_dict['keywords'] = keywords
    python_dict['journal_title'] = "Digital Humanities Quarterly"
    python_dict['ISSN'] = "1938-4122"

    return(python_dict)

def write_new_json():
    # Create list of files to pass as input to the function and call the function
    path = '../data/xml_files'
    folder = os.fsencode(path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.xml'): # whatever file types you're using...
            filenames.append(filename)

    #Create the final json file
    with open(f"../data/json_files/my_schema/Digital_Humanities_Quarterly.json", "a", encoding="utf-8") as fd:
        fd.write("[")
        for file_xml in filenames: 
            json.dump(xml_to_json(f'{path}/{file_xml}'), fd)
            fd.write(",")
        fd.write("]")

write_new_json()