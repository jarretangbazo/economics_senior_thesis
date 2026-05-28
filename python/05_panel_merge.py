# =============================================================================
# 05_panel_merge.py
# Merge cleaned DHS data with conflict exposure measures into one analysis panel.
#
# Inputs:  data/processed/dhs_lga.csv
#          data/processed/conflict_lga_year.csv
# Output:  data/processed/analysis_panel.csv   *** R reads this ***
#
# This is the final Python step. After this, move to the R pipeline.
# =============================================================================

import pandas as pd
import numpy as np
from config import PROCESSED_DIR, ANALYSIS_PANEL

DHS_LGA      = PROCESSED_DIR / "dhs_lga.csv"
CONFLICT_LGA = PROCESSED_DIR / "conflict_lga_year.csv"

# =============================================================================
# 1. Load
# =============================================================================
print("Loading cleaned datasets...")
# dhs      = pd.read_csv(DHS_LGA)
# conflict = pd.read_csv(CONFLICT_LGA)

# print(f"  DHS rows:      {len(dhs):,}")
# print(f"  Conflict rows: {len(conflict):,}")

# =============================================================================
# 2. Merge
# =============================================================================
# The merge key is lga + survey_year.
# DHS surveys are conducted in specific years — each respondent is matched to
# the conflict conditions in their LGA in the year of the survey.

# panel = dhs.merge(
#     conflict,
#     on=["lga", "survey_year"],   # adjust column names if needed
#     how="left",
#     validate="m:1",              # many DHS respondents per LGA-year
# )

# -- Check merge quality -----------------------------------------------------
# unmatched = panel["n_events"].isna().sum()
# print(f"\n  Unmatched DHS rows (no conflict record): {unmatched:,}")
# If unmatched > 0, investigate: LGA name mismatches are common.
# Use fuzzy matching (thefuzz library) or manual crosswalk to fix.

# =============================================================================
# 3. Final variable construction
# =============================================================================

# -- Any remaining variables that need both datasets -------------------------
# e.g., interaction terms you prefer to build in Python

# -- Convert dtypes -----------------------------------------------------------
# panel["treated"]       = panel["treated"].astype(int)
# panel["post"]          = panel["post"].astype(int)
# panel["treated_x_post"] = panel["treated_x_post"].astype(int)

# =============================================================================
# 4. Checks
# =============================================================================
# print("\nFinal panel overview:")
# print(panel.describe())
# print(f"\nPanel shape: {panel.shape}")
# print(f"Unique LGAs: {panel['lga'].nunique():,}")
# print(f"Survey years: {sorted(panel['survey_year'].unique())}")

# -- Check for duplicate rows (there shouldn't be any) -----------------------
# dupes = panel.duplicated().sum()
# if dupes > 0:
#     print(f"WARNING: {dupes:,} duplicate rows found — investigate before proceeding.")

# -- Missing values summary ---------------------------------------------------
# missing = panel.isnull().sum()
# print("\nMissing values:")
# print(missing[missing > 0])

# =============================================================================
# 5. Save
# =============================================================================
# panel.to_csv(ANALYSIS_PANEL, index=False)
# print(f"\nSaved analysis panel to {ANALYSIS_PANEL}")
# print("Python pipeline complete. Proceed to R.")

print("[TODO] Uncomment steps above once dhs_lga.csv and conflict_lga_year.csv are ready.")
