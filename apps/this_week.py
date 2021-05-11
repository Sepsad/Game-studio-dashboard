import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px


from utils import read_weekly_engagement_percentile_data

weekly_engagement_percentile_df= read_weekly_engagement_percentile_data()
weekly_engagement_percentile_df = weekly_engagement_percentile_df.loc[weekly_engagement_percentile_df['weekly']<53]
weekly_engagement_percentile_df['year'] = weekly_engagement_percentile_df["year"].astype(str) 
weekly_engagement_percentile_df['weekly'] = weekly_engagement_percentile_df["weekly"].astype(str) 
weekly_engagement_percentile_df['year_week'] = weekly_engagement_percentile_df[['year', 'weekly']].agg('..'.join, axis=1)

def display_fig():
    fig_2b = px.line(weekly_engagement_percentile_df, x= 'year_week',
                     y=['percentile_1',
                        'percentile_2',
                        'percentile_3',
                        'percentile_4',
                        'percentile_5',
                        'percentile_6',
                        'percentile_7',
                        'percentile_8',
                        'percentile_9',
                        'percentile_99'],
                                          title = 'Weekly engagement percentiles (n level attempts weekly)')
    return fig_2b



fig_2b = display_fig()


layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("This week analysis"),className="text-center", width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "fig-2b", figure = fig_2b)],
             width={"size": 5}) 
    ])
])




