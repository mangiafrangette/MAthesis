import json
import os


# use this file to rewrite json files without unicode characters
def rencode(folder_path):
    # define list of files from a folder
    folder = os.fsencode(folder_path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'): # whatever file types you're using...
            filenames.append(filename)
    
    # read the files
    for file_path in filenames:
        with open(f'{folder_path}/{file_path}', "r", encoding="utf-8") as f:
                loaded = json.load(f)
                with open(f'{folder_path}/{file_path}', "w", encoding="utf-8") as fd:
                    json.dump(loaded, fd, ensure_ascii=False)

# call function
folder_path = "../data/adho_conferences/complete_dataset"
rencode(folder_path)