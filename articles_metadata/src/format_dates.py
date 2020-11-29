import json
import os
import re

def format_dates(ms_folder):
    # define list of files from a folder
    folder2 = os.fsencode(ms_folder)
    filenames2 = []
    for file2 in os.listdir(folder2):
        filename2 = os.fsdecode(file2)
        if filename2.endswith('.json'): # whatever file types you're using...
            filenames2.append(filename2)

    for file_path2 in filenames2:
        with open(f'{ms_folder}/{file_path2}', "r", encoding="utf-8") as file2:
            ms = json.load(file2)
            
            for article in ms:

                if article["date"] is not None:
                    #print(article["date"])
                    if type(article["date"]) == int:
                         article["date"] = str(article["date"])

                    if re.match(r"20..-..-..", article["date"]):
                        #print(article["date"])
                        article["date"] = article["date"]
                        #print(article["date"])
                    elif re.match(r"20..-.-..", article["date"]):
                        #print(article["date"])
                        article["date"] = article["date"][:5] + "0" + article["date"][5:]
                        #print(article["date"])
                    elif re.match(r"20..-.-.", article["date"]):
                        #print(article["date"])
                        article["date"] = article["date"][:5] + "0" + article["date"][5:7] + "0" + article["date"][7:]
                        #print(article["date"])
                    elif re.match(r"20..-..-.", article["date"]):
                        #print(article["date"])
                        article["date"] = article["date"][:8] + "0" + article["date"][8:]
                        #print(article["date"])
                    elif re.match(r"20..-..-", article["date"]):
                        article["date"] = article["date"] + "01"
                    elif re.match(r"20..-.-", article["date"]):
                        article["date"] = article["date"][:5] + "0" + article["date"][5:7] + "01"
                    elif re.match(r"20..", article["date"]):
                        article["date"] = article["date"] + "-01-01"
                    if re.match(r"20..-..-..-01", article["date"]):
                        article["date"] = article["date"][0:9]
                print(article["date"])
                    
                if not re.match(r"20..-..-..", article["date"]):               
                    print(f'AAA {article["date"]}')

        with open(f'{ms_folder}/{file_path2}', "w", encoding="utf-8") as fd:
            json.dump(ms, fd, ensure_ascii=False)
            #print(result["DOI"])
            #print(f'{file_path2}done!')
    

format_dates("../data/research_papers/complete_dataset")