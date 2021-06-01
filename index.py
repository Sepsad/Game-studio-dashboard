from os import path
import dash
import dash_core_components as dcc
import dash_auth
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
import plotly.express as px
import pandas as pd
#import os 
#os.chdir("/home/abbas/myProjects/210428_dashboard_sepsad/irooni-dash/")

# Connect to main app.py file
from app import app
from app import server

from apps import detailed_engagemnet, total, nab_winrate_heatmap, AB_test, room_occupancy, DAU#, this_week, reward
from utils import get_au_db

server = app.server # I add this part here, Abbas


au = get_au_db()
auth = dash_auth.BasicAuth(
    app,
    au
)

app.layout = html.Div([html.H1(children='Game insights Dashboard'), html.H2('Irooni analytics:'),
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Total engagement,sink and source\n', href='/apps/total'),
        html.Br(),
        #dcc.Link('Reward count\n', href='/apps/reward'),
        #html.Br(),
        dcc.Link('Detailed engagemnet\n', href='/apps/detailed_engagemnet'),
        html.Br(),
        #dcc.Link('This Week Analysis', href = '/apps/this_week'),
        html.Br()], 
       className="row"),
    html.H2('Nabardestan analytics:'),
    html.Div([
        dcc.Link('Nabardestan win rate', href = '/apps/nab_winrate_heatmap'),
        html.Br(),
        dcc.Link('Nabardestan AB test win rate', href = '/apps/AB_test'),
        html.Br(),
        dcc.Link('Nabardestan room occupancy: players vs bots', href = '/apps/room_occupancy'),
        html.Br(),
        dcc.Link('Daily Active User Percent', href = '/apps/DAU'),
        html.Br()
    ], className="row"),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/total':
        return total.layout
    if pathname == '/apps/detailed_engagemnet':
        return detailed_engagemnet.layout
    #if pathname == '/apps/reward':
    #    return reward.layout
#    if pathname == '/apps/this_week':
#        return this_week.layout
    if pathname == '/apps/nab_winrate_heatmap':
        return nab_winrate_heatmap.layout
    if pathname == '/apps/AB_test':
        return AB_test.layout
    if pathname == '/apps/room_occupancy':
        return room_occupancy.layout
    if pathname == '/apps/DAU':
        return DAU.layout
    else:
        return html.H6("Please choose a link")



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
    # app.run_server(debug=True)



# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col(html.H1("Irooni Source, Sink, Engagement Dashboard"),className="text-center", width=12)
#     ]),
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id = "fig-0", figure = {})  
#         ],  width={"size": 5})]),

#     dbc.Row([
#         dbc.Col([
#             dcc.Dropdown(id= "reward-type", multi = False, value = 'rocket_reward',
#                          options = [{'label': x, 'value' : x} for x in ['bomb_reward', 'rocket_reward', 'disco_reward', 'cell_reward', 'row_reward', 'col_reward', 'shuffle_reward', 'coin_reward', 'heart_reward']]),
#             dcc.Graph(id="fig-1", figure = {})
#         ], width={"size": 5})]),
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id = "fig-2", figure = {})  
#         ],  width={"size": 5})]),
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id = "fig-3", figure = {})  
#         ],  width={"size": 5})]),

#         dbc.Row([
#         dbc.Col([
#             dcc.Graph(id = "fig-5", figure = {})  
#         ],  width={"size": 5})]),
#                 dbc.Row([
#         dbc.Col([
#             dcc.Graph(id = "fig-6", figure = {})  
#         ],  width={"size": 5})]),
    
# ])

# rewards_df = read_reward_data()
# engagement_df = read_engagement_data()
# engagement_df_1h = read_engagement_data_1hbin()
# hourly_user_df = read_hourly_users()



# max_year = engagement_df['date'].dt.year.max()
# engagement_df_last_year = engagement_df.loc[engagement_df['date'].dt.year == max_year]
# engagement_df_last_year['week_nr'] = pd.DatetimeIndex(engagement_df_last_year['date']).weekofyear
# engagement_df_last_year_agg = \
#     engagement_df_last_year.groupby(['week_nr','weekday'])['n_level_attempts'].sum().reset_index()
    
