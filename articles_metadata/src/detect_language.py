from langdetect import detect
import json
import os

def detect_lang(folder_path):


    # define list of files from a folder
    folder = os.fsencode(folder_path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'): # whatever file types you're using...
            filenames.append(filename)
    
    # read the files
    for file_path in filenames:
        with open(f'{folder_path}/{file_path}', "r", encoding="utf-8") as file:
            articles = json.load(file) 

            for article in articles:
                #print(article["article_title"])
                if article["abstract"] is not None and len(article["abstract"]) < 10:
                    print("CHECK")
                    print(article["abstract"]) 
                
                elif article["abstract"] is not None and detect(article["abstract"]) != "en":
                    print(article["article_title"])

folder_path = "../data/research_papers/complete_dataset"


detect_lang(folder_path)
