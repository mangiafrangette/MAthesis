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
#pdf_to_text(file_path)


def get_layout(file_path):
    for page_layout in extract_pages(file_path):
        for element in page_layout:
            #if isinstance(element, LTTextBoxHorizontal):
                #print(element.get_text())
            with open('../data/xml_files/adho_conferences/testlayout.txt', 'a',encoding="utf-8") as fd:
                fd.write(str(element))
#get_layout(file_path)

def get_fonts(file_path):
    text = ""
    for page_layout in extract_pages(file_path):
            for element in page_layout:
                if isinstance(element, LTTextBox):
                    text += f'<<<<THIS IS A BOX>>>>{element.get_text()}'
                    if isinstance(element, LTTextContainer):
                        for text_line in element:
                            text += text_line.character
                            text += text_line.size
                        
    with open('../data/xml_files/adho_conferences/get_character_size.txt', 'w',encoding="utf-8") as fd:
        fd.write(text)

get_fonts(file_path)

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTFigure, LTTextBox
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser



def test2(pdf_path): 
    text = ""
    with open(pdf_path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=LAParams(all_texts=False, detect_vertical=True))
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            layout = device.get_result()

            for obj in layout:
                if isinstance(obj, LTTextBox):
                    text += f'<<<<THIS IS A BOX>>>>{obj.get_text()}'

                """ elif isinstance(obj, LTFigure):
                    stack += list(obj) """
    with open('../data/xml_files/adho_conferences/test2-1.txt', 'w',encoding="utf-8") as fd:
        fd.write(text)

test2(file_path)

# other code found on the internet
""" from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

def convert_pdf(path):

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    fp = file(path, 'rb')
    process_pdf(rsrcmgr, device, fp)
    fp.close()
    device.close()

    str = retstr.getvalue()
    retstr.close()
    return str """