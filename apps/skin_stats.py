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

from app import app



#import os 
#os.chdir("/home/abbas/myProjects/Game-studio-dashboard/apps/")

from utils import read_skin_stats_data, read_skin_stats2_data



skin_stats_df = read_skin_stats_data()

cosmetics_types = ['headName', 'bodyName',  'legName', 'maskName']
#skin_stats2_df = read_skin_stats2_data()

#print(skin_stats_df)

#print(skin_stats_df['headName'].unique())
#print(skin_stats_df['bodyName'].unique())
#print(skin_stats_df['legName'].unique())
#print(skin_stats_df['maskName'].unique())


layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Nabardestan looks/cosmetics usage stats"),className="text-center", width=12),
            dbc.Col(html.Div(children=''' Please select a cosmetic type: '''),className="text-center", width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id= "category-cosmetics", multi = False, value = 'headName',
                options = [{'label': x, 'value' : x} for x in cosmetics_types]),

                dcc.Graph(id = "fig-cosmetics", figure = {})],
                width={"size": 5})            
         ])       
        ])


@app.callback(
        Output(component_id='fig-cosmetics',component_property = 'figure'), 
        Input('category-cosmetics','value')
    )


def display_fig(cosmetic_type):
    if(cosmetic_type == None):
        cosmetic_type = 'headName'    
    cur_df = skin_stats_df[[cosmetic_type,'count']]
    cur_df = cur_df.groupby([cosmetic_type])['count'].sum().reset_index()
    cur_df['freq'] = -1.
    for x in cur_df[cosmetic_type].tolist():
        cur_df.loc[cur_df[cosmetic_type]==x, 'freq'] = cur_df.loc[cur_df[cosmetic_type]==x, 'count'] / cur_df[ 'count'].sum()

    

    fig = px.pie(cur_df, values='freq', names=cosmetic_type)
    return fig

