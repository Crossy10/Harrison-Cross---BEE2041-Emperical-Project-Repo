""" data_analysis_coding.py                                      Harrison Cross
---|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8

This file examines what drives success in the Six Nations Rugby Tournament, using the data obtained from webscraping the Six Nations website.

The data has been provided in the GitHub repo, and also in replicateable code and thus in csv format , and hence is read in directly with pd.read_csv().
In order to replicate this file, please see the requirements found in the README.md file in GitHub repo, as well as change the ROOt directory to your own local directory.
"""

#------------------------------------------------------------------------------
#--- (0) Loading Libraries, Imports, directory locations and defining functions & colours for consistent plotting
#------------------------------------------------------------------------------
# ──────────────Setting up the root directory and subdirectories─────────────── 
ROOT = "/home/hcross27/BEE2041/Emperical_Project/Harrison-Cross---BEE2041-Emperical-Project-Repo/"

DATA_RAW = ROOT+'data/raw_data/'
DATA = ROOT+'data/clean_data/'
FIG  = ROOT+'results/figures/'
TAB  = ROOT+'results/tables/'

tex_path = TAB + 'regressionTable.tex'
wrapped_path = TAB + 'regressionTable_wrapped.tex'
pdf_path = TAB + 'regressionTable_wrapped.pdf'
png_file = TAB + 'regressionTable.png'

# ──────────────────────Loading Libraries and Imports──────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation # for creating plots as animations
import os


from tkinter import Image


import glob

from pystout import pystout # for creating regression tables in LaTeX format

import subprocess
from pdf2image import convert_from_path
from PIL import Image, ImageChops
from statsmodels.miscmodels.ordinal_model import OrderedModel


import scipy.stats as stats


os.makedirs(FIG, exist_ok=True) # create figures directory if it doesn't exist
os.makedirs(TAB, exist_ok=True) # create tables directory if it doesn't exist

# ─────────────────Define team colours for consistent plotting─────────────────
TEAM_COLOURS = {
    "England":  "#000000",
    "France":   "#80471C",
    "Ireland":  "#068206",
    "Wales":    "#FF0000",
    "Scotland": "#003E79",
    "Italy":    "#00A6FF",
}

TEAM_COLOURS_for_GS = {
    "England":  "#000000",
    "France":   "#103FDA",
    "Ireland":  "#068206",
    "Wales":    "#FF0000",
}

# ──────────────────────Defining Functions used in code─────────────────────
def explore_dataframe(df):
    print(f"The shape of the DataFrame is: {df.shape} \nThe number of rows in the DataFrame is: {df.shape[0]} \nThe number of columns in the DataFrame is: {df.shape[1]} \n\nSome important information about the DataFrame:")
    df.info(verbose=True)
    
    num_countries = len(df['team'].unique())
    countries_list = [country for country in sorted(df['team'].unique())]
    num_years = len(df['year'].unique())
    years_list = [int(yr) for yr in sorted(df['year'].unique().tolist())]
    
    print(f"\n\nThere are {num_countries} Countries represented in the Dataframe; these are: {countries_list} \nThere are {num_years} years of data for the represented in the Dataframe; these are: {years_list}")


def make_frames(years, pause_end=12):
    years = sorted(years)
    return list(years) + [years[-1]] * pause_end


def save_gif(anim, name, fps=2):
    path = FIG + name
    anim.save(path, writer="pillow", fps=fps)

def figure_size_for_plots():
    return (12, 6)

def create_scatter_plot(x, y, ax, team):
            ax.scatter(x, y, color=TEAM_COLOURS[team], s=60, alpha=0.8, edgecolors="white", linewidth=0.5, label=team)

def fit_line_for_scatter_plot(x, y, ax):
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), color='black', linestyle='--', linewidth=2, alpha=0.6)
    return p(x)

def legend_location(ax):
    ax.legend(loc='upper left', fontsize=9, frameon=False, bbox_to_anchor=(1.01, 1))

