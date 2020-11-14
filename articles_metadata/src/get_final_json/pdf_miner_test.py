from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import *
from pdfminer.pdfpage import *
import io
import lxml.etree as etree
import re
from xml.dom import minidom
from xml.etree import ElementTree as ET
import sys
from pdfminer.high_level import extract_pages

from io import StringIO

from pdfminer.layout import *
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

file_path = "../data/xml_files/adho_conferences/dh2008_papers.pdf"

def pdf_to_text(file):
    output_string = StringIO()
    with open(file, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        with open('../data/xml_files/adho_conferences/dh2008_papers.txt', 'w', encoding="utf-8") as fd:
            fd.write(output_string.getvalue())
pdf_to_text(file_path)


def get_layout(file_path):
    for page_layout in extract_pages(file_path):
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                #print(element.get_text())
                with open('../data/xml_files/adho_conferences/testlayout.txt', 'a',encoding="utf-8") as fd:
                    fd.write(element)
get_layout(file_path)

""" for page_layout in extract_pages(file_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            print(character.fontname)
                            print(character.size) """