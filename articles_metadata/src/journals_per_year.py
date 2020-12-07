import json
import os

def journals_per_year(folder_path, destination_path):
    # define list of files from a folder
    folder = os.fsencode(folder_path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'): # whatever file types you're using...
            filenames.append(filename)
    
    final_list = list()
    years_set = set()
    # read the files
    for file_path in filenames:
        with open(f'{folder_path}/{file_path}', "r", encoding="utf-8") as file:
            article = json.load(file) 
            
            current_article_date = article["date"][0:4]
            years_set.add(current_article_date)
    
    for year in years_set:
        final_dict = {
        "year": "",
        "num_of_journals": 0,
        "num_of_articles": 0, 
        "articles_journals_ratio": 0,
        "dict_of_journals": dict()        
    }
        final_dict["year"] = year
        final_list.append(final_dict)   

    for file_path in filenames:
        with open(f'{folder_path}/{file_path}', "r", encoding="utf-8") as file:
            article = json.load(file)
            for year_dict in final_list:
                if article["date"][0:4] == year_dict["year"]:
                    if article["journal_title"] not in year_dict["dict_of_journals"].keys():
                        year_dict["dict_of_journals"][article["journal_title"]] = 1
                        
                    else:
                        year_dict["dict_of_journals"][article["journal_title"]] += 1
                    
                    #write metrics
                    year_dict["num_of_articles"] +=1
                    year_dict["num_of_journals"] = len(year_dict["dict_of_journals"].keys())
                    year_dict["articles_journals_ratio"] = year_dict["num_of_articles"] / year_dict["num_of_journals"]    

    # write the dict to a file
    with open(destination_path, "w", encoding="utf-8") as fd:
        json.dump(final_list, fd, ensure_ascii=False) 
    
destination_path = "../data/journals_per_year.json"

#journals_per_year("../data/research_papers/one_folder_metadata", destination_path)

def create_csv(csv_path):
    with open(csv_path, "r", encoding="utf-8") as file:
        csv = json.load(file)
        first_line = ""
        txt = ""
        for year_dict in csv:
            second_line = f'{year_dict["year"]}'
            for journal, num in year_dict["dict_of_journals"].items():
                first_line += f'{journal}'
                second_line += f'{num}'
                txt += first_line + second_line
        print()

    # write the dict to a file
    #with open("../data/journals_per_year.csv", "w", encoding="utf-8") as fd:
    #    json.dump(final_list, fd, ensure_ascii=False) 
    
create_csv(destination_path)