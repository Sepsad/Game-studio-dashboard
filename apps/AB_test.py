
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
from dash.dependencies import Input,Output
from datetime import date, datetime

import pandas as pd
from utils import read_AB_test_data
from app import app

AB_test_df = read_AB_test_data()
AB_test_df['lastGameDate'] = pd.to_datetime(AB_test_df['lastGameDate'])
AB_test_df['firstGameDate'] = pd.to_datetime(AB_test_df['firstGameDate'])
AB_test_df['is_churned'] = ((datetime.now() - AB_test_df.lastGameDate ).dt.days > 7)
AB_test_df['meanKillNum'] = AB_test_df['sumKillNum'].astype(int) / AB_test_df['matchCount'].astype(int)
AB_test_df['meanDeathNum'] = AB_test_df['sumDeathNum'].astype(int) / AB_test_df['matchCount'].astype(int)









layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Nabardestan AB test"),className="text-center", width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.DatePickerRange(
            id='date-picker-range',
            start_date=date(2021, 3, 3),
            end_date  = date(2021, 5, 31),
            initial_visible_month=date(2021, 3, 20)),
            dcc.Input(id = 'min-games',
            placeholder='Enter minimum games has played...',
            type='number',
            value=1
            ),
            dcc.Dropdown(id= "target-col", multi = False, value = 'winRate',
            options = [{'label': x, 'value' : x} for x in ['matchCount', 'winRate', 'sumKillNum', 'sumDeathNum', 'medianRank', 'meanScore', 'meanKillNum', 'meanDeathNum']]),

            dcc.Graph(id = "fig-AB", figure = {})],
             width={"size": 5}),])
])

@app.callback(
    Output(component_id='fig-AB',component_property = 'figure'),
    [Input('date-picker-range', 'start_date'),
    Input('date-picker-range','end_date'),
    Input('min-games','value'),
    Input('target-col','value')]
)


def display_fig(start_first_game_date, end_first_game_date, minimum_games, target_col):
    if(minimum_games == None):
        minimum_games = 5
    else:
        minimum_games = int(minimum_games)
    df_for_plot = AB_test_df[AB_test_df.matchCount.astype(int) > minimum_games]
    mask = (df_for_plot['firstGameDate'] > start_first_game_date) & (df_for_plot['firstGameDate'] <= end_first_game_date)
    df_for_plot = df_for_plot.loc[mask]

    fig = go.Figure()
    fig.add_trace(go.Box(

    y= df_for_plot[df_for_plot['is_churned'] == True][target_col],
    x= df_for_plot['groupName'],
    name='Churned',
    marker_color='red',boxpoints = 'all'
    ))

    fig.add_trace(go.Box(
    y= df_for_plot[df_for_plot['is_churned'] == False][target_col],
    x= df_for_plot['groupName'],
    name='Not Churned',
    marker_color='green',boxpoints = 'all'
    ))


    fig.update_layout(
    title_text='Compare A & B',
    yaxis_title= target_col + " Value",
    xaxis_title= 'Groups',
    boxmode='group'
    )


    return (fig)
