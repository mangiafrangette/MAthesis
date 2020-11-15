import json
import itertools

# update ms file with affiliations from another

def update(first_path, second_path):
    with open(first_path, "r", encoding="utf-8") as fd:
        parsed = json.load(fd)
        with open(second_path, "r", encoding="utf-8") as f:
            end = json.load(f)
            for article1, article2 in itertools.product(parsed, end):
                if article1["article_title"] == article2["article_title"]:
                    article1 = article2
    with open(first_path, "w", encoding="utf-8") as fd:
        json.dump(parsed, fd, ensure_ascii=False)

first_path = "../data/json_files/no_country_dataset/adho_papers/ms_file/ms_ADHO_Conference copy.json"
second_path = "../data/xml_files/adho_conferences/adho_papers/special_affiliations/ms_ADHO_Conference_aff_speciali.json"
update(first_path, second_path)