def create_line_plot(x, y, ax, team):
    ax.plot(x, y, marker='o', color=TEAM_COLOURS[team], label=team, linewidth=1.8, alpha=0.8)

def line_plot_annotation(name, x, y, ax, team):
                ax.annotate(name, xy=(x,y), xytext=(4, 0), textcoords="offset points", fontsize=7, color=TEAM_COLOURS[team], va="center")

#------------------------------------------------------------------------------
#--- (1) Data Loading and Cleaning
#------------------------------------------------------------------------------
filename =  'six_nations_RAW-DATA.csv'
six_nations_df = pd.read_csv(DATA_RAW + filename, )
six_nations_df = pd.read_csv(DATA_RAW + filename, keep_default_na=False, na_values=['']) # 

six_nations_df_inital_clean_copy = six_nations_df.copy() # creating a copy of the initial dataframe for backup and reference purposes, allowing us to compare the cleaned data with the original raw data if needed.

# ────────────────────Exploring the shape of the Dataframe─────────────────────

explore_dataframe(six_nations_df) # calling the function to explore the shape and structure of the DataFrame

# ─────────────────────────────Adding new features─────────────────────────────
# Win rate (cleaner than raw wins since matches_played is always 5)
six_nations_df["win_rate"] = six_nations_df["matches_won"] / six_nations_df["matches_played"]

#Try efficiency: average tries scored per game (higher = better attack) 
six_nations_df["try_efficiency"] = six_nations_df["tries_scored"] / six_nations_df["matches_played"]

# Try efficiency: average tries conceded per game (lower = better defence)
six_nations_df["try_conceded_efficiency"] = six_nations_df["tries_conceded"] / six_nations_df["matches_played"]

# points difference per game ()
six_nations_df["point_difference_efficiency"] = six_nations_df["points_difference"] / six_nations_df["matches_played"]

# Attacking efficiency index: defenders beaten per carry
six_nations_df["attack_efficiency"] = six_nations_df["defender_beaten"] / six_nations_df["carries"]

# Average offload per game
six_nations_df["avg_offload_per_game"] = six_nations_df["offload"] / six_nations_df["matches_played"]

# Average lineout steals per game
six_nations_df["avg_lineout_steals_per_game"] = six_nations_df["lineout_steals"] / six_nations_df["matches_played"]

# Average kicks in play per game
six_nations_df["avg_kicks_in_play"] = six_nations_df["kicks_in_play"] / six_nations_df["matches_played"]

# Average kicks meters per game
six_nations_df["avg_kick_meters_per_game"] = six_nations_df["kick_metres"] / six_nations_df["matches_played"]

# Average Dominant tackle contact per game
six_nations_df["avg_dominant_tackle_contact_per_game"] = six_nations_df["dominant_tackle_contact"] / six_nations_df["matches_played"]

# Average kicks meters per game
six_nations_df["avg_turnovers_won_per_game"] = six_nations_df["total_turnovers_won"] / six_nations_df["matches_played"]

six_nations_df_all_stats_copy = six_nations_df.copy() # creating a copy of the dataframe after adding new features, allowing us to compare the data with the new features to the previous version of the data without the new features if needed.

explore_dataframe(six_nations_df_all_stats_copy)

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

explore_dataframe(six_nations_df_clean)
print("""
      
      
      """)


#------------------------------------------------------------------------------
#--- (2) Creating visualisation of historical trends in final positions by team (animated line graph)
#------------------------------------------------------------------------------

