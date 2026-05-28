# =============================================================================
# 02_dhs_clean.py
# Load and clean DHS survey microdata.
#
# Input:  data/raw/dhs/dhs_nigeria.dta
# Output: data/processed/dhs_clean.csv
#
# DHS data: download from https://dhsprogram.com (project approval required).
# The individual recode (IR) and household member recode (PR) files are
# the most useful for education outcomes.
# =============================================================================

import pandas as pd
import numpy as np
import pyreadstat          # reads .dta Stata files
from config import DHS_FILE, DHS_CLEAN, OUTCOME_VARS

# -----------------------------------------------------------------------------
# 1. Load
# -----------------------------------------------------------------------------
print("Loading DHS data...")

# pyreadstat preserves Stata value labels — useful for understanding variables
# df, meta = pyreadstat.read_dta(DHS_FILE)

# Alternatively with pandas (no labels):
# df = pd.read_stata(DHS_FILE)

# print(f"  Raw rows: {len(df):,}")
# print(f"  Columns:  {len(df.columns):,}")

# -----------------------------------------------------------------------------
# 2. Inspect
# -----------------------------------------------------------------------------

# -- Print variable labels (Stata metadata) -----------------------------------
# for var, label in meta.column_labels.items():
#     print(f"  {var:30s} {label}")

# -- Check key variables -------------------------------------------------------
# print("\nSample columns:")
# print(df.head(3))

# -----------------------------------------------------------------------------
# 3. Select and rename variables
# -----------------------------------------------------------------------------
# DHS variable names use a prefix system (e.g., hv for household, v for woman).
# Common education-relevant variables in the PR (household member) recode:
#
#   hv001  = cluster number  (links to GPS coordinates)
#   hv002  = household number
#   hvidx  = line number (individual ID within household)
#   hv105  = age of household member
#   hv104  = sex of household member (1=male, 2=female)
#   hv109  = educational attainment
#   hv121  = attended school during current year (1=yes)
#   hv122  = educational level attending
#   hv123  = grade level attending
#   hv108  = years of education
#   shstreg = de jure region (Nigeria-specific)
#   hv024  = region/state
#
# Adjust the rename map below to your actual variable names.

rename_map = {
    # "hv001":  "cluster_id",
    # "hv002":  "household_id",
    # "hvidx":  "person_id",
    # "hv105":  "age",
    # "hv104":  "sex",           # 1=male, 2=female
    # "hv108":  "years_educ",
    # "hv121":  "attend",        # attended school this year
    # "hv024":  "state",
    # "hv025":  "urban_rural",   # 1=urban, 2=rural
    # "hv270":  "wealth_index",  # 1=poorest ... 5=richest
}

# df = df.rename(columns=rename_map)
# keep_cols = list(rename_map.values())
# df = df[keep_cols].copy()

# -----------------------------------------------------------------------------
# 4. Construct variables
# -----------------------------------------------------------------------------

# -- Binary sex indicator (1=male, 0=female) ----------------------------------
# df["male"] = (df["sex"] == 1).astype(int)

# -- School-age children (e.g., 6–18) ----------------------------------------
# df = df[df["age"].between(6, 18)].copy()

# -- Urban indicator ----------------------------------------------------------
# df["urban"] = (df["urban_rural"] == 1).astype(int)

# -- Survey year --------------------------------------------------------------
# DHS files sometimes embed the year; otherwise hard-code from the filename.
# df["survey_year"] = 2018   # adjust to your DHS wave

# -- State name cleaning ------------------------------------------------------
# State names in DHS may include codes or trailing spaces.
# df["state"] = df["state"].str.strip().str.title()

# -----------------------------------------------------------------------------
# 5. Drop missing on key outcomes
# -----------------------------------------------------------------------------
# print(f"\nRows before dropping missing: {len(df):,}")
# df = df.dropna(subset=OUTCOME_VARS)
# print(f"Rows after dropping missing:  {len(df):,}")

# -----------------------------------------------------------------------------
# 6. Quick summary
# -----------------------------------------------------------------------------
# print("\nCleaned data overview:")
# print(df.describe())
# print(f"\nSchool attendance rate: {df['attend'].mean():.1%}")
# print(f"Mean years of education: {df['years_educ'].mean():.2f}")

# -----------------------------------------------------------------------------
# 7. Save
# -----------------------------------------------------------------------------
# df.to_csv(DHS_CLEAN, index=False)
# print(f"\nSaved to {DHS_CLEAN}")

print("[TODO] Uncomment the cleaning steps above once you've inspected your data.")
