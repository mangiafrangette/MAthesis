import json
import os

def create_abstract_txt(folder_path, folder_final_path):
    # these variables are necessary for files that do not have a doi
    
    counter = 0

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
                if article["abstract"] is not None:
                    if article["identifier"]["string_id"] is not None:
                        
                        single_file_name = f'{article["identifier"]["string_id"].replace("/", "_")}'
                        if len(article['date']) > 4:
                            article['date']= article["date"][0:4]
                    else:
                        counter += 1
                        single_file_name = f'no_id_{counter}'
                        if len(article['date']) > 4:
                            article['date']= article["date"][0:4]

                    with open(f'{folder_final_path}/{single_file_name}.json', 'w', encoding='utf-8') as g:
                        #print(article["identifier"]["string_id"])
                        json.dump(article, g, ensure_ascii=False)

folder_path = "../data/adho_conferences/complete_dataset"
folder_final_path = "../data/adho_conferences/one_folder_metadata"

create_abstract_txt(folder_path, folder_final_path)