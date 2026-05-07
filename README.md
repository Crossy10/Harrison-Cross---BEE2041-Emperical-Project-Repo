# What drives success in Rugby Tournaments: A Data-Driven Analysis of the Six Nations

**Author:** Harrison Cross  
**About:** Emperical Project for BEE2041 - Data Science in Economics  
**Contact:** [hc891@exeter.ac.uk](mailto:hc891@exeter.ac.uk)  

---

## Table of Contents

1. [Overview](#overview)
2. [Data](#data)
3. [Repository Structure](#repository-structure)
4. [Requirements](#requirements)
5. [Running Instructions](#running-instructions)
6. [Outputs](#outputs)
7. [Methods](#methods)
8. [References and Resources](#references-and-resources)

---

## Overview
This project involves statistical analysis, using data from:
> Six Nations Rugby (2026) *Statistics*, (https://www.sixnationsrugby.com/en/m6n/stats)

> Six Nations Rugby (2026) *Fixtures and Results*, (https://www.sixnationsrugby.com/en/m6n/fixtures)



This project aims to investigate the key factors that determine success in the Six Nations Rugby Championship.
Thus, the central reseach question is: 
**What factors most strongly predict the match outcomes in rugby?**

This is done in using **Logit regression** (via `OrderedModel`) to evaluate the different performance metrics impact the probability to finishing higher in the Six Nations Championship.


I have used 2 datasets from the Six Nations website, done by webscrapping the results tables and the team statistics tab, and then combined them together using SQL. These datasets involve match statistics such as tries, carry meters and tackles.

The projected is presented in a GitHub Pages website, generated using Quarto, which can be accessed [here:](https://crossy10.github.io/Harrison-Cross---BEE2041-Emperical-Project-Repo/) 

or follow the link: (https://crossy10.github.io/Harrison-Cross---BEE2041-Emperical-Project-Repo/)
 
---

## Data
The raw dataset (`six_nations_RAW-DATA.csv`) comes from combining the two webscrapped datasets from the Six Nations website. It is in `.csv` format and is read directly using `pandas`.

The clean dataset (`six_nations_CLEAN-DATA.csv`), used in this analysis also is in `.csv` format and is read directly using `pandas`.


The key variables used in this analysis are:

| Variable | Description |
|---|---|
| `final_position` | Outcome: Where eache team finished in each year of the Six Nations |
| `year` |  |
| `team` | W |
| `grand_slam` | W |
| `matches_played` | W |
| `matches_won` | W |
| `matches_drawn` | W |
| `matches_lost` | W |
| `points_scored` | W |
| `points_conceded` | W |
| `points_difference` | W |
| `tries_scored` | W |
| `tries_conceded` | W |
| `bonus_points` | W |
| `carries` | W |
| `offload` | W |
| `defender_beaten` | W |
| `missed_tackle` | W |
| `lineout_steals` | W |
| `lineout_throws_won` | W |
| `kicks_in_play` | W |
| `kick_metres` | W |
| `dominant_contact` | W |
| `dominant_tackle_contact` | W |
| `total_successful_tackles` | W |
| `total_turnovers_won` | W |
| `successful_goals` | W |
| `carry_metres_made` | W |
| `post_contact_metres` | W |
| `goal_kick_success_percent` | W |
| `tackle_success_percent` | W |
| `lineout_success_percent` | W |
| `metres_per_carry` | W |
| `post_contact_metres_per_carry` | W |
| `kick_metres_per_kick` | W |
| `win_rate` | W |
| `try_efficiency` | W |
| `try_conceded_efficiency` | W |
| `point_difference_efficiency` | W |
| `attack_efficiency` | W |
| `avg_offload_per_game` | W |
| `avg_lineout_steals_per_game` | W |
| `avg_kicks_in_play` | W |
| `avg_kick_metres_per_game` | W |
| `avg_dominant_tackle_contact_per_game` | W |
| `avg_turnovers_won_per_game` | W |
| `Eras` | W |





**Note:** The data file is included in this repository, however, the raw data is what is required, it will automatically get cleaned. This clean data will be what is used in the analysis, which is done automatically and updated automatically.

---

## Repository Structure

```
Emperical project/
├── README.md
├── Makefile
│
├── website_htmls_for_project/
│    └── Harrison Cross - Emperical Project Website.html   # Project Website html file
│
├── data/
│    ├── raw_data/                                         # Raw data in CSV format
│    │  ├── raw_dataLONG_FORMAT-six_nations_RAWstats.csv 
│    │  ├── raw_dataWIDE_FORMAT-six_nations_RAWstats_.csv 
│    │  ├── six_nations_fixtures_table_scraped.csv 
│    │  └── six_nations_RAW-DATA.csv 
│    │ 
│    └── clean_data/                                       # Clean data in CSV format
|      ├── six_nations_full_columns_&_eras_CLEAN-DATA.csv
|      ├── six_nations_full_columns_CLEAN-DATA.csv
│      └── six_nations_CLEAN-DATA.csv 
│
├── source/
│    └── data_analysis.py                                  # python coding script
│
├── results/
│    ├── figures/                                          # PNG and GIF graphs from coding
│    │  ├── attackingPCM_vs_defensiveTSP_scatter.gif  
│    │  ├── grand_slams.png  
│    │  ├── kicks_in_play_dual_panel.gif  
│    │  ├── regression_coefficients.png 
│    │  └── six_nations.gif  
│    │
│    └── tables/
│       └── regressionTable.png                            # PNG Regression table from coding
│
├── website_coding/
│    ├── _quarto.yml
|    ├── data.qmd                                          # Data & methodology page for my website
|    ├── index.qmd                                         # Home page for my website
|    ├── results.qmd                                       # Results page for my website
│    └── styles.css
|
├── .github/workflows/
│    ├── publish.yml
|
└── .gitignore
```
All raw data lives in `data/raw_data`, all source code in `source/`, and all output is automatically exported to `results/`. The Quarto files reads results, table and figure files directly and automatically, so **running the Python script before is essential**.

---

## Requirements
### System
- Python 3 (tested on **Python 3.12.3**, WSL)
- `make` (optional, but recommended)
- Quarto (for website rendering)

### Python Packages
Install all dependencies via pip:

```bash
pip install
```

Or install without pinned versions (results may differ slightly):

```bash
pip install 
```

The exact versions used to produce the original results are listed below:

| Package | Version |
|---|---|
| `pandas` | 2.3.3 |

---

## Running Instructions
### Step 0: Configure the root directory

Before running anything, open the python files in `source/webscrapping_raw_data` as well as the python files in `source/complete_raw_data_python_code` and `source/data_analysis.py`, you must update the `ROOT` variable to point to the top level of this repository on your machine:

```python
ROOT = "/your/path/to/this/project/"
```

### Step 1: Run the coding
#### Option A: Using `make` (recommended)

If `make` is available, simply run from the top level of the repository:

```bash
make
```

This will automatically run the full pipeline in order:
1. **Scrape** - Collects the Six Nations stats and table data from the Six Nations Championship Website
2. **Data** - Compiles all the scrapped data into a single CSV containing all the raw data
3. **Analysis** - Cleans the raw data and runs the full analysis, producing all output figures and tables

To run individual steps

```bash
make scrape      # Only Scrape data from web
make data        # Only Compile  data into CSV 
make analysis    # Only runs python script to clean and  analysise only
```


### Option B: Manual steps

If `make` is not available, run the following steps in order:

**1. Run the Python script to scrape data:**  
```bash  
python3 source/webscrapping_raw_data/six_nations_stats_scrapper.py
python3 source/webscrapping_raw_data/six_nations_table_data.py
```

This will populate `data/raw_data/` with the CSV files contianing the each scrapped dataset.

**2. Run the Python script to compile the scrapped data:**  
```bash
python3 source/complete_raw_data_python_code/obtaining_six_nations_complete_RAW-DATA.py
```
This will populate `data/raw_data/` with the CSV files contianing ful raw dataset.

**3. Run the Python script to clean and analysise the data**    
```bash
python3 source/data_analysis_coding.py
```

This will populate `data/clean_data/` with the cleaned CSV and all output figures and tables in `results/figures/` and `results/tables` respectively.


### Step 2. Open the website**  
Open the website [here](https://crossy10.github.io/Harrison-Cross---BEE2041-Emperical-Project-Repo/) 

This website was created using Quarto and published on GitHub Pages


---

## Outputs
Running the pipeline produces the following files:

### Figures (`results/figures/`)

| File | Description |
|---|---|
| `attackingPCM_vs_defensiveTSP_scatter.gif` |---|
| `grand_slams.png` |---|
| `kicks_in_play_dual_panel.gif` |---|
| `regression_coefficients.png` |---|
| `six_nations.gif` |---|

### Tables (`results/tables/`)

| File | Description |
|---|---|
| `regressionTable.png` | ---|

## Methods
### Webscrapping
Web scraped relevant data off the Six Nations website as mentioned earlier and using the package selinium in the process. 

This data is correctly referenced on the website and in the references section of this ReadME.

### Coding - Cleaning and Analysis
asldkfj

### Website
To create my website, I used Quarto pages and generated a yml and used css to style and can be accessed in the top of this repositiory

---

## References and Resources

**Data:** 
> Six Nations Rugby. (2026) *Statistics*, (https://www.sixnationsrugby.com/en/m6n/stats)

> Six Nations Rugby. (2026) *Fixtures and Results*, (https://www.sixnationsrugby.com/en/m6n/fixtures)

**Coding:**  
pystout (LaTeX table export): [https://github.com/stephenholtz/pystout](https://github.com/stephenholtz/pystout)

How to animate graphs
> GeeksforGeeks. (2025, July). *Matplotlib.animation.FuncAnimation class in python*, (https://www.geeksforgeeks.org/matplotlib-animation-funcanimation-class-in-python/)