# Creating a function that creates an animated line plot to visualize the historical trends in final positions for each team in the Six Nations tournament from 2000 to 2026.
def plot_historical_positions(six_nations_df):
    frames = make_frames(six_nations_df["year"].unique(), pause_end=12)

    fig, ax = plt.subplots(figsize=figure_size_for_plots()) # creating a figure and axis for the plot

    def animate(year):# animate function for animation, takes in the current frame (year) and updates the plot accordingly
        ax.clear() # clear the plot to redraw it
        six_nations_df_frame = six_nations_df[six_nations_df['year'] <= year]    
        # filter the dataframe to include only data up to the current frame as it cycles through the years

        for team, grp in six_nations_df_frame.groupby('team'): # group the filtered dataframe by team to plot each team's data separately
            create_line_plot(grp['year'], grp['final_position'], ax, team)
            
            last = grp[grp["year"] == grp["year"].max()].iloc[-1]
            line_plot_annotation(team, last["year"], last["final_position"], ax, team)
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
        legend_location(ax) # adding a legend to the plot, positioned outside the plot area on the upper left

    ani = animation.FuncAnimation(fig, animate, frames=frames, interval=300, repeat=True) 
    # creating the animation using the FuncAnimation function from the matplotlib.animation. It takes in the figure, the animate function, the frames (years), the interval between frames (300 milliseconds), and whether to repeat the animation (True).
    
    save_gif(ani, "six_nations.gif", fps=2)

plot_historical_positions(six_nations_df) # calling the function to create and save the animated line plot.

#------------------------------------------------------------------------------
#--- (3) Creating visualisation of grand slams by team (bar chart)
#------------------------------------------------------------------------------

# Creating a function that creates a bar chart of the number of grand slams achieved by each team in the Six Nations tournament from 2000 to 2026.

def plot_grand_slams(six_nations_df):
    grand_slams = six_nations_df[six_nations_df["matches_won"] == 5].groupby("team").size().reset_index(name="grand_slams")
    # filtering the dataframe to include only grand slam rows and grouping the data by team and counting the number of grand slams for each team. The result is stored to a new dataframe

    grand_slams = grand_slams.sort_values(by="grand_slams", ascending=True)

    plt.figure(figsize=figure_size_for_plots()) # creating a figure for the plot 

    bars = plt.barh(grand_slams["team"], grand_slams["grand_slams"], color=[TEAM_COLOURS_for_GS[team] for team in grand_slams["team"]], alpha=0.8) 
    # creating the bar chart, where the bars are colored according to the predefined team colors.

    plt.xlabel("Number of Grand Slams") # setting the x-axis label
    plt.ylabel("Team") # setting the y-axis label
    plt.title("Number of Grand Slams by Team that have won the Six Nations (2000-2026)") # setting the title of the plot
    plt.xticks(range(0, grand_slams["grand_slams"].max() + 1, 1)) # setting the y-axis ticks
    plt.grid(linestyle="--", alpha=0.25) # adding a grid 

    for bar in bars: # adding text labels on top of each bar to show the exact number of grand slams for each team
        width = bar.get_width()
        plt.text(width + 0.05, bar.get_y() + bar.get_height() / 2, str(int(width)), va='center')

    plt.savefig(FIG + "grand_slams.png") # saving the plot as a PNG file 

plot_grand_slams(six_nations_df) # calling the function to create and display the bar chart of the number of grand slams achieved by each team in the Six Nations tournament.

#------------------------------------------------------------------------------
#--- (4) Creating visualisation of kicks in play and their relationship with final position (dual panel line graph and scatter plot)
#------------------------------------------------------------------------------
six_nations_df_2020_onwards = six_nations_df[six_nations_df["year"]>=2020]

