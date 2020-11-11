import json
from basic_operations import *

# This function was used to join strings that were 

def join_strings(file_path):
    articles = json_load(file_path)
    for article in articles:
        article["abstract"] = "CIAO"
    json_dump(file_path, articles)

file_path = "../data/json_files/scraped_metadata/DSH_final_data.json"         
# join_strings(file_path)