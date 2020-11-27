import json
import os

# found an issue in dates extracted from crossref

def fix_crossref_dates(crossref_folder, ms_folder):
    # define list of files from a folder
    folder = os.fsencode(crossref_folder)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'): # whatever file types you're using...
            filenames.append(filename)

    # define list of files from a folder
    folder2 = os.fsencode(ms_folder)
    filenames2 = []
    for file2 in os.listdir(folder2):
        filename2 = os.fsdecode(file2)
        if filename2.endswith('.json'): # whatever file types you're using...
            filenames2.append(filename2)

    
    # read the files
    for file_path in filenames:
        with open(f'{crossref_folder}/{file_path}', "r", encoding="utf-8") as file:
            crossref = json.load(file) 
            for result in crossref:
                if result is not None:
                    #print(result)
                    date = ""
                    #print(result["title"])
                    if "published-online" in result.keys():
                        for index, num in enumerate(result["published-online"]["date-parts"][0]):
                            if len(result["published-online"]["date-parts"][0]) <= 1:
                                date = num
                            elif index < 2:
                                date += f'{num}-'
                            else:
                                date += f'{num}'
                    
                    elif "published-print" in result.keys():
                        for index, num in enumerate(result["published-print"]["date-parts"][0]):
                            if len(result["published-print"]["date-parts"][0]) <= 1:
                                date = num
                            elif index < 2:
                                date += f'{num}-'
                            else:
                                date += f'{num}'
                    #print(date)
                    for file_path2 in filenames2:
                        with open(f'{ms_folder}/{file_path2}', "r", encoding="utf-8") as file2:
                            ms = json.load(file2)
                            for article in ms:
                                if article["identifier"]["string_id"] == result["DOI"]:
                                    print(article["date"])
                                    article["date"] = date
                                    print(article["date"])
                        with open(f'{crossref_folder}/{file_path}', "w", encoding="utf-8") as file:
                            crossref = json.load(file)
    

fix_crossref_dates("../data/unused_files/crossref_api", "../data/research_papers/no_country_dataset")