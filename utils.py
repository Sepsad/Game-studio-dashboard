
import gspread
import sys
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

chest_type_dict = {'0' : 'REWARD_TYPE_LEVEL_CHEST',
'1' : 'CHEST_TYPE_STAR_CHEST',
'2' : 'CHEST_TYPE_DAILY_BONUS',
'3' : 'CHEST_TYPE_TREASURE_CHEST',
'4' : 'CHEST_TYPE_TEAM_CHEST',
'5' : 'CHEST_TYPE_DAILY_TASK',
'6' : 'CHEST_TYPE_TEAM_TOURNAMENT',
'7' : 'CHEST_TYPE_OTHER_TOURNAMENT'}

chest_type_ls = [[0 , 'REWARD_TYPE_LEVEL_CHEST'],
[1 , 'CHEST_TYPE_STAR_CHEST'],
[2 , 'CHEST_TYPE_DAILY_BONUS'],
[3 , 'CHEST_TYPE_TREASURE_CHEST'],
[4 , 'CHEST_TYPE_TEAM_CHEST'],
[5 , 'CHEST_TYPE_DAILY_TASK'],
[6 , 'CHEST_TYPE_TEAM_TOURNAMENT'],
[7 , 'CHEST_TYPE_OTHER_TOURNAMENT']]
chest_type_df = pd.DataFrame(chest_type_ls, columns = ['chest_type', 'chest_type_str'])


daily_4hbins_ls = [[0 , '0_4h'],
[1 , '4_8h'],
[2 , '8_12h'],
[3 , '12_16h'],
[4 , '16_20h'],
[5 , '20_24h']]
daily_4hbins_df = pd.DataFrame(daily_4hbins_ls, columns = ['bin4h', 'bin4h_str'])


#print(chest_type_dict)


def read_data(sheet_name = "rocket_reward"):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
         'Qok-flurry-data-dcfd7cde3e9f.json', scope) 
    gc = gspread.authorize(credentials)
    sheet = gc.open("Irooni - Daily Reward Count")
    worksheet = sheet.worksheet(sheet_name)
    data = worksheet.get_all_values()   
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)

    grouper = df.groupby('chest_type')
    dfList = [v[['date','daily_count_' + sheet_name]].rename(columns={'daily_count_' + sheet_name: chest_type_dict[k]}) for k, v in grouper]
    dfs = [df.set_index('date') for df in dfList]
    final_df = pd.concat(dfs, axis=1)
    final_df.sort_index(inplace=True)
    return df, final_df

def read_reward_data():
    #
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
         'phrasal-datum-311915-03b34c76b093.json', scope) 
    gc = gspread.authorize(credentials)
    sheet = gc.open("irooni_lettuce")
    worksheet = sheet.worksheet('rewards_daily')
    data = worksheet.get_all_values()   
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    df['chest_type'] = df['chest_type'].astype(int)
    df['daily_count'] = df['daily_count'].astype(int)
    df['reward_type'] = df['reward_type'].astype(str)
    df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d', utc= True)
    df = df.merge(chest_type_df, on = 'chest_type')

    return df

def read_consumption_data():
    #
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
         'phrasal-datum-311915-03b34c76b093.json', scope) 
    gc = gspread.authorize(credentials)
    sheet = gc.open("irooni_lettuce")
    worksheet = sheet.worksheet('consmumptions_daily')
    data = worksheet.get_all_values()   
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    df['daily_count'] = df['daily_count'].astype(int)
    df['consumable'] = df['consumable'].astype(str)
    df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d', utc= True)

    return df



def read_engagement_data():
    #
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
         'phrasal-datum-311915-03b34c76b093.json', scope) 
    gc = gspread.authorize(credentials)
    sheet = gc.open("irooni_lettuce")
    worksheet = sheet.worksheet('engagement_daily')
    data = worksheet.get_all_values()   
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    df['bin4h'] = df['bin4h'].astype(int)
    df['n_level_attempts'] = df['n_level_attempts'].astype(int)
    df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d', utc= True)
    df = df.merge(daily_4hbins_df, on = 'bin4h')
    df['weekday'] = df['date'].dt.day_name()

    return df

