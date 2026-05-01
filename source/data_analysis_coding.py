""" data_analysis_coding.py                                      Harrison Cross
---|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8

This file examines what drives success in the Six Nations Rugby Tournament, using the data obtained from webscraping the Six Nations website.

The data has been provided in the GitHub repo, and also in replicateable code and thus in csv format , and hence is read in directly with pd.read_csv().
In order to replicate this file, please see the requirements found in the README.md file in GitHub repo, as well as change the ROOt directory to your own local directory.
"""

#------------------------------------------------------------------------------
#--- (0) Imports and directory locations
#------------------------------------------------------------------------------
ROOT = "/home/hcross27/BEE2041/Emperical_Project/Harrison-Cross---BEE2041-Emperical-Project-Repo/"

DATA_RAW = ROOT+'data/raw_data/'
DATA = ROOT+'data/clean_data/'
FIG  = ROOT+'results/figures/'
TAB  = ROOT+'results/tables/'

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation # for creating plots as animations
import os

os.makedirs(FIG, exist_ok=True)
os.makedirs(TAB, exist_ok=True)

#------------------------------------------------------------------------------
#--- (1) Data Loading and Cleaning
#------------------------------------------------------------------------------
filename =  'six_nations_RAW-DATA.csv'
six_nations_df = pd.read_csv(DATA_RAW + filename, )
six_nations_df = pd.read_csv(DATA_RAW + filename, keep_default_na=False, na_values=[''])

# Deriving new features
#Try efficiency: tries scored relative to points scored
six_nations_df["try_rate"] = six_nations_df["tries_scored"] / six_nations_df["matches_played"]
six_nations_df["tries_conceded_rate"] = six_nations_df["tries_conceded"] / six_nations_df["matches_played"]

# Win rate (cleaner than raw wins since matches_played is always 5)
six_nations_df["win_rate"] = six_nations_df["matches_won"] / six_nations_df["matches_played"]

# points per game ()
six_nations_df["points_per_game"] = six_nations_df["points_scored"] / six_nations_df["matches_played"]

# Missed tackle rate as a fraction of total tackle attempts (lower = better defence)
six_nations_df["missed_tackle_rate"] = six_nations_df["missed_tackle"]/(six_nations_df["total_successful_tackles"] + six_nations_df["missed_tackle"])

# Attacking efficiency index: defenders beaten per carry
six_nations_df["attack_efficiency"] = six_nations_df["defender_beaten"] / six_nations_df["carries"]

pd.save_csv(six_nations_df, DATA + 'six_nations_CLEAN-DATA.csv', index=False)

#historical table points trend figure 
frames = six_nations_df["year"].unique()# get unique years for animation frames
frames = (list(frames) +
    [frames[-1]] * 10        # pause at end
)

fig, ax = plt.subplots(figsize=(12, 6))

def animate(frame):# animate function for animation, takes in the current frame (year) and updates the plot accordingly
    ax.clear()
    six_nations_df_frame = six_nations_df[six_nations_df['year'] <= frame]

    for team, grp in six_nations_df_frame.groupby('team'):
        ax.plot(grp['year'], grp['table_points'],
                marker='o', label=team, linewidth=1.8, alpha=0.8)

        # Label each point with its value
        for idx in range(len(grp)):
            ax.text(
                grp['year'].iloc[idx],
                grp['table_points'].iloc[idx] + 0.15,  # slight offset above the point
                str(int(grp['table_points'].iloc[idx])),
                ha='center',
                fontsize=7,
                alpha=0.8
            )

    ax.set_xlabel("Year")
    ax.set_ylabel("Table Points")
    ax.set_title("Six Nations Table Points by Team (2000–2026)")
    ax.set_xlim(six_nations_df['year'].min() - 0.5,
                six_nations_df['year'].max() + 0.5)
    ax.set_ylim(0, six_nations_df['table_points'].max() + 2)
    ax.legend(loc="upper left", fontsize=9, frameon=False,
              bbox_to_anchor=(1.01, 1))
    
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=frames,
    interval=500,    # ms per frame — adjust to taste
    repeat=False
)

plt.show()

# Optional: save as gif or mp4
# ani.save("six_nations.gif", writer="pillow", fps=2)
# ani.save("six_nations.mp4", writer="ffmpeg", fps=2)

#------------------------------------------------------------------------------
#--- (2) Examine heterogeneity in basic way
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#--- (3) Estimate causal forest
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#--- (4) Visualise causal forest results
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#--- (5) Visualise heterogeneity by subgroups
#            Suppose we want to explore heterogeneity in the treatment effect, 
#            based on the level of education ('ba_quality' in this case).
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#--- (6) Which features are important in generating causal forest?
#        Commented out as a bit slow
#------------------------------------------------------------------------------