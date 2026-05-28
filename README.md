# Education Under Fire
### Conflict Exposure and Educational Attainment in Northern Nigeria

**Author:** Jarret Angbazo 
**Identification strategy:** Difference-in-Differences (DiD) using Boko Haram insurgency onset (2009)  
**Data:** ACLED conflict events + DHS survey microdata + Nigeria LGA shapefiles

---

## Project Overview

This project estimates the causal effect of Boko Haram conflict exposure on educational outcomes (enrolment, attendance, years of schooling, completion) in Northern Nigeria using a two-way fixed effects DiD design comparing high- and low-conflict LGAs before and after the insurgency intensified in 2009.

The project pipeline is split into two stages:

| Stage | Language | Purpose |
|-------|----------|---------|
| **Stage 1** | Python | Cleaning, EDA, feature engineering, and geospatial merge |
| **Stage 2** | R | DiD estimation, event studies, robustness checks, tables, and figures |

**Handoff point:** Python writes `data/processed/analysis_panel.csv`; R reads it.
**Full pipeline:** Run `bash master.sh` from the project root to execute everything.

---

## Folder Structure

```
Economics_senior_thesis/
├── README.md                  # This file
├── master.sh                  # Master script. Runs the full pipeline end-to-end
├── .env                       # API keys and sensitive paths (NOT committed)
├── .gitignore                 # Tells Git what to ignore
├── requirements.txt           # Python package list 
├── renv.lock                  # R packages (reproducible via renv)
│
├── data/
│   ├── raw/                   # Original source files
│   │   ├── acled/             # ACLED conflict event data (.csv)
│   │   ├── dhs/               # DHS microdata (.dta or .csv)
│   │   └── shapefiles/         # Nigeria LGA and state boundary files (.shp)
│   │   
│   └── processed/             # Outputs written by Python — do not edit manually
│
├── python/                    # All Python scripts (run in numbered order)
│   ├── config.py               # Shared paths and constants
│   ├── 01_acled_clean.py      # Clean ACLED conflict event data
│   ├── 02_dhs_clean.py        # Clean DHS microdata
│   ├── 03_geospatial_merge.py # Spatial join: DHS clusters -> LGAs
│   ├── 04_conflict_exposure.py # Build treatment variable
│   ├── 05_panel_merge.py      # Assemble analysis_panel.csv
│   └── explore.ipynb          # EDA scratch notebook (not part of pipeline)
│
├── R/                         # All R scripts (run in numbered order)
│   ├── 00_config.R             # Shared paths and constants
│   ├── 01_describe.R          # Summary stats
│   ├── 02_pretrends.R         # Parallel trends checks
│   ├── 03_main_did.R          # Main TWFE regressions
│   ├── 04_event_study.R       # Event study plot
│   ├── 05_robustness.R        # Robustness checks
│   └── 06_tables_figures.R     # Export all outputs
│
├── output/                    # All outputs — NOT committed to Git
│   ├── tables/                # .tex and regression tables
│   └── figures/                # .pdf and .png figures and maps
│
└── docs/
    ├── thesis.qmd             # Thesis write-up
    ├── thesis.pdf             # Rendered PDF (committed at milestone versions)
    ├── revision_notes.pdf     # Running log of analysis decisions and changes
    └── references.bib         # BibTeX bibliography
```

---

## Reproduction Instructions

### Prerequisites

**Python (>= 3.10)**

```bash
# From project root
pip install -r requirements.txt
```

**R (>= 4.3)**

Open `education_under_fire.Rproj` in RStudio, then:

```r
# Restore the exact package versions used
install.packages("renv")
renv::restore()
```

### Running the entire project pipeline

Run everything at once

```bash
bash master.sh
```

**Master Script (`run_all.sh`)**

```bash
#!/usr/bin/env bash
set -e      # Stop on any error

echo "=== Stage 1: Python pipeline ==="

cd python
python 01_acled_clean.py
python 02_dhs_clean.py
python 03_geospatial_merge.py
python 04_conflict_exposure.py
python 05_panel_merge.py
cd ..

echo "=== Stage 2: R pipeline ==="

Rscript R/01_describe.R
Rscript R/02_pretrends.R
Rscript R/03_main_did.R
Rscript R/04_event_study.R
Rscript R/05_robustness.R
Rscript R/06_tables_figures.R

echo "== Done. Outputs in output/ ==="
```
 
### Running the Python pipeline (Stage 1)

Run scripts in order from the `python/` folder:

```bash
cd python
python 01_acled_clean.py
python 02_dhs_clean.py
python 03_geospatial_merge.py
python 04_conflict_exposure.py
python 05_panel_merge.py
```

After running, confirm `data/processed/analysis_panel.csv` exists before moving to Stage 2.

### Running the R pipeline (Stage 2)

Scripts source `00_config.R` automatically. Run in order from RStudio or the terminal:

```r
source("R/01_describe.R")
source("R/02_pretrends.R")
source("R/03_main_did.R")
source("R/04_event_study.R")
source("R/05_robustness.R")
source("R/06_tables_figures.R")
```

All outputs (tables, figures) are written to `output/`.

---

## Data Sources

| Dataset | Source | Notes |
|---------|--------|-------|
| ACLED conflict events | [acleddata.com](https://acleddata.com) | Requires free registration |
| DHS microdata | [dhsprogram.com](https://dhsprogram.com) | Requires project approval |
| Nigeria LGA shapefiles | GADM or NigeriaGIS | GADM level-2 admin boundaries |

---

## Key Design Choices

- **Treatment:** LGAs classified as high Boko Haram exposure based on pre-2009 conflict intensity
- **Treatment year:** 2009 (insurgency intensification)
- **Outcomes:** School enrolment, attendance rate, years of schooling, primary completion
- **Fixed effects:** LGA fixed effects + survey-year fixed effects
- **Standard errors:** Clustered at the LGA level
- **Conflict measure:** Log fatalities, IHS-transformed fatalities, event counts

---

## Git and Reproducibility

This repository commits all code, documentation, and package lockfiles.
Raw data and outputs are excluded (see `.gitignore`).

A collaborator can reproduce the full pipeline by:
1. Obtaining the raw data files and placing them in `data/raw/`
2. Running `pip install -r requirements.txt` and `renv::restore()`
3. Running scripts in numbered order

---

## Contact

Questions about the project or data access should be directed to the project author.
