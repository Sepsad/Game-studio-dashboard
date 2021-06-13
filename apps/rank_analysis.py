import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.express as px
from dash.dependencies import Input,Output
from datetime import datetime

import pandas as pd
from utils import read_AB_test_data
from app import app

AB_test_df = read_AB_test_data()

AB_test_df['lastGameDate'] = pd.to_datetime(AB_test_df['lastGameDate'])
AB_test_df['firstGameDate'] = pd.to_datetime(AB_test_df['firstGameDate'])
AB_test_df.loc[AB_test_df['medianRank'] == 1.5, 'medianRank'] = 1
AB_test_df.loc[AB_test_df['medianRank'] == 2.5, 'medianRank'] = 2
AB_test_df.loc[AB_test_df['medianRank'] == 3.5, 'medianRank'] = 3
AB_test_df['is_churned'] = ((datetime.now() - AB_test_df.lastGameDate ).dt.days > 7)


layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Nabardestan AB test"),className="text-center", width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.RangeSlider(
                id='winrate-range',
                min=0,
                max=1.0,
                step=0.05,
                value=[0.3, 0.7],
                marks={
                    0: '0',
                    0.25: '0.25',
                    0.5: 'Win Rate',
                    0.75: '0.75',
                    1: '1'
                    }
                ),
                dcc.Graph(id = "fig-rank", figure = {})],
                width={"size": 5}),
        ])       
        ])

@app.callback(
        Output(component_id='fig-rank',component_property = 'figure'),
        Input('winrate-range', 'value')
    )

def display_fig(winrate_range):
    df_for_rank = AB_test_df.loc[ (winrate_range[0] < AB_test_df['winRate']) & (AB_test_df['winRate'] < winrate_range[1]) ]

    df_rank_plot = pd.merge(df_for_rank.groupby('medianRank').count().reset_index().iloc[:,0:2] , 
                            pd.DataFrame(df_for_rank.groupby('medianRank').mean()['is_churned']).reset_index())
    df_rank_plot.columns = ['medianRank', 'size', 'is_churned']

    fig = px.bar(df_rank_plot, x="medianRank", y="is_churned", hover_data=['size'] )
    return fig