def plot_kicks_in_play(six_nations_df_2020_onwards):
    frames = make_frames(six_nations_df_2020_onwards["year"].unique(), pause_end=15) # extracting unique years from 2020 onwards to use as frames for the animation, and extending the list of frames by repeating the last year multiple times to allow the final year (frame) to be displayed longer in the animation.

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figure_size_for_plots()) # creating a figure and axis for the plot
    fig.subplots_adjust(wspace=0.6)

    def animate(year):
        ax1.clear() # clear the first subplot to redraw it
        ax2.clear() # clear the second subplot to redraw it
        six_nations_df_frame = six_nations_df_2020_onwards[six_nations_df_2020_onwards['year'] <= year]    
        # filter the dataframe to include only data up to the current frame as it cycles through the years

        for team, grp in six_nations_df_frame.groupby('team'):
            create_line_plot(grp['year'], grp['avg_kicks_in_play'], ax1, team) 
            
            create_scatter_plot(grp['avg_kicks_in_play'], grp['final_position'], ax2, team)
            
            last = grp[grp["year"] == grp["year"].max()].iloc[-1]
            
            line_plot_annotation(team, last["year"], last["avg_kicks_in_play"], ax1, team)
            # adding annotations to the plot to label each team's line with the team name at the last data point for that team in the current year (frame). 

        # Tournament-average overlay
        avg_by_year = six_nations_df_frame.groupby("year")["avg_kicks_in_play"].mean()
        ax1.plot(
            avg_by_year.index, avg_by_year.values,
            color="purple", linewidth=2, linestyle="--",
            alpha=0.55, label="Tournament avg",
        )
        ax1.annotate("Tournament average",
                     xy=(avg_by_year.index[-1], avg_by_year.values[-1]),
                     xytext=(4, 0), textcoords="offset points",
                     fontsize=7, va="center")
     

        ax1.set_xlim(2019.5, 2026.5) # setting the x-axis limits
        ax1.set_ylim(min(six_nations_df_2020_onwards['avg_kicks_in_play'])-0.5, max(six_nations_df_2020_onwards['avg_kicks_in_play'])+0.5) # setting the y-axis limits
        ax1.set_xticks(range(2020, 2027, 1)) # setting the x-axis ticks to be every year from 2020 to 2026
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Average Kicks in Play per Game")
        ax1.set_title("Average Kicks in Play per Game Over Time")
        ax1.grid(axis="y", linestyle="--", alpha=0.25) # adding a grid to the y-axis for better readability
        legend_location(ax1) # adding a legend to the plot, positioned outside the plot area on the upper left
            
        if year == 2026: # adding a regression line to the scatter plot in the final frame (2026) to show the overall trend in the relationship between average kicks in play per game and final position in the tournament.
            fit_line_for_scatter_plot(six_nations_df_frame['avg_kicks_in_play'], six_nations_df_frame['final_position'], ax2) # fitting a linear regression line to the scatter plot data and plotting it as a dashed grey line to show the overall trend in the relationship between average kicks in play per game and final position in the tournament.

        ax2.set_title("Average Kicks in Play per Game vs Final Position")

        ax2.set_xlabel("Average Kicks in Play per Game")
        ax2.set_xlim(min(six_nations_df_2020_onwards['avg_kicks_in_play'])-0.5, max(six_nations_df_2020_onwards['avg_kicks_in_play'])+0.5) # setting the x-axis limits to be slightly wider than the range of average kicks in play per game in the dataset for better visualization

        ax2.set_ylabel("Final Position")
        ax2.set_ylim(6.3, 0.7) # setting the y-axis limits (inverted: 1st at top)
        ax2.set_yticks(range(1, 7)) # setting the y-axis ticks to be from 1 to 6, representing the final positions of the teams in the tournament
        ax2.set_yticklabels(["1st", "2nd", "3rd", "4th", "5th", "6th"]) 

        ax2.grid(linestyle="--", alpha=0.25) # adding a grid to the y-axis for better readability

        legend_location(ax2) # adding a legend to the scatter plot, positioned outside the plot area on the upper left
        
        fig.suptitle("How average Kicks in Play per Game Relates to Final Position in the Six Nations Tournament",
            fontsize=13, fontweight="bold",
        )

    ani = animation.FuncAnimation(fig,animate, frames=frames, interval=300, repeat=True)
    
    save_gif(ani, "kicks_in_play_dual_panel.gif", fps=2)
    
plot_kicks_in_play(six_nations_df_2020_onwards) # calling the function to create and save the dual panel line graph and scatter plot of average kicks in play per game and their relationship with final position in the Six Nations tournament.



#------------------------------------------------------------------------------
#--- (5) Logit Regression to explore which features are important in winning the Six Nations and achieving a higher final position 
#------------------------------------------------------------------------------


