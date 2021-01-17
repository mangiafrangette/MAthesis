import json
import pandas as pd
import os
import geopandas as gpd
from pycountry_convert import country_alpha3_to_country_alpha2, country_alpha2_to_continent_code, \
    country_name_to_country_alpha3, map_country_alpha3_to_country_name
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
    count = 0
    dict_of_journals = dict()
    affiliations_list = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):
            with open(f'{path_of_files}/{filename}', 'r', encoding='utf-8') as article_file:
                article_dict = json.load(article_file)
                authors = article_dict.pop('authors')
                for author in authors:
                    if author['affiliation'] is not None:
                        for affiliation in author['affiliation']:
                            if affiliation is not None:
                                if affiliation['original_name'] is not None:
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
                                        curr_aff['iso_a3'] = country_name_to_country_alpha3(
                                            affiliation['country'])
                                    affiliations_list.append(curr_aff)
                                else:
                                    count += 1
                                    # print("aff [{None}]")
                                    # print(count)
                                    # print(author)
                                    # print(article_dict['article_title'])
                            else:
                                count += 1
                                # print("aff [None]")
                                # print(count)
                                # print(author)
                                # print(article_dict['article_title'])
                    else:
                        count += 1
                        # print("aff None")
                        # print(count)
                        # print(author)
                        # print(article_dict['article_title'])
            list_of_articles.append(article_dict)
    return pd.DataFrame(list_of_articles), pd.DataFrame(affiliations_list).set_index(
        ['journal', 'article', 'author', 'affiliation']).sort_index()


def create_topics_df(path_of_topics_csv):
    df_topics = pd.read_csv(path_of_topics_csv).set_index('doc').sort_index()
    df_topics.index = [os.path.splitext(os.path.split(idx)[1])[0] for idx in df_topics.index.tolist()]
    df_topics.index.name = 'article'
    return df_topics


def load_world_df():
    world_df = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    countries_to_modify = ['France', 'Norway', 'Somaliland']
    for country in countries_to_modify:
        world_df.loc[world_df['name'] == country, 'iso_a3'] = country_name_to_country_alpha3(country)
    # world_df = world_df[(world_df.pop_est > 0) & (world_df.name != "Antarctica")]
    return world_df.set_index('iso_a3').drop(columns=['gdp_md_est', 'geometry', 'pop_est']).rename(
        columns={'name': 'country'})


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
    missing_countries = list(set(data_df.reset_index()['iso_a3']).difference(set(world_df.index)))
    df_missing_countries = pd.DataFrame(
        [[alpha3_to_continent(iso_a3), alpha3_to_country(iso_a3)] for iso_a3 in missing_countries],
        columns=world_df.columns.values.tolist(), index=missing_countries)
    df_missing_countries.index.name = 'iso_a3'
    world_df = world_df.append(df_missing_countries)
    return world_df.merge(data_df, on='iso_a3')


def alpha3_to_country(iso_alpha3):
    return map_country_alpha3_to_country_name()[iso_alpha3]


def alpha3_to_continent(iso_alpha3):
    return {
        'EU': 'Europa',
        'NA': 'North America',
        'SA': 'South America',
        'AS': 'Asia',
        'OC': 'Oceania',
        'AF': 'Africa',
    }[country_alpha2_to_continent_code(country_alpha3_to_country_alpha2(iso_alpha3))]


