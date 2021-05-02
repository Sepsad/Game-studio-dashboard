
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

