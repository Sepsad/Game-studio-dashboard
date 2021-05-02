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
        dbc.Col(html.H1("Irooni Source, Sink, Engagement Dashboard"),className="text-center", width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id= "reward-type", multi = False, value = 'rocket_reward',
                         options = [{'label': x, 'value' : x} for x in ['bomb_reward', 'rocket_reward', 'disco_reward', 'cell_reward', 'row_reward', 'col_reward', 'shuffle_reward', 'coin_reward', 'heart_reward']]),
            dcc.Graph(id="fig-1", figure = {})
        ], width={"size": 5})]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-2", figure = {})  
        ],  width={"size": 5})]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-3", figure = {})  
        ],  width={"size": 5})]),
    #dbc.Row([
        #dbc.Col([
        #    dcc.Graph(id = "fig-4", figure = {})  
        #],  width={"size": 5})]),
        dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-5", figure = {})  
        ],  width={"size": 5})]),
                dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-6", figure = {})  
        ],  width={"size": 5})]),
    
])

rewards_df = read_reward_data()
engagement_df = read_engagement_data()
engagement_df_1h = read_engagement_data_1hbin()


engagement_df['weekday'] = engagement_df['date'].dt.day_name()
engagement_df_1h['weekday'] = engagement_df_1h['date'].dt.day_name()



max_year = engagement_df['date'].dt.year.max()
engagement_df_last_year = engagement_df.loc[engagement_df['date'].dt.year == max_year]
engagement_df_last_year['week_nr'] = pd.DatetimeIndex(engagement_df_last_year['date']).weekofyear
engagement_df_last_year_agg = \
    engagement_df_last_year.groupby(['week_nr','weekday'])['n_level_attempts'].sum().reset_index()
    
engagement_df_last_year_agg = engagement_df_last_year_agg.loc[engagement_df_last_year_agg['week_nr'] < 53]

cutoff_date = engagement_df["date"].max() - pd.Timedelta(days=180)

engagement_df_recent = engagement_df.loc[engagement_df['date'] > cutoff_date]
engagement_df_1h_recent = engagement_df_1h.loc[engagement_df_1h['date'] > cutoff_date]

engagement_df_1h_recent_agg = engagement_df_1h_recent.groupby(['weekday','bin1h'])['n_level_attempts'].sum().reset_index()
engagement_df_recent_agg = engagement_df_recent.groupby(['weekday','bin4h_str'])['n_level_attempts'].sum().reset_index()

engagement_df_recent_agg_pvt = pd.pivot_table(engagement_df_recent_agg, values = 'n_level_attempts', index='weekday', columns = 'bin4h_str')
engagement_df_1h_recent_agg_pvt = pd.pivot_table(engagement_df_1h_recent_agg, values = 'n_level_attempts', index='weekday', columns = 'bin1h')

