# =============================================================================
# config.py
# Shared paths and constants for the Python pipeline.
# All other scripts import from here — edit paths only in this file.
# =============================================================================

from pathlib import Path

# -----------------------------------------------------------------------------
# Project root
# Adjust this if your folder is in a different location.
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path("/Users/jarretangbazo/Projects/economics_senior_thesis")

# -----------------------------------------------------------------------------
# Data paths
# -----------------------------------------------------------------------------
RAW_DIR        = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR  = PROJECT_ROOT / "data" / "processed"

ACLED_RAW_DIR      = RAW_DIR / "acled"
DHS_RAW_DIR        = RAW_DIR / "dhs"
SHAPEFILES_DIR     = RAW_DIR / "shapefiles"

# Raw source files — update filenames to match what you downloaded
ACLED_FILE     = ACLED_RAW_DIR / "acled_nigeria.csv"        # ACLED export
DHS_FILE       = DHS_RAW_DIR   / "dhs_nigeria.dta"          # DHS Stata file

# Shapefile — GADM level-2 (LGA boundaries)
LGA_SHAPEFILE  = SHAPEFILES_DIR / "gadm41_NGA_2.shp"
STATE_SHAPEFILE = SHAPEFILES_DIR / "gadm41_NGA_1.shp"

# Processed outputs (written by Python, read by R)
ACLED_CLEAN    = PROCESSED_DIR / "acled_clean.csv"
DHS_CLEAN      = PROCESSED_DIR / "dhs_clean.csv"
CONFLICT_LGA   = PROCESSED_DIR / "conflict_lga_year.csv"
ANALYSIS_PANEL = PROCESSED_DIR / "analysis_panel.csv"       # *** R reads this ***

# Output directories
OUTPUT_DIR     = PROJECT_ROOT / "output"
FIGURES_DIR    = OUTPUT_DIR / "figures"
TABLES_DIR     = OUTPUT_DIR / "tables"
LOGS_DIR       = OUTPUT_DIR / "logs"

# -----------------------------------------------------------------------------
# Study parameters
# -----------------------------------------------------------------------------
TREATMENT_YEAR    = 2009          # Boko Haram insurgency intensification
NORTH_STATES      = [             # Northern Nigerian states in the study
    "Adamawa", "Bauchi", "Borno", "Gombe",
    "Jigawa", "Kaduna", "Kano", "Katsina",
    "Kebbi", "Niger", "Plateau", "Sokoto",
    "Taraba", "Yobe", "Zamfara",
    "Kogi", "Kwara", "Nasarawa",
]
OUTCOME_VARS      = [             # DHS education outcome variables (update as needed)
    "attend",
    "highest_enrolled",
]
CONFLICT_MEASURES = [             # Conflict intensity measures to construct
    "n_events",
    "n_fatalities",
    "log_fatalities",
    "ihs_fatalities",
]

# -----------------------------------------------------------------------------
# Utility — make sure processed/output dirs exist before any script runs
# -----------------------------------------------------------------------------
for _dir in [PROCESSED_DIR, FIGURES_DIR, TABLES_DIR, LOGS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)
