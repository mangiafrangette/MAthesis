import json
import os

# this function finds the dates that are incomplete and fills them with 01-01 

def fill_incomplete_dates(folder_path):

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
                if article['date'] is not None:
                    """ if len(article["date"]) < 5:
                        article['date']= f'{article["date"]}-01-01' """
                    if len(article["date"]) < 8:
                        article['date']= f'{article["date"]}-01'
                        
        with open(f'{folder_path}/{file_path}', "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False)



folder_path = "../data/research_papers/complete_dataset"

#fill_incomplete_dates(folder_path)