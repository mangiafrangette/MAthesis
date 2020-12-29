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
import df_manipulation


def calculate_num_of_articles_per_country(articles_df):
    articles_per_country_dict = dict()
    for index, article in articles_df.iterrows():
        if article['countries'] is not None:
            for country in article['countries']:
                if country not in articles_per_country_dict:
                    articles_per_country_dict[country] = 1
                else:
                    articles_per_country_dict[country] += 1
    return articles_per_country_dict


# mean_countries_dict in output: {'<country_code1>' : mean_abs_len1, ...}
def mean_abstract_length(articles_df):
    articles_df['abs_len'] = [len(abstract) for abstract in articles_df["abstract"].values]
    articles_per_country_dict = calculate_num_of_articles_per_country(articles_df)
    mean_countries_dict = dict()
    for index, article in articles_df.iterrows():
        if article['countries'] is not None:
            for country in article['countries']:
                if country not in mean_countries_dict:
                    mean_countries_dict[country] = articles_df['abs_len'][index]*1.0/articles_per_country_dict[country]
                else:
                    mean_countries_dict[country] += articles_df['abs_len'][index]*1.0/articles_per_country_dict[country]
    return pd.DataFrame({'iso_a3': mean_countries_dict.keys(), 'mean number of character per abstract': mean_countries_dict.values()}).set_index('iso_a3')


# def productivity_country_per_topic(df_affiliations, df_topics, normalization="itra_country"):
#     # precomputation:
#     num_affs_series = df_affiliations.reset_index().groupby('article').size()#['affiliation']
#     df_affs_topics = pd.DataFrame({'article': num_affs_series.index, 'num affs': num_affs_series.values}).set_index('article').merge(df_topics, on='article').merge(df_affiliations['year'], on='article')
#
#     df_articles_topics_distributed = df_affs_topics[df_affs_topics.columns.difference(['num affs', 'year'])].div(df_affs_topics.iloc[:, 0], axis='rows')
#     df_affs_topics_distributed = df_affiliations.reset_index().set_index('article').merge(df_articles_topics_distributed, on='article')
#     df_country_topics_absolut_productivity = df_affs_topics_distributed.groupby(['iso_a3', 'year']).sum()
#     if normalization == "intra_country":
#         df_country_topics_relative_productivity = df_country_topics_absolut_productivity.div(
#             df_country_topics_absolut_productivity.sum(axis='columns'), axis='rows')
#     elif normalization == "global":
#         df_country_topics_relative_productivity = df_country_topics_absolut_productivity.div(
#             df_country_topics_absolut_productivity.groupby('year').sum(), axis='rows')
#     else:
#         raise ValueError("normalization can be set only to 'intra_country' or 'global'")
#     return df_country_topics_relative_productivity


def productivity_country_per_topic(df_affiliations, df_topics, normalization='local'):
    # precomputation:
    num_affs_series = df_affiliations.reset_index().groupby('article').size()#['affiliation']
    df_affs_topics = pd.DataFrame({'article': num_affs_series.index, 'num affs': num_affs_series.values}).set_index('article').merge(df_topics, on='article').merge(df_affiliations['year'], on='article')

    df_articles_topics_distributed = df_affs_topics[df_affs_topics.columns.difference(['num affs', 'year'])].div(df_affs_topics.iloc[:, 0], axis='rows')
    df_affs_topics_distributed = df_affiliations.reset_index().set_index('article').merge(df_articles_topics_distributed, on='article')
    df_country_topics_absolut_productivity = df_affs_topics_distributed.groupby(['iso_a3', 'year']).sum()
    if normalization == 'local':
        df_country_topics_relative_productivity = df_country_topics_absolut_productivity.div(
            df_country_topics_absolut_productivity.sum(axis='columns'), axis='rows')
        df_country_topics_relative_productivity['normalization'] = normalization
    elif normalization == 'global':
        df_country_topics_relative_productivity = df_country_topics_absolut_productivity.div(
            df_country_topics_absolut_productivity.groupby('year').sum(), axis='rows')
        df_country_topics_relative_productivity['normalization'] = normalization
    elif normalization == 'both':
        df_productivity_global = productivity_country_per_topic(df_affiliations, df_topics, normalization='global')
        df_productivity_local = productivity_country_per_topic(df_affiliations, df_topics, normalization='local')
        df_country_topics_relative_productivity = pd.concat([df_productivity_global, df_productivity_local])
    else:
        raise ValueError("normalization can be set only to 'local', 'global' or 'both'")
    return df_country_topics_relative_productivity


def random_tests():
    path_of_files = "../../data/research_papers/one_folder_metadata"
    path_of_topics_csv = "doc_topics.csv"

    df_art, df_aff = df_manipulation.new_create_articles_dfs(path_of_files)
    # print(df_art)
    # print(df_aff)
    df_topics = df_manipulation.create_topics_df(path_of_topics_csv)

    # print(df_aff)

    # l = df_aff.index.get_level_values('affiliation').values
    # print(l)
    # df2 = df_aff.groupby('affiliation').nunique()#['author'].nunique()
    # df2 = df_aff.reset_index().groupby('article').nunique()[['affiliation']]  # ['author'].nunique()
    # print("\n\n\n")
    # print(df2)
    # df3 = df_aff.groupby('affiliation').size()
    # print("\n\n\n")
    # print(df3)

    # df_prod_glob = productivity_country_per_topic(df_aff, df_topics, normalization='global')
    # df_prod_loc = productivity_country_per_topic(df_aff, df_topics, normalization='local')
    # df_prod.to_csv("df_prod.csv", index=True, header=True)
    # df_tot = pd.concat([df_prod_glob, df_prod_loc])#, keys=['global', 'local'])
    # print(df_tot)
    # print(df_prod_glob.merge(df_prod_loc, on='normalization'))
    df_tot = productivity_country_per_topic(df_aff, df_topics, normalization='both')
    print(df_tot.query("iso_a3 == 'USA'"))



if __name__ == '__main__':
    random_tests()
