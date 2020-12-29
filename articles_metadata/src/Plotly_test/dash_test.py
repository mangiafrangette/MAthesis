import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import df_manipulation
import data_extraction
import numpy as np


def my_dash_plot(world_df, topic_to_plot, slider_column, threshold):
    # world_df[topic_to_plot][world_df[topic_to_plot] <= threshold] = 0
    # world_df[topic_to_plot][world_df[topic_to_plot] <= threshold] = 0
    # world_df[topic_to_plot] = world_df[topic_to_plot][world_df[topic_to_plot] <= threshold]
    # print(world_df.loc[world_df[topic_to_plot] <= threshold, topic_to_plot])
    # print(world_df.index.name)
    df = world_df#.loc[world_df[topic_to_plot] >= 0.1]

    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.P("Topic modeling:"),
        dcc.Dropdown(
            id='topic',
            options=[{'label': f'Topic {topic}', 'value': topic} for topic in topic_to_plot],
            value=topic_to_plot[0],
            searchable=False,
            clearable=False,
        ),
        dcc.Dropdown(
            id='normalization',
            options=[{'label': 'global', 'value': 'global'}, {'label': 'local', 'value': 'local'}],
            value='global',
            searchable=False,
            clearable=False,
        ),
        dcc.Graph(id="choropleth"),
        dcc.Slider(
            id='year--slider',
            min=int(df[slider_column].min()),
            max=int(df[slider_column].max()),
            value=int(df[slider_column].min()),
            marks={str(year): str(year) for year in df[slider_column].unique()},
            step=None
        )
    ])

    @app.callback(
        Output("choropleth", "figure"),
        [Input("topic", "value"),
         Input("normalization", "value"),
         Input("year--slider", "value")
         ])
    def display_choropleth(topic, normalization, slider):
        dff = world_df[world_df[slider_column] == str(slider)].query(f"normalization == '{normalization}'")
        # test = dff.query(f"normalization == '{normalization}'")
        # print(test)
        fig = px.choropleth(dff, geojson=world_df.geometry,
                            locations=dff.index,
                            range_color=[0, 1],
                            labels={topic: "Topic " + topic},
                            color=topic,  # lifeExp is a column of gapminder
                            # hover_name="country", # column to add to hover information
                            color_continuous_scale=px.colors.sequential.Plasma)

        return fig

    app.run_server(debug=True)


if __name__ == '__main__':
    path_of_files = "../../data/research_papers/one_folder_metadata"
    path_of_topics_csv = "doc_topics.csv"

    df_articles, df_affiliations = df_manipulation.new_create_articles_dfs(path_of_files)
    df_topics = df_manipulation.create_topics_df(path_of_topics_csv)

    aggregation_dict = {
        "NLP": ["1", "3", "6", "9", "10"],
        "Computational literary analysis": ["4", "11", "12", "15"],
        "Digital scholarly editing": ["5"],
        "Data preservation": ["7", "8", "14"],
        "DH discipline": ["13"],
        "Games and interactivity in CH": ["2"],
        "Visual DH": ["16"]
    }
    # hypertopics_list = [hypertopic for hypertopic in aggregation_dict.keys()]
    hypertopics_list = list(aggregation_dict.keys())
    df_hypertopics = df_manipulation.aggregate_topics(df_topics, aggregation_dict)

    productivity = data_extraction.productivity_country_per_topic(df_affiliations, df_hypertopics, normalization='both')
    productivity = productivity.reset_index().set_index('iso_a3')

    world_df = df_manipulation.load_world_df()
    world_df = df_manipulation.add_data_to_world_df(world_df, productivity).sort_values(by=['year'])
    wolrd_df_DataStudio = world_df.drop(columns=['gdp_md_est', 'geometry', 'pop_est']).rename(columns={'name': 'country'})
    # wolrd_df_DataStudio.to_csv("wolrd_df_DataStudio_bubble.csv", index=True, header=True)

    my_dash_plot(world_df, hypertopics_list, 'year', 0.1)

    # dash_plot()
