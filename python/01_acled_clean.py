# =============================================================================
# 01_acled_clean.py
# Load and clean raw ACLED conflict event data.
#
# Input:  data/raw/acled/acled_nigeria.csv
# Output: data/processed/acled_clean.csv
#
# ACLED data: download from https://acleddata.com
# Filter to Nigeria, years relevant to your study window, before downloading.
# =============================================================================

import pandas as pd
import numpy as np
from config import ACLED_FILE, ACLED_CLEAN

# -----------------------------------------------------------------------------
# 1. Load
# -----------------------------------------------------------------------------
print("Loading ACLED data...")
df = pd.read_csv(ACLED_FILE)
print(f"  Raw rows: {len(df):,}")

# -----------------------------------------------------------------------------
# 2. Inspect — run this section first to understand your data
# -----------------------------------------------------------------------------
print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst few rows:")
print(df.head(3))

print("\nDate range:")
# ACLED date column is typically "event_date" formatted as "DD Month YYYY"
# print(df["event_date"].min(), "to", df["event_date"].max())

print("\nEvent types:")
# print(df["event_type"].value_counts())

print("\nAdmin1 (state) sample:")
# print(df["admin1"].value_counts().head(10))

# -----------------------------------------------------------------------------
# 3. Parse and clean
# -----------------------------------------------------------------------------

# -- Parse date ---------------------------------------------------------------
# ACLED stores dates as "DD Month YYYY" (e.g., "15 January 2010")
# df["date"] = pd.to_datetime(df["event_date"], format="%d %B %Y")
# df["year"] = df["date"].dt.year
# df["month"] = df["date"].dt.month

# -- Standardise column names -------------------------------------------------
# Rename to snake_case for consistency with the rest of the pipeline.
# Adjust the mapping below to match your actual ACLED column names.
rename_map = {
    # "event_date":    "event_date",   # keep as-is or rename
    # "event_type":    "event_type",
    # "admin1":        "state",
    # "admin2":        "lga",
    # "latitude":      "latitude",
    # "longitude":     "longitude",
    # "fatalities":    "fatalities",
    # "notes":         "notes",
}
# df = df.rename(columns=rename_map)

# -- Filter to Nigeria (should already be filtered, but double-check) ---------
# df = df[df["country"] == "Nigeria"].copy()

# -- Filter to Boko Haram events (optional — you may want all events first) ---
# boko_keywords = ["Boko Haram", "JAS", "ISWAP"]
# df["is_boko_haram"] = df["actor1"].str.contains("|".join(boko_keywords), na=False) | \
#                       df["actor2"].str.contains("|".join(boko_keywords), na=False)

# -- Clean fatalities ---------------------------------------------------------
# ACLED fatalities are sometimes stored as strings or have missing values.
# df["fatalities"] = pd.to_numeric(df["fatalities"], errors="coerce").fillna(0)

# -- Drop columns you don't need ----------------------------------------------
# keep_cols = ["date", "year", "month", "state", "lga", "latitude", "longitude",
#              "event_type", "fatalities", "is_boko_haram"]
# df = df[keep_cols]

# -----------------------------------------------------------------------------
# 4. Quick summary
# -----------------------------------------------------------------------------
# print(f"\nCleaned rows: {len(df):,}")
# print(f"Year range: {df['year'].min()} – {df['year'].max()}")
# print(f"Total fatalities: {df['fatalities'].sum():,.0f}")
# print(df.describe())

# -----------------------------------------------------------------------------
# 5. Save
# -----------------------------------------------------------------------------
# df.to_csv(ACLED_CLEAN, index=False)
# print(f"\nSaved to {ACLED_CLEAN}")

print("\n[TODO] Uncomment the cleaning steps above once you've inspected your data.")
