import json
import os

file = "../data/json_files/crossref_api/crossref_original_Digital_Scholarship_in_the_Humanities.json"

with open(file, "r", encoding="utf-8") as f:
    crossref_schema = json.load(f)
    with open("../data/json_files/my_schema/ms_DSHTEST", "a", encoding="utf-8") as fd:
        fd.write("[")
        for index, article in enumerate(crossref_schema):
            string_article = json.dumps(article)
            if article is not None and "404" not in string_article:
                identifier = article["DOI"]
                url = article["URL"]
                if "author" in article:
                    authors = [author for author in article["author"]]
                else:
                    authors = []
                if "abstract" in article:
                    abstract = article["abstract"]
                else:
                    abstract = []
                title = article["title"][0]
                date = article["created"]["date-time"]
                publisher = article["publisher"]
                journal_title = article["container-title"][0]
                keywords = []
                if "volume" in article:
                    volume = article["volume"]
                else:
                    volume = ""
                if "issue" in article:
                    issue = article["issue"]
                else:
                    issue = ""    
                if "issn-type" in article:
                    ISSN = article["issn-type"]
                else:
                    ISSN = [{
            "value": "2055-768X",
            "type": "electronic"
        },
        {
            "value": "2055-7671",
            "type": "print"
        }]

                # creating my schema
                python_dict = dict()
                python_dict['url'] = url
                python_dict['identifier'] = {
                    'string_id' : identifier,
                    'id_scheme' : "DOI" 
                    }
                python_dict['abstract'] = abstract
                python_dict['article_title'] = title
                python_dict['authors'] = authors
                python_dict['publisher'] = publisher
                python_dict['date'] = date
                python_dict['keywords'] = keywords
                python_dict['journal_title'] = journal_title
                python_dict['volume'] = volume
                python_dict['issue'] = issue
                python_dict['ISSN'] = ISSN
            
                json.dump(python_dict, fd)
                if index<len(crossref_schema)-1:
                    fd.write(",")
        fd.write("]")