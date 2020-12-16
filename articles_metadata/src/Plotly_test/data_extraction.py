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


def productivity_country_per_topic(df_affiliations, df_topics):
    # precomputation:
    num_affs_series = df_affiliations.reset_index().groupby('article').size()#['affiliation']
    # print(pd.DataFrame({'article': num_affs_series.index, 'num affs': num_affs_series.values}).set_index('article').merge(df_affiliations['year'], on='article'))
    df_affs_topics = pd.DataFrame({'article': num_affs_series.index, 'num affs': num_affs_series.values}).set_index('article').merge(df_topics, on='article').merge(df_affiliations['year'], on='article')
    # print(df_affs_topics)#.set_index(['year', 'iso_a3']))
    # test = df_affs_topics.iloc[:, 1::].div(df_affs_topics.iloc[:, 0], axis='rows')
    # test = df_affs_topics.loc[:, (df_topics.columns != 'num affs') & (df_topics.columns != 'year')].div(df_affs_topics.iloc[:, 0], axis='rows')
    test = df_affs_topics[df_affs_topics.columns.difference(['num affs', 'year'])].div(df_affs_topics.iloc[:, 0], axis='rows')
    test2 = df_affiliations.reset_index().set_index('article').merge(test, on='article')
    test3 = test2.groupby(['iso_a3', 'year']).sum()
    test4 = test3.div(test3.sum(axis=1), axis=0)
    # print(test4.query('country=="Italy"').idxmax(axis="columns"))
    # print(test4['1'].max())
    return test4


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

    df_prod = productivity_country_per_topic(df_aff, df_topics)
    # df_prod.to_csv("df_prod.csv", index=True, header=True)
    print(df_prod)



if __name__ == '__main__':
    random_tests()
