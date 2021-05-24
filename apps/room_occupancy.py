#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 00:21:55 2021

@author: abbas
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

from utils import read_room_occupancy_data


#import os 
#os.chdir("/home/abbas/myProjects/210519_game_analytics_dashboard/Game-studio-dashboard/apps/")

ro_df = read_room_occupancy_data()
ro_df['count'] = ro_df['count'].astype(int)
ro_df['n_players_in_room'] = ro_df['n_players_in_room'].astype(str)
ro_df['startDate_date'] =  pd.to_datetime(ro_df['startDate_date'])

fig = px.line(ro_df, x="startDate_date", y="count", color='n_players_in_room')

fig.update_traces(mode='markers+lines')


layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Nabardestan room occupancy: players vs bots"),className="text-center", width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-ro", figure = fig)],
             width={"size": 5}) 
    ])

])