def read_engagement_data_1hbin():
    #
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
         'phrasal-datum-311915-03b34c76b093.json', scope) 
    gc = gspread.authorize(credentials)
    sheet = gc.open("irooni_lettuce")
    worksheet = sheet.worksheet('engagement_daily_1h')
    data = worksheet.get_all_values()   
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    df['bin1h'] = df['bin1h'].astype(int)
    df['n_level_attempts'] = df['n_level_attempts'].astype(int)
    df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d', utc= True)

    df['weekday'] = df['date'].dt.day_name()
    return df


def get_agg_last_year_engagement_data():
    engagement_df = read_engagement_data()
    max_year = engagement_df['date'].dt.year.max()

    engagement_df_last_year = engagement_df.loc[engagement_df['date'].dt.year == max_year]
    engagement_df_last_year['week_nr'] = pd.DatetimeIndex(engagement_df_last_year['date']).weekofyear

    engagement_df_last_year_agg = engagement_df_last_year.groupby(['week_nr','weekday'])['n_level_attempts'].sum().reset_index()
    engagement_df_last_year_agg = engagement_df_last_year_agg.loc[engagement_df_last_year_agg['week_nr'] < 53]
    return engagement_df_last_year_agg

def get_pvt_agg_recent_engagement_1h_data():
    engagement_df = read_engagement_data()
    engagement_df_1h = read_engagement_data_1hbin()
    cutoff_date = engagement_df["date"].max() - pd.Timedelta(days=180)
    engagement_df_1h_recent = engagement_df_1h.loc[engagement_df_1h['date'] > cutoff_date]
    engagement_df_1h_recent_agg = engagement_df_1h_recent.groupby(['weekday','bin1h'])['n_level_attempts'].sum().reset_index()

    engagement_df_1h_recent_agg_pvt = pd.pivot_table(engagement_df_1h_recent_agg, values = 'n_level_attempts', index='weekday', columns = 'bin1h')
    engagement_df_1h_recent_agg_pvt = engagement_df_1h_recent_agg_pvt.reindex(['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ])
    engagement_df_1h_recent_agg_pvt = engagement_df_1h_recent_agg_pvt[[x for x in range(24)]]

    return engagement_df_1h_recent_agg_pvt


def get_pvt_agg_recent_engagement_data():
    engagement_df = read_engagement_data()
    cutoff_date = engagement_df["date"].max() - pd.Timedelta(days=180)

    engagement_df_recent = engagement_df.loc[engagement_df['date'] > cutoff_date]

    engagement_df_recent_agg = engagement_df_recent.groupby(['weekday','bin4h_str'])['n_level_attempts'].sum().reset_index()
    engagement_df_recent_agg_pvt = pd.pivot_table(engagement_df_recent_agg, values = 'n_level_attempts', index='weekday', columns = 'bin4h_str')
    engagement_df_recent_agg_pvt = engagement_df_recent_agg_pvt.reindex(['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ])

    engagement_df_recent_agg_pvt = engagement_df_recent_agg_pvt[['0_4h', '4_8h', '8_12h', '12_16h', '16_20h', '20_24h']]

    return engagement_df_recent_agg_pvt


def get_recent_hourly_user_agg_ratio():

    engagement_df = read_engagement_data()
    cutoff_date = engagement_df["date"].max() - pd.Timedelta(days=180)
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
    return hourly_user_df_recent_agg_ratio

def read_hourly_users():
    #
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
         'phrasal-datum-311915-03b34c76b093.json', scope) 
    gc = gspread.authorize(credentials)
    sheet = gc.open("irooni_lettuce")
    worksheet = sheet.worksheet('users_daily_pattern')
    data = worksheet.get_all_values()   
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    df['bin1h'] = df['bin1h'].astype(int)
    df['n_distinct_players_l1_l19'] = df['n_distinct_players_l1_l19'].astype(int)
    df['n_distinct_players_l20_99'] = df['n_distinct_players_l20_99'].astype(int)
    df['n_distinct_players_l100_l299'] = df['n_distinct_players_l100_l299'].astype(int)
    df['n_distinct_players_l300_l799'] = df['n_distinct_players_l300_l799'].astype(int)
    df['n_distinct_players_l800plus'] = df['n_distinct_players_l800plus'].astype(int)
    df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d', utc= True)

    return df



#rewards_df = read_reward_data()

def get_rewards_coin_equivalent(rewards_df):
    rewards_df_agg = rewards_df.groupby(['date','reward_type'])['daily_count'].sum().reset_index()
    rewards_df_agg['reward_coin_equivalent'] = -1
    #boosters
    rewards_df_agg.loc[rewards_df_agg.reward_type == 'bomb_reward', 'reward_coin_equivalent']  = rewards_df_agg.loc[rewards_df_agg.reward_type == 'bomb_reward', 'daily_count'] * (150 / 3)
    rewards_df_agg.loc[rewards_df_agg.reward_type == 'rocket_reward', 'reward_coin_equivalent']  = rewards_df_agg.loc[rewards_df_agg.reward_type == 'rocket_reward', 'daily_count'] * (100 / 3)
    rewards_df_agg.loc[rewards_df_agg.reward_type == 'disco_reward', 'reward_coin_equivalent']  = rewards_df_agg.loc[rewards_df_agg.reward_type == 'disco_reward', 'daily_count'] * (200 / 3)
    #power-ups
    rewards_df_agg.loc[rewards_df_agg.reward_type == 'cell_reward', 'reward_coin_equivalent']  = rewards_df_agg.loc[rewards_df_agg.reward_type == 'cell_reward', 'daily_count'] * (200 / 3)
    rewards_df_agg.loc[rewards_df_agg.reward_type == 'row_reward', 'reward_coin_equivalent']  = rewards_df_agg.loc[rewards_df_agg.reward_type == 'row_reward', 'daily_count'] * (400 / 3)	
    rewards_df_agg.loc[rewards_df_agg.reward_type == 'col_reward', 'reward_coin_equivalent']  = rewards_df_agg.loc[rewards_df_agg.reward_type == 'col_reward', 'daily_count'] * (400 / 3)    
    rewards_df_agg.loc[rewards_df_agg.reward_type == 'shuffle_reward', 'reward_coin_equivalent']  = rewards_df_agg.loc[rewards_df_agg.reward_type == 'shuffle_reward', 'daily_count'] * (100 / 3)    
    rewards_df_agg.loc[rewards_df_agg.reward_type == 'coin_reward', 'reward_coin_equivalent']  = rewards_df_agg.loc[rewards_df_agg.reward_type == 'coin_reward', 'daily_count']
    rewards_df_agg.loc[rewards_df_agg.reward_type == 'heart_reward', 'reward_coin_equivalent']  = rewards_df_agg.loc[rewards_df_agg.reward_type == 'heart_reward', 'daily_count'] * 100     

    return(rewards_df_agg)



#consumption_df = read_consumption_data()

def get_consumptions_coin_equivalent(consumption_df):
    consumption_df['consumable_coin_equivalent'] = -1
    #boosters
    consumption_df.loc[consumption_df.consumable == 'bomb_booster_start', 'consumable_coin_equivalent']  = consumption_df.loc[consumption_df.consumable == 'bomb_booster_start', 'daily_count'] * (150 / 3)
    consumption_df.loc[consumption_df.consumable == 'rocket_booster_start', 'consumable_coin_equivalent']  = consumption_df.loc[consumption_df.consumable == 'rocket_booster_start', 'daily_count'] * (100 / 3)
    consumption_df.loc[consumption_df.consumable == 'disco_booster_start', 'consumable_coin_equivalent']  = consumption_df.loc[consumption_df.consumable == 'disco_booster_start', 'daily_count'] * (200 / 3)
    #power-ups
    consumption_df.loc[consumption_df.consumable == 'cell_pu_used', 'consumable_coin_equivalent']  = consumption_df.loc[consumption_df.consumable == 'cell_pu_used', 'daily_count'] * (200 / 3)
    consumption_df.loc[consumption_df.consumable == 'row_pu_used', 'consumable_coin_equivalent']  = consumption_df.loc[consumption_df.consumable == 'row_pu_used', 'daily_count'] * (400 / 3)
    consumption_df.loc[consumption_df.consumable == 'col_pu_used', 'consumable_coin_equivalent']  = consumption_df.loc[consumption_df.consumable == 'col_pu_used', 'daily_count'] * (400 / 3)
    consumption_df.loc[consumption_df.consumable == 'shuffle_pu_used', 'consumable_coin_equivalent']  = consumption_df.loc[consumption_df.consumable == 'shuffle_pu_used', 'daily_count'] * (100 / 3)
    #extra-moves
    consumption_df.loc[consumption_df.consumable == 'extra_moves_wprice1', 'consumable_coin_equivalent']  = consumption_df.loc[consumption_df.consumable == 'extra_moves_wprice1', 'daily_count'] * (100)
    consumption_df.loc[consumption_df.consumable == 'extra_moves_wprice2', 'consumable_coin_equivalent']  = consumption_df.loc[consumption_df.consumable == 'extra_moves_wprice2', 'daily_count'] * (150 )
    consumption_df.loc[consumption_df.consumable == 'extra_moves_wprice3', 'consumable_coin_equivalent']  = consumption_df.loc[consumption_df.consumable == 'extra_moves_wprice3', 'daily_count'] * (200 )
    consumption_df.loc[consumption_df.consumable == 'extra_moves_wprice4', 'consumable_coin_equivalent']  = consumption_df.loc[consumption_df.consumable == 'extra_moves_wprice4', 'daily_count'] * (250 )
    consumption_df.loc[consumption_df.consumable == 'extra_moves_wprice4plus', 'consumable_coin_equivalent']  = consumption_df.loc[consumption_df.consumable == 'extra_moves_wprice4plus', 'daily_count'] * (1000 )

    return(consumption_df)

def get_daily_unique_users():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
         'phrasal-datum-311915-03b34c76b093.json', scope) 
    gc = gspread.authorize(credentials)
    sheet = gc.open("irooni_lettuce")
    worksheet = sheet.worksheet('users_daily_pattern')
    data = worksheet.get_all_values()   
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    df['n_distinct_players_l1_l19'] = df['n_distinct_players_l1_l19'].astype(int)
    df['n_distinct_players_l20_99'] = df['n_distinct_players_l20_99'].astype(int)
    df['n_distinct_players_l100_l299'] = df['n_distinct_players_l100_l299'].astype(int)
    df['n_distinct_players_l300_l799'] = df['n_distinct_players_l300_l799'].astype(int)
    df['n_distinct_players_l800plus'] = df['n_distinct_players_l800plus'].astype(int)
    df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d', utc= True)

    df['user_count'] = df['n_distinct_players_l1_l19'] + \
        df['n_distinct_players_l20_99'] + \
            df['n_distinct_players_l100_l299'] + \
                df['n_distinct_players_l300_l799'] + \
                    df['n_distinct_players_l800plus'] 
    df = df.groupby(['date'])['user_count'].sum().reset_index()
    return(df)


def get_au():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
         'phrasal-datum-311915-03b34c76b093.json', scope) 
    gc = gspread.authorize(credentials)
    sheet = gc.open("irooni_lettuce")
    worksheet = sheet.worksheet('lettuce')
    data = worksheet.get_all_values()   
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    au_ls = df['irooni'].tolist()
    return({au_ls[0]: au_ls[3]})
    


def read_weekly_engagement_percentile_data():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
         'phrasal-datum-311915-03b34c76b093.json', scope) 
    gc = gspread.authorize(credentials)
    sheet = gc.open("irooni_lettuce")
    worksheet = sheet.worksheet('weekly_engagement_percentiles')
    data = worksheet.get_all_values()   
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    col_names = list(df)
    for col in col_names:
        if col in ['year', 'weekly']:
            df[col] = df[col].astype(int)
        if col not in ['year', 'weekly']:
            df[col] = df[col].astype(float)
    return df


