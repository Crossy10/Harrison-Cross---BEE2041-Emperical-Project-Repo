"""
six_nations_scraper.py          Harrison Cross          22-04-2026
---|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8

Scrapes team-level stats from the Six Nations website for every tournament
year from 2000 to 2026, then reshapes the data into a clean wide-format CSV.

The site is JavaScript-rendered, so we use Playwright 

The data has been provided in replication materials in dta format, and hence is read in directly with pd.read_stata().  In order to replicate this file, the only required change is the ROOT directory, indicated on line 29.

This file uses Causal forests, as well as standard regression analysis. For details on the underlying causal forest implementation, please refer to:
https://econml.azurewebsites.net/spec/estimation/forest.html

Full details related to the replication of this file can be found in the README code in the top level of this directory.
"""

""" obtaining_raw_data.py               Harrison Cross               22-04-2026
---|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8

  This file creates the basic raw data that will be used as the backbone to the rest of the raw data and subsequently for the rest of the project

  The data comes from the table from each year from the Six Nations Rugby website where we copied the result table gtom each year.
https://www.sixnationsrugby.com/en/m6n/fixtures/202600/table

At times where the table was unclear, I used the corresponding results table from https://www.rugbypass.com/six-nations/history/ 

This code will create the basic raw data and save into the data folder. 
In order to replicate this file, the only required change is the ROOT directory, indicated on line 25.
The basic raw data can, however, simply be obtained from the GitHub repo - this code is only for the creation.

Full details related to the replication of this file can be found in the README code in the top level of this directory.

"""

# ==============================================================================
# 0. Imports the necessary Python Libraries and directory locations
# ==============================================================================

import pandas as pd
from playwright.sync_api import sync_playwright


ROOT = "/home/hcross27/BEE2041/Emperical_Project/Harrison-Cross---BEE2041-Emperical-Project-Repo/"

DAT_RAW = ROOT+'data/raw_data/'

# ==============================================================================
# 1. Scrape stats for every year (2000-2026) → long-format list of dicts
# ==============================================================================


# The Six Nations website uses a URL pattern like:
#    https://www.sixnationsrugby.com/en/m6n/fixtures/200000/table   for 2000
#    https://www.sixnationsrugby.com/en/m6n/fixtures/202600/table   for 2026
# i.e.  {year}00  as the path segment.
years = range(2000, 2027)
rows = []

with sync_playwright() as p:
    # Launch a headless Chromium browser — no visible window opens.
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for year in years:
        print(f"Scraping table from {year}...")

        url = f"https://www.sixnationsrugby.com/en/m6n/fixtures/{year}00/table"
        page.goto(url)

        # Waiting for 6 seconds to allow content to load and to finish rendering the stat cards.
        page.wait_for_timeout(6000)


        # Locating the table on the webpage
        table = page.query_selector("table")
        
        # Normalise the metric name so it works as a column header later,
        # e.g. "Points Scored" → "points_scored".
        for tr in table.query_selector_all("thead tr"):
            headers = tr.query_selector_all("th")


            if not headers:
                    headers = tr.query_selector_all("tr:first-child td")

        metric_TABLE_columns = [head.inner_text().strip()for head in headers]
        
        col_index = {h: i for i, h in enumerate(metric_TABLE_columns)}
        
        for tr in table.query_selector_all("tbody tr"):
            data_rows = tr.query_selector_all("td")

            # Each data row needs at least as many cells as there are headers.
            if len(data_rows)<len(metric_TABLE_columns):
                 continue
            
            data_vals = [c.inner_text().strip() for c in data_rows]

            row = {'year': year}

            for web_col in metric_TABLE_columns:
                idx = col_index.get(web_col)

                # If a column isn't present for this year, fill with None.
                if idx is None:
                    row[web_col] = None
                    continue

                raw = data_vals[idx]

                # Team name: normalise to title case (e.g. "FRANCE" → "France")
                if web_col == 'TEAM':
                    row[web_col] = raw.lower().capitalize()

                else:
                    try:
                        row[web_col] = float(raw.replace(",", ""))
                        
                    except ValueError:
                         pass
                
            rows.append(row)

    browser.close()


# ==============================================================================
# 3. Assemble and clean the dataframe
# ==============================================================================

fixtures_table_df = pd.DataFrame(rows)
print("\n\n\nChecking the first 5 rows to see if successful\n")
print(fixtures_table_df.head())    # checking the first 5 rows to see if it's as wanted

fixtures_table_df2 = fixtures_table_df.rename(columns={
     'POS':'final_position', 'TEAM':'team', 'P':'matches_played',
     'W':'matches_won', 'D':'matches_drawn', 'L':'matches_lost',
     'PF':'points_scored', 'PA':'points_conceded', 'DIFF':'points_difference',
     'TF':'tries_scored', 'TA':'tries_conceded', 'BP':'bonus_points',
     'PTS':'table_points'})


def derive_grand_slam(df):
    if df['final_position'] == 1 and (df['matches_won'] == 5):
        return 1
    elif df['final_position'] == 1:
        return 0
    else:
        return "N/A"

fixtures_table_df2['grand_slam'] = fixtures_table_df2.apply(derive_grand_slam, axis=1)

# Reorder columns to a logical sequence consistent with the hand-coded data style
column_order = [
    'year', 'team', 'final_position', 'grand_slam', 'matches_played', 'matches_won', 'matches_drawn', 'matches_lost', 'points_scored', 'points_conceded', 'points_difference', 'tries_scored', 'tries_conceded','bonus_points', 'table_points']

# format for each list: Year, Team, Position, Gram Slam (1 = Yes, 0 = No), matches Won, matches Lost, matches Drawn, points for, points against, point difference, tries for, tries against, bonus points, table points

# Only keep columns that were actually scraped (older years may omit BP/PTS)
column_order = [c for c in column_order if c in fixtures_table_df2.columns]
fixtures_table_df2 = fixtures_table_df2[column_order]

# Sort: most recent year first, then alphabetically by team —
# consistent with the sort used in obtaining_raw_data.py
fixtures_table_df2 = fixtures_table_df2.sort_values(
    by=['year','final_position'],
    ascending=[True, True]
).reset_index(drop=True)

# ==============================================================================
# 4. Output
# ==============================================================================

print("\n\n\nChecking the first 20 rows to see if successful\n")
print(fixtures_table_df2.head(20))


# ==============================================================================
# 4. cleaning
# ==============================================================================

# Helper to patch a single cell
def fix(year, team, col, value):
    mask = (fixtures_table_df2["year"] == year) & (fixtures_table_df2["team"] == team)
    fixtures_table_df2.loc[mask, col] = value

# 2015: Ireland was champion, scraper misread position
fix(2015, "Ireland", "final_position", 1)
fix(2015, "Ireland", "grand_slam", 0)

# 2019: France 4th, Scotland 5th (scraper swapped them)
fix(2019, "France", "final_position", 4)
fix(2019, "Scotland", "final_position", 5)

# 2009 Italy: official points_difference was -121 not -79
fix(2009, "Italy", "points_difference", -121)

fixtures_table_df2 = fixtures_table_df2.sort_values(
    by=['year','final_position'],
    ascending=[True, True]
).reset_index(drop=True)

fixtures_table_df2.to_csv(DAT_RAW + "six_nations_fixtures_table_scraped.csv", index=False)

print("\n\n\nFixtures table data saved successfully")