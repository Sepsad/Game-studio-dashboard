
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
                dcc.Input(id = 'churn-threshold',
                placeholder='Enter Churn-threshold',
                type='number',
                value=1
                ),
                dcc.Dropdown(id= "target-col", multi = False, value = 'winRate',
                options = [{'label': x, 'value' : x} for x in ['matchCount', 'winRate', 'sumKillNum', 'sumDeathNum',\
                                                                'medianRank', 'meanScore', 'meanKillNum', 'meanDeathNum',\
                                                                'killDeathRatio']]),

                dcc.Graph(id = "fig-AB", figure = {})],
                width={"size": 5}),
            dbc.Col([

                dcc.Graph(id = "fig-Churn", figure = {})],
                width={"size": 5}),
            dbc.Col([

                dcc.Graph(id = "fig-Total", figure = {})],
                width={"size": 5})
            ])
            
                
        ])



@app.callback(
        [Output(component_id='fig-AB',component_property = 'figure'),
        Output(component_id='fig-Churn',component_property = 'figure'), 
        Output(component_id='fig-Total',component_property = 'figure')],
        [Input('date-picker-range', 'start_date'),
        Input('date-picker-range','end_date'),
        Input('min-games','value'),
        Input('target-col','value'),
        Input('churn-threshold','value')]
    )


def display_fig(start_first_game_date, end_first_game_date, minimum_games, target_col, churn_thershold = 7):
        if(minimum_games == None):
            minimum_games = 5
        else:
            minimum_games = int(minimum_games)

        AB_test_df['is_churned'] = ((datetime.now() - AB_test_df.lastGameDate ).dt.days > churn_thershold)
        df_for_plot = AB_test_df[AB_test_df.matchCount.astype(int) > minimum_games]
        mask = (df_for_plot['firstGameDate'] > start_first_game_date) & (df_for_plot['firstGameDate'] <= end_first_game_date)
        df_for_plot = df_for_plot.loc[mask]


        fig_AB = go.Figure()
        fig_AB.add_trace(go.Box(
        y= df_for_plot[df_for_plot['is_churned'] == True][target_col],
        x= df_for_plot['groupName'],
        name='Churned', notched=True,
        marker_color='red',boxpoints = 'all'
        ))

        fig_AB.add_trace(go.Box(
        y= df_for_plot[df_for_plot['is_churned'] == False][target_col],
        x= df_for_plot['groupName'],
        name='Not Churned', notched=True,
        marker_color='green',boxpoints = 'all'
        ))

        fig_AB.update_layout(
        title_text='Compare A & B',
        yaxis_title= target_col + " Value",
        xaxis_title= 'Groups',
        boxmode='group'
        )

        fig_churn = go.Figure()
        fig_churn.add_trace(go.Box(

        y= df_for_plot[df_for_plot['groupName'] == "A"][target_col],
        x= df_for_plot['is_churned'],
        name='A group',
        marker_color='blue',boxpoints = 'all', notched=True,
        ))

        fig_churn.add_trace(go.Box(
        y= df_for_plot[df_for_plot['groupName'] == "B"][target_col],
        x= df_for_plot['is_churned'],
        name='B group',
        marker_color='#ff7f0e',boxpoints = 'all', notched=True,
        ))


        fig_churn.update_layout(

        title = "Churned = True & Not Churned = False ",    
        boxmode='group'
        )



        
        fig_Total = go.Figure()
        fig_Total.add_trace(go.Box(
        y= df_for_plot[df_for_plot['is_churned'] == True][target_col],
        name='Churned',
        marker_color='red',boxpoints = 'all'
        ))

        fig_Total.add_trace(go.Box(
        y= df_for_plot[df_for_plot['is_churned'] == False][target_col],
        name='Not Churned',
        marker_color='green',boxpoints = 'all'
        ))

        fig_Total.update_layout(
        title_text='Churn Box plot',
        yaxis_title= target_col + " Value",
        xaxis_title= 'Groups',
        boxmode='group'
        )



        return fig_AB, fig_churn, fig_Total
