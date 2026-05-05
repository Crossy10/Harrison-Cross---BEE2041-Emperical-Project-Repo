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
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation # for creating plots as animations
import os

os.makedirs(FIG, exist_ok=True) # create figures directory if it doesn't exist
os.makedirs(TAB, exist_ok=True) # create tables directory if it doesn't exist




#------------------------------------------------------------------------------
#--- (1) Data Loading and Cleaning
#------------------------------------------------------------------------------
filename =  'six_nations_RAW-DATA.csv'
six_nations_df = pd.read_csv(DATA_RAW + filename, )
six_nations_df = pd.read_csv(DATA_RAW + filename, keep_default_na=False, na_values=['']) # 


# ────────────────────────────Categorising data────────────────────────────────
six_nations_df["advanced_stats_era"] = np.where(six_nations_df["year"] <= 2019, "2000–2019", "2020–2026") # creating a new column to categorise data into two eras: 2000–2019 and 2020–2026, based on the year column. This is useful since the 2020–2026 era has more advanced stats available.

# ─────────────────────────────Adding new features─────────────────────────────
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


# ────────────────────────────Storing cleaned data─────────────────────────────
six_nations_df.to_csv(DATA + 'six_nations_CLEAN-DATA.csv', index=False)


# ─────────────────Define team colours for consistent plotting─────────────────
TEAM_COLOURS = {
    "England":  "#000000",
    "France":   "#80471C",
    "Ireland":  "#068206",
    "Wales":    "#FF0000",
    "Scotland": "#003E79",
    "Italy":    "#00A6FF",
}


#------------------------------------------------------------------------------
#--- (2) Visualise historical trends in final positions (animated line plot)
#------------------------------------------------------------------------------
def plot_historical_positions(six_nations_df):
    # This function creates an animated line plot to visualize the historical trends in final positions for each team in the Six Nations tournament from 2000 to 2026.

    frames = six_nations_df["year"].unique()
    frames = (list(frames) +[frames[-1]] * 15)
    # extracting the unique years from the dataframe to use as frames for the animation. 
    # Each frame will represent a different year in the tournament, allowing us to see the final positions of the teams over time. 
    # The list is extended by repeating the last year multiple times to allow the final year(frame) to be displayed longer in the animation.

    fig, ax = plt.subplots(figsize=(12, 6)) # creating a figure and axis for the plot with a specified size of 12x6

    def animate(year):# animate function for animation, takes in the current frame (year) and updates the plot accordingly
        ax.clear() # clear the plot to redraw it
        six_nations_df_frame = six_nations_df[six_nations_df['year'] <= year]    
        # filter the dataframe to include only data up to the current frame as it cycles through the years

        for team, grp in six_nations_df_frame.groupby('team'): # group the filtered dataframe by team to plot each team's data separately
            ax.plot(grp['year'], grp['final_position'],
                    marker='o', color=TEAM_COLOURS[team], label=team, linewidth=1.8, alpha=0.8)
            
            last = grp[grp["year"] == grp["year"].max()].iloc[-1]
            ax.annotate(team,
                        xy=(last["year"], last["final_position"]),
                        xytext=(4, 0), textcoords="offset points",
                        fontsize=7, color=TEAM_COLOURS[team], va="center")
            # adding annotations to the plot to label each team's line with the team name at the last data point for that team in the current year (frame). 
             
        if year >= 2020:
            ax.axvline(2019.5, color="grey", linestyle="--",linewidth=1, alpha=0.6)
            ax.text(2019.7, 5.8, "Advanced\nstats begin", fontsize=8, color="black")
            # adding a vertical dashed line before 2020 to indicate the point in time when advanced stats began to be recorded in the dataset.

        if year >=2017:
            ax.axvline(2016.5, color="grey", linestyle="--", linewidth=1, alpha=0.6)
            ax.text(2016.7, 5.8, "New points\nscoring system", fontsize=8, color="black")
        # adding a vertical dashed line before 2017 to indicate the point in time when the new points scoring system was implemented.


        ax.set_xlim(1999.5, 2026.5) # setting the x-axis limits
        ax.set_ylim(6.3, 0.7) # setting the y-axis limits (inverted: 1st at top)
        ax.set_xticks(range(2000, 2027, 2)) # setting the x-axis ticks to be every 2 years from 2000 to 2026
        ax.set_yticks(range(1, 7)) # setting the y-axis ticks to be from 1 to 6, representing the final positions of the teams in the tournament
        ax.set_yticklabels(["1st", "2nd", "3rd", "4th", "5th", "6th"]) 
        ax.set_xlabel("Year")
        ax.set_ylabel("Final Position")
        ax.set_title("Six Nations Final Position by Team")
        ax.grid(axis="y", linestyle="--", alpha=0.25) # adding a grid to the y-axis for better readability
        ax.legend(loc='upper left', fontsize=9, frameon=False, bbox_to_anchor=(1.01, 1)) # adding a legend to the plot, positioned outside the plot area on the upper left

    ani = animation.FuncAnimation(fig, animate, frames=frames, interval=300, repeat=True) 
    # creating the animation using the FuncAnimation function from the matplotlib.animation. It takes in the figure, the animate function, the frames (years), the interval between frames (300 milliseconds), and whether to repeat the animation (True).
    
    ani.save(FIG + "six_nations.gif", writer="pillow", fps=2) # saving the animation as a GIF file in the specified figures directory, using the Pillow writer and setting the frames per second to 2 for a smooth animation.
    plt.show()

plot_historical_positions(six_nations_df) # calling the function to create and display the animated line plot of historical trends in final positions for each team in the Six Nations tournament.



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