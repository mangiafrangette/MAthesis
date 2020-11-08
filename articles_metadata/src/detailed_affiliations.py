# Script to query ROR and/or GRID to get detailed info of articles' affiliations
# Overall steps: 1) create a set of affiliations, 2) for every affiliation in the set query ROR and/or GRID

import json
import os
import requests
import copy
import itertools


def import_json_dict(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def create_affiliations_set(path_of_files):
    folder = os.fsencode(path_of_files)
    affiliations_set = set()
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):  # whatever file types you're using...
            journal_dict = import_json_dict(f"{path_of_files}/{filename}")
            for article in journal_dict:
                if article['authors'] is not None:
                    for author in article['authors']:
                        if isinstance(author, dict):
                            if 'affiliation' in author.keys():
                                if author['affiliation'] is not None:
                                    #print(article['article_title'])
                                    #print(author['affiliation'])
                                    if len(author['affiliation']) > 0 and isinstance(author['affiliation'][0], str):
                                        affiliations_set.update(author['affiliation'])
                                        # print(len(author['affiliation']))
                                        # print(author)
                                        # print(author['affiliation'])

    affiliations_set.remove('')

    # for affiliation in affiliations_set:
    #     if len(affiliation) <= 1:
    #         print(affiliation)
    return affiliations_set

# Create a file with original and splitted names by comma. Testing a method to only query strings that communicate the university or institution and avoid noise
def filter_affiliation_set(affiliations_set):    
    with open("../data/json_files/affiliations_set.json", "w", encoding="utf-8") as f:
        affiliations_to_query = []
        words_to_check = ["university", "academy", "institute", "college"]
        for item in affiliations_set:
            splitted_affiliations = item.lower().split(",")
            query = item
            for word, string in itertools.product(words_to_check, splitted_affiliations):
                if word in string:
                    query = string                    
                    break                                    
            item_dict = {
                "original_name": item,
                "splitted_name": splitted_affiliations,
                "query": query
            }
            affiliations_to_query.append(item_dict)

        json.dump(affiliations_to_query, f)
    return affiliations_to_query


# The output of this function is a dictionary with this structure:
# { <affiliation of the set> : <list of dictionaries containing the result of the ror query>, ... }
def ror_queries(affiliations_to_query, file_path):
    queries_affiliations_dict = {}
    query_beginning = "https://api.ror.org/organizations?affiliation="
    for index, item in enumerate(affiliations_to_query[:30]):
        print(item["query"])
        query = query_beginning + item["query"]
        response = requests.get(query).json()
        print(index, "  ", f'{item["query"]}')
        print(response)
        if response['number_of_results'] == 0:
            queries_affiliations_dict[f'{item["query"]}'] = None
            print("errorinooo")
        else:
            queries_affiliations_dict[f'{item["query"]}'] = response['items']
        print()
        # if index == 5:
        #     write_json("../data/json_files/ror_queries.json", queries_affiliations_dict)
        #     return None
    return queries_affiliations_dict


