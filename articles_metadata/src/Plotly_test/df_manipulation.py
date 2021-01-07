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
import copy
import data_extraction


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
                                    'year': article_dict['date'],
                                    'country': None,
                                    'iso_a3': None
                                    }
                        if affiliation['normalized_name'] is not None:
                            curr_aff['affiliation'] = affiliation['normalized_name']
                            curr_aff['country'] = affiliation['country']
                            curr_aff['iso_a3'] = pycountry_convert.country_name_to_country_alpha3(
                                affiliation['country'])
                        affiliations_list.append(curr_aff)
                list_of_articles.append(article_dict)
    return pd.DataFrame(list_of_articles), pd.DataFrame(affiliations_list).set_index(
        ['journal', 'article', 'author', 'affiliation']).sort_index()


def articles_dfs_DataSudio(path_of_files):
    list_of_articles = []
    folder = os.fsencode(path_of_files)
    dict_of_journals = dict()
    affiliations_list = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):
            with open(f'{path_of_files}/{filename}', 'r', encoding='utf-8') as article_file:
                article_dict = json.load(article_file)
                # print(list(article_dict.keys()))
                authors = article_dict.pop('authors')
                for author in authors:
                    # curr_author_affs = []
                    for affiliation in author['affiliation']:
                        curr_aff = {'url': article_dict['url'],
                                    'publisher': None if 'publisher' not in article_dict.keys() else article_dict[
                                        'publisher'],
                                    'journal': article_dict['journal_title'],
                                    'article_title': article_dict['article_title'],
                                    'article': os.path.splitext(filename)[0],
                                    'author': f"{author['given']} {author['family']}",
                                    'affiliation': affiliation['original_name'],
                                    'original_name': affiliation['original_name'],
                                    'year': article_dict['date'],
                                    'country': None,
                                    'iso_a3': None
                                    }
                        if affiliation['normalized_name'] is not None:
                            curr_aff['affiliation'] = affiliation['normalized_name']
                            curr_aff['country'] = affiliation['country']
                            curr_aff['iso_a3'] = pycountry_convert.country_name_to_country_alpha3(
                                affiliation['country'])
                        affiliations_list.append(curr_aff)
                list_of_articles.append(article_dict)
    return pd.DataFrame(list_of_articles), pd.DataFrame(affiliations_list).set_index(
        ['publisher', 'journal', 'article', 'author', 'affiliation']).sort_index()


def create_topics_df(path_of_topics_csv):
    df_topics = pd.read_csv(path_of_topics_csv).set_index('doc').sort_index()
    df_topics.index = [os.path.splitext(os.path.split(idx)[1])[0] for idx in df_topics.index.tolist()]
    df_topics.index.name = 'article'
    return df_topics


def load_world_df():
    world_df = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world_df = world_df[(world_df.pop_est > 0) & (world_df.name != "Antarctica")]
    return world_df.set_index('iso_a3')


# aggregation_dict = {"hypertopic 1": ["2", "3", "5"], "hypertopic 2": ["7", "8"], ... }
def aggregate_topics(df_topics, aggregation_dict):
    df_hypertopics = copy.deepcopy(df_topics)
    for hypertopic, topic_to_aggregate in aggregation_dict.items():
        df_hypertopics[hypertopic] = df_topics[topic_to_aggregate].sum(axis=1)
        df_hypertopics.drop(topic_to_aggregate, axis=1, inplace=True)
    return df_hypertopics


def generate_bubble_chart_column(world_df, topics_to_show):
    original_index_name = world_df.index.name
    world_df.reset_index(inplace=True)
    remaining_columns = list(set(world_df.columns).difference(set(topics_to_show)))
    return world_df.melt(id_vars=remaining_columns, var_name='topic', value_name='topic_productivity').set_index(
        original_index_name)


def add_data_to_world_df(world_df, data_df):
    return world_df.merge(data_df, on='iso_a3')


def magic_function_that_does_everything_ma_non_il_caffe(path_of_json_files, path_of_topic_modeling_csv,
                                                        path_of_csv_for_DataStudio, hypertopics_aggregation_dict):
    df_articles, df_affiliations = new_create_articles_dfs(path_of_json_files)
    df_topics = create_topics_df(path_of_topic_modeling_csv)

    hypertopics_list = list(hypertopics_aggregation_dict.keys())
    df_hypertopics = aggregate_topics(df_topics, hypertopics_aggregation_dict)

    productivity = data_extraction.productivity_country_per_topic(df_affiliations, df_hypertopics, normalization='both')
    productivity = productivity.reset_index().set_index('iso_a3')

    world_df = load_world_df()
    world_df = add_data_to_world_df(world_df, productivity).sort_values(by=['year'])
    wolrd_df_DataStudio = world_df.drop(columns=['gdp_md_est', 'geometry', 'pop_est']).rename(
        columns={'name': 'country'})

    topics_to_show = hypertopics_list
    bubble_df = generate_bubble_chart_column(wolrd_df_DataStudio, topics_to_show)
    bubble_df.to_csv(path_of_csv_for_DataStudio, index=True, header=True)
    print("I have finished to write the csv file! :) You can upload it to DataStudio")


def main():
    # INPUTS
    path_of_json_research_papers = "../../data/research_papers/one_folder_metadata"
    path_of_json_conference_papers = "../../ILPERCORSOCHEVUOIPORCODIO"
    path_of_topic_modeling_csv = "doc_topics.csv"
    path_of_csv_for_DataStudio_research_papers = "research_wolrd_df_DataStudio_bubble.csv"
    path_of_csv_for_DataStudio_conference_papers = "conference_wolrd_df_DataStudio_bubble.csv"
    hypertopics_aggregation_dict_research = {
        "Text analysis/mining": ["1", "3", "4", "9", "11", "12"],
        "Digital heritage and multimedia": ["2", "16"],
        "Textual scholarship": ["5"],
        "Data preservation and  digital curation": ["7", "8", "14"],
        "DH discipline": ["13"],
        "NLP": ["10"],
        "Other": ["6"],
        "Other/Hypertext": ["15"]
    }
    hypertopics_aggregation_dict_conference = {
        "Text analysis and mining": ["8"],
        "Literary text analysis": ["1", "6"],
        "Textual scholarship": ["7", "9"],
        "Data preservation and curation": ["4"],
        "DH discipline": ["2", "11"],
        "Digital history": ["3"],
        "Digital libraries": ["10"],
        "Other/Measuring": ["5"],
        "Other": ["12"]
    }

    # OUTPUT: IT WRITES THE CSV TO UPLOAD IN DATASTUDIO
    magic_function_that_does_everything_ma_non_il_caffe(path_of_json_research_papers, path_of_topic_modeling_csv,
                                                        path_of_csv_for_DataStudio_research_papers,
                                                        hypertopics_aggregation_dict_research)
    magic_function_that_does_everything_ma_non_il_caffe(path_of_json_conference_papers, path_of_topic_modeling_csv,
                                                        path_of_csv_for_DataStudio_conference_papers,
                                                        hypertopics_aggregation_dict_conference)


if __name__ == '__main__':
    main()
