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


# Creates a Panda DataFrames of all articles
def create_articles_data_frame(path_of_files):
    list_of_articles = []
    folder = os.fsencode(path_of_files)
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):
            with open(f"{path_of_files}/{filename}", "r", encoding="utf-8") as article_file:
                list_of_articles.append(json.load(article_file))
    return pd.DataFrame(list_of_articles)


def load_world_df():
    world_df = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world_df = world_df[(world_df.pop_est > 0) & (world_df.name != "Antarctica")]
    return world_df.rename(columns={'iso_a3': 'country_iso_a3'}).set_index('country_iso_a3')


def calculate_abstract_length(articles_df):
    articles_df['abs_len'] = [len(abstract) for abstract in articles_df["abstract"].values]
    return articles_df


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


# aggiunge una colonna ad articles_df per indicare i countries di ogni articolo
def associate_countries(articles_df):
    list_of_countries = list()
    for authors in articles_df["authors"].values:
        curr_article_countries = set()
        for author in authors:
            for affiliation in author['affiliation']:
                if affiliation['country'] is not None:
                    curr_article_countries.add(pycountry_convert.country_name_to_country_alpha3(affiliation['country']))
        if len(curr_article_countries) == 0:
            list_of_countries.append(None)
        else:
            list_of_countries.append(curr_article_countries)
    articles_df["countries"] = list_of_countries
    return articles_df


# mean_countries_dict in output: {'<country_code1>' : mean_abs_len1, ...}
def mean_abstract_length(articles_df):
    articles_df = calculate_abstract_length(articles_df)
    articles_per_country_dict = calculate_num_of_articles_per_country(articles_df)
    mean_countries_dict = dict()
    for index, article in articles_df.iterrows():
        if article['countries'] is not None:
            for country in article['countries']:
                if country not in mean_countries_dict:
                    mean_countries_dict[country] = articles_df['abs_len'][index]*1.0/articles_per_country_dict[country]
                else:
                    mean_countries_dict[country] += articles_df['abs_len'][index]*1.0/articles_per_country_dict[country]
    return pd.DataFrame({'country_iso_a3': mean_countries_dict.keys(), 'mean number of character per abstract': mean_countries_dict.values()}).set_index('country_iso_a3')


def add_data_to_world_df(world_df, data_df):
    # return pd.concat(world_df, data_df)

    return world_df.merge(data_df, on='country_iso_a3')


def main():
    path_of_files = "../../data/research_papers/one_folder_metadata"
    path_of_csv = "df_articles.csv"
    articles_df = create_articles_data_frame(path_of_files)
    world_df = load_world_df()
    # print(add_interesting_field(world_df, articles_df))
    articles_df = associate_countries(articles_df)


    # print(mean_abstract_length(articles_df))
    mean_countries_df = mean_abstract_length(articles_df)

    new_world_df = add_data_to_world_df(world_df, mean_countries_df)
    fig = px.choropleth(new_world_df, geojson=new_world_df.geometry,
                        locations=new_world_df.index,
                        color="mean number of character per abstract",  # lifeExp is a column of gapminder
                        # hover_name="country", # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma)
    fig.show()
    # new_world_df.plot(column='abs_len')


def random_tests():
    # Define a dictionary containing Students data
    data = {'Name': ['Jai', 'Princi', 'Gaurav', 'Anuj'],
            'Height': [5.1, 6.2, 5.1, 5.2],
            'Qualification': ['Msc', 'MA', 'Msc', 'Msc']}

    # Define a dictionary with key values of
    # an existing column and their respective
    # value pairs as the # values for our new column.
    address = {'Delhi': 'Princi', 'Bangalore': 'Jai',
               'Patna': 'Gaurav', 'Chennai': 'Anuj'}
    address_df = pd.DataFrame(address)
    print(address_df)
    print()

    # Convert the dictionary into DataFrame
    df = pd.DataFrame(data)
    df.set_index('Name')
    print(df)
    print()

    # Provide 'Address' as the column name
    df['Address'] = address

    # Observe the output
    print(df)


if __name__ == '__main__':
    main()
    # random_tests()
