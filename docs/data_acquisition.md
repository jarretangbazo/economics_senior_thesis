# Data Acquisition Guide

**Project**: Education Under Fire: Conflict Exposure and Educational Attainment in Northern Nigeria
**Last Updated**: March 2026

---

## Overview

This project uses two primary datasets: **ACLED** for conflict events and **Nigeria DHS** for individual-level education outcomes. Both are freely available but require registration. This guide covers how to download, what to request, and where to store the files.

Raw data files **must never be committed to GitHub**. Confirm `.gitignore` includes `data/raw/` before downloading anything.

---

## 1. ACLED — Armed Conflict Location & Event Data

### What it is
ACLED is a disaggregated conflict data collection project coding the dates, actors, locations, fatalities, and types of all reported political violence and protest events in Africa (and globally). For this project, ACLED is the source of conflict exposure measures at the LGA level.

### Access

**Website**: https://acleddata.com/data-export-tool/

**Registration**:
1. Go to https://developer.acleddata.com and create a free account
2. You will receive an API key via email (typically within minutes)
3. Store your API key in a local `.env` file — never hardcode it in scripts

**Manual Download (recommended for reproducibility)**:
1. Log in at https://acleddata.com
2. Go to **Export Data → Custom Export**
3. Apply the following filters:
   - **Country**: Nigeria
   - **Year range**: 2000–2024 (captures pre-insurgency baseline and full conflict period)
   - **Event types**: Select all (Battle, Explosion/Remote Violence, Violence Against Civilians, Riots, Protests, Strategic Developments)
4. Export as `.csv`
5. Save to `data/raw/acled/`

**API Download (for automated pipeline)**:
```python
import requests
import pandas as pd

API_KEY = "your_key_here"  # load from .env in practice
EMAIL = "your_email@here.com"

url = "https://api.acleddata.com/acled/read"
params = {
    "key": API_KEY,
    "email": EMAIL,
    "country": "Nigeria",
    "year": "2000|2001|2002|...|2024",  # pipe-separated
    "limit": 0,  # 0 = no limit
}

response = requests.get(url, params=params)
df = pd.DataFrame(response.json()["data"])
df.to_csv("data/raw/acled/nigeria_acled_2000_2024.csv", index=False)
```

### Key Variables to Keep
| Variable | Description |
|---|---|
| `event_id_cnty` | Unique event identifier |
| `event_date` | Date of event (YYYY-MM-DD) |
| `year` | Year of event |
| `event_type` | Broad category (Battle, VAC, etc.) |
| `sub_event_type` | Granular type (Attack, Abduction, etc.) |
| `actor1` | Primary actor |
| `actor2` | Secondary actor (if applicable) |
| `admin1` | State (e.g., Borno, Yobe, Adamawa) |
| `admin2` | LGA (Local Government Area) |
| `admin3` | Town/settlement (if available) |
| `latitude` | Decimal latitude |
| `longitude` | Decimal longitude |
| `fatalities` | Number killed (may be 0) |
| `notes` | Event description (useful for manual review) |

### Notes and Caveats
- **Coverage begins**: ACLED Nigeria coverage starts in 1997, but is most complete from ~2009 onward
- **Reporting bias**: Events in remote or inaccessible areas are systematically underreported; Borno state interior is the most affected
- **Fatalities**: Treat as a lower bound; ACLED uses conservative estimates from news sources
- **Actor coding**: "Boko Haram" appears under multiple actor labels over time — document and standardize during cleaning (see `code/data_processing/01_acled_clean.py`)
- **Versioned data**: ACLED periodically revises historical records; download and document the version date in `data/raw/acled/README_acled_version.txt`

### Recommended Citation
```
Raleigh, C., Linke, A., Hegre, H., & Karlsen, J. (2010). Introducing ACLED: An Armed
Conflict Location and Event Dataset. Journal of Peace Research, 47(5), 651–660.
```

---

## 2. Nigeria DHS — Demographic and Health Surveys

### What it is
The Nigeria DHS provides individual- and household-level data on education, health, and demographics. The surveys include geocoded cluster coordinates, enabling linkage to conflict data. Multiple rounds (2003, 2008, 2013, 2018, 2023) allow cohort-based analysis comparing individuals who were school-age before and during the Boko Haram insurgency.

### Access

**Website**: https://dhsprogram.com/data/dataset_admin/login_main.cfm

**Registration**:
1. Go to https://dhsprogram.com and click **Get Datasets**
2. Create a free account (requires institutional affiliation — use your university)
3. Submit a **dataset request** form for each Nigeria DHS round you need:
   - Provide a brief project description: *"Examining the causal impact of the Boko Haram insurgency on educational attainment in Northeast Nigeria using a difference-in-differences design."*
   - Select: Individual Recode (IR), Household Recode (HR), Geographic Data (GE)
4. Approval typically takes 1–3 business days

