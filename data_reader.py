
import gspread
import sys
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

chest_type_dict = {'0' : 'REWARD_TYPE_LEVEL_CHEST',
'1' : 'REWARD_TYPE_STAR_CHEST',
'2' : 'REWARD_TYPE_DAILY_BONUS',
'3' : 'REWARD_TYPE_TREASURE_CHEST',
'4' : 'REWARD_TYPE_TEAM_CHEST',
'5' : 'REWARD_TYPE_DAILY_TASK',
'6' : 'REWARD_TYPE_TEAM_TOURNAMENT',
'7' : 'OTHER_REWARD'}

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