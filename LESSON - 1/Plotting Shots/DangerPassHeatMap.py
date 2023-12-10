# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 19:12:54 2023

@author: acer
"""

import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Sbopen
import pandas as pd

file_path = 'C:/Users/acer/Documents/GitHub/open-data/data/competitions.json'
df_comp = pd.read_json(file_path)

file_path = 'C:/Users/acer/Documents/GitHub/open-data/data/matches/43/106.json'
df_match = pd.read_json(file_path)

df_match["home_team_name"] = df_match['home_team'].apply(lambda x: x['home_team_name'])
df_match["away_team_name"] = df_match['away_team'].apply(lambda x: x['away_team_name'])

team = "Argentina"
#get list of games by our team, either home or away
match_ids = df_match.loc[(df_match["home_team_name"] == team) | (df_match["away_team_name"] == team)]["match_id"].tolist()
#calculate number of games
no_games = len(match_ids)


file_list = []
pattern1 = 'C:/Users/acer/Documents/GitHub/open-data/data/events/'
pattern2 = '.json'
for i in match_ids:
    result = pattern1 + str(i) +pattern2
    file_list.append(result)
    
dfs = [] # an empty list to store the data frames
for file in file_list:
    data = pd.read_json(file) # read data frame from json file
    dfs.append(data) # append the data frame to the list

df = pd.concat(dfs, ignore_index=True) # concatenate all the data frames in the list.
df['team_name'] = df['team'].apply(lambda x: x['name'])
df['type_name'] = df['type'].apply(lambda x: x['name'])
df['outcome_name'] = df['pass'].apply(lambda x: x['outcome']['name'] if pd.notna(x) and 'outcome' in x and 'name' in x['outcome'] else None)

df['x'] = df['location'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 1 else np.nan)
df['y'] = df['location'].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 1 else np.nan)
df['end_x'] = df['pass'].apply(lambda x: x['end_location'][0] if pd.notna(x) and 'end_location' in x else None)
df['end_y'] = df['pass'].apply(lambda x: x['end_location'][1] if pd.notna(x) and 'end_location' in x else None)
df['player_name'] = df['player'].apply(lambda x: x['name'] if pd.notna(x) else None)

danger_passes = pd.DataFrame()
for period in [1, 2]:
    #keep only accurate passes by Argentina that were not set pieces in this period
    mask_pass = (df.team_name == team) & (df.type_name == "Pass") & (df.outcome_name.isnull()) & (df.period == period)
    #keep only necessary columns
    passes = df.loc[mask_pass, ["x", "y", "end_x", "end_y", "minute", "second", "player_name"]]
    #keep only Shots by Argentina in this period
    mask_shot = (df.team_name == team) & (df.type_name == "Shot") & (df.period == period)
    #keep only necessary columns
    shots = df.loc[mask_shot, ["minute", "second"]]
    #convert time to seconds
    shot_times = shots['minute']*60+shots['second']
    shot_window = 15
    #find starts of the window
    shot_start = shot_times - shot_window
    #condition to avoid negative shot starts
    shot_start = shot_start.apply(lambda i: i if i>0 else (period-1)*45)
    #convert to seconds
    pass_times = passes['minute']*60+passes['second']
    #check if pass is in any of the windows for this half
    pass_to_shot = pass_times.apply(lambda x: True in ((shot_start < x) & (x < shot_times)).unique())

    #keep only danger passes
    danger_passes_period = passes.loc[pass_to_shot]
    #concatenate dataframe with a previous one to keep danger passes from the whole tournament
    danger_passes = pd.concat([danger_passes, danger_passes_period], ignore_index = True)
    

#plot pitch
pitch = Pitch(line_color='black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#scatter the location on the pitch
pitch.scatter(danger_passes.x, danger_passes.y, s=100, color='blue', edgecolors='grey', linewidth=1, alpha=0.2, ax=ax["pitch"])
#uncomment it to plot arrows
#pitch.arrows(danger_passes.x, danger_passes.y, danger_passes.end_x, danger_passes.end_y, color = "blue", ax=ax['pitch'])
#add title
fig.suptitle('Location of danger passes by ' + team, fontsize = 30)
plt.show()

#plot vertical pitch
pitch = Pitch(line_zorder=2, line_color='black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#get the 2D histogram
bin_statistic = pitch.bin_statistic(danger_passes.x, danger_passes.y, statistic='count', bins=(6, 5), normalize=False)
#normalize by number of games
bin_statistic["statistic"] = bin_statistic["statistic"]/no_games
#make a heatmap
pcm  = pitch.heatmap(bin_statistic, cmap='Reds', edgecolor='grey', ax=ax['pitch'])
#legend to our plot
ax_cbar = fig.add_axes((1, 0.093, 0.03, 0.786))
cbar = plt.colorbar(pcm, cax=ax_cbar)
fig.suptitle('Danger passes by ' + team + " per game", fontsize = 30)
plt.show()

#keep only surnames
danger_passes["player_name"] = danger_passes["player_name"].apply(lambda x: str(x).split()[-1])
#count passes by player and normalize them
pass_count = danger_passes.groupby(["player_name"]).x.count()/no_games
#make a histogram
ax = pass_count.plot.bar(pass_count)
#make legend
ax.set_xlabel("")
ax.set_ylabel("Number of danger passes per game")
plt.show()
        