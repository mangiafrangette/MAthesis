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
    '{http://www.digitalhumanities.org/ns/dhq}q'
    '{http://www.tei-c.org/ns/1.0}title[@rend="quotes"]')
      
    # Access the nodes with relevant data and take the textual string only
    # Data is wrapped into a function to clean text from unnecessary characters
    abstract = remove_spaces(parsed_xml.find('.//{http://www.digitalhumanities.org/ns/dhq}abstract').text)
    print(parsed_xml.find('.//{http://www.digitalhumanities.org/ns/dhq}abstract').text)
    
    title = remove_spaces(parsed_xml.find('.//{http://www.tei-c.org/ns/1.0}title').text)
    authors_list = parsed_xml.findall('.//{http://www.digitalhumanities.org/ns/dhq}authorInfo')
    
    authors = [{
        'given': remove_spaces(author.find('.//{http://www.digitalhumanities.org/ns/dhq}author_name').text),
        'family' : remove_spaces(author.find('.//{http://www.digitalhumanities.org/ns/dhq}family').text),
        'affiliation' : [remove_spaces(author.find('.//{http://www.digitalhumanities.org/ns/dhq}affiliation').text)]
        }
        for author in authors_list
        ]
#   publisher = remove_spaces(parsed_xml.find('.//{http://www.digitalhumanities.org/ns/dhq}family').text)
    date = parsed_xml.find('.//{http://www.tei-c.org/ns/1.0}date').text
    keywords_list = parsed_xml.find('.//{http://www.tei-c.org/ns/1.0}keywords//*')
    keywords = [keyword.text for keyword in keywords_list]
    volume = remove_spaces(parsed_xml.find('.//{http://www.tei-c.org/ns/1.0}idno[@type="volume"]').text)
    issue = remove_spaces(parsed_xml.find('.//{http://www.tei-c.org/ns/1.0}idno[@type="issue"]').text)

    # Create python dict and append metadata text following my schema
    python_dict = dict()
    python_dict['abstract'] = abstract
    python_dict['title'] = title
    python_dict['authors'] = authors
#   python_dict['publisher'] = 
    python_dict['date'] = date
    python_dict['keywords'] = keywords
    python_dict['journal_title'] = "Digital Humanities Quarterly"
    python_dict['volume'] = volume
    python_dict['issue'] = issue
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
    with open(f"../data/dhq.json", "a", encoding="utf-8") as fd:
        fd.write("[")
        for file_xml in filenames: 
            json.dump(xml_to_json(f'{path}/{file_xml}'), fd)
            fd.write(",")
        fd.write("]")

write_new_json()

# old codes
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

"""
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
    """

"""
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
"""