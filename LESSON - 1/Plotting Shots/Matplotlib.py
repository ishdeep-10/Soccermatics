# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 18:58:52 2023

@author: acer
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.patheffects as path_effects

from PIL import Image
import requests
from io import BytesIO
import highlight_text
from highlight_text import htext
from highlight_text import HighlightText, ax_text, fig_text

df = pd.read_csv("C:/Users/acer/Desktop/Soccermatics/Codes/LESSON - 1/friends-of-tracking-viz-lecture-master/data/pl_goal_summary_data.csv")
df.head(20)

team = "Man City"

title_font = "Arial"
body_font = "Arial"
text_color = "w"
background = "#313332"
filler = "grey"
primary = "red"

mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color
mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10


fig, ax = plt.subplots(figsize=(8,8))
fig.set_facecolor(background)
ax.patch.set_alpha(0)

ax.grid(ls="dotted",lw="0.5",color="lightgrey", zorder=1)

x = df.goals_for.tolist()
y = df.goals_against.tolist()

ax.scatter(x,y,s=120,color=filler,edgecolors=background, alpha=0.3, lw=0.5, zorder=2)


x = df[df.team == team].goals_for.tolist()
y = df[df.team == team].goals_against.tolist()
t = df[df.team == team].team_season.tolist()

ax.plot(x,y, zorder=3, color=text_color)

ax.scatter(x[-1],y[-1],s=120,color=primary,edgecolors=background, alpha=1, lw=.25, zorder=4)
t = ax.text(x[-1],y[-1]-2,t[-1],color=text_color,fontsize=12, ha="center", fontfamily=body_font)
t.set_path_effects([path_effects.withStroke(linewidth=3,foreground=background)])


ssn_start = df[df.team == team].season_id.iloc[0]
ssn_end = df[df.team == team].season_id.iloc[-1]

ssn_start = str(ssn_start)+"/"+str(ssn_start+1)
ssn_end = str(ssn_end)+"/"+str(ssn_end+1)

s = "{}'s goal difference from {} to <{}>\n"
#htext.fig_text(s.format(team,ssn_start,ssn_end),0.15,0.99,highlight_colors=[primary], highlight_weights=["bold"],string_weight="bold",fontsize=22, fontfamily=title_font,color=text_color)

fig.text(0.15,1,"Manchester City's Goal Difference from 2010/11 to 2019/20",fontweight="regular", fontsize=18,fontfamily=title_font, color=text_color)

ax.set_xlabel("Goals For", fontfamily=title_font, fontweight="bold", fontsize=16, color=text_color)
ax.set_ylabel("Goals Against", fontfamily=title_font, fontweight="bold", fontsize= 16, color=text_color)

ax.tick_params(axis="both",length=0)

ax.set_ylim(90,18)
ax.set_xlim(10,120)


spines = ["top","right","bottom","left"]
for s in spines:
    if s in ["top","right"]:
        ax.spines[s].set_visible(False)
    else:
        ax.spines[s].set_color(text_color)




ax2 = fig.add_axes([0.02,0.96,0.15,0.15]) # badge
ax2.axis("off")
#url = "https://logos-world.net/wp-content/uploads/2020/05/Arsenal-Logo.png"
url = "https://logos-world.net/wp-content/uploads/2020/06/Manchester-City-Logo-700x394.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
ax2.imshow(img)

fig.text(0.05, -0.025, "Created by Ishdeep Chadha. Data provided by football-data.co.uk",
        fontstyle="italic",fontsize=9, fontfamily=body_font, color=text_color)


plt.tight_layout()
plt.savefig("C:/Users/acer/Desktop/Soccermatics/Codes/LESSON - 1/advanced_mpl", bbox_inches = "tight",dpi=300)
plt.show()