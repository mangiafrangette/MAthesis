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
import numpy as np
import plotly.graph_objs as go


def custom_geo_plot(world_df, column_to_plot):
    #voglio poter definire il topic qui non fuori (come secondo argomento di questa funzione in cui dico la colonna che voglio)
    """ fig = px.choropleth(world_df, geojson=world_df.geometry,
                        locations=world_df.index,
                        #color=column_to_plot,
                        color="productivity",
                          # lifeExp is a column of gapminder
                        #hover_name="country", # column to add to hover information
                        # create slider
                        animation_frame="date",
                        #create selection of topics? not working
                        #animation_group="topic",
                        color_continuous_scale=px.colors.sequential.Plasma)
    # test for dropdown
   
    #fig.show()
    print(world_df) """

    # example with dropdown
    # Data
    df = px.data.gapminder()
    df = df.rename(columns=dict(pop="Population",
                                gdpPercap="GDP per Capita",
                                lifeExp="Life Expectancy"))
    cols_dd = ["Population", "GDP per Capita", "Life Expectancy"]
    # we need to add this to select which trace 
    # is going to be visible
    visible = np.array(cols_dd)

    # define traces and buttons at once
    traces = []
    buttons = []

    for value in cols_dd:
        traces.append(go.Choropleth(
        locations=df['iso_alpha'], # Spatial coordinates
            z=df[value].astype(float), # Data to be color-coded
            colorbar_title=value,
            visible= True if value==cols_dd[0] else False))

        buttons.append(dict(label=value,
                            method="update",
                            args=[{"visible":list(visible==value)},
                                {"title":f"<b>{value}</b>"}]))

    updatemenus = [{"active":0,
                    "buttons":buttons,
                }]

    # Show figure
    fig = go.Figure(data=traces,
                    layout=dict(updatemenus=updatemenus))
    # This is in order to get the first title displayed correctly
    first_title = cols_dd[0]
    fig.update_layout(title=f"<b>{first_title}</b>",title_x=0.5) 
    
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
    # source files for data
    path_of_files = "../../data/research_papers/one_folder_metadata"
    path_of_topics_csv = "doc_topics.csv"

    # series of functions defined in external files 

    # creates dataframes with articles and affiliations data
    df_articles, df_affiliations = df_manipulation.new_create_articles_dfs(path_of_files)
    
    # creates dataframe with documents X topics percentages (complete)
    df_topics = df_manipulation.create_topics_df(path_of_topics_csv)

    # computes productivity value 
    # productivity = data_extraction.productivity_country_per_topic(df_affiliations, df_topics, "2011")
    productivity = data_extraction.productivity_country_per_topic(df_affiliations, df_topics, "2011")

    """ test_data = {
        'iso_a3': ["ITA", "ITA", "ITA", "ITA", "ESP", "ESP","ESP", "ESP"],
        'year': [2000, 2000, 2001, 2003, 2000, 2000, 2001, 2003],
        'topic': ["Topic 1", "Topic 2", "Topic 1", "Topic 1", "Topic 1", "Topic 1", "Topic 2", "Topic 1"],
        'productivity': [0.4, 0.8, 0.8, 0.1, 0.8, 0.4, 0.9, 0.8]
        }
    test_df = pd.DataFrame.from_dict(test_data)
    print(test_df) """

    # loads the world map data 
    world_df = df_manipulation.load_world_df()
    
    # adds relevant data to the world map
    world_df = df_manipulation.add_data_to_world_df(world_df, productivity)
    #world_df = df_manipulation.add_data_to_world_df(world_df, test_df)
    #print(world_df)
    
    custom_geo_plot(world_df, "2")

    #print(productivity)


if __name__ == '__main__':
    # main()
    random_tests()
