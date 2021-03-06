# Script to query ROR and/or GRID to get detailed info of articles' affiliations
# Overall steps: 1) create a set of affiliations, 2) for every affiliation in the set query ROR and/or GRID

import json
import os
import requests
import copy
import itertools
import re



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
    if "" in affiliations_set:
        affiliations_set.remove("")

    # for affiliation in affiliations_set:
    #     if len(affiliation) <= 1:
    #         print(affiliation)
    return affiliations_set

# Create a file with original and splitted names by comma. Testing a method to only query strings that communicate the university or institution and avoid noise
def filter_affiliation_set(affiliations_set):    
    with open("../data/conference_affiliations_set.json", "w", encoding="utf-8") as f:
        affiliations_to_query = []
        words_to_check = ["university", "universidade", "università", "universitat", "universidad", "universität", "université", "universiteit", "academy", "institute", "institut", "instituut", "college", "center", "centre"]
        for item in affiliations_set:
            splitted_affiliations = re.split(r'[,|;|:|(|)]', item.lower())
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

        json.dump(affiliations_to_query, f, ensure_ascii=False)
    return affiliations_to_query


# The output of this function is a dictionary with this structure:
# { <affiliation of the set> : <list of dictionaries containing the result of the ror query>, ... }
def ror_queries(affiliations_to_query, file_path):
    queries_results = []
    query_beginning = "https://api.ror.org/organizations?affiliation="
    for index, item in enumerate(affiliations_to_query):
        #print(item["query"])
        query = query_beginning + item["query"]
        response = requests.get(query, verify=False, timeout=10)
        response_json = response.json()
        #print(index, "  ", f'{item["query"]}')
        #print(response)
        if response_json['number_of_results'] == 0:
            queries_results.append({
                "query": item["query"],
                "original_name": item["original_name"],
                "response": None
            })
            print("errorinooo")
        else:
            queries_results.append({
                "query": item["query"],
                "original_name": item["original_name"],
                "response": response_json['items']
            })
            print(query)
        # print()
        # if index == 5:
        #     write_json("../data/json_files/ror_queries.json", queries_affiliations_dict)
        #     return None
    return queries_results


# Comment the call of this function in main() if queries have NOT been already saved
def load_ror_queries(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Chose only the first ror result for every affiliation (i.e. with the highest score, descending order by score value
# is automatically provided by ror queries). The output is a dictionary with the same structure of the input.
def chose_single_result(queries_results):
    chosen_affiliations = []
    for affiliation_dict in queries_results:       
        if affiliation_dict["response"] == None :
            chosen_affiliations.append(affiliation_dict)
        elif len(affiliation_dict["response"]) > 0:
            for result in affiliation_dict["response"]:
                if not any(aff['original_name'] == affiliation_dict['original_name'] for aff in chosen_affiliations):
                    if result['score'] >= 0.9 and (result['matching_type'] == "PHRASE" or result['matching_type'] == "COMMON TERMS"):                        
                        affiliation_dict["response"] = result
                        chosen_affiliations.append(affiliation_dict)
                    else: 
                        affiliation_dict["response"] = None
                        chosen_affiliations.append(affiliation_dict)

    return chosen_affiliations

# Extract useful data from ror results.
# The dictionary in input MUST contain only ONE ror result for every affiliation.
def data_from_ror_results(chosen_results):
    def_affiliations = []
    for aff in chosen_results:
        if aff["response"] == None:
            aff = {
                    'original_name': aff["original_name"],
                    'normalized_name': None,
                    'country': None,
                    'identifiers': {
                        'ror': None,
                        'GRID': None
                    }                    
                } 
            def_affiliations.append(aff)
        else:
            aff = {
                    'original_name': aff["original_name"],
                    'normalized_name': aff["response"]['organization']['name'],
                    'country': aff["response"]['organization']['country']['country_name'],'identifiers': {
                        'ror': aff["response"]['organization']['id'],
                        'GRID': aff["response"]['organization']['external_ids']['GRID']['preferred']
                    }  
                } 
            def_affiliations.append(aff) 
    
    return def_affiliations


""" # NEED TO STUDY https://www.dimensions.ai/dimensions-apis/
# useful links:
def add_grid_data(data_affiliations_dict):
    added_data_affiliations_dict = {} """


# Create COPIES of journals' json files with filled affiliations.
def fill_affiliations_json(path_of_files, path_of_new_files, data_affiliations_dict):
    folder = os.fsencode(path_of_files)
    affiliations_set = set()
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):  # whatever file types you're using...
            with open(f"{path_of_files}/{filename}", "r", encoding="utf-8") as fd:
                filled_journal_dict = json.load(fd)
                for article in filled_journal_dict:
                    if article['authors'] is not None:
                        for author in article['authors']:
                            if isinstance(author, dict):
                                if 'affiliation' in author.keys():
                                    if author['affiliation'] is None:
                                        author['affiliation'] = [{
                                                "original_name": None,
                                                "normalized_name": None,
                                                "country": None,
                                                "identifiers": {
                                                    "ror": None,
                                                    "GRID": None
                                                }                    
                                            }]
                                    elif author['affiliation'] is not None:
                                            list_of_affiliations = []
                                            
                                            for affiliation, result in itertools.product(author['affiliation'], data_affiliations_dict):
                                                if affiliation == result["original_name"]:
                                                    #print(affiliation)
                                                    #print(result["original_name"])
                                                    list_of_affiliations.append(result)
                                            author['affiliation'] = list_of_affiliations
                                    

                filename_without_extension = filename.split('.')[0]
                new_filename = f'{filename_without_extension}_filled_aff.json'
                with open(f'{path_of_new_files}/{new_filename}', "w", encoding="utf-8") as f:
                    json.dump(filled_journal_dict, f, ensure_ascii=False)
def main():
    path_of_json_files = "../data/adho_conferences/no_country_dataset"
    path_of_new_files = "../data/adho_conferences/complete_dataset"
    ror_queries_file_path = "../data/conference_ror_queries.json"

    # Generate the set of the affiliation in the corpus of journals
    affiliations_set = create_affiliations_set(path_of_json_files)

    filter_affiliation_set(affiliations_set)

    # Comment the following lines if ror queries have already been saved and load them with the next lines
    queries_results = ror_queries(filter_affiliation_set(affiliations_set), ror_queries_file_path)
    with open(ror_queries_file_path, "w", encoding="utf-8") as file:
        json.dump(queries_results, file, ensure_ascii=False)

    # Comment the following lines if ror queries have NOT already been saved and save them with the previous lines
    
    """ with open(ror_queries_file_path, "r", encoding="utf-8") as file:
        queries_results = json.load(file) """

    chosen_results = chose_single_result(queries_results)
    with open("../data/conference_ror_single_result.json", "w", encoding="utf-8") as file:
        json.dump(chosen_results, file, ensure_ascii=False)

    data_affiliations_dict = data_from_ror_results(chosen_results)

    fill_affiliations_json(path_of_json_files, path_of_new_files, data_affiliations_dict)

if __name__ == '__main__':
    main()
