import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import df_manipulation
import data_extraction
import numpy as np


def my_dash_plot(world_df, topic_to_plot, slider_column):
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
         Input("year--slider", "value")
         ])
    def display_choropleth(topic, slider):
        dff = world_df[world_df[slider_column] == str(slider)]
        fig = px.choropleth(dff, geojson=world_df.geometry,
                            locations=dff.index,
                            range_color=[0, 1],
                            labels={topic: "Topic " + topic},
                            color=topic,  # lifeExp is a column of gapminder
                            # hover_name="country", # column to add to hover information
                            color_continuous_scale=px.colors.sequential.Plasma)

        return fig

    app.run_server(debug=True)


def dash_plot():
    df = px.data.election()
    geojson = px.data.election_geojson()
    candidates = df.winner.unique()
    df.to_csv("df_dash2.csv", index=True, header=True)

    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.P("Candidate:"),
        dcc.RadioItems(
            id='candidate',
            options=[{'value': x, 'label': x}
                     for x in candidates],
            value=candidates[0],
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id="choropleth"),
        dcc.Slider(
            id='year--slider',
            min=df['district_id'].min(),
            max=df['district_id'].max(),
            value=df['district_id'].max(),
            # marks={str(year): str(year) for year in df['district_id'].unique()},
            step=None
        )
    ])

    @app.callback(
        Output("choropleth", "figure"),
        [Input("candidate", "value"),
         Input("year--slider", "value")])
    def display_choropleth(candidate, year):
        print(year)
        print(type(year))
        fig = px.choropleth(
            df, geojson=geojson, color=candidate,
            locations="district", featureidkey="properties.district",
            projection="mercator", range_color=[0, 6500])
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        return fig

    app.run_server(debug=True)


def dash_plot_pro():

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
    df.to_csv("df_dash.csv", index=True, header=True)

    available_indicators = df['Indicator Name'].unique()

    app.layout = html.Div([
        html.Div([

            html.Div([
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Fertility rate, total (births per woman)'
                )
                ,
                dcc.RadioItems(
                    id='xaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],
            style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Life expectancy at birth, total (years)'
                ),
                dcc.RadioItems(
                    id='yaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),

        dcc.Graph(id='indicator-graphic'),

        dcc.Slider(
            id='year--slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=df['Year'].max(),
            marks={str(year): str(year) for year in df['Year'].unique()},
            step=None
        )
    ])

    @app.callback(
        Output('indicator-graphic', 'figure'),
        [Input('xaxis-column', 'value'),
         Input('yaxis-column', 'value'),
         Input('xaxis-type', 'value'),
         Input('yaxis-type', 'value'),
         Input('year--slider', 'value')])
    def update_graph(xaxis_column_name, yaxis_column_name,
                     xaxis_type, yaxis_type,
                     year_value):
        dff = df[df['Year'] == year_value]

        return {
            'data': [dict(
                x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
                mode='markers',
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            )],
            'layout': dict(
                xaxis={
                    'title': xaxis_column_name,
                    'type': 'linear' if xaxis_type == 'Linear' else 'log'
                },
                yaxis={
                    'title': yaxis_column_name,
                    'type': 'linear' if yaxis_type == 'Linear' else 'log'
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
            )
        }


if __name__ == '__main__':
    path_of_files = "../../data/research_papers/one_folder_metadata"
    path_of_topics_csv = "doc_topics.csv"

    df_articles, df_affiliations = df_manipulation.new_create_articles_dfs(path_of_files)
    df_topics = df_manipulation.create_topics_df(path_of_topics_csv)
    productivity = data_extraction.productivity_country_per_topic(df_affiliations, df_topics)
    productivity = productivity.reset_index().set_index('iso_a3')
    world_df = df_manipulation.load_world_df()
    world_df = df_manipulation.add_data_to_world_df(world_df, productivity).sort_values(by=['year'])

    my_dash_plot(world_df, ['2', '3', '4'], 'year')

    # dash_plot()
