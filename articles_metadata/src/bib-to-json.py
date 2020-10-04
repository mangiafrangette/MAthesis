import bibtexparser
import json

with open('Computers-and-the-Humanities.bib', encoding="utf-8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)
    with open("Computers-and-the-Humanities.json", "w") as json_file:
        json.dump(bib_database.entries_dict, json_file)

with open('Computers-and-the-Humanities-proceedings.bib', encoding="utf-8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)
    with open("Computers-and-the-Humanities-proceedings.json", "w") as json_file:
        json.dump(bib_database.entries_dict, json_file)

with open('IJHAC.bib', encoding="utf-8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)
    with open("IJHAC.json", "w") as json_file:
        json.dump(bib_database.entries_dict, json_file)

with open('IJHAC-proceedings.bib', encoding="utf-8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)
    with open("IJHAC-proceedings.json", "w") as json_file:
        json.dump(bib_database.entries_dict, json_file)