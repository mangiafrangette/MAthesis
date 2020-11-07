import json
import xmltodict
from lxml import etree
import xml.etree.ElementTree as ET
from django.utils.html import strip_tags
import re
import os


# Search Element object with specified path in the tree. Key-Element association is kept in  elements_dict
def find_elements(tree, paths_dict):
    elements_dict = dict()
    for key, value in paths_dict.items():
        elements_dict[key] = tree.find(value)
    return elements_dict


# Removes all unnecessary elements from within not None elements but keep content
def remove_tags(tree, elements_dict):
    for element in elements_dict.values():
        if element is not None:
            etree.strip_tags(element, '*')
    return tree


# Get string value from elements 
def get_string_dict(tree, elements_dict):
    strings_dict = dict()
    for key, element in elements_dict.items():
        if element is None:
            strings_dict[key] = None
        else:
            strings_dict[key] = element.text
    return strings_dict


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
    keywords_path = './/{http://www.tei-c.org/ns/1.0}keywords[@scheme="#authorial_keywords"]//{http://www.tei-c.org/ns/1.0}item'
    #keywords = [keyword_element.text for keyword_element in parsed_xml.findall(keywords_path)]

    # Create list with path of elements (to be cleaned and added to final json)
    paths_dict = {
        'abstract': abstract_path,
        'article_title': title_path,
        'date': date_path,
        # 'publisher': publisher_path,
        #'keywords': keywords_path,
        'volume': volume_path,
        'issue': issue_path
        }

    # Call function to search into the xml Tree the elements' paths specified in paths_dict
    elements_dict = find_elements(parsed_xml, paths_dict)

    # Collect keywords before cleaning all tags in parsed_xml with remove_tags() function
    keywords_element_list = parsed_xml.findall(keywords_path)
    keywords = None
    if keywords_element_list is not None:
        if len(keywords_element_list) > 0:
            if keywords_element_list[0] is not None:
                if keywords_element_list[0].text is not None:
                    keywords = [keyword_element.text for keyword_element in keywords_element_list]

    # Call function to remove tags 
    cleaned_tree = remove_tags(parsed_xml, elements_dict)
    #keywords = None if cleaned_tree.find(keywords_path) is None else cleaned_tree.find(keywords_path).text

    #print(None if keywords is None else keywords.text)

    # Create dictionary with strings
    strings_dict = get_string_dict(cleaned_tree, elements_dict)
    #print(strings_dict['keywords'])


    # Remove spaces from non None elements
    for key, value in strings_dict.items():
        if value is None:
            strings_dict[key] = None
        else:
            strings_dict[key] = remove_spaces(value)

    #print(None if strings_dict['keywords'] is None else strings_dict['keywords'])

    # Collect authors' information
    author_elements = parsed_xml.findall(authors_path)
    authors_list = [
        {
        'given': None if author.find(author_name) is None else remove_author_spaces(author.find(author_name).text),
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
    python_dict['authors'] = authors_list
#   python_dict['publisher'] = 
    #python_dict['keywords'] = [keyword_element.text for keyword_element in parsed_xml.findall(keywords_path)]
    #python_dict['keywords'] = None if parsed_xml.find(keywords_path) is None else parsed_xml.find(keywords_path).text
    python_dict['keywords'] = keywords
    python_dict['journal_title'] = "Digital Humanities Quarterly"
    python_dict['ISSN'] = [{'value': "1938-4122", 'type': None}]

    return python_dict


def write_new_json():
    # Create list of files to pass as input to the function and call the function
    path = '../data/xml_files/digital_humanities_quarterly'
    folder = os.fsencode(path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.xml'): # whatever file types you're using...
            filenames.append(filename)

    # Create the final json file
    with open(f"../data/json_files/my_schema/ms_Digital_Humanities_Quarterly.json", "w", encoding="utf-8") as fd:
        fd.write("[")
        for file_xml in filenames: 
            json.dump(xml_to_json(f'{path}/{file_xml}'), fd)
            fd.write(",")
        fd.write("]")


if __name__ == '__main__':
    write_new_json()
