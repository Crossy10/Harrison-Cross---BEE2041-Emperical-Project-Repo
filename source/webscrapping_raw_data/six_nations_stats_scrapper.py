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

# ==============================================================================
# 0. Imports the necessary Python Libraries and directory locations
# ==============================================================================

import pandas as pd
from playwright.sync_api import sync_playwright
from collections import defaultdict


ROOT = "/home/hcross27/BEE2041/Emperical_Project/Harrison-Cross---BEE2041-Emperical-Project-Repo/"

DAT_RAW = ROOT+'data/raw_data/'

# ==============================================================================
# 1. Scrape stats for every year (2000-2026) → long-format list of dicts
# ==============================================================================

# The six teams that appear in Six Nations stats tables.
# Stored as a set for fast membership checks inside the scraping loop.
SIX_NATIONS_TEAMS = {
    "FRANCE", "ENGLAND", "IRELAND", "SCOTLAND", "WALES", "ITALY"
    }

# Metrics that appear fromn the site when scrapping but aren't actually performance stats —
# they're either country names (picked up as spurious rows) or an all-time wins counter that skews year-on-year comparisons.
JUNK_METRICS = {
    "top_line_stats_since_2000", "all_time_6nations_wins", "ireland", "scotland", "france" "italy", "wales", "england"
    }

# The Six Nations website uses a URL pattern like:
#    https://www.sixnationsrugby.com/en/m6n/stats/200000?tab=teams   for 2000
#    https://www.sixnationsrugby.com/en/m6n/stats/202600?tab=teams   for 2026
# i.e.  {year}00  as the path segment.

years = range(2000, 2027)
rows = []

with sync_playwright() as p:
    # Launch a headless Chromium browser — no visible window opens.
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for year in years:
        print(f"Scraping {year}...")

        url = f"https://www.sixnationsrugby.com/en/m6n/stats/{year}00?tab=teams"
        page.goto(url)

        # Waiting for 6 seconds to allow content to load and to finish rendering the stat cards.
        page.wait_for_timeout(6000)

        # Each metric (e.g. "Points Scored", "Tries") lives inside its own card div that contains an <h2>/<h3> title and a <table>.
        cards = page.query_selector_all("div")

        for card in cards:
            try:
                title_el = card.query_selector("h2, h3")
                table = card.query_selector("table")

                # Skip any div that isn't a proper stat card.
                if not title_el or not table:
                    continue

                # Normalise the metric name so it works as a column header later,
                # e.g. "Points Scored" → "points_scored".
                metric = title_el.inner_text().strip().lower().replace(" ", "_")

                for tr in table.query_selector_all("tr"):
                    cols = tr.query_selector_all("td")

                    # Each data row needs at least a team cell and a value cell.
                    if len(cols) < 2:
                        continue

                    text_vals = [c.inner_text().strip() for c in cols]

                    # Rather than assuming a fixed column order, we scan every cell in the row: if it's a team name we store it, if it looks like a number we store that. 
                    # This handles tables where the columns aren't always in the same position.
                    team  = None
                    value = None

                    for cell in text_vals:
                        if cell.upper() in SIX_NATIONS_TEAMS:
                            team = cell.lower().capitalize()
                        else:
                            try:
                                value = float(cell.replace(",", ""))
                            except ValueError:
                                pass

                    # Only keep rows where we found both a team and a number.
                    if team is None or value is None:
                        continue

                    rows.append({
                        "year":   year,
                        "metric": metric,
                        "team":   team,
                        "value":  value,
                    })

            except Exception:
                # Individual card failures (stale elements, missing nodes, etc.)are common on a JS site — skip silently and move on.
                continue

    browser.close()

# Build the raw long-format DataFrame and save it 
long_df = pd.DataFrame(rows)

print("\n\n\nChecking the first 5 rows to see if successful\n")
print(long_df.head())    # checking the first 5 rows to see if it's as wanted

long_df.to_csv(DAT_RAW + "LONG_FORMAT-six_nations_RAWstats.csv", index=False)


# ==============================================================================
# 2. Re-scrape 2026 in isolation to establish the column order used on the webiste
# ==============================================================================
# The website's stat cards appear in a specific order that the pivot later needs to preserve.  
# Rescraping 2026 on its own gives us a reliable list of metric names in the right sequence.