# engagement_df_last_year_agg = engagement_df_last_year_agg.loc[engagement_df_last_year_agg['week_nr'] < 53]

# cutoff_date = engagement_df["date"].max() - pd.Timedelta(days=180)

# engagement_df_recent = engagement_df.loc[engagement_df['date'] > cutoff_date]
# engagement_df_1h_recent = engagement_df_1h.loc[engagement_df_1h['date'] > cutoff_date]


# engagement_df_recent_agg = engagement_df_recent.groupby(['weekday','bin4h_str'])['n_level_attempts'].sum().reset_index()
# engagement_df_1h_recent_agg = engagement_df_1h_recent.groupby(['weekday','bin1h'])['n_level_attempts'].sum().reset_index()

# engagement_df_recent_agg_pvt = pd.pivot_table(engagement_df_recent_agg, values = 'n_level_attempts', index='weekday', columns = 'bin4h_str')
# engagement_df_1h_recent_agg_pvt = pd.pivot_table(engagement_df_1h_recent_agg, values = 'n_level_attempts', index='weekday', columns = 'bin1h')

# engagement_df_recent_agg_pvt = engagement_df_recent_agg_pvt.reindex(['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ])
# engagement_df_recent_agg_pvt = engagement_df_recent_agg_pvt[['0_4h', '4_8h', '8_12h', '12_16h', '16_20h', '20_24h']]

# engagement_df_1h_recent_agg_pvt = engagement_df_1h_recent_agg_pvt.reindex(['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ])
# engagement_df_1h_recent_agg_pvt = engagement_df_1h_recent_agg_pvt[[x for x in range(24)]]
#################################


# hourly_user_df_recent = hourly_user_df.loc[hourly_user_df['date'] > cutoff_date]

# hourly_user_df_recent_agg = hourly_user_df_recent.groupby(['bin1h'])['n_distinct_players_l1_l19',
#                                                                      'n_distinct_players_l20_99',
#                                                                      'n_distinct_players_l100_l299',
#                                                                      'n_distinct_players_l300_l799',
#                                                                      'n_distinct_players_l800plus'].sum().reset_index()

# hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg
# hourly_user_df_recent_agg_ratio['ratio_distinct_players_l1_l19'] = hourly_user_df_recent_agg_ratio['n_distinct_players_l1_l19'] / hourly_user_df_recent_agg_ratio['n_distinct_players_l1_l19'].sum()
# hourly_user_df_recent_agg_ratio['ratio_distinct_players_l20_99'] = hourly_user_df_recent_agg_ratio['n_distinct_players_l20_99'] / hourly_user_df_recent_agg_ratio['n_distinct_players_l20_99'].sum()
# hourly_user_df_recent_agg_ratio['ratio_distinct_players_l100_l299'] = hourly_user_df_recent_agg_ratio['n_distinct_players_l100_l299'] / hourly_user_df_recent_agg_ratio['n_distinct_players_l100_l299'].sum()
# hourly_user_df_recent_agg_ratio['ratio_distinct_players_l300_l799'] = hourly_user_df_recent_agg_ratio['n_distinct_players_l300_l799'] / hourly_user_df_recent_agg_ratio['n_distinct_players_l300_l799'].sum()
# hourly_user_df_recent_agg_ratio['ratio_distinct_players_l800plus'] = hourly_user_df_recent_agg_ratio['n_distinct_players_l800plus'] / hourly_user_df_recent_agg_ratio['n_distinct_players_l800plus'].sum()


