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

from utils import read_nabardestan_winrate_data_db, read_nabardestan_winrate_AB_t1_data_db
import plotly.figure_factory as ff



#import os 
#os.chdir("/home/abbas/myProjects/210428_dashboard_sepsad/Game-studio-dashboard/apps/")





my_df = read_nabardestan_winrate_data_db()




#my_df['gameNumber'] = pd.to_numeric(my_df['gameNumber'],errors='coerce')
#my_df['win_rate'] = pd.to_numeric(my_df['win_rate'],errors='coerce')
my_df['gameNumber'] = my_df['gameNumber'].astype(int)
my_df['win_rate'] = my_df['win_rate'].astype(float)
my_df['startDate_date'] =  pd.to_datetime(my_df['startDate_date'])

my_df['n_games'] = my_df['n_games'].astype(int)
my_df['players_per_room_mean'] = my_df['players_per_room_mean'].astype(float)
my_df['rank_mean'] = my_df['rank_mean'].astype(float)




df_win_rate_pvt = pd.pivot_table(my_df[my_df['gameNumber']< 30], values = 'win_rate', index='gameNumber', columns = 'startDate_date').reset_index()
df_win_rate_pvt = df_win_rate_pvt.set_index('gameNumber')
df_win_rate_pvt.columns =df_win_rate_pvt.columns.map(lambda t: t.strftime('%Y-%m-%d'))


df_win_rate_pvt_n_games = pd.pivot_table(my_df[my_df['gameNumber']< 30], values = 'n_games', index='gameNumber', columns = 'startDate_date').reset_index()
df_win_rate_pvt_n_games = df_win_rate_pvt_n_games.set_index('gameNumber')
df_win_rate_pvt_n_games.columns = df_win_rate_pvt_n_games.columns.map(lambda t: t.strftime('%Y-%m-%d'))

df_win_rate_pvt_ppr = pd.pivot_table(my_df[my_df['gameNumber']< 30], values = 'players_per_room_mean', index='gameNumber', columns = 'startDate_date').reset_index()
df_win_rate_pvt_ppr = df_win_rate_pvt_ppr.set_index('gameNumber')
df_win_rate_pvt_ppr.columns = df_win_rate_pvt_ppr.columns.map(lambda t: t.strftime('%Y-%m-%d'))

df_win_rate_pvt_rank = pd.pivot_table(my_df[my_df['gameNumber']< 30], values = 'rank_mean', index='gameNumber', columns = 'startDate_date').reset_index()
df_win_rate_pvt_rank = df_win_rate_pvt_rank.set_index('gameNumber')
df_win_rate_pvt_rank.columns = df_win_rate_pvt_rank.columns.map(lambda t: t.strftime('%Y-%m-%d'))


df_annot = df_win_rate_pvt_n_games.copy()
for cur_date in list(df_annot):
    df_annot[cur_date] = 'n_games: ' + df_annot[cur_date].astype(str) 
    df_annot[cur_date] =  df_annot[cur_date]  + '<br>'
    df_annot[cur_date] =  df_annot[cur_date]  + 'players per room (mean): '
    df_annot[cur_date] = df_annot[cur_date] + df_win_rate_pvt_ppr[cur_date].astype(str)
    df_annot[cur_date] =  df_annot[cur_date]  + '<br>'
    df_annot[cur_date] =  df_annot[cur_date]  + 'rank mean: '
    df_annot[cur_date] = df_annot[cur_date] + df_win_rate_pvt_rank[cur_date].astype(str)


fig = px.imshow(df_win_rate_pvt, 
                x = df_win_rate_pvt.columns.tolist(),
                 labels=dict(x="date - game start", y="game number", color="win rate"),
                 zmin=0, zmax=1, origin= 'lower')


fig.update(data=[{'customdata': df_annot,
    'hovertemplate': 'date - game start: %{x}<br>game number: %{y}<br>%{customdata}<br>win rate: %{z}<extra></extra>'}])


