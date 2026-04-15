# Harrison Cross: Emperical Project README

**Author:** Harrison Cross  
**Date:** 13-04-2026  
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

---

## Data

**Note:** The raw data is what is required, it will automatically get cleaned. This clean data will be what is used in the analysis, which is done automatically and updated automatically.
---

## Repository Structure

```
Emperical project/
├── README.md
├── Makefile
├── website
├── refs.bib                           # Bibliography
│
├── data/
│    ├── raw                               # Raw data
│    └── clean                             # Clean data
│
├── source/
│    └── data_analysis.py                           # python coding script
│
├── results/
│    ├── figures/
│    └── tables/
|
│
├── website_coding/
│    ├── _quarto.yml
|    ├── about.qmd
|    ├── blog_website.qmd
|    ├── conclusion.qmd
|    ├── index.qmd
|    ├── results.qmd
│    └── styles.css
|
├── .github/workflows/
│    ├── publish.yml
|
└── .gitignore
```
All raw data lives in `data/raw_data`, all source code in `source/`, and all output is automatically exported to `results/`.


---

## Requirements
### System
- Python 3 (tested on **Python 3.12.3**, WSL)
- `make` (optional, but recommended)

### Python Packages

---

## Running Instructions

---

## Outputs

---

## Methods

---

## References and Resources
