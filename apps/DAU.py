import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from utils import read_dau_percent_data, read_dau_data


dau_percent_df = read_dau_percent_data()[['startDate','day_number_from_install', 'size']]
dau_df = read_dau_data()[['startDate','day_number_from_install', 'size']]

DAU = pd.merge(dau_df, dau_percent_df, on= ['startDate','day_number_from_install'])

DAU.columns = ['startDate','day_number_from_install', 'size', 'percent']

def display_fig():
    fig_2b = px.line(DAU, x='startDate', y= 'percent', color = 'day_number_from_install',hover_data=['size'], title= 'DAU percent per day')

    return fig_2b



fig_2b = display_fig()


layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("DAU percent"),className="text-center", width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-DAU-percent", figure = fig_2b)],
             width={"size": 5}) 
    ])
])