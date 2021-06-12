import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import pathlib
from app import app

from utils import read_reward_data

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Rewards"),className="text-center", width=12)
    ]),
    dbc.Row([
        
        dbc.Col([
            dcc.Dropdown(id= "reward-type", multi = False, value = 'rocket_reward',
                         options = [{'label': x, 'value' : x} for x in ['bomb_reward', 'rocket_reward', 'disco_reward', 'cell_reward', 'row_reward', 'col_reward', 'shuffle_reward', 'coin_reward', 'heart_reward']]),
            dcc.Graph(id = "fig-4", figure = {})],
             width={"size": 5}) 
    ])
])

rewards_df = read_reward_data()

@app.callback(
    Output(component_id='fig-4',component_property = 'figure'),
    Input('reward-type', 'value')
)
def display_fig(reward_selected):
    print("-------------REWARD EJRA SHOD---------------------")
    rewards_df_sub = rewards_df.loc[rewards_df.reward_type == reward_selected]
    fig_0 = px.line(rewards_df_sub, x='date', y= 'daily_count', color = 'chest_type_str', title= 'Reward count')
    return fig_0