import json
import xmltodict
from lxml import etree
import xml.etree.ElementTree as ET
from django.utils.html import strip_tags
import re
import os
from lxml.html.soupparser import fromstring
from bs4 import BeautifulSoup
from lxml import html


path = '../../data/DSH'
folder = os.fsencode(path)
filenames = []
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith('.xml'): # whatever file types you're using...
        filenames.append(filename)

with open("DSH_final_data.json", "a+", encoding="utf-8") as fd:
    fd.write("[")
    for file in filenames:
        doc = file
        with open(f'{path}/{doc}', "r", encoding="utf-8") as doc:
            doc = doc.read()
            tree = etree.HTML(doc)
            id = tree.xpath("//meta[@name='citation_doi']/@content")
            abstract = tree.xpath("//section[@class='abstract']/descendant::text()")
            authors = tree.xpath('//meta[@name="citation_author"]/@content')
            authors_institutions = tree.xpath('//meta[@name="citation_author_institution"]/@content')

            authors_dicts_list = []
            for index1, author in enumerate(authors):
                for index2, institution in enumerate(authors_institutions):
                    if index1 == index2:
                        names = author.split(",")
                        if len(names) == 2:
                            author_dict = {
                                    'given': names[1],
                                    'family' : names[0],
                                    'affiliation' : [institution]
                                    }
                            authors_dicts_list.append(author_dict)
                        else:
                            author_dict = {
                                    'given': author,
                                    'family' : None,
                                    'affiliation' : [institution]
                                    }
                            authors_dicts_list.append(author_dict)
            data = {
                "string_id": id,
                "abstract": abstract,
                "authors": authors_dicts_list
            }
            json.dump(data, fd)
            fd.write(",")
            

    fd.write("]")



""" def final_dsh(file):

    parser = etree.XMLParser(remove_comments=True)
    # Parse the xml file so that it can be manipulated
    parsed_xml = etree.parse(file, parser=parser) 
    from elementtree.ElementTree import ElementTree
    mydoc = ElementTree(file=full_file)
    for e in mydoc.findall('/foo/bar'):
        print e.get('title').text
    
    # Define path of elements of interest
    abstract = xpath('//section[@class="abstract"]').get()
    authors = xpath('//meta[@name="citation_author"]/@content').getall()
    authors_institutions = xpath('//meta[@name="citation_author_institution"]/@content').getall()

    #get authors and their affiliations
    authors_dicts_list = []
    for index1, author in enumerate(authors):
        for index2, institution in enumerate(authors_institutions):
            if index1 == index2:
                names = author.split(",")
                if len(names) == 2:
                    author_dict = {
                            'given': names[1],
                            'family' : names[0],
                            'affiliation' : [institution]
                            }
                    authors_dicts_list.append(author_dict)
                else:
                    author_dict = {
                            'given': author,
                            'family' : None,
                            'affiliation' : [institution]
                            }
                    authors_dicts_list.append(author_dict)

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


    # Create python dict and append metadata text following my schema
    python_dict = dict()
    python_dict['id'] = 
    python_dict['authors'] = authors_dicts_list
    python_dict['abstract'] = abstract


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
 """