# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 18:24:29 2023

@author: acer
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

fig , ax = plt.subplots(figsize = (8,8))
fig.set_facecolor("white")

ax.grid(linewidth = 0.25, zorder = 1)

ax.set_title("This is a plot using default matplotlib")

np.random.seed(402)
x = np.random.uniform(0,1,50)
y = np.random.uniform(0,1,50)

ax.scatter(x,y,s=400,edgecolor = "white",linewidth = 0.5,zorder=2)

ax.set_xlim(0,1)
ax.set_ylim(0,1)

plt.tight_layout()
plt.savefig("C:/Users/acer/Desktop/Soccermatics/Codes/LESSON - 1/default_mpl", bbox_inches = "tight",dpi=300)
plt.show()