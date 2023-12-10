# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 17:11:11 2023

@author: acer
"""

import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Sbopen
import pandas as pd

file_path = 'C:/Users/acer/Documents/GitHub/open-data/data/competitions.json'
df_comp = pd.read_json(file_path)

file_path = 'C:/Users/acer/Documents/GitHub/open-data/data/matches/16/1.json'
df_match = pd.read_json(file_path)

#18245
file_path = 'C:/Users/acer/Documents/GitHub/open-data/data/events/18245.json'
df = pd.read_json(file_path)
df['type_name'] = df['type'].apply(lambda x: x['name'])
df['team_name'] = df['team'].apply(lambda x: x['name'])
df['player_name'] = df['player'].apply(lambda x: x['name'] if pd.notna(x) else None)
df['outcome_name'] = df['pass'].apply(lambda x: x['outcome']['name'] if pd.notna(x) and 'outcome' in x and 'name' in x['outcome'] else None)
df['x'] = df['location'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 1 else np.nan)
df['y'] = df['location'].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 1 else np.nan)
df['endX'] = df['pass'].apply(lambda x: x['end_location'][0] if pd.notna(x) and 'end_location' in x else None)
df['endY'] = df['pass'].apply(lambda x: x['end_location'][1] if pd.notna(x) and 'end_location' in x else None)
df['pass_recipient_name'] =df['pass'].apply(lambda x: x['recipient']['name'] if pd.notna(x) and 'recipient' in x and 'name' in x['recipient'] else None)

#check for index of first sub
sub = df.loc[df["type_name"] == "Substitution"].loc[df["team_name"] == "Liverpool"].iloc[0]["index"]
#make df with successfull passes by England until the first substitution
mask = (df.type_name == 'Pass') & (df.team_name == "Liverpool") & (df.index < sub) & (df.outcome_name.isnull()) & (df.type_name != "Throw-in")
#taking necessary columns
df_pass = df.loc[mask, ['x', 'y', 'endX', 'endY', "player_name", "pass_recipient_name"]]
#adjusting that only the surname of a player is presented.
df_pass["player_name"] = df_pass["player_name"].apply(lambda x: str(x).split()[-1])
df_pass["pass_recipient_name"] = df_pass["pass_recipient_name"].apply(lambda x: str(x).split()[-1])


###For each player we calculate average location of passes made and receptions. 
###Then, we calculate number of passes made by each player
scatter_df = pd.DataFrame()
for i, name in enumerate(df_pass["player_name"].unique()):
    passx = df_pass.loc[df_pass["player_name"] == name]["x"].to_numpy()
    recx = df_pass.loc[df_pass["pass_recipient_name"] == name]["endX"].to_numpy()
    passy = df_pass.loc[df_pass["player_name"] == name]["y"].to_numpy()
    recy = df_pass.loc[df_pass["pass_recipient_name"] == name]["endY"].to_numpy()
    scatter_df.at[i, "player_name"] = name
    #make sure that x and y location for each circle representing the player is the average of passes and receptions
    scatter_df.at[i, "x"] = np.mean(np.concatenate([passx, recx]))
    scatter_df.at[i, "y"] = np.mean(np.concatenate([passy, recy]))
    #calculate number of passes
    scatter_df.at[i, "no"] = df_pass.loc[df_pass["player_name"] == name].count().iloc[0]

#adjust the size of a circle so that the player who made more passes
scatter_df['marker_size'] = (scatter_df['no'] / scatter_df['no'].max() * 1500)

###To calculate edge width we again look at the number of passes between players We need to group the 
###dataframe of passes by the combination of passer and recipient and count passes between them. 
###As the last step, we set the threshold ignoring players that made fewer than 2 passes. 
#counting passes between players
df_pass["pair_key"] = df_pass.apply(lambda x: "_".join(sorted([x["player_name"], x["pass_recipient_name"]])), axis=1)
lines_df = df_pass.groupby(["pair_key"]).x.count().reset_index()
lines_df.rename({'x':'pass_count'}, axis='columns', inplace=True)
#setting a treshold. You can try to investigate how it changes when you change it.
lines_df = lines_df[lines_df['pass_count']>2]


#Drawing pitch
pitch = Pitch(line_color='grey')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#Scatter the location on the pitch
pitch.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='red', edgecolors='grey', linewidth=1, alpha=1, ax=ax["pitch"], zorder = 3)
#annotating player name
for i, row in scatter_df.iterrows():
    pitch.annotate(row.player_name, xy=(row.x, row.y), c='black', va='center', ha='center', weight = "bold", size=16, ax=ax["pitch"], zorder = 4)

fig.suptitle("Nodes location - Liverpool", fontsize = 30)
plt.show()


#plot once again pitch and vertices
pitch = Pitch(line_color='grey')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
pitch.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='red', edgecolors='grey', linewidth=1, alpha=1, ax=ax["pitch"], zorder = 3)
for i, row in scatter_df.iterrows():
    pitch.annotate(row.player_name, xy=(row.x, row.y), c='black', va='center', ha='center', weight = "bold", size=16, ax=ax["pitch"], zorder = 4)

for i, row in lines_df.iterrows():
        player1 = row["pair_key"].split("_")[0]
        player2 = row['pair_key'].split("_")[1]
        #take the average location of players to plot a line between them
        player1_x = scatter_df.loc[scatter_df["player_name"] == player1]['x'].iloc[0]
        player1_y = scatter_df.loc[scatter_df["player_name"] == player1]['y'].iloc[0]
        player2_x = scatter_df.loc[scatter_df["player_name"] == player2]['x'].iloc[0]
        player2_y = scatter_df.loc[scatter_df["player_name"] == player2]['y'].iloc[0]
        num_passes = row["pass_count"]
        #adjust the line width so that the more passes, the wider the line
        line_width = (num_passes / lines_df['pass_count'].max() * 10)
        #plot lines on the pitch
        pitch.lines(player1_x, player1_y, player2_x, player2_y,
                        alpha=1, lw=line_width, zorder=2, color="black", ax = ax["pitch"])

fig.suptitle("Liverpool Passing Network against Real Madrid", fontsize = 30)
plt.show()


#calculate number of successful passes by player
no_passes = df_pass.groupby(['player_name']).x.count().reset_index()
no_passes.rename({'x':'pass_count'}, axis='columns', inplace=True)
#find one who made most passes
max_no = no_passes["pass_count"].max()
#calculate the denominator - 10*the total sum of passes
denominator = 10*no_passes["pass_count"].sum()
#calculate the nominator
nominator = (max_no - no_passes["pass_count"]).sum()
#calculate the centralisation index
centralisation_index = nominator/denominator
print("Centralisation index is ", centralisation_index) #0.05714285714285714
