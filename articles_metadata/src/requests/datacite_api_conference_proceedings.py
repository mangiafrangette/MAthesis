import requests 
import json
# eventually  add this: from requests.auth import HTTPBasicAuth
# eventually add this to the requests.get argument after url: auth=HTTPBasicAuth('user', 'pass')

def get_datacite_metadata(file_name):
    # open the json that contains the full list of dois of which we need metadata
    with open(file_name, "r", encoding="utf-8") as journals_articles:
        json_data = json.load(journals_articles)
        # we access one by one the json objects that are divided by journals. within the journal, we access the values for research articles 
    for object in json_data:
        id_list_research = object["conference_proceedings"]
        # Define the file name for the metadata json final file
        new_file_name = (f'CF_{object["journal_title"]}_datacite_metadata.json').replace(" ", "_").replace("/", "").replace(":", "")
        with open(f'../data/json_files/datacite_api/{new_file_name}', "a", encoding="utf-8") as fd:
                fd.write("[")
                # Make api request to datacite for each of the dois present in the list
                for index, id in enumerate(id_list_research):
                    url = f'https://api.datacite.org/works/{id}'
                    # the following line makes the request to crossref  
                    r = requests.get(url)
                    datacite_dict = r.json()
                    json.dump(datacite_dict, fd) 
                    if index<len(id_list_research)-1:
                        fd.write(",")                                   
                fd.write("]")         

get_datacite_metadata("../data/json_files/full_list_of_ids.json")

""" url = "https://api.test.datacite.org/dois/10.5438/0012"
# payload = {'some': 'data'}
r = requests.get(url)
r.json()

with open("datacite-api.json", "wb") as fd:
  for chunk in r.iter_content():
    fd.write(chunk)  """