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
import data_extraction


def custom_geo_plot(world_df, column_to_plot):
    fig = px.choropleth(world_df, geojson=world_df.geometry,
                        locations=world_df.index,
                        color=column_to_plot,  # lifeExp is a column of gapminder
                        #hover_name="country", # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma)
    fig.show()


# def main():
#     path_of_files = "../../data/research_papers/one_folder_metadata"
#     path_of_csv = "df_articles.csv"
#     articles_df = create_articles_data_frame(path_of_files)
#     world_df = load_world_df()
#     # print(add_interesting_field(world_df, articles_df))
#     articles_df = associate_countries(articles_df)
#
#
#     # print(mean_abstract_length(articles_df))
#     mean_countries_df = mean_abstract_length(articles_df)
#
#     new_world_df = add_data_to_world_df(world_df, mean_countries_df)
#     fig = px.choropleth(new_world_df, geojson=new_world_df.geometry,
#                         locations=new_world_df.index,
#                         color="mean number of character per abstract",  # lifeExp is a column of gapminder
#                         # hover_name="country", # column to add to hover information
#                         color_continuous_scale=px.colors.sequential.Plasma)
#     fig.show()
#     # new_world_df.plot(column='abs_len')


def random_tests():
    path_of_files = "../../data/research_papers/one_folder_metadata"
    path_of_topics_csv = "doc_topics.csv"

    df_articles, df_affiliations = df_manipulation.new_create_articles_dfs(path_of_files)
    df_topics = df_manipulation.create_topics_df(path_of_topics_csv)
    productivity = data_extraction.productivity_country_per_topic(df_affiliations, df_topics)
    #carica il mondo
    world_df = df_manipulation.load_world_df()
    # aggiungi dati al mondo
    world_df = df_manipulation.add_data_to_world_df(world_df, productivity)
    # print(world_df)
    #print(world_df)
    #custom_geo_plot(world_df, '2')
    print(productivity)


if __name__ == '__main__':
    # main()
    random_tests()
