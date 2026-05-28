# =============================================================================
# 03_geospatial_merge.py
# Spatial join: assign DHS clusters and ACLED events to LGAs.
# Produces choropleth maps of conflict intensity.
#
# Inputs:  data/processed/acled_clean.csv
#          data/processed/dhs_clean.csv
#          data/raw/shapefiles/gadm41_NGA_2.shp  (LGA boundaries)
#          data/raw/shapefiles/gadm41_NGA_1.shp  (state boundaries)
# Outputs: data/processed/acled_lga.csv
#          data/processed/dhs_lga.csv
#          output/figures/map_conflict_intensity.png
#          output/figures/map_treatment_lgas.png
# =============================================================================

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
from config import (
    ACLED_CLEAN, DHS_CLEAN,
    LGA_SHAPEFILE, STATE_SHAPEFILE,
    PROCESSED_DIR, FIGURES_DIR,
    TREATMENT_YEAR,
)

# Processed output paths
ACLED_LGA = PROCESSED_DIR / "acled_lga.csv"
DHS_LGA   = PROCESSED_DIR / "dhs_lga.csv"

# =============================================================================
# PART 1: Load shapefiles
# =============================================================================
print("Loading shapefiles...")
# lga_gdf   = gpd.read_file(LGA_SHAPEFILE)
# state_gdf = gpd.read_file(STATE_SHAPEFILE)

# print(f"  LGAs:   {len(lga_gdf):,}")
# print(f"  States: {len(state_gdf):,}")

# -- Inspect shapefile columns ------------------------------------------------
# GADM column names for Nigeria level-2:
#   NAME_1 = state name
#   NAME_2 = LGA name
#   geometry = polygon
# print(lga_gdf.columns.tolist())
# print(lga_gdf[["NAME_1", "NAME_2"]].head(10))

# -- Standardise CRS to WGS84 (EPSG:4326) ------------------------------------
# All spatial objects must share the same CRS before joining.
# lga_gdf   = lga_gdf.to_crs("EPSG:4326")
# state_gdf = state_gdf.to_crs("EPSG:4326")

# =============================================================================
# PART 2: Assign ACLED events to LGAs
# =============================================================================
print("Assigning ACLED events to LGAs...")
# acled = pd.read_csv(ACLED_CLEAN)

# -- Convert ACLED to GeoDataFrame using lat/lon ------------------------------
# acled_gdf = gpd.GeoDataFrame(
#     acled,
#     geometry=gpd.points_from_xy(acled["longitude"], acled["latitude"]),
#     crs="EPSG:4326",
# )

# -- Spatial join: which LGA does each event fall in? -------------------------
# acled_lga = gpd.sjoin(
#     acled_gdf,
#     lga_gdf[["NAME_1", "NAME_2", "geometry"]],
#     how="left",
#     predicate="within",
# )

# -- Check how many events could not be matched to an LGA --------------------
# unmatched = acled_lga["NAME_2"].isna().sum()
# print(f"  Unmatched events: {unmatched:,} ({unmatched/len(acled_lga):.1%})")

# -- Drop geometry column before saving (not needed downstream) ---------------
# acled_lga_df = acled_lga.drop(columns="geometry")
# acled_lga_df.to_csv(ACLED_LGA, index=False)
# print(f"  Saved to {ACLED_LGA}")

# =============================================================================
# PART 3: Assign DHS clusters to LGAs
# =============================================================================
print("Assigning DHS clusters to LGAs...")
# DHS cluster GPS coordinates come from the DHS GPS dataset (a separate file).
# Download the geographic data file (.dbf/.shp) alongside the survey data.

# dhs = pd.read_csv(DHS_CLEAN)

# -- If DHS GPS data is a separate file, load and merge on cluster_id --------
# dhs_gps = gpd.read_file("data/raw/dhs/dhs_gps.shp")
# dhs_gps = dhs_gps.to_crs("EPSG:4326")
# dhs_lga = gpd.sjoin(dhs_gps, lga_gdf[["NAME_1", "NAME_2", "geometry"]],
#                     how="left", predicate="within")

# -- Merge LGA assignment back to DHS household data -------------------------
# dhs_merged = dhs.merge(
#     dhs_lga[["cluster_id", "NAME_1", "NAME_2"]].rename(
#         columns={"NAME_1": "state_shp", "NAME_2": "lga"}
#     ),
#     on="cluster_id", how="left",
# )
# dhs_merged.to_csv(DHS_LGA, index=False)
# print(f"  Saved to {DHS_LGA}")

# =============================================================================
# PART 4: Maps
# =============================================================================
print("Producing maps...")

# -- Map 1: Conflict intensity pre-treatment (before TREATMENT_YEAR) ----------
# acled_pre = acled_lga_df[acled_lga_df["year"] < TREATMENT_YEAR]
# conflict_by_lga = (
#     acled_pre.groupby("NAME_2")["fatalities"].sum().reset_index()
#     .rename(columns={"NAME_2": "lga", "fatalities": "total_fatalities"})
# )
# map_df = lga_gdf.merge(conflict_by_lga, left_on="NAME_2", right_on="lga", how="left")
# map_df["total_fatalities"] = map_df["total_fatalities"].fillna(0)

# fig, ax = plt.subplots(1, 1, figsize=(10, 10))
# map_df.plot(
#     column="total_fatalities",
#     ax=ax,
#     cmap="YlOrRd",
#     legend=True,
#     legend_kwds={"label": "Total Fatalities (pre-2009)", "shrink": 0.6},
#     missing_kwds={"color": "lightgrey"},
#     edgecolor="white",
#     linewidth=0.3,
# )
# state_gdf.boundary.plot(ax=ax, color="black", linewidth=0.6)
# ax.set_title("ACLED Conflict Fatalities by LGA (Pre-2009)", fontsize=14)
# ax.axis("off")
# plt.tight_layout()
# plt.savefig(FIGURES_DIR / "map_conflict_intensity.png", dpi=300)
# plt.savefig(FIGURES_DIR / "map_conflict_intensity.pdf")
# plt.close()
# print(f"  Saved map_conflict_intensity")

# -- Map 2: Treatment assignment (high vs low conflict LGAs) ------------------
# See 04_conflict_exposure.py — run that first, then add a treatment map here.

print("[TODO] Uncomment steps above once shapefiles and cleaned data are ready.")
