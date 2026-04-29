"""
obtaining_six_nations_complete_RAW-DATA.py                       Harrison Cross
---|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8

This file creates the complete raw data that will be used for the rest of the project

This code will use SQL and merge the basic raw data and the webscrapped stats data and save into the raw data folder. 

This code was partial written, adjusted and refined with the help of Claude AI. 


Full details related to the replication of this file can be found in the README code in the top level of this directory.
The complete raw data can, however, simply be obtained from the GitHub repo - this code is only for the creation.
"""


# ==============================================================================
# 0. Imports the necessary Python Libraries and directory locations
# ==============================================================================
import pandas as pd
import sqlite3

ROOT = "/home/hcross27/BEE2041/Emperical_Project/Harrison-Cross---BEE2041-Emperical-Project-Repo/"

DAT_RAW = ROOT+'data/raw_data/'

# ==============================================================================
# 1. Load both CSVs
# ==============================================================================
 
stats_raw = pd.read_csv(DAT_RAW + 'raw_dataWIDE_FORMAT-six_nations_RAWstats_.csv')
tables_raw = pd.read_csv(DAT_RAW + 'six_nations_fixtures_table_scraped.csv', keep_default_na=False, na_values=[''])


 
# ==============================================================================
# 2. Load into an in-memory SQLite database
# ==============================================================================
 
con = sqlite3.connect(":memory:")
stats_raw.to_sql("stats_raw", con, index=False, if_exists="replace") # load stats_raw into SQL table
tables_raw.to_sql("tables_raw", con, index=False, if_exists="replace") # load tables_raw into SQL table



# ==============================================================================
# 3. SQL JOIN on year + team
# ==============================================================================

#  - All fixture table columns kept with their original names
#  - raw_stats columns brought in; 'try_scored' from raw_stats renamed to avoid collision with 'tries_scored' in fixtures
#  - raw_stats 'points' renamed to avoid collision with fixtures 'points_scored'

merged = pd.read_sql("""
    SELECT f.year, 
        f.team,
        f.final_position,
        f.grand_slam,
        f.matches_played,
        f.matches_won,
        f.matches_drawn,
        f.matches_lost,
        f.points_scored,
        f.points_conceded,
        f.points_difference,
        f.tries_scored,
        f.tries_conceded,
        f.bonus_points,
        f.table_points,
        r.carries,
        r.offload,
        r.try_assist,
        r.defender_beaten,
        r.missed_tackle,
        r.lineout_steals,
        r.lineout_throws_won,
        r.kicks_in_play,
        r.kick_metres,
        r.retained_kick,
        r.dominant_contact,
        r.dominant_tackle_contact,
        r.total_successful_tackles,
        r.box_kicks,
        r.total_turnovers_won,
        r.attacking_catch_success,
        r.successful_goals,
        r.carry_metres_made,
        r.post_contact_metres,
        r.kick_bounced,
        r.initial_break,
        r.goal_kick_success_percent,
        r.tackle_success_percent,
        r.retained_kicks_percent,
        r.lineout_success_percent,
        r.metres_per_carry,
        r.post_contact_metres_per_carry,
        r.total_jackals,
        r.kick_metres_per_kick
    
    FROM tables_raw  AS f
    INNER JOIN stats_raw AS r
    ON f.year = r.year
    AND f.team = r.team
    ORDER BY f.year ASC, f.final_position ASC
""",con) 

# ==============================================================================
# 4. Saving and storing the complete raw data
# ==============================================================================
merged.to_csv(DAT_RAW + "six_nations_RAW-DATA.csv", index=False)
 