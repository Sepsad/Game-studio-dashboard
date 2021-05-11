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

from utils import read_reward_data, get_rewards_coin_equivalent, get_consumptions_coin_equivalent, read_consumption_data, get_daily_unique_users

rewards_df = read_reward_data()
rewards_coin_equiv_df  = get_rewards_coin_equivalent(rewards_df)
rewards_coin_equiv_df_agg = rewards_coin_equiv_df.groupby(['date'])['reward_coin_equivalent'].sum().reset_index()

consumption_df = read_consumption_data()
consumables_coin_equiv_df = get_consumptions_coin_equivalent(consumption_df)
consumption_df_agg = consumables_coin_equiv_df.groupby(['date'])['consumable_coin_equivalent'].sum().reset_index()


daily_unique_users_df = get_daily_unique_users()

df_coin_eq_reward_consumption_eng = rewards_coin_equiv_df_agg.merge(consumption_df_agg)
df_coin_eq_reward_consumption_eng = df_coin_eq_reward_consumption_eng.merge(daily_unique_users_df)

def display_fig(selected_reward):
    print(selected_reward)
    fig_0 = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    fig_0.add_trace(
        go.Scatter(x=df_coin_eq_reward_consumption_eng['date'], y=df_coin_eq_reward_consumption_eng['reward_coin_equivalent'], name="total rewards coin equivalent"),
        secondary_y=False
    )
    fig_0.add_trace(
        go.Scatter(x=df_coin_eq_reward_consumption_eng['date'], y=df_coin_eq_reward_consumption_eng['consumable_coin_equivalent'], name="total consumables coin equivalent"),
        secondary_y=False
    )
    fig_0.add_trace(
        go.Scatter(x=df_coin_eq_reward_consumption_eng['date'], y=df_coin_eq_reward_consumption_eng['user_count'], name="engagement - unique user count"),
        secondary_y=True
    )
    return fig_0


layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Source, Sink, Engagement"),className="text-center", width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-0", figure = display_fig("---------TOTAL EJRA SHOD-------"))],
             width={"size": 5}) 
    ])
])

# prepare data

####################


# @app.callback(
#     Output(component_id='fig-0',component_property = 'figure'),
#     Input('reward-type', 'value')
# )
# def display_fig(selected_reward):
#     fig_0 = make_subplots(specs=[[{"secondary_y": True}]])
#     # Add traces
#     fig_0.add_trace(
#         go.Scatter(x=df_coin_eq_reward_consumption_eng['date'], y=df_coin_eq_reward_consumption_eng['reward_coin_equivalent'], name="total rewards coin equivalent"),
#         secondary_y=False
#     )
#     fig_0.add_trace(
#         go.Scatter(x=df_coin_eq_reward_consumption_eng['date'], y=df_coin_eq_reward_consumption_eng['consumable_coin_equivalent'], name="total consumables coin equivalent"),
#         secondary_y=False
#     )
#     fig_0.add_trace(
#         go.Scatter(x=df_coin_eq_reward_consumption_eng['date'], y=df_coin_eq_reward_consumption_eng['user_count'], name="engagement - unique user count"),
#         secondary_y=True
#     )
#     return fig_0