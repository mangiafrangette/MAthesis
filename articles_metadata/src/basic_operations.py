import os
import json

# In this file are saved some functions to open, read or write different kinds of files

def json_load(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    

def json_dump(file_path, json_dict):
    with open(file_path, "w", encoding="utf-8") as fd:
        json.dump(json_dict, fd)

def paths_from_directory(dir_path, extension):
    folder = os.fsencode(dir_path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(extension): # whatever file types you're using...
            filenames.append(filename)
    return filenames
