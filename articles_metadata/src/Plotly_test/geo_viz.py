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
import plotly
import plotly.offline as offline


def new_plot(world_df, columns_to_plot, slider_column):
    # min year in your dataset
    year = 1998

    # your color-scale
    scl = [[0.0, '#ffffff'], [0.2, '#b4a8ce'], [0.4, '#8573a9'],
           [0.6, '#7159a3'], [0.8, '#5732a1'], [1.0, '#2c0579']]  # purples

    data_slider = []
    for year in world_df['year'].unique():
        df_segmented = world_df[(world_df['year'] == year)]

        for col in df_segmented.columns:
            df_segmented[col] = df_segmented[col].astype(str)

        data_each_yr = dict(
            type='choropleth',
            locations=world_df.index,
            z=df_segmented['sightings'].astype(float),
            colorscale=scl,
            colorbar={'title': '# Sightings'})

        data_slider.append(data_each_yr)

    steps = []
    for i in range(len(data_slider)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data_slider)],
                    label='Year {}'.format(i + 1998))
        step['args'][1][i] = True
        steps.append(step)

    sliders = [dict(active=0, pad={"t": 1}, steps=steps)]

    # layout = dict(title='UFO Sightings by State Since 1998', geo=dict(scope='usa',
    #                                                                   projection={'type': 'albers usa'}),
    #               sliders=sliders)
    layout = dict(title='UFO Sightings by State Since 1998', geo=world_df.geometry, sliders=sliders)

    fig = dict(data=data_slider, layout=layout)
    # periscope.plotly(fig)
    plotly.offline.iplot(fig)


def ble():
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
            locations=df['iso_alpha'],  # Spatial coordinates
            z=df[value].astype(float),  # Data to be color-coded
            colorbar_title=value,
            visible=True if value == cols_dd[0] else False))

        buttons.append(dict(label=value,
                            method="update",
                            args=[{"visible": list(visible == value)},
                                  {"title": f"<b>{value}</b>"}]))

    updatemenus = [{"active": 0,
                    "buttons": buttons,
                    }]

    # Show figure
    fig = go.Figure(data=traces,
                    layout=dict(updatemenus=updatemenus))
    # This is in order to get the first title displayed correctly
    first_title = cols_dd[0]
    fig.update_layout(title=f"<b>{first_title}</b>", title_x=0.5)

    fig.show()


def geo_plot_slider(world_df, topic_to_plot, slider_column):
    fig = px.choropleth(world_df, geojson=world_df.geometry,
                        locations=world_df.index,
                        animation_frame=slider_column,
                        range_color=[0, 1],
                        labels={topic_to_plot: "Topic " + topic_to_plot},
                        color=topic_to_plot,  # lifeExp is a column of gapminder
                        # hover_name="country", # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma)
    # fig.show()
    offline.plot(fig)


def custom_geo_plot(world_df, columns_to_plot, slider_column):
    # fig = px.choropleth(world_df, geojson=world_df.geometry,
    #                     locations=world_df.index,
    #                     animation_frame=slider_column,
    #                     range_color=[0, 1],
    #                     labels={column_to_plot: "Topic "+column_to_plot},
    #                     color=column_to_plot,  # lifeExp is a column of gapminder
    #                     # hover_name="country", # column to add to hover information
    #                     color_continuous_scale=px.colors.sequential.Plasma)

    cols_dd = columns_to_plot
    # we need to add this to select which trace
    # is going to be visible
    visible = np.array(cols_dd)

    # define traces and buttons at once
    traces = []
    buttons = []

    for value in cols_dd:
        traces.append(px.choropleth(world_df, geojson=world_df.geometry,
                                    locations=world_df.index,
                                    # animation_frame=slider_column,
                                    range_color=[0, 1],
                                    labels={value: "Topic " + value},
                                    color=value,  # lifeExp is a column of gapminder
                                    # hover_name="country", # column to add to hover information
                                    color_continuous_scale=px.colors.sequential.Plasma))

        buttons.append(dict(label=value,
                            method="update",
                            args=[{"visible": list(visible == value)},
                                  {"title": f"<b>{value}</b>"}]))

    updatemenus = [{"active": 0,
                    "buttons": buttons,
                    }]

    # Show figure
    fig = go.Figure(data=traces,
                    layout=dict(updatemenus=updatemenus))
    # This is in order to get the first title displayed correctly
    first_title = cols_dd[0]
    fig.update_layout(title=f"<b>{first_title}</b>", title_x=0.5)

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
    productivity = data_extraction.productivity_country_per_topic(df_affiliations, df_topics, normalization='global')
    productivity = productivity.reset_index().set_index('iso_a3')
    world_df = df_manipulation.load_world_df()
    world_df = df_manipulation.add_data_to_world_df(world_df, productivity).sort_values(by=['year'])
    # print("oooooo"+productivity.query('year == "2008"').iloc[0, 0]+"oooo")
    # print(world_df['year'])
    # custom_geo_plot(world_df, ['2', '3'], 'year')
    geo_plot_slider(world_df, '2', 'year')
    # ble()
    # new_plot(world_df,  ['2', '3'], 'year')


if __name__ == '__main__':
    # main()
    random_tests()
