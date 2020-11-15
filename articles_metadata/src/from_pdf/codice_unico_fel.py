from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter,TextConverter,XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import lxml.etree as etree
import re
from xml.dom import minidom
from xml.etree import ElementTree as ET
import pandas as pd

def convert(case, pdfpath, targetfilepath, pages=100):
    if not pages: pagenums = set();
    else:         pagenums = set(pages);
    manager = PDFResourceManager()
    codec = 'utf-8'
    caching = True
    word_margin = 1
    laparams2 = LAParams(all_texts=True, detect_vertical=True,
                      line_overlap=0.5, char_margin=1000.0, #set char_margin to a large number
                      line_margin=0.5, word_margin=0.5,
                      boxes_flow=0.5)

    laparams3 = LAParams(all_texts=True, line_margin=0.1, boxes_flow=None)

    if case == 'text':
        output = io.StringIO()
        converter = TextConverter(manager, output, codec=codec, laparams=LAParams())
    if case == 'HTML':
        output = io.BytesIO()
        converter = HTMLConverter(manager, output, codec=codec, laparams=LAParams())
    if case == 'XML':
        output = io.BytesIO()
        converter = XMLConverter(manager, output, codec=codec, laparams= laparams2)

    interpreter = PDFPageInterpreter(manager, converter)
    infile = open(pdfpath, 'rb')

    for page in PDFPage.get_pages(infile, pagenums,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    convertedPDF = output.getvalue()

    infile.close(); converter.close(); output.close()

    convertedFile = open(targetfilepath, 'wb')
    convertedFile.write(convertedPDF)
    convertedFile.close()

    return targetfilepath

def uniform_cm(pdfpath):
    targetfilepath = convert('XML', pdfpath, 'bo.xml', pages=None)
    parser = etree.XMLParser(remove_blank_text=True, recover=True)
    ntree = etree.parse(targetfilepath, parser)


    for node in ntree.getiterator():
        if node.attrib.get('size') == '10.439':
            node.attrib['size'] = '10.238'
    root = ntree.getroot()
    for node in ntree.getiterator():
        if node.attrib.get('size') == '10.060'  or node.attrib.get('size') =='10.958':
            node.attrib['size'] = '10.482'
    root = ntree.getroot()

    for node in ntree.getiterator():
        if node.attrib.get('size') == '8.988' or node.attrib.get('size') =='6.926' :
            node.attrib['size'] = '10.238'
    root = ntree.getroot()
    #print(ET.tostring(root))
    return ntree

def getBBoxFirstValue(line):
    if line is not None:
        bb = line.attrib.get('bbox')
        if bb is not None:
            try:
                return float(bb.split(",")[0])
            except ValueError:
                pass
    return None

# Remove all 'textline' elements
def due(pdfpath):
    ntree = uniform_cm(pdfpath)
    etree.strip_tags(ntree, 'textline')

    # Search for all text "textbox" elements
    for textbox in ntree.xpath('//textbox'):
        new_line = etree.Element("new_line")
        previous_bb = None

        # From a given textbox element, iterate over all the "text" elements
        for x in textbox.iter("text"):
            # Get current bb valu
            bb = getBBoxFirstValue(x)
            # Check current and past values aren't empty
            if bb is not None and previous_bb is not None and (bb - previous_bb) > 20:
                # Inserte newline into parent tag
                x.getparent().insert(x.getparent().index(x), new_line)

                # A new "new_line" element is created
                new_line = etree.Element("new_line")

            # Append current element is new_line tag
            new_line.append(x)

            # Keep latest non empty BBox 1st value
            if bb is not None:
                previous_bb = bb

        # Add last new_line element if not null
        textbox.append(new_line)
    tree = ntree
    return tree

def newline(pdfpath):
    tree = due(pdfpath)
    root = tree.getroot()
    for new_line_block in tree.xpath('//new_line'):
        # Find all "text" element in the new_line block
        list_text_elts = new_line_block.findall('text')

        # Iterate over all of them with the current and previous ones
        for previous_text, current_text in zip(list_text_elts[:-1], list_text_elts[1:]):
            # Get size elements
            prev_size = previous_text.attrib.get('size')
            curr_size = current_text.attrib.get('size')
            # If they are equals and not both null
            if curr_size == prev_size and curr_size is not None:
                # Get current and previous text
                pt = previous_text.text if previous_text.text is not None else ""
                ct = current_text.text if current_text.text is not None else ""
                # Add them to current element
                current_text.text = pt + ct
                # Remove preivous element
                previous_text.getparent().remove(previous_text)

    newtree = etree.tostring(root, encoding='utf-8', pretty_print=True)
    # newtree = newtree.decode("utf-8")
    return newtree

def get_xml_by_tag_names(xml_path, tag_name_1, tag_name_2):

    data = {}
    xml_tree = minidom.parseString(xml_path)
    item_group_nodes = xml_tree.getElementsByTagName(tag_name_1)
    for idx, item_group_node in enumerate(item_group_nodes):
        cl_compile_nodes = item_group_node.getElementsByTagName(tag_name_2)
        for _ in cl_compile_nodes:
            data[idx]=[item_group_node.toxml()]
    return data


def find_regex_fasi(regex, text):
    matches_fasi = re.findall(regex, text)
    return len(matches_fasi)

def find_regex(regex, text, opzione2= None, opzione3 = None, opzione4 = None, opzione5=None):
    lista = []
    for x in text:
        matches_prima = re.findall(regex, x)
        matches_prima2 = []
        matches_prima3 = []
        matches_prima4 = []
        matches_prima5 = []
        if opzione2 is not None:
            matches_prima2 = re.findall(opzione2, x)
            if opzione3 is not None:
                matches_prima3 = re.findall(opzione3, x)
                if opzione4 is not None:
                    matches_prima4 = re.findall(opzione4, x)
                    if opzione5 is not None:
                        matches_prima5 = re.findall(opzione5, x)
        lunghezza = len(matches_prima) + len(matches_prima2) + len(matches_prima3) + len(matches_prima4) + len(matches_prima5)
        lista.append(lunghezza)
        #print(matches_prima, matches_prima2, matches_prima3, matches_prima4, matches_prima5)
    return sum(lista)



def search_delete_append(dizionario, dizionariofasi):
    deletekeys = []

    for k in dizionario:
        for v in dizionario[k]:
            if "7.489" in v:
                deletekeys.append(k)
                dizionariofasi[k] = v

    for item in deletekeys:
        del dizionario[item]

def clean(dizionario, lista):
    for value in dizionario.values():
        myxml = ' '.join(value)
        tree = ET.fromstring(myxml)
        tmpstring = ' '.join(text.text for text in tree.findall('text'))
        for to_remove in ("<", ">", ".", ",", ";", "-", "!", ":", "’", "?", "<>", "=", "|", "(", ")", "\n", "/", "\uf8ee", "−", "[]","↔", "…" ):
            tmpstring = tmpstring.replace(to_remove, "")
        lista.append(tmpstring)
    return lista

def clean_fasi(dizionario, lista):
    pattern = re.compile("(?<!\d)\d{2}(?!\d)")
    for value in dizionario.values():

        myxml2 = ''.join(value)
        tree2 = ET.fromstring(myxml2)
        tmpstring2 = ' '.join(text.text for text in tree2.findall('text'))
        for to_remove in ("<", ">", ".", ",", ";", "-", "!", ":", "’", "?", "<>", "=", "|", "(", ")", "\n", "/", "\uf8ee", "−", "[]","↔", "…"):
            tmpstring2 = tmpstring2.replace(to_remove, "")
            tmpstring2 = pattern.sub("", tmpstring2)
        lista.append(tmpstring2)
    return lista

def main(pdfpath):
    newtree= newline(pdfpath)
    dict_fasi = {}
    data = get_xml_by_tag_names(newtree, 'new_line', 'text')
    search_delete_append(data, dict_fasi)
    testoo = []
    clean(data, testoo)
    #testo = ''.join(testo)
    find_prima = re.compile(r"\]\s*prima(?!\S)")

    FIND_FASE12T = re.compile(r"\]\s*1\s*([\w\s]+)\s*2\s*T")
    FIND_FASE123T_PRIMA = re.compile(r"\]\s*prima\s*1\s*(?!\d+\s+)[^\s→]+(?:\s+(?!\d+\b)[^\s→]+)*\s*2\s+(?!\d+\b)[^\s→|T]+(?:\s+(?!\d+\b)[^\s→]+)*\s*$") #SBAGLIATA
    FIND_FASE123T = re.compile(r"\]\s*1([\w\s]+)\s*2([\w\s]+)\s3\sT")
    FIND_FASE123T_OPZ2 = re.compile(r"\]\s*1\s*(?!\d+\s+)[^\s→]+(?:\s+(?!\d+\b)[^\s→]+)*\s*2\s+(?!\d+\b)[^\s→|T]+(?:\s+(?!\d+\b)[^\s→|T]+)*\s*$")
    FIND_FASE_123FRECCIAT = re.compile(r"\]\s*1\s*([\w\s]+)\s*2([\w\s][^3]+)\s*→\s*T")
    FIND_FASE_1FRECCIA23T = re.compile(r"\]\s*1\s*([\w\s]+)\s*→\s*2([\w\s]+)\s*(T|3\sT)")
    FIND_FASE_FRECCIA1F2FT = re.compile(r"\]\s*1\s*([\w\s]+)\s*→\s*2([\w\s]+)\s*→\s*(T|3\sT)[^→]")
    FIND_FASE_PRIMA_123FRECCIAT = re.compile(r"\]\s*prima\s*1\s*([\w\s]+)\s*2([\w\s]+)\s*→\s*T")
    FIND_FASE_PRIMA_1FRECCIA23T = re.compile(r"\]\s*prima\s*1\s*([\w\s]+)\s*→\s*2([\w\s]+)\s*(T|3\sT)")
    FIND_FASE_PRIMA_FRECCIA1F2FT = re.compile(r"\]\s*prima\s*1\s*([\w\s]+)\s*→\s*2([\w\s]+)\s*→\s*(T|3\sT)")
    FIND_FASE_PRIMA_1FRECCIA2 = re.compile(r"\]\s*prima\s*1\s*([\w\s]+)\s*→\s*2([\w\s]+)")
    FIND_FASE_PRIMA_12345T_OPZ2 = re.compile(r"\]\s*prima\s*1\s*([\w\s]+)\s*2([\w\s]+)\s*3([\w\s]+)\s*4\s*([\w\s][^T|5]+)$")
    FIND_FASE_12345T = re.compile(r"\]\s*1\s*([\w\s]+)\s*2([\w\s]+)\s*3([\w\s]+)\s*4([\w\s]+)\s*5\sT")
    FIND_FASE_12345T_OPZ_2 = re.compile(r"\]([\w\s][^prima]+)\s*1\s*([\w\s]+)\s*2([\w\s]+)\s*3([\w\s]+)\s*4([\w\s]+)\s*5\sT")
    FASE_RICAVATA_12T = re.compile(r"\]\s*1\s*([\w\s][^2]+)\s*→\s*(T|2\s*T)")
    FIND_FASE_1234T_OPZ_1 = re.compile(r"]\s*1([\w\s]+)\s*2([\w\s]+)\s*3([\w\s][^4|→]+)\s*(T|4\s*T)")
    FIND_FASE_1234T_OPZ_2 = re.compile(r"(?!.*\s4\s)\]\s*1\s*([\w\s]+)\s*2\s*([\w\s]+)\s*3\s*([^\d_T→]+)\b(?:\s)$")
    FIND_FASE_123456T = re.compile(
        r"\]\s*1([\w\s]+)\s*2([\w\s]+)\s*3([\w\s][^5|→]+)\s*4\s*([\w\s][^5|→]+)\s*5\s*([\w\s][^T|→]+)\s*(T|6\s*T)")
    FIND_FASE_PRIMA_1234567T = re.compile(
        r"\]\s*prima\s*([\w\s]+)\s*1([\w→\s]+)\s*2([\w→\s]+)\s*3([\w→\s][^5]+)\s*4\s*([\w→\s][^5]+)\s*5\s*([\w→\s]+)\s*6\s*([\w\s]+)")

    #fase ricavata 1234T
    FIND_FASE_123FRECCIA4T = re.compile(r"\]\s*1\s*([\w\s]+)\s*2([\w\s]+)\s*3([\w\s][^4]+)\s*→\s*(T|4\s*T)")
    FIND_FASE_1FRECCIA234T = re.compile(r"\]\s*1\s*([\w\s]+)\s*→\s*2([\w\s]+)\s*3([\w\s][^T]+)\s*(T|4\s*T)")
    FIND_FASE_12FRECCIA34T = re.compile(r"\]\s*1\s*([\w\s]+)\s*2([\w\s]+)\s*→\s*3([\w\s]+)\s*(T|4\s*T)")
    FIND_FASE_FRECCIA1F2F4T = re.compile(r"\]\s*1\s*([\w\s]+)\s*→\s*2([\w\s]+)\s*→\s*3([\w\s][^4]+)\s*→\s*T")
    FIND_FASE_12F3F4T = re.compile(r"\]\s*1\s*([\w\s]+)\s*2([\w\s]+)\s*→\s*3([\w\s]+)\s*→\s*(T|4\s*T)")

    #fase ricavata prima 1234T
    FIND_FASE_PRIMA_123FRECCIA4T = re.compile(r"\]\s*prima\s*1\s*([\w\s]+)\s*2([\w\s]+)\s*3([\w\s][^4]+)\s*→\s*(T|4\s*T)")
    FIND_FASE_PRIMA_1FRECCIA234T = re.compile(r"\]\s*prima\s*1\s*([\w\s]+)\s*→\s*2([\w\s]+)\s*3([\w\s][^T]+)\s*(T|4\s*T)")
    FIND_FASE_PRIMA_12FRECCIA34T = re.compile(r"\]\s*prima\s*1\s*([\w\s]+)\s*2([\w\s]+)\s*→\s*3([\w\s]+)\s*(T|4\s*T)")
    FIND_FASE_PRIMA_FRECCIA1F2F4T = re.compile(r"\]\s*prima\s*1\s*([\w\s]+)\s*→\s*2([\w\s]+)\s*→\s*3([\w\s][^4]+)\s*→\s*T")
    FIND_FASE_PRIMA_12F3F4T = re.compile(r"\]\s*prima\s*1\s*([\w\s]+)\s*2([\w\s]+)\s*→\s*3([\w\s]+)\s*→\s*(T|4\s*T)")


    FIND_FASE_PRIMA1234T = re.compile(r"(?!.*\s4\s)\]\s*prima\s*1\s*([\w\s]+)\s*2\s*([\w\s]+)\s*3\s*([^\d_T]+)\b(?:\s)")
    PAROLEFT = re.compile(r"\]\s*(?!\d+\s+)[^\s→]+(?:\s+(?!\d+\b)[^\s→]+)*\s*→\s*T\s*")
    FIND_FASE_RICAVATE12345T = re.compile(
        r"\]\s*1\s*([\w\s]+)\s*2([\w\s]+)\s*3([\w\s]+)\s*4\s*([\w\s^5]+)\s*→\s*(T|5\sT)")
    FIND_FASE_RICAVATE_123456T = re.compile(r"\]\s*1\s*([\w\s]+)\s*2([\w\s]+)\s*3([\w\s]+)\s*4\s*([\w\s][^5]+)\s*5\s*([\w\s][^6]+)\s*→\s*(T)")

    FIND_FASE_PRIMA_123456T = re.compile(
        r"]\s*prima\s*1\s*([\w\s]+)\s*2\s*([\w\s]+)\s*3\s*([\w\s]+)\s*4\s*([\w\s]+)\s*5\s*([\w\s][^T|6]+)$")



    FIND_FASE_PRIMA_12345678T = re.compile(
        r"]\s*prima\s*1\s*([\w\s]+)\s*2\s*([\w\s]+)\s*3\s*([\w\s]+)\s*4\s*([\w\s]+)\s*5\s*([\w\s]+)\s*6\s*([\w\s]+)\s*7\s*([\w\s][^T|8]+)$")

    find_da = re.compile(r"\]\s*da(?!\S)")
    #find_da_cui = re.compile(r"\]\s*([\w\s]+)\s*da\scui")
    find_sps = re.compile(r"\]\s*([\w\s]+)\s*sps")
    find_su = re.compile(r"\]\s*([\w\s]+)\s*su")
    find_as = re.compile(r"\]\s*([\w\s]+)\s*as")
    find_ins = re.compile(r"\]\s*([\w\s]+)\s*ins")
    find_segue = re.compile(r"\]\s*([\w\s]+)\s*segue")
    find_corrin = re.compile(r"\]\s*([\w\s]+)\s*corr\s*in")

    df2 = pd.DataFrame([find_regex(find_prima, testoo),
                       find_regex(find_da, testoo),
                       find_regex(find_sps, testoo),
                       find_regex(find_su, testoo),
                       find_regex(find_as, testoo),
                       find_regex(find_ins, testoo),
                       find_regex(find_segue, testoo),
                       find_regex(FIND_FASE12T, testoo),
                       find_regex(FIND_FASE123T, testoo, FIND_FASE123T_OPZ2),
                       find_regex(FIND_FASE_1FRECCIA23T, testoo, FIND_FASE_123FRECCIAT, FIND_FASE_FRECCIA1F2FT),
                       find_regex(FIND_FASE_PRIMA_1FRECCIA2, testoo),
                       find_regex(FIND_FASE_PRIMA_12345T_OPZ2, testoo),
                       find_regex(FIND_FASE123T_PRIMA, testoo),
                       find_regex(find_corrin, testoo),
                       find_regex(FASE_RICAVATA_12T, testoo),
                       find_regex(FIND_FASE_1234T_OPZ_1, testoo, FIND_FASE_1234T_OPZ_2),
                       find_regex(FIND_FASE_12345T, testoo),
                       find_regex(FIND_FASE_123456T, testoo),
                       find_regex(FIND_FASE_PRIMA_1234567T, testoo),
                       find_regex(FIND_FASE_1FRECCIA234T, testoo, FIND_FASE_123FRECCIA4T, FIND_FASE_FRECCIA1F2F4T,
                                  FIND_FASE_12FRECCIA34T, FIND_FASE_12F3F4T),
                       find_regex(FIND_FASE_PRIMA1234T, testoo),
                       find_regex(PAROLEFT, testoo),
                       find_regex(FIND_FASE_RICAVATE12345T, testoo),
                       find_regex(FIND_FASE_RICAVATE_123456T, testoo),
                        0,
                        find_regex(FIND_FASE_PRIMA_1FRECCIA234T, testoo, FIND_FASE_PRIMA_123FRECCIA4T, FIND_FASE_PRIMA_FRECCIA1F2F4T,
                                   FIND_FASE_PRIMA_12FRECCIA34T, FIND_FASE_PRIMA_12F3F4T),
                        find_regex(FIND_FASE_PRIMA_123456T, testoo),
                        find_regex(FIND_FASE_PRIMA_12345678T, testoo),


                       ])
    df2.rename(index={0: 'prima', 1: 'da', 2: 'sps.', 3:'su', 4:'as.', 5:'ins.', 6:'segue',
                     7:'fase 12T', 8:'fase 123T', 9:'fasericavata 123T', 10:'fasericavataprima 123T',
                     11:'faseprima 12345T', 12:'faseprima 123T', 13:'corr.in', 14:'fasericavata 12T',
                      15:'fase 1234T', 16:'fase 12345T',
                     17:'fase 123456T', 18:'fasericavataprima 1234567T',
                     19:'fasericavata 1234T', 20:'faseprima 1234T', 21:'fasericavata T', 22:'fasericavata 12345T', 23:'fasericavata 123456T',
                      24:'corpo minore', 25:'fasericavataprima 1234T', 26:'faseprima 123456T', 27:'faseprima 12345678T'}, inplace=True)


    #################

    testo_fasi = []
    values = [x for x in dict_fasi.values()]
    myxml_fasi = ' '.join(values)
    find_CM = re.compile(r"10\.238")
    find_regex_fasi(find_CM, myxml_fasi) #quanti CM ci sono?
    #print(myxml_fasi)
    clean_fasi(dict_fasi, testo_fasi)
    #testo_fasi = ''.join(testo_fasi)
    print(testo_fasi)


    df = pd.DataFrame([find_regex(find_prima, testo_fasi),#why?
                       find_regex(find_da, testo_fasi),
                       find_regex(find_sps, testo_fasi),
                       find_regex(find_su, testo_fasi),
                       find_regex(find_as, testo_fasi),
                       find_regex(find_ins, testo_fasi),
                       find_regex(find_segue, testo_fasi),
                       find_regex(FIND_FASE12T, testo_fasi),
                       find_regex(FIND_FASE123T, testo_fasi, FIND_FASE123T_OPZ2),
                       find_regex(FIND_FASE_1FRECCIA23T, testo_fasi, FIND_FASE_123FRECCIAT, FIND_FASE_FRECCIA1F2FT),
                       find_regex(FIND_FASE_PRIMA_1FRECCIA2, testo_fasi),
                       find_regex(FIND_FASE_PRIMA_12345T_OPZ2, testo_fasi),
                       #find_regex(FIND_FASE_PRIMA_1FRECCIA23T, testo_fasi, FIND_FASE_PRIMA_123FRECCIAT,
                                  #FIND_FASE_PRIMA_FRECCIA1F2FT),
                       find_regex(FIND_FASE123T_PRIMA, testo_fasi),
                       find_regex(find_corrin, testo_fasi),
                       find_regex(FASE_RICAVATA_12T, testo_fasi),
                       find_regex(FIND_FASE_1234T_OPZ_1, testo_fasi, FIND_FASE_1234T_OPZ_2),
                       find_regex(FIND_FASE_12345T, testo_fasi, FIND_FASE_12345T_OPZ_2),
                       find_regex(FIND_FASE_123456T, testo_fasi),
                       find_regex(FIND_FASE_PRIMA_1234567T, testo_fasi),
                       find_regex(FIND_FASE_1FRECCIA234T, testo_fasi, FIND_FASE_123FRECCIA4T, FIND_FASE_FRECCIA1F2F4T,
                                  FIND_FASE_12FRECCIA34T),
                       find_regex(FIND_FASE_PRIMA1234T, testo_fasi),
                       find_regex(PAROLEFT, testo_fasi),
                       find_regex(FIND_FASE_RICAVATE12345T, testo_fasi),
                       find_regex(FIND_FASE_RICAVATE_123456T, testo_fasi),
                       find_regex_fasi(find_CM, myxml_fasi),
                       find_regex(FIND_FASE_PRIMA_1FRECCIA234T, testo_fasi, FIND_FASE_PRIMA_123FRECCIA4T,
                                  FIND_FASE_PRIMA_FRECCIA1F2F4T,
                                  FIND_FASE_PRIMA_12FRECCIA34T, FIND_FASE_PRIMA_12F3F4T),
                       find_regex(FIND_FASE_PRIMA_123456T, testo_fasi),
                       find_regex(FIND_FASE_PRIMA_12345678T, testo_fasi),


                       ])
    df.rename(index={0: 'prima', 1: 'da', 2: 'sps.', 3:'su', 4:'as.', 5:'ins.', 6:'segue',
                     7:'fase 12T', 8:'fase 123T', 9:'fasericavata 123T', 10:'fasericavataprima 123T',
                     11:'faseprima 12345T', 12:'faseprima 123T', 13:'corr.in', 14:'fasericavata 12T',
                      15:'fase 1234T', 16:'fase 12345T',
                     17:'fase 123456T', 18:'fasericavataprima 1234567T',
                     19:'fasericavata 1234T', 20:'faseprima 1234T', 21:'fasericavata T', 22:'fasericavata 12345T', 23:'fasericavata 123456T',
                      24:'corpo minore', 25:'fasericavataprima 1234T', 26:'faseprima 123456T', 27:'faseprima 12345678T'}, inplace=True)
    print(df)
    #print(df2)
    df.to_csv('csv/fermoelucia/testofasifet1c8.csv')
    df2.to_csv('csv/fermoelucia/testonormalefet1c8.csv')

print(main('fet1c8.pdf'))
