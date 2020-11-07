import json

file = "../data/json_files/DSH_final_data.json"

with open(file, "r", encoding="utf-8") as f:
    articles = json.load(f)
    for article in articles:
        article["abstract"] = "".join(article["abstract"])
with open(file, "w", encoding="utf-8") as fd:
    json.dump(articles, fd)
         