engagement_df_recent_agg_pvt = engagement_df_recent_agg_pvt.reindex(['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ])
engagement_df_recent_agg_pvt = engagement_df_recent_agg_pvt[['0_4h', '4_8h', '8_12h', '12_16h', '16_20h', '20_24h']]

engagement_df_1h_recent_agg_pvt = engagement_df_1h_recent_agg_pvt.reindex(['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ])
engagement_df_1h_recent_agg_pvt = engagement_df_1h_recent_agg_pvt[[x for x in range(24)]]
#################################


hourly_user_df = read_hourly_users()
hourly_user_df_recent = hourly_user_df.loc[hourly_user_df['date'] > cutoff_date]

hourly_user_df_recent_agg = hourly_user_df_recent.groupby(['bin1h'])['n_distinct_players_l1_l19',
                                                                     'n_distinct_players_l20_99',
                                                                     'n_distinct_players_l100_l299',
                                                                     'n_distinct_players_l300_l799',
                                                                     'n_distinct_players_l800plus'].sum().reset_index()

hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg
hourly_user_df_recent_agg_ratio['ratio_distinct_players_l1_l19'] = hourly_user_df_recent_agg_ratio['n_distinct_players_l1_l19'] / hourly_user_df_recent_agg_ratio['n_distinct_players_l1_l19'].sum()
hourly_user_df_recent_agg_ratio['ratio_distinct_players_l20_99'] = hourly_user_df_recent_agg_ratio['n_distinct_players_l20_99'] / hourly_user_df_recent_agg_ratio['n_distinct_players_l20_99'].sum()
hourly_user_df_recent_agg_ratio['ratio_distinct_players_l100_l299'] = hourly_user_df_recent_agg_ratio['n_distinct_players_l100_l299'] / hourly_user_df_recent_agg_ratio['n_distinct_players_l100_l299'].sum()
hourly_user_df_recent_agg_ratio['ratio_distinct_players_l300_l799'] = hourly_user_df_recent_agg_ratio['n_distinct_players_l300_l799'] / hourly_user_df_recent_agg_ratio['n_distinct_players_l300_l799'].sum()
hourly_user_df_recent_agg_ratio['ratio_distinct_players_l800plus'] = hourly_user_df_recent_agg_ratio['n_distinct_players_l800plus'] / hourly_user_df_recent_agg_ratio['n_distinct_players_l800plus'].sum()


hourly_user_df_recent_agg_ratio.index = hourly_user_df_recent_agg_ratio['bin1h']
hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio.drop('bin1h', 1)
hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio.drop('n_distinct_players_l1_l19', 1)
hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio.drop('n_distinct_players_l20_99', 1)
hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio.drop('n_distinct_players_l100_l299', 1)
hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio.drop('n_distinct_players_l300_l799', 1)
hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio.drop('n_distinct_players_l800plus', 1)
hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio[['ratio_distinct_players_l1_l19', 
                                                             'ratio_distinct_players_l20_99', 
                                                             'ratio_distinct_players_l100_l299', 
                                                             'ratio_distinct_players_l300_l799', 
                                                             'ratio_distinct_players_l800plus']]



# CallBack
#*****************************************************
@app.callback(
    Output('fig-1', 'figure'),
    Output('fig-2', 'figure'),
    Output('fig-3', 'figure'),
    #Output('fig-4', 'figure'),
    Output('fig-5', 'figure'),
    Output('fig-6', 'figure'),
    Input('reward-type', 'value')
)
def update_graph(reward_selected):
    #sdf, dff = read_data(reward_selected)
    #dff['date'] = dff.index
    #fig_time_per_session = px.line(dff, x='date', y=['REWARD_TYPE_LEVEL_CHEST','REWARD_TYPE_STAR_CHEST','REWARD_TYPE_DAILY_BONUS','REWARD_TYPE_TREASURE_CHEST','REWARD_TYPE_TEAM_CHEST', 'REWARD_TYPE_DAILY_TASK', 'REWARD_TYPE_TEAM_TOURNAMENT', 'OTHER_REWARD'])
    #fig_time_per_session_box = px.box(df,x= "chest_type", y= "daily_count_" + str(reward_selected), notched=True)

    rewards_df_sub = rewards_df.loc[rewards_df.reward_type == reward_selected]
    #print(rewards_df_sub)
    fig_1 = px.line(rewards_df_sub, x='date', y= 'daily_count', color = 'chest_type_str', title= 'Reward count')
    fig_2 = px.line(engagement_df, x='date', y= 'n_level_attempts', color = 'bin4h_str', title = 'Daily engagement')
    fig_3 = px.line(engagement_df_last_year_agg, x='week_nr', y= 'n_level_attempts', color = 'weekday',\
                    title = 'Engagement separated for week days, Current year data, x-axis week of year nr')
    fig_4 = px.imshow(engagement_df_recent_agg_pvt,
                      y = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ],
                      x = ['0_4h', '4_8h', '8_12h', '12_16h', '16_20h', '20_24h'],
                labels=dict(x="Time of Day", y="Day of Week", color="Total level attempts"),
                title= 'Engagement for Week-day & day-interval, data of the last 6 months'
               )
    fig_5 = px.imshow(engagement_df_1h_recent_agg_pvt,
                      y = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ],
                      x = [x for x in range(24)],
                labels=dict(x="Time of Day (h)", y="Day of Week", color="Total level attempts"),
                title= 'Engagement for Week-day & day-interval, data of the last 6 months'
               )
    fig_6 = px.imshow(hourly_user_df_recent_agg_ratio,
                labels=dict(x="Level Interval", y="Time of Day (h)", color="n Distinct Users"),
                x = ['ratio_distinct_players_l1_l19', 
                                                             'ratio_distinct_players_l20_99', 
                                                             'ratio_distinct_players_l100_l299', 
                                                             'ratio_distinct_players_l300_l799', 
                                                             'ratio_distinct_players_l800plus'], 
                title= 'Number of distinct users in hours and levels, data of the last 6 months'
               )

    return fig_1, fig_2, fig_3, fig_5, fig_6



if __name__ == '__main__':
    app.run_server(debug=True)
