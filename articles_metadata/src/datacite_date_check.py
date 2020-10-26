import json
import os

def datacite_to_my_schema(origin, ms):
    with open(origin, "r", encoding="utf-8") as f:
        datacite_schema = json.load(f)
        with open(ms, "r", encoding="utf-8") as fd:
            ms_journal = json.load(fd)
            for article1 in datacite_schema:
                for article2 in ms_journal:
                    if article1["data"]["attributes"]["doi"] ==  article2["identifier"]["string_id"]:
                        article2["date"] = article1["data"]["attributes"]["registered"]
                        with open(ms, "w", encoding="utf-8") as fd:
                            json.dump(ms_journal, fd)         

                

datacite_to_my_schema("../data/json_files/datacite_api/datacite_original_International_Journal_for_Digital_Art_History.json", "../data/json_files/my_schema/ms_International_Journal_for_Digital_Art_History.json")
    
