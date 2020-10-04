import json
import xmltodict
from lxml import etree
import xml.etree.ElementTree as ET
from django.utils.html import strip_tags
import re

def xml_to_json(file):
    # Parse the xml file so that it can be manipulated
    parsed_xml = etree.parse(file)
    # Remove in-tag elements that are unnecessary 
    etree.strip_tags(parsed_xml,'{http://www.tei-c.org/ns/1.0}emph', '{http://www.tei-c.org/ns/1.0}p')
    # Transform the etree object into an xml string
    string_xml = etree.tostring(parsed_xml, encoding='unicode', method='xml')
    # Remove extra spaces
    string_xml = re.sub(r'\n\s+', ' ', string_xml)
    # Transform the xml string to a python dictionary
    xml_to_dict = xmltodict.parse(string_xml)
    # Create the json file
    json_data = json.dumps(xml_to_dict)
    with open("../data/dhq.json", "w", encoding="utf-8") as json_file:
        json_file.write(json_data)

xml_to_json("../data/xml_files/000436.xml")