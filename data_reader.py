
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

    return df

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


