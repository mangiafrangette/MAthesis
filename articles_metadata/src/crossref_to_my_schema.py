import json

def crossref_to_my_schema(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        crossref_schema = json.load(f)
        authors = [author for author in crossref_schema["author"]]
        # no abstract in crossref
        title = crossref_schema["title"]
        date = crossref_schema["created"]["date-time"]
        journal_title = crossref_schema["container-title"]
        # keywords = crossref_schema["title"]
        volume = crossref_schema['volume']
        issue = crossref_schema["issue"]
        ISSN = crossref_schema["ISSN"]

    # creating my schema
        python_dict = dict()
        # python_dict['abstract'] = abstract
        python_dict['title'] = title
        python_dict['authors'] = authors
    #   python_dict['publisher'] = 
        python_dict['date'] = date
    #    python_dict['keywords'] = keywords
        python_dict['journal_title'] = journal_title
        python_dict['volume'] = volume
        python_dict['issue'] = issue
        python_dict['ISSN'] = ISSN

        json_data = json.dumps(python_dict)
        with open(f"../data/my_schema_{file_name}", "w", encoding="utf-8") as json_file:
            json_file.write(json_data)

crossref_to_my_schema("crossref-api.json")