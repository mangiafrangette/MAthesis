import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import df_manipulation
import data_extraction
import numpy as np


def my_dash_ts(world_df, topic_to_plot, slider_column):
    df = world_df

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
        dcc.Graph(id="time-series-chart"),
    ])

    @app.callback(
        Output("time-series-chart", "figure"),
        [Input("topic", "value")
         ])
         
    def display_time_series(topic):
        # dff = df.query("iso_a3 == 'USA'")
        selected_countries = df.groupby("iso_a3")[topic].mean().to_frame(name="mean").query("mean > 0.2")
        i1 = selected_countries.index
        #print(i1)
        i2 = df.index
        ts_df = df[i2.isin(i1)].reset_index().sort_values(by=['year'])

        # dfff = dff[]
        print(ts_df)
        
        fig = px.line(ts_df, x='year', y=topic, color="name")
        return fig

    app.run_server(debug=True)

if __name__ == '__main__':
    path_of_files = "../../data/research_papers/one_folder_metadata"
    path_of_topics_csv = "doc_topics.csv"

    df_articles, df_affiliations = df_manipulation.new_create_articles_dfs(path_of_files)
    df_topics = df_manipulation.create_topics_df(path_of_topics_csv)
    productivity = data_extraction.productivity_country_per_topic(df_affiliations, df_topics)
    productivity = productivity.reset_index().set_index('iso_a3')
    world_df = df_manipulation.load_world_df()
    world_df = df_manipulation.add_data_to_world_df(world_df, productivity).sort_values(by=['year'])

    my_dash_ts(world_df, ['2', '3', '4'], 'year')

    # dash_plot()
