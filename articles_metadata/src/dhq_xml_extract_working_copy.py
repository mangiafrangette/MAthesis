import json
import xmltodict
from lxml import etree
import xml.etree.ElementTree as ET
from django.utils.html import strip_tags
import re
import os

def xml_to_json(file):
    # Parse the xml file so that it can be manipulated
    parsed_xml = etree.parse(file)
    # Remove in-tag elements that are unnecessary 
    etree.strip_tags(parsed_xml,
    '{http://www.tei-c.org/ns/1.0}emph', 
    '{http://www.tei-c.org/ns/1.0}p', 
    '{http://www.digitalhumanities.org/ns/dhq}@rend', 
    '{http://www.digitalhumanities.org/ns/dhq}#text')
    print(type(parsed_xml))
#    abstract = parsed_xml.find('.//{http://www.digitalhumanities.org/ns/dhq}abstract')
#    title = parsed_xml.find('.//{http://www.tei-c.org/ns/1.0}title')
#    authors = parsed_xml.findall('.//{http://www.digitalhumanities.org/ns/dhq}authorInfo')
#    print(abstract, title, authors)

    # Transform the etree object into an xml string
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
    xml_to_json(f'{path}/{file_xml}')