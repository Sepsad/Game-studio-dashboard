import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px


from utils import read_dau_percent_data, read_dau_data


df_dau_percent = read_dau_percent_data()
df_dau = read_dau_data()

def display_fig():
    fig_2b = px.line(df_dau_percent, x='startDate', y= 'size', color = 'day_number_from_install', title= 'DAU percent per day')
    fig_2c = px.line(df_dau, x='startDate', y= 'size', color = 'day_number_from_install', title= 'DAU size per day')

    return fig_2b, fig_2c



fig_2b, fig_2c = display_fig()


layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("DAU percent"),className="text-center", width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-DAU-percent", figure = fig_2b)],
             width={"size": 5}) 
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-DAU", figure = fig_2c)],
             width={"size": 5}) 
    ])
])