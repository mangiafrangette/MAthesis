import json


# use this file to rewrite json files without unicode characters
def rencode(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            with open(file_path, "w", encoding="utf-8") as fd:
                json.dump(loaded, fd, ensure_ascii=False)

# call function
file_path = "../data/json_files/no_country_dataset/adho_papers/ms_ADHO_Conference_special_affs.json"
rencode(file_path)