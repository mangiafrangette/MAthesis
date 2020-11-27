import json
import os

def journals_per_year(folder_path):
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
        "num_of_journals": int,
        "list_of_journals": list(),
        "num_of_articles": int, 
        "list_of_articles": list(),
        "articles_journals_ratio": int
    }
        final_dict["year"] = year
        final_list.append(final_dict)   

    for file_path in filenames:
        with open(f'{folder_path}/{file_path}', "r", encoding="utf-8") as file:
            article = json.load(file)
            for year_dict in final_list:
                if article["date"][0:4] == year_dict["year"]:
                    for key, value in year_dict.items():
                        if key == "list_of_journals":
                            value = value.append(article["journal_title"])
                        if key == "list_of_articles":
                            value = value.append(article["article_title"])

# take away duplicates of journals
    for year_dict in final_list:
        new_value = list()
        for li in year_dict["list_of_journals"]:
            if li not in new_value:
                new_value.append(li)
        year_dict["list_of_journals"] = new_value

        # create metrics
        year_dict["num_of_articles"] = len(year_dict["list_of_articles"])
        year_dict["num_of_journals"] = len(year_dict["list_of_journals"])
        year_dict["articles_journals_ratio"] = len(year_dict["list_of_articles"]) / len(year_dict["list_of_journals"])

        if year_dict["articles_journals_ratio"] < 15 or year_dict["articles_journals_ratio"] > 20:
            print(f'Check year {year_dict["year"]}')
#print(list_of_journals)
    

    # write the dict to a file
    with open("../data/journals_per_year.json", "w", encoding="utf-8") as fd:
        json.dump(final_list, fd, ensure_ascii=False) 
    
journals_per_year("../data/research_papers/one_folder_metadata")
