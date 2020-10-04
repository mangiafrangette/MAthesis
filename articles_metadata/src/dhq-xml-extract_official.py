import json
import xmltodict
from lxml import etree
import xml.etree.ElementTree as ET
from django.utils.html import strip_tags
import re
import os

def remove_spaces(string):
    cleaned_string = re.sub(r'\n\s+', ' ', string)
    return cleaned_string

def xml_to_json(file):
    # Parse the xml file so that it can be manipulated
    parsed_xml = etree.parse(file)
    # Remove in-tag elements that are unnecessary 
    etree.strip_tags(parsed_xml,
    '{http://www.tei-c.org/ns/1.0}emph',
    '{http://www.tei-c.org/ns/1.0}p',
    '{http://www.digitalhumanities.org/ns/dhq}@rend',
    '{http://www.digitalhumanities.org/ns/dhq}#text',
    '{http://www.tei-c.org/ns/1.0}title[@rend="quotes"]')
    # Access the nodes with relevant data and take the textual string only
    abstract = parsed_xml.find('.//{http://www.digitalhumanities.org/ns/dhq}abstract').text
    title = parsed_xml.find('.//{http://www.tei-c.org/ns/1.0}title').text
    authors = parsed_xml.findall('.//{http://www.digitalhumanities.org/ns/dhq}authorInfo')
    print(abstract)

    # Create python dict and append metadata text
    python_dict = dict()
    python_dict['abstract'] = remove_spaces(abstract)
    print(abstract)
    python_dict['title'] = remove_spaces(title)
    print(python_dict)

    # Uncomment the following when ready to process all xml files in the folder
    """ #Create json from python dict
    json_data = json.dumps(python_dict)
    with open(f"../data/{file}.json", "w", encoding="utf-8") as json_file:
        json_file.write(json_data) """
xml_to_json("../data/xml_files/000417.xml")

# Uncomment the following to process all xml files from the xml_files folder
""" # Create list of files to pass as input to the function
path = '../data/xml_files'
folder = os.fsencode(path)
filenames = []
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith('.xml'): # whatever file types you're using...
        filenames.append(filename)
for file_xml in filenames: 
    xml_to_json(f'{path}/{file_xml}') """





# old tests
"""     # Transform the etree object into an xml string
    string_xml = etree.tostring(parsed_xml, encoding='unicode', method='xml')
    # Remove extra spaces
    string_xml = re.sub(r'\n\s+', ' ', string_xml) 
    # Transform the xml string to a python dictionary
    xml_to_dict = xmltodict.parse(string_xml)
    # Create the json file
    json_data = json.dumps(xml_to_dict)
    with open(f"../data/{file}.json", "w", encoding="utf-8") as json_file:
        json_file.write(json_data)

#List of all the xml files to pass to the function
path = '../data/xml_files'
folder = os.fsencode(path)
filenames = []
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith('.xml'): # whatever file types you're using...
        filenames.append(filename)

print(filenames)
for file_xml in filenames: 
    xml_to_json(f'{path}/{file_xml}') """

""" # creation of a new xml
root = ET.Element("root")
ET.SubElement(root, string_abstract)
ET.SubElement(root, string_title)
#string the new xml
tree = ET.ElementTree(root)
tree.write("../data/xml_files/dhq_updated_data.xml") """
""" string_new_xml = etree.tostring(tree, encoding='unicode', method='xml')
with open("../data/xml_files/dhq_updated_data.xml", "w") as new_xml:
    new_xml.write(string_new_xml) """