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
import glob

from pystout import pystout # for creating regression tables in LaTeX format

import subprocess
from pdf2image import convert_from_path


from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.iolib.table import SimpleTable
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
from statsmodels.iolib.summary2 import summary_col


tex_path = TAB + 'regressionTable.tex'
wrapped_path = TAB + 'regressionTable_wrapped.tex'
pdf_path = TAB + 'regressionTable_wrapped.pdf'
png_file = TAB + 'regressionTable.png'

os.makedirs(FIG, exist_ok=True) # create figures directory if it doesn't exist
os.makedirs(TAB, exist_ok=True) # create tables directory if it doesn't exist



#------------------------------------------------------------------------------
#--- (1) Data Loading and Cleaning
#------------------------------------------------------------------------------
filename =  'six_nations_RAW-DATA.csv'
six_nations_df = pd.read_csv(DATA_RAW + filename, )
six_nations_df = pd.read_csv(DATA_RAW + filename, keep_default_na=False, na_values=['']) # 

six_nations_df_inital_clean_copy = six_nations_df.copy() # creating a copy of the initial dataframe for backup and reference purposes, allowing us to compare the cleaned data with the original raw data if needed.

# ────────────────────Exploring the shape of the Dataframe─────────────────────
def explore_dataframe(df):
    # This function takes a DataFrame as input and prints its shape, the number of rows, and the number of columns in a formatted string for better readability.
    print(f"The shape of the DataFrame is: {df.shape} \nThe number of rows in the DataFrame is: {df.shape[0]} \nThe number of columns in the DataFrame is: {df.shape[1]} \n\nSome important information about the DataFrame:")
    df.info(verbose=True)
    
    num_countries = len(df['team'].unique())
    countries_list = [country for country in sorted(df['team'].unique())]
    num_years = len(df['year'].unique())
    years_list = [yr for yr in sorted(df['year'].unique())]
    
    print(f"\n\nThere are {num_countries} Countries represented in the Dataframe; these are: {countries_list} \nThere are {num_years} years of data for the represented in the Dataframe; these are: {years_list}")

explore_dataframe(six_nations_df) # calling the function to explore the shape and structure of the DataFrame, providing insights into the number of rows, columns, unique teams, and years represented in the dataset.

# ─────────────────────────────Adding new features─────────────────────────────
#Try efficiency: average tries scored per game (higher = better attack) 
six_nations_df["average_tries_per_game"] = six_nations_df["tries_scored"] / six_nations_df["matches_played"]

# Try efficiency: average tries conceded per game (lower = better defence)
six_nations_df["average_tries_conceded_per_game"] = six_nations_df["tries_conceded"] / six_nations_df["matches_played"]

# Win rate (cleaner than raw wins since matches_played is always 5)
six_nations_df["win_rate"] = six_nations_df["matches_won"] / six_nations_df["matches_played"]

# points per game ()
six_nations_df["average_points_per_game"] = six_nations_df["points_scored"] / six_nations_df["matches_played"]

# Missed tackle rate as a fraction of total tackle attempts (lower = better defence)
six_nations_df["missed_tackle_rate"] = six_nations_df["missed_tackle"]/(six_nations_df["total_successful_tackles"] + six_nations_df["missed_tackle"])

# Average missed tackle rate per game (lower = better defence)
six_nations_df["average_missed_tackle_rate_per_game"] = six_nations_df["missed_tackle_rate"]/(six_nations_df["matches_played"])


# Attacking efficiency index: defenders beaten per carry
six_nations_df["attack_efficiency"] = six_nations_df["defender_beaten"] / six_nations_df["carries"]

six_nations_df_all_stats_copy = six_nations_df.copy() # creating a copy of the dataframe after adding new features, allowing us to compare the data with the new features to the previous version of the data without the new features if needed.

# ────────────────────────────Storing cleaned data─────────────────────────────
six_nations_df_all_stats_copy.to_csv(DATA + 'six_nations_full_columns_CLEAN-DATA.csv', index=False)

