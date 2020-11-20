import json
import os

# Function to check for double articles in a specific file (from a list). Rewrites the file without duplicates.

def search_doubles(files_list):
    for file in files_list:
        with open(file, "r", encoding="utf-8") as f:
            json_file = json.load(f)
            output_list = list()
            id_set = set()
            for article in json_file:
                if article["identifier"]["string_id"] not in id_set:
                    id_set.add(article["identifier"]["string_id"])
                    output_list.append(article)
        with open(file, "w", encoding="utf-8") as fd:
            json.dump(output_list, fd)

files_list = [
    "../data/json_files/my_schema/ms_Digital_Medievalist.json",
]

# search_doubles(files_list)



#The following function checks if there is more than one affiliation in the same element. does not modify anything, returns the specific place where the double affiliation might be so that one can check it manually.

# list of files to check
path = '../data/json_files/no_country_dataset'
folder = os.fsencode(path)
filenames = []
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith('.json'): # whatever file types you're using...
        filenames.append(filename)

def too_many_aff(path, list_of_files):
    with open(f'../data/affiliations_to_separate.txt', "w", encoding="utf-8") as f:
        text = ""
        for file in list_of_files:
            with open(f"{path}/{file}", "r", encoding="utf-8") as fd: 
                parsed = json.load(fd)
                
                for article in parsed:
                    for author in article["authors"]:
                        
                        if author["affiliation"] is not None:
                            #print(author)
                            #print(author["affiliation"])
                            
                            for affiliation in author["affiliation"]:
                                
                                if affiliation is not None:
                
                                    if affiliation.lower().count("university") > 1:
                                        text += f'{affiliation}\n\n\n'
        f.write(text)

too_many_aff(path, filenames)
                

