from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
import os
import time
import geopandas as gpd
import matplotlib.pyplot as plt
import pycountry_convert
import math


# Creates two Panda DataFrames of all articles; the first without the authors' data, the second only with authors' data
def create_articles_dfs(path_of_files):
    list_of_articles = []
    folder = os.fsencode(path_of_files)
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):
            with open(f"{path_of_files}/{filename}", "r", encoding="utf-8") as article_file:
                list_of_articles.append(json.load(article_file))
    return pd.DataFrame(list_of_articles)


# Creates two Panda DataFrames of all articles; the first without the authors' data, the second only with authors' data
def new_create_articles_dfs(path_of_files):
    list_of_articles = []
    folder = os.fsencode(path_of_files)
    dict_of_journals = dict()
    affiliations_list = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):
            with open(f'{path_of_files}/{filename}', 'r', encoding='utf-8') as article_file:
                article_dict = json.load(article_file)
                authors = article_dict.pop('authors')
                for author in authors:
                    # curr_author_affs = []
                    for affiliation in author['affiliation']:
                        curr_aff = {'journal': article_dict['journal_title'],
                                    'article': os.path.splitext(filename)[0],
                                    'author': f"{author['given']} {author['family']}",
                                    'affiliation': affiliation['original_name'],
                                    'original_name': affiliation['original_name'],
                                    'country': None,
                                    'iso_a3': None
                                    }
                        if affiliation['normalized_name'] is not None:
                            curr_aff['affiliation'] = affiliation['normalized_name']
                            curr_aff['country'] = affiliation['country']
                            curr_aff['iso_a3'] = pycountry_convert.country_name_to_country_alpha3(affiliation['country'])
                        affiliations_list.append(curr_aff)
                list_of_articles.append(article_dict)
    return pd.DataFrame(list_of_articles), pd.DataFrame(affiliations_list).set_index(['journal', 'article', 'author', 'affiliation']).sort_index()


def create_topics_df(path_of_topics_csv):
    df_topics = pd.read_csv(path_of_topics_csv).set_index('doc').sort_index()
    df_topics.index = [os.path.splitext(os.path.split(idx)[1])[0] for idx in df_topics.index.tolist()]
    df_topics.index.name = 'article'
    return df_topics


def load_world_df():
    world_df = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world_df = world_df[(world_df.pop_est > 0) & (world_df.name != "Antarctica")]
    return world_df.set_index('iso_a3')

def find_correlation(df_topics):

    """ selectedrows = df_topics[(df_topics[topic_n] >= threshold) & (df_topics[topic_m] >= threshold)]
    return selectedrows[[topic_n, topic_m]] """
    correlation_matrix = df_topics.corr(method ='kendall')
    # select only relevant correlations
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df_topics.columns
    for i in range(0, df_topics.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))

    n = 5
    au_corr = correlation_matrix.abs().unstack()
    labels_to_drop = pairs_to_drop
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    print(correlation_matrix["9"])

    return au_corr[0:n]


# # aggiunge una colonna ad articles_df per indicare i countries di ogni articolo
# def associate_countries(articles_df):
#     list_of_countries = list()
#     for authors in articles_df["authors"].values:
#         curr_article_countries = set()
#         for author in authors:
#             for affiliation in author['affiliation']:
#                 if affiliation['country'] is not None:
#                     curr_article_countries.add(pycountry_convert.country_name_to_country_alpha3(affiliation['country']))
#         if len(curr_article_countries) == 0:
#             list_of_countries.append(None)
#         else:
#             list_of_countries.append(curr_article_countries)
#     articles_df["countries"] = list_of_countries
#     return articles_df


def add_data_to_world_df(world_df, data_df):
    return world_df.merge(data_df, on='iso_a3')


def random_tests():
    path_of_files = "../../data/research_papers/one_folder_metadata"
    path_of_topics_csv = "doc_topics.csv"

    #df_art, df_aff = new_create_articles_dfs(path_of_files)
    # print(df_art)
    # print(df_aff)
    df_topics = create_topics_df(path_of_topics_csv)
    # call function find correlation after dataframe is loaded from topicsXdocuments csv

    #print(df_topics)
    #print("\n\n")
    print(find_correlation(df_topics))
    #print(find_correlation(df_topics, "10", "12", 0.3))

    # are topics correlated? 
    
    #print(df_aff)




if __name__ == '__main__':
    random_tests()