# Comment the call of this function in main() if queries have NOT been already saved
def load_ror_queries(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Select ror results with a score grater than or equal to the threshold in input. Default threshold is 0.7.
# The output is a dictionary with the same structure of the input.
def select_results(affiliations_dict, threshold=0.7):
    if threshold > 1.0 or threshold < 0.0:
        raise ValueError("threshold value must be between 0 and 1")
    else:
        selected_affiliations_dict = {}
        for affiliation, results_list in affiliations_dict.items():
            if results_list is not None: # two if statements in order to have a robust algorithm independently from previous
                if len(results_list) > 0:
                    selected_affiliations_dict[affiliation] = []
                    for result in results_list:
                        if result['score'] >= threshold:
                            selected_affiliations_dict[affiliation].append(result)
        return selected_affiliations_dict


# Chose only the first ror result for every affiliation (i.e. with the highest score, descending order by score value
# is automatically provided by ror queries). The output is a dictionary with the same structure of the input.
def chose_single_result(affiliations_dict):
    chosen_affiliations_dict = {}
    for affiliation, results_list in affiliations_dict.items():
        if results_list is not None: # two if statements in order to have a robust algorithm independently from previous
            if len(results_list) > 0:
                chosen_affiliations_dict[affiliation] = results_list[0]
    return chosen_affiliations_dict


# Extract useful data from ror results.
# The dictionary in input MUST contain only ONE ror result for every affiliation.
def data_from_ror_results(chosen_affiliations_dict):
    return {
        affiliation: {
            'original_name': affiliation,
            'identifiers': {
                'ror': result['organization']['id'],
                'GRID': result['organization']['external_ids']['GRID']['preferred']
            },
            'normalized_name': result['organization']['name'],
            'country': result['organization']['country']['country_name']
        }
        for affiliation, result in chosen_affiliations_dict.items()
    }


# NEED TO STUDY https://www.dimensions.ai/dimensions-apis/
# useful links:
def add_grid_data(data_affiliations_dict):
    added_data_affiliations_dict = {}


# NEED TO BE TESTED WITH ALL JSON FILES
# Create COPIES of journals' json files with filled affiliations.
def fill_affiliations_json(path_of_files, data_affiliations_dict):
    folder = os.fsencode(path_of_files)
    affiliations_set = set()
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):  # whatever file types you're using...
            journal_dict = import_json_dict(f"{path_of_files}/{filename}")
            filled_journal_dict = copy.deepcopy(journal_dict)
            for article in filled_journal_dict:
                if article['authors'] is not None:
                    for author in article['authors']:
                        if isinstance(author, dict):
                            if 'affiliation' in author.keys():
                                if author['affiliation'] is not None:
                                    #print(article['article_title'])
                                    #print(author['affiliation'])
                                    if len(author['affiliation']) > 0 and isinstance(author['affiliation'][0], str):
                                        for affiliation in author['affiliation']:
                                            print(data_affiliations_dict)
                                            affiliation = data_affiliations_dict[affiliation]
            filename_without_extension = filename.split('.')[0]
            new_filename = f'{filename_without_extension}_filled_aff.json'
            with open(f"{path_of_files}/{new_filename}", "w", encoding="utf-8") as f:
                json.dump(data_affiliations_dict, f)


def main():
    path_of_json_files = "../data/json_files/my_schema/"
    ror_queries_file_path = "../data/json_files/affiliations/ror_queries.json"

    # Generate the set of the affiliation in the corpus of journals
    affiliations_set = create_affiliations_set(path_of_json_files)

    # filter_affiliation_set(affiliations_set)

    # Comment the following lines if ror queries have already been saved and load them with the next lines
    queries_affiliations_dict = ror_queries(filter_affiliation_set(affiliations_set), ror_queries_file_path)
    with open(ror_queries_file_path, "w", encoding="utf-8") as file:
        json.dump(queries_affiliations_dict, file)

    # Comment the following lines if ror queries have NOT already been saved and save them with the previous lines
    with open(ror_queries_file_path, "r", encoding="utf-8") as file:
        affiliations_dict = json.load(file)

    # Chose a threshold with which ror results will be selected
    threshold = 0.9
    selected_affiliations_dict = select_results(affiliations_dict, threshold)
    #print(selected_affiliations_dict)
    with open("../data/json_files/ror_selected.json", "w", encoding="utf-8") as file:
        json.dump(selected_affiliations_dict, file)

    chosen_affiliations_dict = chose_single_result(affiliations_dict)
    with open("../data/json_files/ror_single_result.json", "w", encoding="utf-8") as file:
        json.dump(chosen_affiliations_dict, file)

    data_affiliations_dict = data_from_ror_results(chosen_affiliations_dict)

    fill_affiliations_json(path_of_json_files, data_affiliations_dict)


if __name__ == '__main__':
    main()