#fig.update_layout(hovermode='closest')
#fig.show()



#############################################

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
########################################################3
#winrate heatmap sep for AB t1


my_df = read_nabardestan_winrate_AB_t1_data_db()

#my_df['gameNumber'] = pd.to_numeric(my_df['gameNumber'],errors='coerce')
#my_df['win_rate'] = pd.to_numeric(my_df['win_rate'],errors='coerce')
my_df['gameNumber'] = my_df['gameNumber'].astype(int)
my_df['win_rate'] = my_df['win_rate'].astype(float)
my_df['startDate_date'] =  pd.to_datetime(my_df['startDate_date'])
my_df = my_df[my_df.startDate_date >= '2021-05-06']#AB test start date approx.
my_df['n_games'] = my_df['n_games'].astype(int)
my_df['players_per_room_mean'] = my_df['players_per_room_mean'].astype(float)
my_df['rank_mean'] = my_df['rank_mean'].astype(float)



df_win_rate_pvt_A = pd.pivot_table(my_df[(my_df['gameNumber']< 30) & (my_df['groupName'] == 'A')], values = 'win_rate', index='gameNumber', columns = 'startDate_date').reset_index()
df_win_rate_pvt_A = df_win_rate_pvt_A.set_index('gameNumber')
df_win_rate_pvt_A.columns =df_win_rate_pvt_A.columns.map(lambda t: t.strftime('%Y-%m-%d'))

df_win_rate_pvt_B = pd.pivot_table(my_df[(my_df['gameNumber']< 30) & (my_df['groupName'] == 'B')], values = 'win_rate', index='gameNumber', columns = 'startDate_date').reset_index()
df_win_rate_pvt_B = df_win_rate_pvt_B.set_index('gameNumber')
df_win_rate_pvt_B.columns =df_win_rate_pvt_B.columns.map(lambda t: t.strftime('%Y-%m-%d'))

my_df_A = my_df[my_df['groupName'] == 'A']
my_df_B = my_df[my_df['groupName'] == 'B']


df_win_rate_pvt_n_games = pd.pivot_table(my_df_A[my_df_A['gameNumber']< 30], values = 'n_games', index='gameNumber', columns = 'startDate_date').reset_index()
df_win_rate_pvt_n_games = df_win_rate_pvt_n_games.set_index('gameNumber')
df_win_rate_pvt_n_games.columns = df_win_rate_pvt_n_games.columns.map(lambda t: t.strftime('%Y-%m-%d'))

df_win_rate_pvt_ppr = pd.pivot_table(my_df_A[my_df_A['gameNumber']< 30], values = 'players_per_room_mean', index='gameNumber', columns = 'startDate_date').reset_index()
df_win_rate_pvt_ppr = df_win_rate_pvt_ppr.set_index('gameNumber')
df_win_rate_pvt_ppr.columns = df_win_rate_pvt_ppr.columns.map(lambda t: t.strftime('%Y-%m-%d'))

df_win_rate_pvt_rank = pd.pivot_table(my_df_A[my_df_A['gameNumber']< 30], values = 'rank_mean', index='gameNumber', columns = 'startDate_date').reset_index()
df_win_rate_pvt_rank = df_win_rate_pvt_rank.set_index('gameNumber')
df_win_rate_pvt_rank.columns = df_win_rate_pvt_rank.columns.map(lambda t: t.strftime('%Y-%m-%d'))


df_annot_A = df_win_rate_pvt_n_games.copy()
for cur_date in list(df_annot_A):
    df_annot_A[cur_date] = 'n_games: ' + df_annot_A[cur_date].astype(str) 
    df_annot_A[cur_date] =  df_annot_A[cur_date]  + '<br>'
    df_annot_A[cur_date] =  df_annot_A[cur_date]  + 'players per room (mean): '
    df_annot_A[cur_date] = df_annot_A[cur_date] + df_win_rate_pvt_ppr[cur_date].astype(str)
    df_annot_A[cur_date] =  df_annot_A[cur_date]  + '<br>'
    df_annot_A[cur_date] =  df_annot_A[cur_date]  + 'rank mean: '
    df_annot_A[cur_date] = df_annot_A[cur_date] + df_win_rate_pvt_rank[cur_date].astype(str)