data_2026 = defaultdict(dict)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    url_2026 = "https://www.sixnationsrugby.com/en/m6n/stats/202600?tab=teams"
    page.goto(url_2026)
    page.wait_for_timeout(7000)

    cards_2026_scrape = page.query_selector_all("div")

    for card in cards_2026_scrape:
        try:
            title_el_2026_scrape = card.query_selector("h2, h2")
            table_2026_scrape = card.query_selector("table")

            if not title_el_2026_scrape or not table_2026_scrape:
                continue

            stat_name = title_el_2026_scrape.inner_text().strip().lower().replace(" ", "_")

            for row in table_2026_scrape.query_selector_all("tr"):
                cols_2026_scrape = row.query_selector_all("td")
                
                
                if len(cols_2026_scrape) < 2:
                    continue

                text_vals_2026_scrape = [c.inner_text().strip() for c in cols_2026_scrape]

                # Rather than assuming a fixed column order, we scan every cell in the row: if it's a team name we store it, if it looks like a number we store that. 
                # This handles tables where the columns aren't always in the same position.
                team_2026_scrape  = None
                value_2026_scrape = None

                for cell in text_vals_2026_scrape:
                    if cell.upper() in SIX_NATIONS_TEAMS:
                        team_2026_scrape = cell.lower().capitalize()

                    else:
                        try:
                            value_2026_scrape = float(cell.replace(",", ""))
                            
                        except ValueError:
                            pass

                # Only keep rows where we found both a team and a number.
                if team_2026_scrape is None or value_2026_scrape is None:
                    continue

                data_2026[team_2026_scrape][stat_name] = value_2026_scrape

        except Exception:
            # Individual card failures (stale elements, missing nodes, etc.) are common on a JS site — skip silently and move on.
            continue

    browser.close()
                
# Turn the nested dict into a wide DataFrame (one row per team).
pure_2026_df = pd.DataFrame.from_dict(data_2026, orient="index")
pure_2026_df.reset_index(inplace=True)

# Drop columns that are junk metrics or team-name columns the site generated as spurious headings.
cols_to_drop = ["index"] + list(JUNK_METRICS)

for col in cols_to_drop:
    if col in pure_2026_df.columns:
        pure_2026_df.drop(columns=col, inplace=True)



print("\n\n\nChecking the first 5 rows to see if successful\n")
print(pure_2026_df.head())    # checking this worked

# This is the column order we want in the final wide CSV.
ordered_STATS_cols = [col for col in pure_2026_df.columns]
METRIC_columns = ["year", "team"] + ordered_STATS_cols


print("\n\n\nChecking if the columns in the desired order\n")
print(METRIC_columns) # checking we have successfully collected the columns in the desired order


# ==============================================================================
# 3. Clean the long-format CSV and reshape to wide format
# ==============================================================================

temp_df = pd.read_csv(DAT_RAW + "LONG_FORMAT-six_nations_RAWstats.csv")

# --- Remove junk metrics ---
# These are the junk metrics as described at the beginning of code
# This is done by grabbing the entire metric column from the long-format dataframe, checking if the contents matches those in the JUNK_METRICS list, if a match is found then it is removed

temp_df = temp_df[~temp_df["metric"].isin(JUNK_METRICS)]
temp_df = temp_df[~temp_df["metric"].str.lower().isin(JUNK_METRICS)]   # accounting for strictly lowercase words

# --- Pivot long-format to  wide ---
# Each (year, team) pair becomes one row; every metric gets its own column.

wide_df = temp_df.pivot_table(
    index   = ["year", "team"],
    columns = "metric",
    values  = "value",
    aggfunc = "first", # This handles the case where the same stat appears multiplies times for a team in a year
).reset_index()


wide_df.columns.name = None # pivot_table sets columns.name = "metric"; clear that so the header row looks clean.

# --- Reordering the columns to match the website order ---

cols_present = [c for c in METRIC_columns if c in wide_df.columns]
wide_df = wide_df[cols_present]

print("\n\n\nChecking the first 5 rows to see if successful\n")
print(wide_df)   # checking first 5 rows to see if successful




# ==============================================================================
# 4. Saving the raw stats data
# ==============================================================================
wide_df.to_csv(DAT_RAW + "WIDE_FORMAT-six_nations_RAWstats_.csv", index=False)

print("\n\n\nRaw Data saved succesfully")