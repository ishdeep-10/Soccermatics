# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 19:02:58 2023

@author: acer
"""

import pandas as pd
import numpy as np
import json
# plotting
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
# statistical fitting of models
import statsmodels.api as sm
import statsmodels.formula.api as smf
#opening data
import os
import pathlib
import warnings 

pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

##############################################################################
# Opening data
'''
{
  "competition_id" : 43,
  "season_id" : 106,
  "country_name" : "International",
  "competition_name" : "FIFA World Cup",
  "competition_gender" : "male",
  "competition_youth" : false,
  "competition_international" : true,
  "season_name" : "2022",
  "match_updated" : "2023-08-12T16:44:27.619465",
  "match_updated_360" : "2023-08-17T15:55:15.164685",
  "match_available_360" : "2023-08-17T15:55:15.164685",
  "match_available" : "2023-08-12T16:44:27.619465"
}
'''
#load data - store it in train dataframe

file_path = 'C:/Users/acer/Documents/GitHub/open-data/data/matches/43/106.json'
train = pd.read_json(file_path)

match_ids = []
for id in train['match_id']:
    match_ids.append(id)
    
    
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
shots = df.loc[df['type'].apply(lambda x: x['name']) == 'Shot'].set_index('id')
shots['player_name'] = shots['player'].apply(lambda x: x['name'] if pd.notna(x) else None)

shots_messi = shots.loc[shots['player_name'] == 'Lionel Andrés Messi Cuccittini']


