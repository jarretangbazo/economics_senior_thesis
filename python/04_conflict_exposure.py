# =============================================================================
# 04_conflict_exposure.py
# Build conflict exposure measures and treatment indicator at the LGA level.
#
# Input:  data/processed/acled_lga.csv
# Output: data/processed/conflict_lga_year.csv
#
# This script aggregates ACLED events to LGA × year and constructs the
# treatment variable used in the DiD design.
# =============================================================================

import pandas as pd
import numpy as np
from config import PROCESSED_DIR, TREATMENT_YEAR

ACLED_LGA       = PROCESSED_DIR / "acled_lga.csv"
CONFLICT_LGA    = PROCESSED_DIR / "conflict_lga_year.csv"

# =============================================================================
# 1. Load
# =============================================================================
print("Loading ACLED-LGA data...")
# df = pd.read_csv(ACLED_LGA)
# print(f"  Rows: {len(df):,}")

# =============================================================================
# 2. Aggregate to LGA × year
# =============================================================================
print("Aggregating to LGA-year level...")

# -- Count events and fatalities per LGA per year ----------------------------
# lga_year = (
#     df.groupby(["lga", "year"])
#     .agg(
#         n_events    = ("event_type",  "count"),
#         n_fatalities = ("fatalities", "sum"),
#     )
#     .reset_index()
# )

# -- Create a balanced panel (all LGA × year combinations) -------------------
# Some LGAs have zero conflict in certain years — we need those rows.
# all_lgas  = lga_year["lga"].unique()
# all_years = range(df["year"].min(), df["year"].max() + 1)
# full_idx  = pd.MultiIndex.from_product([all_lgas, all_years], names=["lga", "year"])
# lga_year  = lga_year.set_index(["lga", "year"]).reindex(full_idx, fill_value=0).reset_index()

# =============================================================================
# 3. Construct conflict intensity measures
# =============================================================================

# -- Log fatalities (add 1 to handle zeros) -----------------------------------
# lga_year["log_fatalities"] = np.log1p(lga_year["n_fatalities"])

# -- Inverse hyperbolic sine (IHS) transformation -----------------------------
# IHS is preferred over log for variables with many zeros.
# lga_year["ihs_fatalities"] = np.arcsinh(lga_year["n_fatalities"])

# =============================================================================
# 4. Construct treatment indicator
# =============================================================================
# Treatment = LGA was in the top quartile of conflict intensity pre-2009.
# This is one approach; adjust the threshold to fit your theoretical motivation.

# -- Pre-treatment conflict intensity per LGA --------------------------------
# pre_treatment = lga_year[lga_year["year"] < TREATMENT_YEAR]
# pre_intensity = (
#     pre_treatment.groupby("lga")["n_fatalities"]
#     .sum()
#     .reset_index()
#     .rename(columns={"n_fatalities": "pre_fatalities"})
# )

# -- Treatment = above median pre-treatment fatalities -----------------------
# You may want to experiment with different thresholds (median, top quartile, etc.)
# threshold = pre_intensity["pre_fatalities"].quantile(0.75)  # top quartile
# threshold = pre_intensity["pre_fatalities"].median()        # median split
# pre_intensity["treated"] = (pre_intensity["pre_fatalities"] > threshold).astype(int)

# -- Merge treatment indicator back onto the panel ---------------------------
# lga_year = lga_year.merge(pre_intensity[["lga", "treated", "pre_fatalities"]],
#                           on="lga", how="left")

# -- Post-treatment indicator ------------------------------------------------
# lga_year["post"] = (lga_year["year"] >= TREATMENT_YEAR).astype(int)

# -- DiD interaction term ----------------------------------------------------
# lga_year["treated_x_post"] = lga_year["treated"] * lga_year["post"]

# =============================================================================
# 5. Inspect
# =============================================================================
# print("\nTreatment group counts:")
# print(lga_year.drop_duplicates("lga")["treated"].value_counts())
# print(f"\nPanel rows: {len(lga_year):,}")
# print(lga_year.head())

# =============================================================================
# 6. Save
# =============================================================================
# lga_year.to_csv(CONFLICT_LGA, index=False)
# print(f"\nSaved to {CONFLICT_LGA}")

print("[TODO] Uncomment steps above once acled_lga.csv is ready.")
