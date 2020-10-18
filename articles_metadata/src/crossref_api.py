from crossref.restful import Works
import json

from crossref.restful import Works
import json

def get_crossref_metadata(file_name):
    # work needs to be defined for crossref
    works = Works()
    # open the json that contains the full list of dois of which we need metadata
    with open(file_name, "r", encoding="utf-8") as journals_articles:
        json_data = json.load(journals_articles)
        # we access one by one the json objects that are divided by journals. within the journal, we access the values for research articles
        for object in json_data:
            id_list_research = object["research_articles"]
            # Define the file name for the metadata json final file
            new_file_name = (f'{object["journal_title"]}_crossref_metadata.json').replace(" ", "_").replace("/", "")
            with open(f'../data/json_files/{new_file_name}', "a", encoding="utf-8") as fd:
                fd.write("[")
                # Make api request to crossref for each of the dois present in the list
                for index, id in enumerate(id_list_research):
                    # the following line makes the request to crossref
                    record = works.doi(id)                     
                    # Write the final json with append mode
                    json.dump(record, fd)
                    if index<len(id_list_research)-1:
                        fd.write(",")
                fd.write("]")         

get_crossref_metadata("../data/full_list_of_ids.json") 

# old code
""" def get_crossref_metadata(file_name):
    works = Works()
    record = works.doi("10.3389/fdigh.2018.00019")
    print(record)

     new_file_name = file_name.replace("id_list", "metadata")

    with open(new_file_name, "w") as fd:
        json.dump(record, fd) 

get_crossref_metadata("umanistica_digitale_id_list.json") """

