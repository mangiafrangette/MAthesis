import json
import os

# modify and then run to change values of the final json schema with other values from another json (in my case scraped data) if there is a control variable (in this case a string_id)
def change_json_values(ms_json, other_json): 
    with open(ms_json, "r", encoding="utf-8") as f:
        my_schema_json = json.load(f)
        with open(other_json, "r", encoding="utf-8") as fd:
            scrapy_file = json.load(fd)
            for article1 in my_schema_json:
                for article2 in scrapy_file:
                    if article1["identifier"]["string_id"] == article2["string_id"][0]:
                        if article2["abstract"] is not None:
                            article1["abstract"] = article2["abstract"]
                        if article2["authors"] is not None:    
                            article1["authors"] = article2["authors"]

                        
    with open(ms_json, "w", encoding="utf-8") as g:
        json.dump(my_schema_json, g)



# this was used to add affiliations
def add_scraped_affiliations(my_schema_file, scrapy_affiliations):
    with open(my_schema_file, "r", encoding="utf-8") as f:
        articles = json.load(f)
    with open(scrapy_affiliations, "r", encoding="utf-8") as g: 
        scrapy_affiliations = json.load(g)
        for article in articles:
            for affiliation in scrapy_affiliations:
                if article["identifier"]["string_id"] == affiliation["string_id"]:
                    for author1 in article["authors"]:
                        for author2 in affiliation["authors"]:
                            if author1["given"] in author2["given"]: 
                                author1["affiliation"] = author2["affiliation"]
                                with open(my_schema_file, "w", encoding="utf-8") as fd:
                                    json.dump(articles, fd)

# this was used to add abstracts
def add_scraped_abstracts(my_schema_file, scrapy_abstracts):
    with open(my_schema_file, "r", encoding="utf-8") as f:
        articles = json.load(f)
    with open(scrapy_abstracts, "r", encoding="utf-8") as g: 
        scrapy_abstracts = json.load(g)
        for article in articles:
            for abstract in scrapy_abstracts:
                if article["identifier"]["string_id"] == abstract["string_id"]:
                    article["abstract"] = abstract["abstract"]
                    with open(my_schema_file, "w", encoding="utf-8") as fd:
                        json.dump(articles, fd)

# The function can be run with iteration over a list of files as input adding:
# 
# for file in files_list:
#   files_list = ["../data/json_files/my_schema/ms_Zeitschrift_für_digitale_Geisteswissenschaften.json",]
# 
# Or you can have just one file per time:
# 
# ms_file = "../data/json_files/my_schema/ms_DSH.json"
# scraped_file = "../data/json_files/DSH_final_data.json"
# 
# Then you can finally run the functions
#
# change_json_values(ms_file, scrapy_file)
# add_scraped_affiliations(ms_file, scraped_file)
# # add_scraped_abstracts(ms_file, scraped_file)