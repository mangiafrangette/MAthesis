import json
import os

#The following function checks if there is more than one affiliation in the same element. does not modify anything, returns the specific place where the double affiliation might be so that one can check it manually.

# necessary for following function, imports the dict
def import_json_dict(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# create affiliations set
def create_affiliations_set(path_of_files):
    folder = os.fsencode(path_of_files)
    affiliations_set = set()
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):  # whatever file types you're using...
            journal_dict = import_json_dict(f"{path_of_files}/{filename}")
            for article in journal_dict:
                if article['authors'] is not None:
                    for author in article['authors']:
                        if isinstance(author, dict):
                            if 'affiliation' in author.keys():
                                if author['affiliation'] is not None:
                                    if len(author['affiliation']) > 0 and isinstance(author['affiliation'][0], str):
                                        affiliations_set.update(author['affiliation'])
    return affiliations_set


def too_many_aff(affiliations_set):
    with open(f'../data/affiliations_to_separate.txt', "w", encoding="utf-8") as f:
        text = ""
        list = []
        for affiliation in affiliations_set:    
            # ... series of heuristics to comment or uncomment 
            #        
            # words_to_check = ["university", "universidade", "università", "universitat", "universidad", "universität", "université", "universiteit", "academy", "institute", "institut", "instituut", "college", "center", "centre", " and "]   
            # for word in words_to_check:
            #   if affiliation.lower().count(word) > 1:
            #        text += f'{affiliation}\n\n\n'
            # ... or another heuristic:
            """ countries_to_check = ["Afghanistan","Albania","Algeria","Andorra","Angola","Antigua & Deps","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bosnia Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Central African Rep","Chad","Chile","China","Colombia","Comoros","Congo","Congo {Democratic Rep}","Costa Rica","Croatia","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","East Timor","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Fiji","Finland","France","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Ivory Coast","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Korea North","Korea South","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar","Romania","Russian Federation","Rwanda","St Kitts & Nevis","St Lucia","Saint Vincent & the Grenadines","Samoa","San Marino","Sao Tome & Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Sudan","Spain","Sri Lanka","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Togo","Tonga","Trinidad & Tobago","Tunisia","Turkey","Turkmenistan","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]
            for country1 in countries_to_check:
                if country1.lower() in affiliation.lower():
                    for country2 in countries_to_check:
                        if (country1 != country2) and country2.lower() in affiliation.lower():
                            text += f'{affiliation}\n\n\n' """
            symbols_to_check = ["  ", ";", "-", "/"]
            for symbol in symbols_to_check:
                if symbol in affiliation:
                    list.append(affiliation)
        f.write(str(set(list)))


# main

def main():
    path = '../data/json_files/no_country_dataset'   
    aff_set_return = create_affiliations_set(path)
    too_many_aff(aff_set_return)

if __name__ == '__main__':
    main()








""" # list of files from a folder
path = '../data/json_files/no_country_dataset'
folder = os.fsencode(path)
filenames = []
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith('.json'): # whatever file types you're using...
        filenames.append(filename) """