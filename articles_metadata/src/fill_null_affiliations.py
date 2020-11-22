import json
import os

# since the threshold to fill affiliations with ror results is very high and ror is not very good, in the end i'm checking those affiliations that remained null to see if they can be associated to a ror manually. this is what this function does. specify the association in the association dict in the beginning and then run!

def fill_null_aff(folder_path):

    association_dict = {
        "Istituto di Linguistica Computazionale (ILC) - CNR": {"normalized_name": "Institute for Computational Linguistics “A. Zampolli”", "country": "Italy", "identifiers": {"ror": "https://ror.org/028g3pe33", "GRID": "grid.503055.6"}},
        "University of Maryland": {"normalized_name": "University of Maryland, College Park", "country": "United States", "identifiers": {"ror": "https://ror.org/047s2c258", "GRID": "grid.164295.d"}},
        "Department of Psychology, Hunter College of CUNY": {"normalized_name": "Hunter College", "country": "United States", "identifiers": {"ror": "https://ror.org/00g2xk477", "GRID": "grid.257167.0"}},
        "University of Maryland, College Park": {"normalized_name": "University of Maryland, College Park", "country": "United States", "identifiers": {"ror": "https://ror.org/047s2c258", "GRID": "grid.164295.d"}},
        "Ludwig Maximilian University of Munich": {"normalized_name": "Ludwig-Maximilians-Universität München", "country": "Germany", "identifiers": {"ror": "https://ror.org/05591te55", "GRID": "grid.5252.0"}},
        "Centre for Language Studies, Radboud University, Nijmegen, The Netherlands": {"normalized_name": "Radboud University Nijmegen", "country": "Netherlands", "identifiers": {"ror": "https://ror.org/016xsfp80", "GRID": "grid.5590.9"}},
        "Radboud University": {"normalized_name": "Radboud University Nijmegen", "country": "Netherlands", "identifiers": {"ror": "https://ror.org/016xsfp80", "GRID": "grid.5590.9"}},
        "Centre for Language and Speech Technology, Radboud University, Nijmegen, The Netherlands": {"normalized_name": "Radboud University Nijmegen", "country": "Netherlands", "identifiers": {"ror": "https://ror.org/016xsfp80", "GRID": "grid.5590.9"}},
        "University of Macedonia, Thessaloniki, Greece": {"normalized_name": "University of Macedonia", "country": "Greece", "identifiers": {     "ror": "https://ror.org/05fg6gr82", "GRID": "grid.10212.30"   }},
        "Signal Processing Laboratory, Tampere University of Technology, Finland": {"normalized_name": "Tampere University", "country": "Finland", "identifiers": {"ror": "https://ror.org/033003e23", "GRID": "grid.502801.e"}},
        "Istituto di Linguistica Computazionale - CNR, Pisa, Italy": {"normalized_name": "Institute for Computational Linguistics “A. Zampolli”", "country": "Italy", "identifiers": {"ror": "https://ror.org/028g3pe33", "GRID": "grid.503055.6"}},
        "ISTI-CNR, Italy": {"normalized_name": "Institute of Information Science and Technologies", "country": "Italy", "identifiers": {"ror": "https://ror.org/05kacka20", "GRID": "grid.451498.5"}},
        "Visual Computing Lab, ISTI-CNR, Pisa, Italy": {"normalized_name": "Institute of Information Science and Technologies", "country": "Italy", "identifiers": {"ror": "https://ror.org/05kacka20", "GRID": "grid.451498.5"}},
        "ISTI-CNR, Pisa, Italy": {"normalized_name": "Institute of Information Science and Technologies", "country": "Italy", "identifiers": {"ror": "https://ror.org/05kacka20", "GRID": "grid.451498.5"}},
        "Visual Computing Laboratory ISTI-CNR, Pisa, Italy": {"normalized_name": "Institute of Information Science and Technologies", "country": "Italy", "identifiers": {"ror": "https://ror.org/05kacka20", "GRID": "grid.451498.5"}},
        "Goteborg University, Sweden": {"normalized_name": "University of Gothenburg", "country": "Sweden", "identifiers": {"ror": "https://ror.org/01tm6cn81", "GRID": "grid.8761.8"}},
        "CNRS-ITEM, France": {"normalized_name": "French National Centre for Scientific Research", "country": "France", "identifiers": {"ror": "https://ror.org/02feahw73", "GRID": "grid.4444.0"}},
        "CNRS": {"normalized_name": "French National Centre for Scientific Research", "country": "France", "identifiers": {"ror": "https://ror.org/02feahw73", "GRID": "grid.4444.0"}}

    }

    # define list of files from a folder
    folder = os.fsencode(folder_path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'): # whatever file types you're using...
            filenames.append(filename)
    
    # read the files
    for file_path in filenames:
        with open(f'{folder_path}/{file_path}', "r", encoding="utf-8") as file:
            articles = json.load(file) 
            for article in articles:
                if article['authors'] is not None:
                    for author in article['authors']:
                        if isinstance(author, dict):
                            if 'affiliation' in author.keys():
                                for single_aff in author['affiliation']:
                                    
                                    if single_aff["country"] is None:
                                        
                                        if single_aff["original_name"] is not None:
                                            
                                            for original_name, ror_query in association_dict.items():
                                                
                                                if single_aff["original_name"] == original_name:

                                                    single_aff["normalized_name"] = ror_query["normalized_name"]
                                                    single_aff["country"] = ror_query["country"]
                                                    single_aff["identifiers"]["ror"] = ror_query["identifiers"]["ror"]
                                                    single_aff["identifiers"]["GRID"] = ror_query["identifiers"]["GRID"]

        with open(f'{folder_path}/{file_path}', "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False)



folder_path = "../data/research_papers/complete_dataset"

fill_null_aff(folder_path)