# What Wins Rugby Tournaments: A Data-Driven Analysis of the Six Nations

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
- > Six Nations Rugby (2026) *Statistics*, (https://www.sixnationsrugby.com/en/m6n/stats)

- > Six Nations Rugby (2026) *Fixtures and Results*, (https://www.sixnationsrugby.com/en/m6n/fixtures)


This project aims to investigate the key factors that determine success in the Six Nations Rugby Championship.

Thus, the central reseach question is: 
**What factors most strongly predict the match outcomes in rugby?**

This is done in two complementary approaches:
- **OLS regression** with interaction terms, to test for heterogeneity along specific, pre-specified dimensions

- **Causal Forests** (via `econml`), a machine learning method that estimates individualised treatment effects (CATEs) without requiring pre-specification of interaction terms.

I have used 2 datasets from the Six Nations website, done by webscrapping the results tables and the team statistics tab, and then combined them together using SQL. These datasets involve match statistics such as tries, carry meters and tackles.

The projected is presented in a GitHub Pages website, generated using Quarto,  
An easy to view version is checked in and available via GitHub pages.

---

## Data
The raw dataset (`six_nations_RAW-DATA.csv`) comes from combining the two webscrapped datasets from the Six Nations website. It is in `.csv` format and is read directly using `pandas`.

The clean dataset (`six_nations_RAW-DATA.csv`), used in this analysis also is in `.csv` format and is read directly using `pandas`.


The key variables used in this analysis are:

| Variable | Description |
|---|---|
| `c` | Outcome: |
| `f` | Treatment: |
| `final_position` | Where eache team finished in each year of the Six Nations |

**Note:** The data file is included in this repository, however, the raw data is what is required, it will automatically get cleaned. This clean data will be what is used in the analysis, which is done automatically and updated automatically.

---

## Repository Structure

```
Emperical project/
├── README.md
├── Makefile
├── website
├── refs.bib                                # Bibliography
│
├── data/
│    ├── raw_data/                          # Raw data in CSV format
│    │  ├── raw_dataLONG_FORMAT-six_nations_RAWstats.csv 
│    │  ├── raw_dataWIDE_FORMAT-six_nations_RAWstats_.csv 
│    │  ├── six_nations_fixtures_table_scraped.csv 
│    │  └── six_nations_RAW-DATA.csv 
│    │ 
│    └── clean_data/                         # Clean data in CSV format
│      └── six_nations_RAW-DATA.csv 
│
├── source/
│    └── data_analysis.py             # python coding script
│
├── results/
│    ├── figures/
│    └── tables/
|
│
├── website_coding/
│    ├── _quarto.yml
|    ├── about.qmd               # About page for my website 
|    ├── blog_website.qmd           # Info page for my website
|    ├── conclusion.qm        # Conclusion page for my website
|    ├── index.qmd                  # Home page for my website
|    ├── results.qmd             # Results page for my website
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

Before running anything, open the python files in `source/webscrapping_raw_data` as well as the python files in `source/complete_raw_data_python_code` and `source/data_analysis.py`, you update the `ROOT` variable to point to the top level of this repository on your machine:

```python
ROOT = "/your/path/to/this/project/"
```

### Option A: Using `make` (recommended)

If `make` is available, simply run from the top level of the repository:

```bash
make
```

This will automatically:
1. 

To 

```bash
make clean
```

To run only the Python script:

```bash
make run_python
```

### Option B: Manual steps

If `make` is not available, run the following steps in order:

**1. Run the Python script:**

```bash
python3 source/data_analysis.py
```

This will populate `results/figures/` and `results/tables/` with all output files.

**2. 

**3. Open the website**
Open the website

---

## Outputs
Running the pipeline produces the following files:

### Figures (`results/figures/`)

| File | Description |
|---|---|

### Tables (`results/tables/`)

| File | Description |
|---|---|

---

## Methods
### Webscrapping
Web scraped relevant data off the Six Nations website as mentioned earlier and using the package selinium in the process. 

This data is correctly referenced on the website and in the references section of this ReadME.

### Website
To create my website, I used Quarto pages and generated a yml and used css to style and can be accessed in the top of this repositiory

---

## References and Resources

**Data:** 
- > Six Nations Rugby (2026) *Statistics*, (https://www.sixnationsrugby.com/en/m6n/stats)

- > Six Nations Rugby (2026) *Fixtures and Results*, (https://www.sixnationsrugby.com/en/m6n/fixtures)