def magic_function_that_does_everything_ma_non_il_caffe(path_of_json_files, path_of_topic_modeling_csv,
                                                        hypertopics_aggregation_dict,
                                                        source_tag):
    df_articles, df_affiliations = new_create_articles_dfs(path_of_json_files)
    df_affiliations['source_tag'] = source_tag
    df_topics = create_topics_df(path_of_topic_modeling_csv)

    hypertopics_list = list(hypertopics_aggregation_dict.keys())
    df_hypertopics = aggregate_topics(df_topics, hypertopics_aggregation_dict)

    productivity = data_extraction.productivity_country_per_topic(df_affiliations, df_hypertopics, normalization='both')
    productivity = productivity.reset_index().set_index('iso_a3')

    productivity_country_indipendent = data_extraction.productivity_country_per_topic(df_affiliations, df_hypertopics,
                                                                                      normalization='country_indipendent')

    world_df = load_world_df()
    wolrd_df_DataStudio = add_data_to_world_df(world_df, productivity).sort_values(by=['year'])

    topics_to_show = hypertopics_list
    bubble_df = generate_bubble_chart_column(wolrd_df_DataStudio, topics_to_show)
    bubble_df['source_tag'] = source_tag

    df_no_country_productivity = generate_bubble_chart_column(productivity_country_indipendent, topics_to_show)
    df_no_country_productivity['source_tag'] = source_tag

    return bubble_df, df_affiliations, df_no_country_productivity
    # bubble_df.to_csv(path_of_csv_for_DataStudio, index=True, header=True)
    # print("I have finished to write the csv file! :) You can upload it to DataStudio")


def main():
    # INPUTS
    path_of_json_research_papers = "../../data/research_papers/one_folder_metadata"
    path_of_json_conference_papers = "../../data/adho_conferences/one_folder_metadata"
    path_of_topic_modeling_csv_research = "../../data/research_papers/research_bow_lemmatized_16topics/doc_topics.csv"
    path_of_topic_modeling_csv_conference = "../../data/adho_conferences/conference_bow_12_lemmatized/doc_topics.csv"

    path_of_csv_for_datastudio = "complete_df_DataStudio.csv"

    inputs_dict = {
        "journal": {
            "path_of_json_papers": path_of_json_research_papers,
            "path_of_topic_modeling_csv": path_of_topic_modeling_csv_research,
            "hypertopics_aggregation": {
                "Text analysis/mining": ["1", "3", "4", "9", "11", "12"],
                "Digital heritage and multimedia": ["2", "16"],
                "Textual scholarship": ["5"],
                "Data preservation and  digital curation": ["7", "8", "14"],
                "DH discipline": ["13"],
                "NLP": ["10"],
                "Other": ["6", "15"]
            }
        },
        "conference": {
            "path_of_json_papers": path_of_json_conference_papers,
            "path_of_topic_modeling_csv": path_of_topic_modeling_csv_conference,
            "hypertopics_aggregation": {
                "Text analysis and mining": ["8"],
                "Literary text analysis": ["1", "6"],
                "Textual scholarship": ["7", "9"],
                "Data preservation and curation": ["4"],
                "DH discipline": ["2", "11"],
                "Digital history": ["3"],
                "Digital libraries": ["10"],
                "Other": ["5", "12"]
            }
        }
    }

    # OUTPUT: IT WRITES THE CSV TO UPLOAD IN DATASTUDIO
    world_dfs_list_for_datastudio = []
    aff_dfs_list_for_datastudio = []
    dfs_no_country_productivity = []
    for source_tag in inputs_dict.keys():
        world_df, df_affs, df_no_country_productivity = magic_function_that_does_everything_ma_non_il_caffe(
            inputs_dict[source_tag]['path_of_json_papers'],
            inputs_dict[source_tag]['path_of_topic_modeling_csv'],
            inputs_dict[source_tag]['hypertopics_aggregation'],
            source_tag)
        world_dfs_list_for_datastudio.append(world_df)
        aff_dfs_list_for_datastudio.append(df_affs)
        dfs_no_country_productivity.append(df_no_country_productivity)

    world_df_for_datastudio = pd.concat(world_dfs_list_for_datastudio)
    world_df_for_datastudio.to_csv("complete_df_DataStudio.csv", index=True, header=True)
    aff_df_for_datastudio = pd.concat(aff_dfs_list_for_datastudio)
    aff_df_for_datastudio.to_csv("affiliation_df_DataStudio.csv", index=True, header=True)
    no_country_productivity_datastudio = pd.concat(dfs_no_country_productivity)
    no_country_productivity_datastudio.to_csv("no_country_productivity_DataStudio.csv", index=True, header=True)


if __name__ == '__main__':
    main()