six_nations_regression_df = six_nations_df.copy() # creating a copy of the cleaned dataframe to use for regression analysis

regression_columns = ['win_rate', 'try_efficiency','try_conceded_efficiency',
                      'point_difference_efficiency','attack_efficiency ', 
                      'avg_offload_per_game', 'goal_kick_success_percent',
                      'tackle_success_percent', 'lineout_success_percent',
                      'avg_lineout_steals_per_game', 'metres_per_carry', 
                      'post_contact_metres_per_carry','avg_kicks_in_play',
                      'avg_kick_metres_per_game', 
                      'avg_dominant_tackle_contact_per_game', 
                      'avg_turnovers_won_per_game']


y_var = "final_position"

# X variables
x_vars = [col for col in six_nations_df.columns if col in regression_columns]

# Convert everything to numeric for regression, coercing errors to NaN (which we will drop later)
six_nations_regression_df[x_vars] = six_nations_regression_df[x_vars].apply(pd.to_numeric, errors="coerce")
six_nations_regression_df[y_var] = pd.to_numeric(six_nations_regression_df[y_var], errors="coerce")

# Remove infinities and missing values because OLS can't handle them
six_nations_regression_df = six_nations_regression_df.replace([np.inf, -np.inf], np.nan).dropna()

# Define final clean variables
y_var_clean = six_nations_regression_df[y_var]
x_vars_clean = six_nations_regression_df[x_vars]

# Logit regression with ordered dependent variable (final position 1-6) because we have a non-linear relationship and the dependent variable is ordinal (lower final position = better performance)
model_ordered = OrderedModel(y_var_clean, x_vars_clean,distr='logit').fit(method='bfgs', disp=False) 

n_vars = len(x_vars)
 

print(model_ordered.summary()) 

llf       = model_ordered.llf
llnull    = model_ordered.llnull  # built-in, no manual null model needed
lr_df     = len(x_vars)

pseudo_r2 = 1 - (llf / llnull)
lr_stat   = -2 * (llnull - llf)
lr_pval   = stats.chi2.sf(lr_stat, lr_df)

#----------------------------------------------------------------------
# creating a regression table using the pystout library, which formats the results of the logit regression into a LaTeX table. The table will include the coefficients, standard errors, significance levels, and other relevant statistics for each variable in the regression model all to 2 decimal places. 
# Then taking the .tex file generated by pystout, wraps it in a full LaTeX document, compiles it to PDF, and then converts the PDF to a PNG image. This allows us to easily include the regression table as an image in our website. then deleting the intermediate files generated during the process to keep the directory clean.
pystout(models= [model_ordered],
        file=TAB+'regressionTable.tex',
        exogvars=list(x_vars_clean.columns),
        addnotes=[
            'Dependent variable is final tournament position (1 = best, 6 = worst).', 
            'Ordered Logit (proportional odds model). Threshold parameters not reported.',
            'Negative coefficient = associated with a better (lower-numbered) finish.',
            'Standard errors in parentheses. *: p$<$0.10; **: p$<$0.05; ***: p$<$0.01'
            ],    
        digits=3, 
        endog_names=["Final Position"], 
        varlabels={'const':'Constant',
                   'win_rate':'Winning Percentage',
                   'try_efficiency':'Average Tries Scored Per Game',
                   'try_conceded_efficiency':'Average Tries Conceded Per Game',
                   'point_difference_efficiency':'Average Points Difference Per Game ',
                   'attack_efficiency ':'Average Defenders Beaten per carry',
                   'avg_offload_per_game':'Average Offload per Game',
                   'goal_kick_success_percent':'Goal Kick Success Percent',
                   'tackle_success_percent':'Tackle Success Percent',
                   'lineout_success_percent':'Lineout Success Percent',
                   'avg_lineout_steals_per_game':'Average Lineout Steals per Game',
                   'metres_per_carry':'Average Metres Per Carry per game',
                   'post_contact_metres_per_carry':'Average Post Contact Metres Per Carry per game',
                   'avg_kicks_in_play':'Average Kicks In Play per Game',
                   'avg_kick_metres_per_game':'Average Kick Metres per Game',
                   'avg_dominant_tackle_contact_per_game':'Average Dominant Tackle Contact per Game',
                   'avg_turnovers_won_per_game':'Average Turnovers Won per Game'}, 
        modstat={'nobs':'Obs'},
        stars =  {.1:'*',.05:'**',.01:'***'})
