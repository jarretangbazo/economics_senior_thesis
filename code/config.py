# =============================================================================
# config.py
# Shared paths and constants for the Python notebooks (01–02).
# Every notebook runs `from config import *` — edit paths only in this file.
# =============================================================================

from pathlib import Path

# -----------------------------------------------------------------------------
# Project root: the folder that contains code/. Resolved from this file's
# location so the project runs wherever it is cloned.
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# -----------------------------------------------------------------------------
# Raw data
# -----------------------------------------------------------------------------
RAW_DIR        = PROJECT_ROOT / "data" / "raw"
DHS_RAW_DIR    = RAW_DIR / "dhs"
SHAPEFILES_DIR = RAW_DIR / "shapefiles"

# DHS Household Member Recode (PR): every household member, with age, sex,
# completed schooling (hv108, hv109) and state of residence (shstate)
DHS_PR_FILES = {
    2003: DHS_RAW_DIR / "NG_2003_DHS" / "NGPR4CDT" / "NGPR4CFL.DTA",
    2008: DHS_RAW_DIR / "NG_2008_DHS" / "NGPR53DT" / "NGPR53FL.DTA",
}

# State boundaries (for map)
STATE_SHAPEFILE = SHAPEFILES_DIR / "nga_admin_boundaries.shp" / "nga_admin1.shp"

# -----------------------------------------------------------------------------
# Processed data
# -----------------------------------------------------------------------------
PROCESSED_DIR  = PROJECT_ROOT / "data" / "processed"
DHS_ADULTS     = PROCESSED_DIR / "dhs_adults.csv"        # 01
ANALYSIS_FILE  = PROCESSED_DIR / "analysis_war.csv"      # 02 — Read by R analysis scripts

# -----------------------------------------------------------------------------
# Outputs
# -----------------------------------------------------------------------------
OUTPUT_DIR  = PROJECT_ROOT / "output"
FIGURES_DIR = OUTPUT_DIR / "figures"
TABLES_DIR  = OUTPUT_DIR / "tables"

# -----------------------------------------------------------------------------
# Study parameters — keep in sync with code/config.R
# -----------------------------------------------------------------------------
WAR_YEARS     = [1967, 1968, 1969]       # Nigerian Civil War: July 1967 – January 1970
SCHOOL_AGE    = (6, 17)                  # primary (6–12) through secondary (13–17)
BIRTH_YEARS   = (1935, 1975)             # cohorts kept for analysis
PLACEBO_YEARS = [1957, 1958, 1959]       # fake war, ten years earlier

# War region: Igbo-majority states that remained under Biafran control for most of the
# war (the former East Central State)
WAR_STATES = ["Abia", "Anambra", "Ebonyi", "Enugu", "Imo"]

# Rest of the former Eastern Region (recaptured early in the war) and the
# Mid-West (invaded in August 1967): partly exposed, so excluded from the
# comparison group in the main specification
PARTLY_EXPOSED_STATES = ["Akwa Ibom", "Bayelsa", "Cross River", "Rivers", "Delta", "Edo"]

# DHS spells some states differently from the shapefile
DHS_STATE_FIXES = {
    "nassarawa": "Nasarawa",
    "zamfora": "Zamfara",
    "abuja": "Federal Capital Territory",
    "abuja (fct)": "Federal Capital Territory",
}

# -----------------------------------------------------------------------------
# Make sure output directories exist before any notebook writes to them
# -----------------------------------------------------------------------------
for _dir in [PROCESSED_DIR, FIGURES_DIR, TABLES_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)
