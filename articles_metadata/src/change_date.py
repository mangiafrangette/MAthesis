import json
import os
import re

path = "../data/json_files/my_schema"
months_dict = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}

# 2011-06-29T16:36:57Z [done]
""" 
files_list = [
    "ms_CF_Humanist_Studies_&_the_Digital_Age.json",
    "ms_CF_Digital_Studies__Le_champ_numérique.json",
    "ms_CF_Journal_of_the_Text_Encoding_Initiative.json",
    "ms_CF_Umanistica_Digitale.json",
    "ms_Digital_Medievalist.json",
    "ms_Digital_Philology_A_Journal_of_Medieval_Cultures.json",
    "ms_Digital_Studies__Le_champ_numérique.json",
    "ms_Digitális_Bölcsészet__Digital_Humanities.json",
    "ms_DSH.json",
    "ms_Frontiers_in_Digital_Humanities.json",
    "ms_Humanist_Studies_&_the_Digital_Age.json",
    "ms_International_Journal_for_Digital_Art_History.json",
    "ms_International_Journal_of_Digital_Humanities.json",
    "ms_JOCCH.json",
    "ms_Journal_of_Cultural_Analytics.json",
    "ms_Journal_of_the_Japanese_Association_for_Digital_Humanities.json",
    "ms_Journal_of_the_Text_Encoding_Initiative.json",
    "ms_Umanistica_Digitale.json"
] 

for file in files_list:
    with open(f'{path}/{file}', "r", encoding="utf-8") as f:
        json_file = json.load(f)
        for article in json_file:
            if article["date"] is not None:
                article["date"] = re.findall("^.*(?=T)", article["date"])[0]
    with open(f'{path}/{file}', "w", encoding="utf-8") as fd:
        json.dump(json_file, fd)
"""
    
# 2009 fine?
#files_list = [
# "ms_Computers_and_the_Humanities.json"
#]

# September 2003 [done]
""" files_list = [
 "ms_Computers_in_the_Humanities_Working_Papers.json"
]

for file in files_list:
    with open(f'{path}/{file}', "r", encoding="utf-8") as f:
        json_file = json.load(f)
        for article in json_file:
            if article["date"] is not None and re.search("[a-zA-Z]", article["date"]):
                month = article["date"].split(" ")[0]
                for key, value in months_dict.items():
                    if month == key:
                        month = value
                year = article["date"].split(" ")[1]
                article["date"] = f'{year}-{month}'
            else:
                article["date"] = f'{article["date"]}AAA'
    with open(f'{path}/{file}', "w", encoding="utf-8") as fd:
        json.dump(json_file, fd) """

# 19 June 2020 [done]
""" files_list = [
 "ms_Digital_Humanities_Quarterly.json"]
for file in files_list:
    with open(f'{path}/{file}', "r", encoding="utf-8") as f:
        json_file = json.load(f)
        for article in json_file:
            if article["date"] is not None and re.search("[a-zA-Z]", article["date"]):
                day = article["date"].split(" ")[0]
                month = article["date"].split(" ")[1]
                for key, value in months_dict.items():
                    if month == key:
                        month = value
                year = article["date"].split(" ")[2]
                article["date"] = f'{year}-{month}-{day}'
            else:
                article["date"] = f'{article["date"]}AAA'
    with open(f'{path}/{file}', "w", encoding="utf-8") as fd:
        json.dump(json_file, fd) """

# 17.06.2009 [done]
""" files_list = [
 "ms_Jahrbuch_für_Computerphilologie.json",
 "ms_Zeitschrift_für_digitale_Geisteswissenschaften.json"
]
for file in files_list:
    with open(f'{path}/{file}', "r", encoding="utf-8") as f:
        json_file = json.load(f)
        for article in json_file:
            if article["date"] is not None and re.search("[a-zA-Z]", article["date"]) is None:
                day = article["date"].split(".")[0]
                month = article["date"].split(".")[1]
                year = article["date"].split(".")[2]
                article["date"] = f'{year}-{month}-{day}'
    with open(f'{path}/{file}', "w", encoding="utf-8") as fd:
        json.dump(json_file, fd) """


# 2013/11/21 [done]
""" files_list = [
 "ms_Journal_of_Data_Mining_and_Digital_Humanities.json",
 "ms_Journal_of_Digital_Archives_and_Digital_Humanities.json"
]


for file in files_list:
    with open(f'{path}/{file}', "r", encoding="utf-8") as f:
        json_file = json.load(f)
        for article in json_file:
            if article["date"] is not None:
                article["date"] = article["date"].replace("/", "-")
    with open(f'{path}/{file}', "w", encoding="utf-8") as fd:
        json.dump(json_file, fd) """
        