# ────────────────────────────Categorising data────────────────────────────────
six_nations_df["Eras"] = np.where(
    six_nations_df["year"] <= 2016, "traditional_table_points_&_simple_stats_era",
    np.where(six_nations_df["year"] <= 2019, "new_table_points_but_simple_stats_era", "advanced_stats_era")
) # creating a new column "Eras" to categorise the data into three different eras based on the year: traditional table points and simple stats era (up to 2016), new table points but simple stats era (2017-2019), and advanced stats era (2020 onwards). This categorisation allows us to analyse how changes in the tournament structure and the availability of advanced statistics may have influenced team performance and final positions over time.

# ────────────────────────────Storing cleaned data─────────────────────────────
six_nations_df_eras_copy = six_nations_df.copy() # creating a copy of the dataframe

six_nations_df_eras_copy.to_csv(DATA + 'six_nations_full_columns_&_eras_CLEAN-DATA.csv', index=False)

# ─────────────────────────Removing irrelevant data────────────────────────────
six_nations_df = six_nations_df.drop(columns=["matches_played", "kick_bounced", "retained_kick", "try_assist", "attacking_catch_success", "retained_kicks_percent"])

# ────────────────────────────Storing cleaned data─────────────────────────────
six_nations_df_clean = six_nations_df.copy() # creating a copy of the dataframe

six_nations_df_clean.to_csv(DATA + 'six_nations_CLEAN-DATA.csv', index=False)


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
#--- (2) OLS Regression to explore which features are important in winning the Six Nations and achieving a higher final position 
#------------------------------------------------------------------------------


six_nations_regression_df = six_nations_df.copy() # creating a copy of the cleaned dataframe to use for regression analysis

y_var = "final_position"

# X variables
x_vars = [col for col in six_nations_df.columns 
          if col not in ["year", "team", "final_position", "grand_slam", "table_points", "Eras"]]

# Convert everything to numeric for regression, coercing errors to NaN (which we will drop later)
six_nations_regression_df[x_vars] = six_nations_regression_df[x_vars].apply(pd.to_numeric, errors="coerce")
six_nations_regression_df[y_var] = pd.to_numeric(six_nations_regression_df[y_var], errors="coerce")

# Remove infinities and missing values because OLS can't handle them
six_nations_regression_df = six_nations_regression_df.replace([np.inf, -np.inf], np.nan).dropna()

# Define final clean variables
y_var_clean = six_nations_regression_df[y_var]
x_vars_clean = six_nations_regression_df[x_vars]

# OLS model
model_ols = OLS(y_var_clean, add_constant(x_vars_clean)).fit()

print(model_ols.summary()) # printing the summary of the OLS regression results to assess whether the OLS regression worked


###

table = summary_col(
    results=[model_ols], 
    stars=True, 
    float_format="%0.3f", 
    model_names=["Baseline"], 
    info_dict={ "N": lambda x: f"{int(x.nobs)}", "Adj. R2": lambda x: f"{x.rsquared_adj:.3f}" }
    )


raw = table.as_text().split("\n")

formatted = []
skip_next = False

for i in range(len(raw)):

    if skip_next:
        skip_next = False
        continue

    line = raw[i]

    formatted.append(line)

    # detect coefficient line (variable names)
    is_var_row = any(var in line for var in x_vars) and ("const" not in line.lower())

    if is_var_row:
        # next line is assumed SE line
        if i + 1 < len(raw):
            se_line = raw[i + 1]
            formatted.append(se_line)
            skip_next = True

        # add BLANK line AFTER SE line (your key requirement)
        formatted.append("")

# insert underline before constant
final_output = []
for i, line in enumerate(formatted):

    # detect constant line
    if "const" in line.lower() or "constant" in line.lower():
        final_output.append("=" * 80)  # solid underline BEFORE constant

    final_output.append(line)

# plot
fig, ax = plt.subplots(figsize=(12, 7))
ax.axis("off")

ax.text(
    0, 1,
    "\n".join(final_output),
    family="monospace",
    fontsize=10,
    va="top"
)

plt.show()

"""plt.savefig(TAB + "ols_regression_results.png", bbox_inches="tight", dpi=300)
plt.close()"""


