# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
import plotly.express as px
import pandas as pd
#import os 
#os.chdir("/home/abbas/myProjects/210428_dashboard_sepsad/irooni-dash/")

from data_reader import *






external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options




app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Irooni Source Dashboard"),className="text-center", width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id= "reward-type", multi = False, value = 'rocket_reward',
                         options = [{'label': x, 'value' : x} for x in ['bomb_reward', 'rocket_reward', 'disco_reward', 'cell_reward', 'row_reward', 'col_reward', 'shuffle_reward', 'coin_reward', 'heart_reward']]),
            dcc.Graph(id="fig-1", figure = {})
        ], width={"size": 5}),
        dbc.Col([
            dcc.Graph(id = "fig-2", figure = {})  
        ],  width={"size": 5}),
        dbc.Col([
            dcc.Graph(id = "fig-3", figure = {})  
        ],  width={"size": 5}),
        dbc.Col([
            dcc.Graph(id = "fig-4", figure = {})  
        ],  width={"size": 5})
    ]),
])

rewards_df = read_reward_data()
engagement_df = read_engagement_data()



engagement_df['weekday'] = engagement_df['date'].dt.day_name()



max_year = engagement_df['date'].dt.year.max()
engagement_df_last_year = engagement_df.loc[engagement_df['date'].dt.year == max_year]
engagement_df_last_year['week_nr'] = pd.DatetimeIndex(engagement_df_last_year['date']).weekofyear
engagement_df_last_year_agg = \
    engagement_df_last_year.groupby(['week_nr','weekday'])['n_level_attempts'].sum().reset_index()
    
engagement_df_last_year_agg = engagement_df_last_year_agg.loc[engagement_df_last_year_agg['week_nr'] < 53]

cutoff_date = engagement_df["date"].max() - pd.Timedelta(days=180)

engagement_df_recent = engagement_df.loc[engagement_df['date'] > cutoff_date]

engagement_df_recent_agg = engagement_df_recent.groupby(['weekday','bin4h_str'])['n_level_attempts'].sum().reset_index()


engagement_df_recent_agg_pvt = pd.pivot_table(engagement_df_recent_agg, values = 'n_level_attempts', index='weekday', columns = 'bin4h_str')

engagement_df_recent_agg_pvt = engagement_df_recent_agg_pvt.reindex(['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ])
engagement_df_recent_agg_pvt = engagement_df_recent_agg_pvt[['0_4h', '4_8h', '8_12h', '12_16h', '16_20h', '20_24h']]




# CallBack
#*****************************************************
@app.callback(
    Output('fig-1', 'figure'),
    Output('fig-2', 'figure'),
    Output('fig-3', 'figure'),
    Output('fig-4', 'figure'),
    Input('reward-type', 'value')
)
def update_graph(reward_selected):
    #sdf, dff = read_data(reward_selected)
    #dff['date'] = dff.index
    #fig_time_per_session = px.line(dff, x='date', y=['REWARD_TYPE_LEVEL_CHEST','REWARD_TYPE_STAR_CHEST','REWARD_TYPE_DAILY_BONUS','REWARD_TYPE_TREASURE_CHEST','REWARD_TYPE_TEAM_CHEST', 'REWARD_TYPE_DAILY_TASK', 'REWARD_TYPE_TEAM_TOURNAMENT', 'OTHER_REWARD'])
    #fig_time_per_session_box = px.box(df,x= "chest_type", y= "daily_count_" + str(reward_selected), notched=True)

    rewards_df_sub = rewards_df.loc[rewards_df.reward_type == reward_selected]
    #print(rewards_df_sub)
    fig_1 = px.line(rewards_df_sub, x='date', y= 'daily_count', color = 'chest_type_str')
    fig_2 = px.line(engagement_df, x='date', y= 'n_level_attempts', color = 'bin4h_str')
    fig_3 = px.line(engagement_df_last_year_agg, x='week_nr', y= 'n_level_attempts', color = 'weekday',\
                    title = 'Trends separated for week days, Current year data, x-axis week of year nr')
    fig_4 = px.imshow(engagement_df_recent_agg_pvt,
                labels=dict(x="Time of Day", y="Day of Week", color="Total level attempts in the last 6 months")
               )

    return fig_1, fig_2, fig_3, fig_4



if __name__ == '__main__':
    app.run_server(debug=True)
