# Script to add parenthesis to the affiliations of Digital_Humanities_Quarterly.json, so affiliations will be list of
# strings instead of just a string

import json


def import_json_dict(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def add_parenthesis(journal_dict):
    for article in journal_dict:
        for author in article['authors']:
            author['affiliation'] = [author['affiliation']]
    return journal_dict


def overwrite_json(file_path, new_dict):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(new_dict, file)


def main():
    file_path = "../data/json_files/my_schema/ms_Digital_Humanities_Quarterly.json"
    journal_dict = import_json_dict(file_path)
    journal_dict = add_parenthesis(journal_dict)
    overwrite_json(file_path, journal_dict)


if __name__ == '__main__':
    main()
