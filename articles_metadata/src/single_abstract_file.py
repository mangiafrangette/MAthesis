import json
import os

def create_abstract_txt(folder_path):
    # these variables are necessary for files that do not have a doi
    
    counter = 0
    no_id_name = f'no_id_{counter}'

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
        #each abstract is a document
            for article in articles:
                if article["identifier"]["string_id"] is not None:
                    with open(f'../data/test_DSH_abstracts/{article["identifier"]["string_id"]}.txt', 'w', encoding='utf-8') as g:
                        g.write(article["abstract"])
                else:
                    counter += 1
                    with open(f'../data/test_DSH_abstracts/{no_id_name}.txt', 'w', encoding='utf-8') as g:
                        g.write(article["abstract"])


folder_path = "../data/research_papers/complete_dataset"

create_abstract_txt(folder_path)