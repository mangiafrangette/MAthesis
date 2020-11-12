import json

path = "../data/json_files/complete_dataset"
file = "ms_DSH_filled_aff.json"

def aaa(file):
    with open(file, "r", encoding="utf-8") as f:
        json_file = json.load(f)
        for article in json_file:
            for author in article["authors"]:
                if len(author["affiliation"]) > 1: 
                    print(author["affiliation"])

aaa(f'{path}/{file}')