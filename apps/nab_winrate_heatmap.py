#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 00:33:53 2021

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
import pathlib
#from app import app

from utils import read_nabardestan_winrate_data


my_df = read_nabardestan_winrate_data()


#my_df['gameNumber'] = pd.to_numeric(my_df['gameNumber'],errors='coerce')
#my_df['win_rate'] = pd.to_numeric(my_df['win_rate'],errors='coerce')
my_df['gameNumber'] = my_df['gameNumber'].astype(int)
my_df['win_rate'] = my_df['win_rate'].astype(float)
my_df['startDate_date'] =  pd.to_datetime(my_df['startDate_date'])



df_win_rate_pvt = pd.pivot_table(my_df[my_df['gameNumber']< 30], values = 'win_rate', index='gameNumber', columns = 'startDate_date').reset_index()
df_win_rate_pvt = df_win_rate_pvt.set_index('gameNumber')


fig = px.imshow(df_win_rate_pvt, 
                 labels=dict(x="date - game start", y="game number", color="win rate"),
                 zmin=0, zmax=1, origin= 'lower')
fig.update_layout(hovermode='closest')
#fig.show()


#cutoff_date = my_df["startDate_date"].max() - pd.Timedelta(days=10)

#my_df_today = my_df[my_df["startDate_date"] ==  my_df["startDate_date"].max()][['gameNumber', 'win_rate']]
#my_df_today['group'] = 'today'

my_df_yesterday = my_df[my_df["startDate_date"] ==  (my_df["startDate_date"].max()- pd.Timedelta(days=1))][['gameNumber', 'win_rate']]
my_df_yesterday['group'] = 'yesterday'

my_df_yesterday2 = my_df[my_df["startDate_date"] ==  (my_df["startDate_date"].max()- pd.Timedelta(days=2))][['gameNumber', 'win_rate']]
my_df_yesterday2['group'] = '1d_before_yesterday'


#my_df_lastweek = my_df[my_df["startDate_date"] >  (my_df["startDate_date"].max()- pd.Timedelta(days=7))][['gameNumber', 'win_rate']]
my_df_lastweek = my_df[my_df["startDate_date"] >  (my_df["startDate_date"].max()- pd.Timedelta(days=7))].groupby(['gameNumber'])[['win_rate']].median()
my_df_lastweek.reset_index(inplace=True)

my_df_lastweek['group'] = 'last_week_median'

#my_df_last30 = my_df[my_df["startDate_date"] >  (my_df["startDate_date"].max()- pd.Timedelta(days=30))][['gameNumber', 'win_rate']]
my_df_last30 = my_df[my_df["startDate_date"] >  (my_df["startDate_date"].max()- pd.Timedelta(days=30))].groupby(['gameNumber'])[['win_rate']].median()
my_df_last30.reset_index(inplace=True)
my_df_last30['group'] = 'last_30days_median'

mydf2 = my_df_yesterday
mydf2 = mydf2.append(my_df_yesterday2, ignore_index=True)
mydf2 = mydf2.append(my_df_lastweek, ignore_index=True)
mydf2 = mydf2.append(my_df_last30, ignore_index=True)

fig2 = px.line(mydf2, x='gameNumber', y= 'win_rate', color = 'group', title= 'win rate curve')

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Nabardestan win rate"),className="text-center", width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-nab-1", figure = fig)],
             width={"size": 5}) 
    ]),
        dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-nab-2", figure = fig2)],
             width={"size": 5}) 
    ])

])