**Datasets to Request**:

| Round | Survey Code | Years | Key Notes |
|---|---|---|---|
| 2003 | NG2003DHS | 2003 | Pre-insurgency baseline |
| 2008 | NG2008DHS | 2008 | Pre-insurgency baseline |
| 2013 | NG2013DHS | 2013 | Overlaps with insurgency peak |
| 2018 | NG2018DHS | 2018 | Post-peak, displacement era |
| 2023 | NG2023DHS | 2023 | Most recent (if available) |

**File Types to Download** for each round:
- `NGIR*.DTA` — Individual Recode (women 15–49); primary source for education outcomes
- `NGMR*.DTA` — Men's Recode (men 15–54); for gender heterogeneity analysis
- `NGHR*.DTA` — Household Recode; for household-level controls
- `NGGE*.shp` — GPS cluster shapefile; **critical** for spatial merge with ACLED

Store each round in a separate subdirectory: `data/raw/dhs/2003/`, `data/raw/dhs/2008/`, etc.

### Key Variables to Keep
| Variable | Description |
|---|---|
| `v001` | Cluster number |
| `v005` | Sample weight (divide by 1,000,000 before use) |
| `v007` | Year of interview |
| `v012` | Respondent's current age |
| `v106` | Highest education level |
| `v107` | Highest year of education within level |
| `v133` | Education in single years (imputed) — **primary outcome** |
| `v149` | Educational attainment (6-category) |
| `v025` | Urban/rural |
| `v024` | Region (state) |
| `v190` | Wealth index (5 quintiles) |
| `b0`–`b16` | Birth history (for women) |
| `v102` | Type of place of residence |

**From GPS file**:
| Variable | Description |
|---|---|
| `DHSCLUST` | Cluster number (links to `v001`) |
| `LATNUM` | Latitude |
| `LONGNUM` | Longitude |
| `URBAN_RURA` | Urban/rural classification |
| `ADM1NAME` | State name |

### Notes and Caveats
- **GPS displacement**: DHS deliberately displaces cluster GPS coordinates by up to 2 km (urban) and 5 km (rural) to protect respondent privacy. This introduces measurement error in your conflict exposure variable. Account for this in robustness checks.
- **Geographic identifiers**: State-level identifiers (`v024`) are always available; LGA-level is not included in standard DHS files and requires spatial join with GPS coordinates
- **Weights**: Always apply sample weights for descriptive statistics; for regression, decision depends on your estimator (document your choice)
- **Women only in IR**: The Individual Recode covers women 15–49. For men, use the MR recode but note it is a sub-sample
- **Education variable construction**: `v133` (education in single years) is most useful but imputed; cross-check with `v106` + `v107` for consistency

### Recommended Citation
```
National Population Commission (NPC) [Nigeria] and ICF. (2019). Nigeria Demographic and 
Health Survey 2018. Abuja, Nigeria, and Rockville, Maryland, USA: NPC and ICF.
```

---

## 3. Shapefiles — Nigeria LGA Boundaries

### What they are
LGA (Local Government Area) boundary shapefiles are needed to (1) aggregate conflict events from points to LGA-level counts and (2) assign DHS clusters to LGAs.

### Access

**Option 1 — OCHA HDX (recommended)**:
- URL: https://data.humdata.org/dataset/nigeria-administrative-level-0-1-and-2-boundaries
- Download: `nga_admbnda_adm2_osgof_20190417.shp` (LGA-level boundaries)
- Free, no registration required

**Option 2 — GADM**:
- URL: https://gadm.org/download_country.html
- Select Nigeria, Level 2
- Also free

Save to: `data/raw/shapefiles/nga_lga/`

### Notes
- Nigeria has **774 LGAs** across 36 states + FCT
- LGA names are inconsistent across datasets — you will need a crosswalk; one is included in `data/raw/shapefiles/lga_name_crosswalk.csv` (create this manually during data cleaning)

---

## 4. File Storage Conventions

```
data/
├── raw/
│   ├── acled/
│   │   ├── nigeria_acled_2000_2024.csv        # Raw download
│   │   └── README_acled_version.txt           # Download date, version
│   ├── dhs/
│   │   ├── 2003/
│   │   │   ├── NGIR4AFL.DTA                   # Individual recode
│   │   │   ├── NGHR4AFL.DTA                   # Household recode
│   │   │   └── NGGE4AFL/                      # GPS shapefiles
│   │   ├── 2008/
│   │   ├── 2013/
│   │   └── 2018/
│   └── shapefiles/
│       └── nga_lga/                           # LGA boundaries
├── intermediate/                              # Output of cleaning scripts
└── processed/
    └── analysis_dataset.csv                   # Final merged dataset
```

**Version tracking**: Create a `data/raw/DOWNLOAD_LOG.txt` file recording what you downloaded, when, and from which URL. This ensures reproducibility even when source data is updated.
