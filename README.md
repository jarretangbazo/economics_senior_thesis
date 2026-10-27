# Education Under Fire
### Conflict Exposure and Educational Attainment in Nigeria

**Author:** Jarret Angbazo
**Period of work:** August 2012 – June 2013 (uses only data released by mid-2013)
**Identification strategy:** Difference-in-differences across region and birth cohort
**Data:** Nigeria DHS 2003 and 2008 household rosters + state boundaries

---

## Project Overview

Does exposure to armed conflict during childhood reduce how much schooling people complete? This project studies the Nigerian Civil War (July 1967 – January 1970), which closed schools across the Biafran-controlled south-east for nearly three years.

The design compares adults who were of school age (6–17) during the war with those who had already finished school, in the war region (Abia, Anambra, Ebonyi, Enugu, Imo) and in the rest of Nigeria. Completed schooling comes from the 2003 and 2008 DHS household rosters, which record the education of every household member, so cohorts born from 1935 onwards are observed with their schooling complete.

The pipeline has two stages, both in `code/`:

| Stage | Language | Files | Purpose |
|-------|----------|-------|---------|
| **Stage 1** | Python (Jupyter) | `01`–`02` `.ipynb` | Cleaning, cohort exposure, map |
| **Stage 2** | R | `03`–`05` `.R` | Descriptives, main estimates, event study, robustness |

**Handoff point:** `02_war_exposure.ipynb` writes `data/processed/analysis_war.csv`; the R scripts read it.
**Full pipeline:** run `bash code/master.sh` from anywhere (about 3 minutes).

---

## Folder Structure

```
econ-senior-thesis/
├── README.md                     # This file
├── .gitignore                    # Only code/, output/, README.md and renv.lock are committed
├── renv.lock                     # R package versions (restore with renv::restore())
│
├── code/
│   ├── master.sh                 # Runs the full pipeline end to end
│   ├── requirements.txt          # Python packages
│   ├── config.py                 # Python paths and study parameters
│   ├── config.R                  # R paths, parameters, permutation test, theme
│   ├── 01_dhs_clean.ipynb        # DHS 2003/2008 adults: birth year, schooling, age heaping
│   ├── 02_war_exposure.ipynb     # War region, cohort exposure, map
│   ├── 03_descriptives.R         # Summary table, schooling by cohort and region
│   ├── 04_main_results.R         # Main DiD table, cohort event study, permutation test
│   └── 05_robustness.R           # Robustness, placebo war, women vs men
│
├── output/                       # Committed
│   ├── tables/                   # .tex tables
│   └── figures/                  # .pdf and .png figures and maps
│
├── data/                         # Local only (license-restricted)
│   ├── raw/
│   │   ├── dhs/                  # NG_2003_DHS/, NG_2008_DHS/ (PR recode used)
│   │   ├── shapefiles/           # nga_admin_boundaries.shp/ (state map)
│   │   ├── acled/, ucdp/         # Conflict events up to 2012 (not used in the main analysis)
│   │   └── new_data/             # Data released after mid-2013 — not used here
│   └── processed/                # Written by the notebooks — do not edit manually
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
python3 -m venv .venv
.venv/bin/pip install -r code/requirements.txt
.venv/bin/nbstripout --install   # strip notebook outputs on commit
```

**R (>= 4.3)** with `tidyverse`, `fixest`, `modelsummary`, `here`, `glue`, `scales` and `withr`. Open `economics_senior_thesis.Rproj` and run `renv::restore()`.

### Running the pipeline

```bash
bash code/master.sh              # everything
bash code/master.sh --python     # notebooks only
bash code/master.sh --r          # R scripts only
```

`master.sh` executes the notebooks in place with `jupyter nbconvert` (using `.venv` if present), checks that `analysis_war.csv` exists, then runs the R scripts from the project root. Logs go to `output/logs/` (not committed).

---

## Data Sources

| Dataset | Source | Notes |
|---------|--------|-------|
| Nigeria DHS 2003, 2008 | [dhsprogram.com](https://dhsprogram.com) | Requires project approval; Household Member Recode (PR) used |
| Nigeria state boundaries | [OCHA / HDX](https://data.humdata.org/dataset/cod-ab-nga) | For the map only |

---

## Key Design Choices

- **Sample:** De facto household members born 1935–1975 in the DHS 2003 and 2008 rosters. Birth year is interview year minus reported age.
- **Treatment:** Living in the war region (Abia, Anambra, Ebonyi, Enugu, Imo) × being of school age (6–17) in at least one war year (born 1950–63). Intensity version: number of war years at school age (0–3).
- **Comparison:** Cohorts born 1935–49, who finished school before the war, and the rest of Nigeria. The partly exposed states (Akwa Ibom, Bayelsa, Cross River, Rivers, Delta, Edo) are excluded from the main sample.
- **Outcomes:** Completed years of schooling (`hv108`) and completed primary school (`hv109`).
- **Fixed effects:** State, birth year and survey wave, plus a sex control. Current wealth and urban residence are not controlled for: they are measured decades later and could be affected by the war.
- **Inference:** SEs clustered by state, plus a permutation test that reassigns the war region to 1,000 random sets of 5 states, because only 5 states are treated.
- **Event study:** War-region gap by 5-year birth cohort relative to those born 1945–49.
- **Robustness:** Wider war region, dropping heaped ages, each survey wave separately, survey weights, a placebo war in 1957–59, and women vs men.

---

## Git and Reproducibility

Only `code/`, `output/`, this README and `renv.lock` are committed. Raw and processed data, `docs/`, environments and R project files stay local (see `.gitignore`).

The `extended-2026` branch holds a later, larger version of the project (DHS 2003–2018, Boko Haram exposure from ACLED). It reads the files now in `data/raw/new_data/` from their original locations.

A collaborator can reproduce the full pipeline by:
1. Obtaining the DHS 2003 and 2008 files and placing them in `data/raw/dhs/` as shown above
2. Installing the Python and R prerequisites
3. Running `bash code/master.sh`

---

## Contact

Questions about the project or data access should be directed to the project author.