pystout(models= [model_ols],
        file=TAB+'regressionTable.tex',
        addnotes=['All dependent variables are call back rates in percent.',
                  'Standard errors are presented in parentheses. *: p<0.10; **:p<0.05; ***:p<0.01.'],
        digits=2,
        endog_names=["Final Position"],
        varlabels={'const':'Constant',                   'matches_won':'Matches Won',
                   'matches_drawn':'Matches Drawn',
                   'matches_lost':'Matches Lost',
                   'points_scored':'Points Scored',
                   'points_conceded':'Points Conceded',
                   'points_difference':'Points Difference',
                   'tries_scored':'Tries Scored',
                   'tries_conceded':'Tries Conceded',
                   'bonus_points':'Bonus Points',
                   'carries':'Carries',
                   'offload':'Offload',
                   'defender_beaten':'Defender Beaten',
                   'missed_tackle':'Missed Tackle',
                   'lineout_steals':'Lineout Steals',
                   'lineout_throws_won':'Lineout Throws Won',
                   'kicks_in_play':'Kicks In Play',
                   'kick_metres':'Kick Metres',
                   'dominant_contact':'Dominant Contact',
                   'dominant_tackle_contact':'Dominant Tackle Contact',
                   'total_successful_tackles':'Total Successful Tackles',
                   'box_kicks':'Box Kicks',
                   'total_turnovers_won':'Total Turnovers Won',
                   'successful_goals':'Successful Goals',
                   'carry_metres_made':'Carry Metres Made',
                   'post_contact_metres':'Post Contact Metres',
                   'initial_break':'Initial Break',
                   'goal_kick_success_percent':'Goal Kick Success Percent',
                   'tackle_success_percent':'Tackle Success Percent',
                   'lineout_success_percent':'Lineout Success Percent',
                   'metres_per_carry':'Metres Per Carry',
                   'post_contact_metres_per_carry':'Post Contact Metres Per Carry',
                   'total_jackals':'Total Jackals',
                   'kick_metres_per_kick':'Kick Metres Per Kick',
                   'average_tries_per_game':'Average Tries Per Game',
                   'average_tries_conceded_per_game':'Average Tries Conceded Per Game',
                   'win_rate':'Win Rate',
                   'average_points_per_game ':'Average Points Per Game ',
                   'missed_tackle_rate ':'Missed Tackle Rate ',
                  'average_missed_tackle_rate_per_game ':'Average Missed Tackle Rate Per Game ',
                  'attack_efficiency ':'Attack Efficiency '
                    },
        mgroups={'Baseline':1},
        modstat={'nobs':'Obs','rsquared_adj ':'Adj. R\sym{2}','fvalue ':'F-stat'},
        stars =  {.1:'*',.05:'**',.01:'***'}
        )


# Read the pystout-generated .tex fragment
with open(tex_path, 'r') as f:
    table_content = f.read()

# Wrap it in a full LaTeX document
wrapped_tex = r"""
\documentclass{article}
\usepackage{booktabs}
\usepackage{geometry}
\geometry{margin=0.5in, landscape}
\usepackage{caption}
\usepackage{adjustbox}

\begin{document}
\pagestyle{empty}
\thispagestyle{empty}

\begin{adjustbox}{max width=\textwidth, max totalheight=\textheight, keepaspectratio}
""" + table_content + r"""
\end{adjustbox}

\end{document}
"""

# Write the wrapped document
with open(wrapped_path, 'w') as f:
    f.write(wrapped_tex)

# Compile to PDF
subprocess.run(
    ['pdflatex', '-interaction=nonstopmode', '-output-directory', TAB, wrapped_path],
    check=True
)

# Convert to PNG
images = convert_from_path(pdf_path, dpi=300)
for i, image in enumerate(images):
    image.save(TAB + f'regressionTable_page_{i+1}.png', 'PNG')
    print(f"Saved page {i+1}")


# Delete specific extensions in a directory
for ext in ['*.aux', '*.log', '*.pdf', '*.tex']:
    for f in glob.glob(TAB + ext):
        os.remove(f)

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