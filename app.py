# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
import plotly.express as px
import pandas as pd

from data_reader import read_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options




app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Irooni Source Dashboard"),className="text-center", width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id= "reward-type", multi = False, value = 'rocket_reward',
                         options = [{'label': x, 'value' : x} for x in ['bomb_reward', 'rocket_reward', 'disco_reward', 'cell_reward', 'row_reward', 'col_reward', 'shuffle_reward', 'coin_reward', 'heart_reward']]),
            dcc.Graph(id="time-per-session", figure = {})
        ], width={"size": 5}),
        dbc.Col([
            dcc.Graph(id = "time-per-session-box", figure = {})  
        ],  width={"size": 5})
    ]),
])


# CallBack
#*****************************************************
@app.callback(
    Output('time-per-session', 'figure'),
    Output('time-per-session-box', 'figure'),
    Input('reward-type', 'value')
)
def update_graph(reward_selected):
    df, dff = read_data(reward_selected)
    dff['date'] = dff.index
    fig_time_per_session = px.line(dff, x='date', y=['REWARD_TYPE_LEVEL_CHEST','REWARD_TYPE_STAR_CHEST','REWARD_TYPE_DAILY_BONUS','REWARD_TYPE_TREASURE_CHEST','REWARD_TYPE_TEAM_CHEST', 'REWARD_TYPE_DAILY_TASK', 'REWARD_TYPE_TEAM_TOURNAMENT', 'OTHER_REWARD'])
    fig_time_per_session_box = px.box(df,x= "chest_type", y= "daily_count_" + str(reward_selected), notched=True)

    return fig_time_per_session, fig_time_per_session_box



if __name__ == '__main__':
    app.run_server(debug=True)