# hourly_user_df_recent_agg_ratio.index = hourly_user_df_recent_agg_ratio['bin1h']
# hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio.drop('bin1h', 1)
# hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio.drop('n_distinct_players_l1_l19', 1)
# hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio.drop('n_distinct_players_l20_99', 1)
# hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio.drop('n_distinct_players_l100_l299', 1)
# hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio.drop('n_distinct_players_l300_l799', 1)
# hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio.drop('n_distinct_players_l800plus', 1)
# hourly_user_df_recent_agg_ratio = hourly_user_df_recent_agg_ratio[['ratio_distinct_players_l1_l19', 
#                                                              'ratio_distinct_players_l20_99', 
#                                                              'ratio_distinct_players_l100_l299', 
#                                                              'ratio_distinct_players_l300_l799', 
#                                                              'ratio_distinct_players_l800plus']]
##########################################
# rewards_coin_equiv_df  = get_rewards_coin_equivalent(rewards_df)
# rewards_coin_equiv_df_agg = rewards_coin_equiv_df.groupby(['date'])['reward_coin_equivalent'].sum().reset_index()

# consumption_df = read_consumption_data()
# consumables_coin_equiv_df = get_consumptions_coin_equivalent(consumption_df)
# consumption_df_agg = consumables_coin_equiv_df.groupby(['date'])['consumable_coin_equivalent'].sum().reset_index()


# daily_unique_users_df = get_daily_unique_users()

# df_coin_eq_reward_consumption_eng = rewards_coin_equiv_df_agg.merge(consumption_df_agg)
# df_coin_eq_reward_consumption_eng = df_coin_eq_reward_consumption_eng.merge(daily_unique_users_df)



# CallBack
# #*****************************************************
# @app.callback(
#     Output('fig-0', 'figure'),
#     Output('fig-1', 'figure'),
#     Output('fig-2', 'figure'),
#     Output('fig-3', 'figure'),
#     Output('fig-5', 'figure'),
#     Output('fig-6', 'figure'),
#     Input('reward-type', 'value')
# )
# def update_graph(reward_selected):
#     # rewards_df_sub = rewards_df.loc[rewards_df.reward_type == reward_selected]
#     # fig_1 = px.line(rewards_df_sub, x='date', y= 'daily_count', color = 'chest_type_str', title= 'Reward count')
#     # fig_2 = px.line(engagement_df, x='date', y= 'n_level_attempts', color = 'bin4h_str', title = 'Daily engagement')
#     # fig_3 = px.line(engagement_df_last_year_agg, x='week_nr', y= 'n_level_attempts', color = 'weekday',\
#     #                 title = 'Engagement separated for week days, Current year data, x-axis week of year nr')

#     # fig_5 = px.imshow(engagement_df_1h_recent_agg_pvt,
#     #                   y = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ],
#     #                   x = [x for x in range(24)],
#     #             labels=dict(x="Time of Day (h)", y="Day of Week", color="Total level attempts"),
#     #             title= 'Engagement for Week-day & day-interval, data of the last 6 months'
#     #            )
#     # fig_6 = px.imshow(hourly_user_df_recent_agg_ratio,
#     #             labels=dict(x="Level Interval", y="Time of Day (h)", color="n Distinct Users"),
#     #             x = ['ratio_distinct_players_l1_l19', 
#     #                                                          'ratio_distinct_players_l20_99', 
#     #                                                          'ratio_distinct_players_l100_l299', 
#     #                                                          'ratio_distinct_players_l300_l799', 
#     #                                                          'ratio_distinct_players_l800plus'], 
#     #             title= 'Number of distinct users in hours and levels, data of the last 6 months'
#     #            )


#     fig_0 = make_subplots(specs=[[{"secondary_y": True}]])
#     # Add traces
#     fig_0.add_trace(
#         go.Scatter(x=df_coin_eq_reward_consumption_eng['date'], y=df_coin_eq_reward_consumption_eng['reward_coin_equivalent'], name="total rewards coin equivalent"),
#         secondary_y=False
#     )
#     fig_0.add_trace(
#         go.Scatter(x=df_coin_eq_reward_consumption_eng['date'], y=df_coin_eq_reward_consumption_eng['consumable_coin_equivalent'], name="total consumables coin equivalent"),
#         secondary_y=False
#     )
#     fig_0.add_trace(
#         go.Scatter(x=df_coin_eq_reward_consumption_eng['date'], y=df_coin_eq_reward_consumption_eng['user_count'], name="engagement - unique user count"),
#         secondary_y=True
#     )

#     return fig_0, fig_1, fig_2, fig_3, fig_5, fig_6