#----------------------------------------------------------------------
# Step 2: Inject custom stats into the .tex file
# pystout uses \hline\hline (not \bottomrule) as its closing rule.
# The structure is: Obs row, then \hline\hline, then footnotes, then \end{tabular}
# We inject our custom rows BEFORE the last \hline\hline
with open(tex_path, 'r') as f:
    tex = f.read()

custom_rows = (
    f"LR chi2({lr_df}) & {round(lr_stat, 3)} \\\\\n"
    f"Prob $>$ chi2 & {round(lr_pval, 4)} \\\\\n"
    f"Pseudo R$^2$ & {round(pseudo_r2, 4)} \\\\\n"
)

# pystout closes the stats block with \hline\hline then footnotes then \end{tabular}
# Find the last \hline\hline and inject our rows before it
last_hline_idx = tex.rfind(r'\hline\hline')
tex = tex[:last_hline_idx] + custom_rows + tex[last_hline_idx:]

with open(tex_path, 'w') as f:
    f.write(tex)

#----------------------------------------------------------------------
# Step 3: Read updated .tex and wrap in full LaTeX document
with open(tex_path, 'r') as f:
    table_content = f.read()

wrapped_tex = r"""
\documentclass{article}
\usepackage{booktabs}
\usepackage{geometry}
\geometry{margin=0.5in, landscape, paperwidth=20in, paperheight=15in}
\usepackage{caption}
\usepackage{adjustbox}

\begin{document}
\pagestyle{empty}
\thispagestyle{empty}

\noindent{\large\textbf{Logit Regression Results}}\\[0.5em]
\begin{adjustbox}{max width=\textwidth, max totalheight=\textheight, keepaspectratio}
""" + table_content + r"""
\end{adjustbox}

\end{document}
"""

with open(wrapped_path, 'w') as f:
    f.write(wrapped_tex)

#----------------------------------------------------------------------
# Step 4: Compile to PDF, catching errors
result = subprocess.run(
    ['pdflatex', '-interaction=nonstopmode', '-output-directory', TAB, wrapped_path],
    capture_output=True, text=True
)

if result.returncode != 0:
    log_file = TAB + 'regressionTable_wrapped.log'
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            log = f.read()
        for line in log.splitlines():
            if any(kw in line for kw in ['!', 'Error', 'error', 'Undefined', 'Missing']):
                print(line)
    raise RuntimeError("pdflatex failed — see errors above")

#----------------------------------------------------------------------
# Step 5: Convert PDF to PNG and crop whitespace
images = convert_from_path(pdf_path, dpi=300)

for i, image in enumerate(images):
    image = image.convert("RGB")
    bg   = Image.new("RGB", image.size, (255, 255, 255))
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    cropped = image.crop(bbox) if bbox else image
    cropped.save(TAB + 'regressionTable.png', 'PNG')

#----------------------------------------------------------------------
# Step 6: Clean up intermediate files
for ext in ['*.aux', '*.log', '*.pdf', '*.tex']:
    for f in glob.glob(TAB + ext):
        os.remove(f)


#------------------------------------------------------------------------------
#--- (6) Creating visualisation of regression coefficients (box and whisker plot)
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#--- (7) Creating visualisation of relationship between attacking and defensive performance (scatter plot)
#------------------------------------------------------------------------------

