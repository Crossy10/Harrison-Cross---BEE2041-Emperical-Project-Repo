# ============================================================
# Makefile for Six Nations Data Analysis Pipeline
# ============================================================

# Define file paths
WEBSCRAPPING_STATS := source/webscrapping_raw_data/six_nations_stats_scrapper.py
WEBSCRAPPING_TABLE := source/webscrapping_raw_data/six_nations_table_data.py
PYTHON_RAW_DATA := source/complete_raw_data_python_code/obtaining_six_nations_complete_RAW-DATA.py
PYTHON_SCRIPT := source/data_analysis_coding.py

# Define data files
RAW_DATA_FILE := data/clean_data/six_nations_RAW-DATA.csv
CLEAN_DATA_FILE := data/clean_data/six_nations_CLEAN-DATA.csv



# --- File paths ---
WEBSCRAPING_STATS  := source/webscrapping_raw_data/six_nations_stats_scrapper.py
WEBSCRAPING_TABLE  := source/webscrapping_raw_data/six_nations_table_data.py
PYTHON_RAW_DATA    := source/complete_raw_data_python_code/obtaining_six_nations_complete_RAW-DATA.py
PYTHON_SCRIPT      := source/data_analysis_coding.py

# --- Data files ---
RAW_DATA_FILE      := data/raw_data/six_nations_RAW-DATA.csv
CLEAN_DATA_FILE    := data/clean_data/six_nations_CLEAN-DATA.csv

# ============================================================


# --- Run full pipeline ---
all: scrape data analysis

# --- Scrape all data from web ---
scrape:
	python3 $(WEBSCRAPING_STATS)
	python3 $(WEBSCRAPING_TABLE)

# --- Compile scraped data into raw CSV ---
data:
	python3 $(PYTHON_RAW_DATA)

# --- Clean and analyse (cleaning handled at top of script) ---
analysis:
	python3 $(PYTHON_SCRIPT)

.PHONY: all scrape data analysis clean help