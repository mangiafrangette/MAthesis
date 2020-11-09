import os
import json
from basic_operations import *

# This file was run to get Digital Scholarship in the Humanities data through a service called proxies api. It's absolutely necessary to changhe the free trial proxy (you can use Proxy API for free for 1000 api queries but it's necessary to create your own account)

def start_request(file_path, proxy): 
    articles = json_load(file_path)
    for index, article in enumerate(articles):
        url = article["url"]
        output_file_name = f'dsh{index}.xml'
        os.system(f'curl "{proxy}{url}" -o {output_file_name}')

free_trial_proxy = "http://api.proxiesapi.com/?auth_key=b0bbd56ab84d8fb27d722c27d323a9c5_sr98766_ooPq87&url="
filename = "../data/json_files/my_schema/ms_DSH.json"
start_request(filename, free_trial_proxy)