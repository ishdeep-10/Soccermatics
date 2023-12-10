"""
Plotting passes
==============
"""

import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Sbopen, VerticalPitch
import pandas as pd

file_path = 'C:/Users/acer/Documents/GitHub/open-data/data/competitions.json'
df_comp = pd.read_json(file_path)

file_path = 'C:/Users/acer/Documents/GitHub/open-data/data/matches/43/106.json'
df_match = pd.read_json(file_path)

file_path = 'C:/Users/acer/Documents/GitHub/open-data/data/events/3869321.json'
df = pd.read_json(file_path)
team1, team2 = df['team'].apply(lambda x: x['name']).unique()
#A dataframe of passes
passes = df.loc[df['type'].apply(lambda x: x['name']) == 'Pass'].set_index('id')
    

##############################################################################
# Using mplsoccer's Pitch class

#create pitch
pitch = Pitch(line_color='black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#query
passes_team1 = df.loc[(df['type'].apply(lambda x: x['name']) == 'Pass') & (df['team'].apply(lambda x: x['name']) == team1)].set_index('id')
#finding rows in the df and keeping only necessary columns
df_team1 = passes_team1.filter(['pass','location', 'player'],axis=1)
df_team1['Outcome'] = df_team1['pass'].apply(lambda x: x['outcome']['name'] if 'outcome' in x else None)
df_team1['x'] = df_team1['location'].apply(lambda x: x[0])
df_team1['y'] = df_team1['location'].apply(lambda x: x[1])
df_team1['player_name'] = df_team1['player'].apply(lambda x: x['name'])

#plot them - if shot ended with Goal - alpha 1 and add name
#for team 1
for i, row in df_team1.iterrows():
    if row["player_name"] == 'Frenkie de Jong' and row["Outcome"] == 'Incomplete':
    #make circle 
       pitch.scatter(row.x, row.y, alpha = 1, s = 500, color = "orange", ax=ax['pitch']) 
       #pitch.annotate(row["player_name"], (row.x + 1, row.y - 2), ax=ax['pitch'], fontsize = 12)
       
passes_team2 = df.loc[(df['type'].apply(lambda x: x['name']) == 'Pass') & (df['team'].apply(lambda x: x['name']) == team2)].set_index('id')
df_team2 = passes_team2.filter(['pass','location', 'player'],axis=1)
df_team2['Outcome'] = df_team2['pass'].apply(lambda x: x['outcome']['name'] if 'outcome' in x else None)
df_team2['x'] = df_team2['location'].apply(lambda x: x[0])
df_team2['y'] = df_team2['location'].apply(lambda x: x[1])
df_team2['player_name'] = df_team2['player'].apply(lambda x: x['name'])   

#for team 2 we need to revert coordinates
for i, row in df_team2.iterrows():
    if row["player_name"] == 'Lionel Andrés Messi Cuccittini'  and row["Outcome"] == 'Incomplete':
       pitch.scatter(120 - row.x, 80 - row.y, alpha = 1, s = 500, color = "blue", ax=ax['pitch']) 
       #pitch.annotate(row["player_name"], (120 - row.x + 1, 80 - row.y - 2), ax=ax['pitch'], fontsize = 12)
       
fig.suptitle("Netherlands (FDJ) and Argentina (Messi) Incomplete passes", fontsize = 30)           
plt.show()

##############################################################################
# Plotting shots on one half
# ----------------------------
# To plot shots of only one team on one half we use VerticalPitch() class
# If you set *half* to *True*, you will plot only one half of the pitch.
# It is a nice way of plotting shots since they rarely occur on the defensive half.
# We plot all the shots at once this time, without looping through the dataframe this time.

pitch = VerticalPitch(line_color='black', half = True)
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#plotting all shots
pitch.scatter(df_team2.x, df_team2.y, alpha = 1, s = 500, color = "red", ax=ax['pitch'], edgecolors="black") 
fig.suptitle("Argentina passes against Netherlands", fontsize = 30)           
plt.show()

##############################################################################
# Challenge - try it before looking at the next page
# ----------------------------
# 1) Create a dataframe of passes which contains all the passes in the match
# 2) Plot the start point of every Sweden pass. Attacking left to right.
# 3) Plot only passes made by Caroline Seger (she is Sara Caroline Seger in the database)
# 4) Plot arrows to show where the passes went to.


{'recipient': {'id': 3306, 'name': 'Nathan Aké'}, 'length': 24.242525, 
 'angle': -2.929635, 'height': {'id': 1, 'name': 'Ground Pass'}, 
 'end_location': [36.3, 34.9], 'body_part': {'id': 40, 'name': 'Right Foot'}, 'type': {'id': 65, 'name': 'Kick Off'}}

df_team2['endX'] = df_team2['pass'].apply(lambda x: x['end_location'][0])
df_team2['endY'] = df_team2['pass'].apply(lambda x: x['end_location'][1])

df_enzo = df_team2[df_team2['player_name'] == 'Enzo Fernandez']

fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)

pitch.arrows(df_enzo.x, df_enzo.y,df_enzo.endX, df_enzo.endY, color = "blue", ax=ax['pitch'])
pitch.scatter(df_enzo.x, df_enzo.y, alpha = 0.2, s = 500, color = "blue", ax=ax['pitch'])
        
fig.suptitle("Enzo Fernandez passes against Netherlands", fontsize = 30)
plt.show()



##### Plotting multiple passes on one figure
names = df_team2['player_name'].unique()
df_team2['type'] = df_team2['pass'].apply(lambda x: x['type']['name']  if 'type' in x else None)
df_passes = df_team2[df_team2['type'] != 'Throw-in']

#draw 4x4 pitches
pitch = Pitch(line_color='black', pad_top=20)
fig, axs = pitch.grid(ncols = 4, nrows = 4, grid_height=0.85, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0.04, endnote_space=0.01)

#for each player
for name, ax in zip(names, axs['pitch'].flat[:len(names)]):
    #put player name over the plot
    ax.text(60, -10, name,
            ha='center', va='center', fontsize=14)
    #take only passes by this player
    player_df = df_passes.loc[df_passes["player_name"] == name]
    #scatter
    pitch.scatter(player_df.x, player_df.y, alpha = 0.2, s = 50, color = "blue", ax=ax)
    #plot arrow
    pitch.arrows(player_df.x, player_df.y,
            player_df.endX, player_df.endY, color = "blue", ax=ax, width=1)

#We have more than enough pitches - remove them
for ax in axs['pitch'][-1, 16 - len(names):]:
    ax.remove()

#Another way to set title using mplsoccer
axs['title'].text(0.5, 0.5, 'Argentina passes against Netherland', ha='center', va='center', fontsize=30)
plt.show()


