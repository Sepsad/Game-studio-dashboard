
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
from utils import get_agg_last_year_engagement_data, get_recent_hourly_user_agg_ratio, get_pvt_agg_recent_engagement_1h_data
from app import app



engagement_df_last_year_agg = get_agg_last_year_engagement_data()
engagement_df_1h_recent_agg_pvt = get_pvt_agg_recent_engagement_1h_data()
hourly_user_df_recent_agg_ratio = get_recent_hourly_user_agg_ratio()

def display_fig():
    fig_0 = px.line(engagement_df_last_year_agg, x='week_nr', y= 'n_level_attempts', color = 'weekday',\
                    title = 'Engagement separated for week days, Current year data, x-axis week of year nr')
    fig_1 = px.imshow(engagement_df_1h_recent_agg_pvt,
                      y = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ],
                      x = [x for x in range(24)],
                labels=dict(x="Time of Day (h)", y="Day of Week", color="Total level attempts"),
                title= 'Engagement for Week-day & day-interval, data of the last 6 months'
               )
    fig_2 = px.imshow(hourly_user_df_recent_agg_ratio,
                labels=dict(x="Level Interval", y="Time of Day (h)", color="n Distinct Users"),
                x = ['ratio_distinct_players_l1_l19', 
                                                             'ratio_distinct_players_l20_99', 
                                                             'ratio_distinct_players_l100_l299', 
                                                             'ratio_distinct_players_l300_l799', 
                                                             'ratio_distinct_players_l800plus'], 
                title= 'Number of distinct users in hours and levels, data of the last 6 months'
               )
    return fig_0, fig_1, fig_2

fig_0, fig_1, fig_2 = display_fig()


layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Detailed engagement"),className="text-center", width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-5", figure = fig_0)],
             width={"size": 5}) 
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-1", figure = fig_1)],
             width={"size": 5}) 
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-2", figure = fig_2)],
             width={"size": 5}) 
    ])
])