#################################

df_win_rate_pvt_n_games = pd.pivot_table(my_df_B[my_df_B['gameNumber']< 30], values = 'n_games', index='gameNumber', columns = 'startDate_date').reset_index()
df_win_rate_pvt_n_games = df_win_rate_pvt_n_games.set_index('gameNumber')
df_win_rate_pvt_n_games.columns = df_win_rate_pvt_n_games.columns.map(lambda t: t.strftime('%Y-%m-%d'))

df_win_rate_pvt_ppr = pd.pivot_table(my_df_B[my_df_B['gameNumber']< 30], values = 'players_per_room_mean', index='gameNumber', columns = 'startDate_date').reset_index()
df_win_rate_pvt_ppr = df_win_rate_pvt_ppr.set_index('gameNumber')
df_win_rate_pvt_ppr.columns = df_win_rate_pvt_ppr.columns.map(lambda t: t.strftime('%Y-%m-%d'))

df_win_rate_pvt_rank = pd.pivot_table(my_df_B[my_df_B['gameNumber']< 30], values = 'rank_mean', index='gameNumber', columns = 'startDate_date').reset_index()
df_win_rate_pvt_rank = df_win_rate_pvt_rank.set_index('gameNumber')
df_win_rate_pvt_rank.columns = df_win_rate_pvt_rank.columns.map(lambda t: t.strftime('%Y-%m-%d'))


df_annot_B = df_win_rate_pvt_n_games.copy()
for cur_date in list(df_annot_B):
    df_annot_B[cur_date] = 'n_games: ' + df_annot_B[cur_date].astype(str) 
    df_annot_B[cur_date] =  df_annot_B[cur_date]  + '<br>'
    df_annot_B[cur_date] =  df_annot_B[cur_date]  + 'players per room (mean): '
    df_annot_B[cur_date] = df_annot_B[cur_date] + df_win_rate_pvt_ppr[cur_date].astype(str)
    df_annot_B[cur_date] =  df_annot_B[cur_date]  + '<br>'
    df_annot_B[cur_date] =  df_annot_B[cur_date]  + 'rank mean: '
    df_annot_B[cur_date] = df_annot_B[cur_date] + df_win_rate_pvt_rank[cur_date].astype(str)


####################################

fig_3A = px.imshow(df_win_rate_pvt_A, 
                x = df_win_rate_pvt_A.columns.tolist(),
                 labels=dict(x="date - game start", y="game number", color="win rate"),
                 title = 'win rate for group A - AB test T1',
                 zmin=0, zmax=1, origin= 'lower')
fig_3A.update(data=[{'customdata': df_annot_A,
    'hovertemplate': 'date - game start: %{x}<br>game number: %{y}<br>%{customdata}<br>win rate: %{z}<extra></extra>'}])


fig_3B= px.imshow(df_win_rate_pvt_B, 
                x = df_win_rate_pvt_B.columns.tolist(),
                 labels=dict(x="date - game start", y="game number", color="win rate"),
                 title = 'win rate for group B - AB test T1',
                 zmin=0, zmax=1, origin= 'lower')

fig_3B.update(data=[{'customdata': df_annot_B,
    'hovertemplate': 'date - game start: %{x}<br>game number: %{y}<br>%{customdata}<br>win rate: %{z}<extra></extra>'}])



######################################################3
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
    ]),
        dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-nab-3", figure = fig_3A)],
             width={"size": 5}) 
    ]),
        dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-nab-4", figure = fig_3B)],
             width={"size": 5}) 
    ])

])