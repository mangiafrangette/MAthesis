import json

path = "../data/json_files/my_schema"
file = "ms_DSH.json"

def find_multiple_affiliations(file):
    with open(file, "r", encoding="utf-8") as f:
        json_file = json.load(f)
        for article in json_file:
            for author in article["authors"]:
                if author["affiliation"] is not None:
                    for affiliation in author["affiliation"]:
                        aff_split = affiliation.lower().split(" ")
                        if aff_split.count("university") >= 2:
                            author["affiliation"].append("DIVIDE")
    with open(file, "w", encoding="utf-8") as fd:
        json.dump(json_file, fd)

find_multiple_affiliations(f'{path}/{file}')