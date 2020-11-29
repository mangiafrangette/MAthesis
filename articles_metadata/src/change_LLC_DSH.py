import json
import os

# found an issue with naming LLC and DSH

def change_name(ms_file):


    with open(ms_file, "r", encoding="utf-8") as file2:
        ms = json.load(file2)
        
        for article in ms:
            #print(article["date"][0:4])
            if int(article["date"][0:4]) < 2015:
                article["journal_title"] = "Literary and Linguistic Computing"
                #print(article["journal_title"])
            else:
                article["journal_title"] = "Digital Scholarship in the Humanities"
                #print(article["journal_title"])
    with open(ms_file, "w", encoding="utf-8") as fd:
        json.dump(ms, fd, ensure_ascii=False)
    
change_name("../data/research_papers/complete_dataset/ms_DSH_filled_aff.json")