def scatter_plot_pcm_vs_tsp(six_nations_df_2020_onwards):
    frames = make_frames(six_nations_df_2020_onwards["year"].unique(), pause_end=15) # extracting unique years from 2020 onwards to use as frames for the animation, and extending the list of frames by repeating the last year multiple times to allow the final year (frame) to be displayed longer in the animation.

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figure_size_for_plots()) # creating a figure and axis for the plot
    fig.subplots_adjust(wspace=0.6)

    def animate(year):
        ax1.clear() # clear the first subplot to redraw it
        ax2.clear() # clear the second subplot to redraw it
        six_nations_df_frame = six_nations_df_2020_onwards[six_nations_df_2020_onwards['year'] <= year]    
        # filter the dataframe to include only data up to the current frame as it cycles through the years

        # Scatter plot of average post-contact meters per carry against final position
        for team, grp in six_nations_df_frame.groupby('team'):
            create_scatter_plot(grp['post_contact_metres_per_carry'], grp['final_position'], ax1, team)
            create_scatter_plot(grp['tackle_success_percent'], grp['final_position'], ax2, team)

        if year == 2026: # adding a regression line to the scatter plot in the final frame (2026) to show the overall trend in the relationship between average post-contact meters per carry and final position in the tournament.
            fit_line_for_scatter_plot(six_nations_df_frame['post_contact_metres_per_carry'], six_nations_df_frame['final_position'], ax1)
            fit_line_for_scatter_plot(six_nations_df_frame['tackle_success_percent'], six_nations_df_frame['final_position'], ax2)
             
        ax1.set_title("Average Post-Contact Meters per Carry vs Final Position")
        ax1.set_xlabel("Average Post-Contact Meters per Carry")
        ax1.set_xlim(min(six_nations_df_2020_onwards['post_contact_metres_per_carry'])-0.5, max(six_nations_df_2020_onwards['post_contact_metres_per_carry'])+0.5) # setting the x-axis limits to be slightly wider than the range of average post-contact meters per carry in the dataset for better visualization
        ax1.set_ylabel("Final Position")
        ax1.set_ylim(6.3, 0.7) # setting the y-axis limits (inverted: 1st at top)
        ax1.set_yticks(range(1, 7)) # setting the y-axis ticks to be from 1 to 6, representing the final positions of the teams in the tournament
        ax1.set_yticklabels(["1st", "2nd", "3rd", "4th", "5th", "6th"]) 
        ax1.grid(linestyle="--", alpha=0.25) # adding a grid to the y-axis for better readability
        legend_location(ax1) # adding a legend to the scatter plot, positioned outside the plot area on the upper left


        ax2.set_title("Tackle Success Percentage vs Final Position")
        ax2.set_xlabel("Tackle Success Percentage")
        ax2.set_xlim(min(six_nations_df_2020_onwards['tackle_success_percent'])-0.5, max(six_nations_df_2020_onwards['tackle_success_percent'])+0.5) # setting the x-axis limits to be slightly wider than the range of average post-contact meters per carry in the dataset for better visualization

        ax2.set_ylabel("Final Position")
        ax2.set_ylim(6.3, 0.7) # setting the y-axis limits (inverted: 1st at top)
        ax2.set_yticks(range(1, 7)) # setting the y-axis ticks to be from 1 to 6, representing the final positions of the teams in the tournament
        ax2.set_yticklabels(["1st", "2nd", "3rd", "4th", "5th", "6th"]) 

        ax2.grid(linestyle="--", alpha=0.25) # adding a grid to the y-axis for better readability

        legend_location(ax2) # adding a legend to the scatter plot, positioned outside the plot area on the upper left
        
        fig.suptitle("How Attacking (Post-Contact Meters per Carry) and Defensive Performance (Tackle Success Percentage) Relate to Final Position",
            fontsize=13, fontweight="bold",
        )

    ani = animation.FuncAnimation(fig,animate, frames=frames, interval=300, repeat=True)

    save_gif(ani, "attackingPCM_vs_defensiveTSP_scatter.gif", fps=2)
    
scatter_plot_pcm_vs_tsp(six_nations_df_2020_onwards) # calling the function to create and save the dual panel line graph and scatter plot of average kicks in play per game and their relationship with final position in the Six Nations tournament.