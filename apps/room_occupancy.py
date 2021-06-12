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
#import os 
#os.chdir("/home/abbas/myProjects/210519_game_analytics_dashboard/Game-studio-dashboard/apps/")
from utils import read_room_occupancy_data




ro_df = read_room_occupancy_data()
ro_df['count'] = ro_df['count'].astype(int)
ro_df['n_players_in_room'] = ro_df['n_players_in_room'].astype(str)
ro_df['startDate_date'] =  pd.to_datetime(ro_df['startDate_date'])

fig = px.line(ro_df, x="startDate_date", y="count", color='n_players_in_room', title='room counts separated by player count')
fig.update_traces(mode='markers+lines')
#fig.show()

ro_df['count_players_in_room_group']  = ro_df['n_players_in_room'].astype(int) * ro_df['count'].astype(int)

fig1 = px.line(ro_df, x="startDate_date", y="count_players_in_room_group", color='n_players_in_room', title='player counts seperated by room group')
fig1.update_traces(mode='markers+lines')


dau_df = ro_df.groupby('startDate_date')['count_players_in_room_group'].sum().reset_index()
dau_df.rename(columns={'count_players_in_room_group':'dau'}, inplace=True)

ro_df2 = ro_df.merge(dau_df, how = 'left')
ro_df2['count_players_in_room_group_dau_norm'] =  ro_df2['count_players_in_room_group'].astype(float) / ro_df2['dau'].astype(float)

fig2 = px.line(ro_df2, x="startDate_date", y="count_players_in_room_group_dau_norm", color="n_players_in_room",
                   title='player counts seperated by room group, DAU normalized', hover_data=['dau'])

fig2.update_traces(mode='markers+lines')
#fig2.show()


fig3 = px.line(dau_df, x="startDate_date", y="dau",
                   title='DAU')

fig3.update_traces(mode='markers+lines')




layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Nabardestan room occupancy: players vs bots"),className="text-center", width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Div(children=''' تعداد اتاق‌ها، تفکیک‌ شده بر اساس تعداد بازیکن درون آن‌ها. '''),className="text-center", width=12)
    ]),
        
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-ro", figure = fig)],
             width={"size": 5}) 
    ]),
    dbc.Row([
        dbc.Col(html.Div(children=''' تعداد بازیکن‌ها به تفکیک نوع اتاقی که در آن بازی کردند. '''),className="text-center", width=12)
    ]),
        
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-ro1", figure = fig1)],
             width={"size": 5}) 
    ]),
    dbc.Row([
        dbc.Col(html.Div(children='''  ٓٓـتعداد بازیکن‌هاـ/ـ بازیکن فعال روزانه ـ به تفکیک نوع اتاقی که در آن بازی کردند '''),className="text-center", width=12)
    ]),
        
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-ro2", figure = fig2)],
             width={"size": 5}) 
    ]),
    dbc.Row([
        dbc.Col(html.Div(children='''   بازیکن فعال روزانه '''),className="text-center", width=12)
    ]),
        
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-ro4", figure = fig3)],
             width={"size": 5}) 
    ])
])
