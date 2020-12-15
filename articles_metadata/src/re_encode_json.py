import json


# use this file to rewrite json files without unicode characters
def rencode(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            with open(file_path, "w", encoding="utf-8") as fd:
                json.dump(loaded, fd, ensure_ascii=False)

# call function
file_path = "../data/adho_conferences/ms_ADHO_2008.json"
rencode(file_path)