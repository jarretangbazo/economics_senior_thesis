# DHS Codebook

**Dataset**: Nigeria Demographic and Health Surveys (NDHS)  
**Rounds used**: 2003, 2008, 2013, 2018, [2023 if available]  
**Source**: https://dhsprogram.com  
**Last Updated**: March 2026

> Working codebook. Add cleaning notes, recoding decisions, and variable construction details as you work through the data. The DHS recode manual (available at dhsprogram.com) is the authoritative reference — cross-check anything unclear there.

---

## Survey Structure

Nigeria DHS uses a stratified, two-stage cluster sampling design:
- **Stage 1**: Census enumeration areas (EAs) selected as clusters, stratified by state and urban/rural
- **Stage 2**: Households selected within clusters

**Key implication**: Standard errors must account for clustering at the EA level (match to `v001`). DHS sample weights (`v005`) must be applied for nationally representative estimates.

**Recode files used in this project**:
- **IR (Individual Recode)** — `NGIR*.DTA` — women 15–49; primary file for education outcomes
- **MR (Men's Recode)** — `NGMR*.DTA` — men 15–54; for gender heterogeneity analysis
- **HR (Household Recode)** — `NGHR*.DTA` — household-level variables; wealth, assets
- **GE (Geographic)** — `NGGE*.shp` — GPS cluster coordinates; critical for spatial merge

---

## Section 1: Identifiers and Weights

| Variable | Recode | Type | Description | Notes |
|---|---|---|---|---|
| **`v001`** | IR/MR | integer | Cluster number | Links to GPS file `DHSCLUST` |
| `v002` | IR | integer | Household number | |
| `v003` | IR | integer | Respondent line number | |
| **`v005`** | IR/MR | integer | Sample weight | **Divide by 1,000,000** before use. Required for all descriptive stats. |
| `v006` | IR | integer | Month of interview | |
| **`v007`** | IR | integer | Year of interview | Use to identify DHS round |
| `v008` | IR | integer | Date of interview (CMC) | Century-month code |

**Weight application**:
```python
df['weight'] = df['v005'] / 1_000_000
# For weighted mean: np.average(df['outcome'], weights=df['weight'])
```

---

## Section 2: Geography

| Variable | Recode | Type | Description | Notes |
|---|---|---|---|---|
| **`v024`** | IR | integer/label | Region (state) | 36 states + FCT; numeric codes differ across rounds — use value labels |
| **`v025`** | IR | integer | Urban/rural | 1 = Urban, 2 = Rural |
| `v101` | IR | integer | Region (alternative) | Sometimes = v024; verify |
| `v102` | IR | integer | Type of place of residence | 1=Capital/large city, 2=Small city, 3=Town, 4=Countryside |
| `sstate` | HR | string | State name | In HR recode; link through cluster |

**State code crosswalk**: DHS numeric state codes vary between rounds. Build a crosswalk table when merging rounds. Document here:

| State | 2008 code | 2013 code | 2018 code |
|---|---|---|---|
| Borno | [add] | [add] | [add] |
| Yobe | [add] | [add] | [add] |
| Adamawa | [add] | [add] | [add] |
| [continue] | | | |

**GPS file variables** (from `NGGE*.shp`):

| Variable | Description | Notes |
|---|---|---|
| `DHSCLUST` | Cluster number | Links to `v001` |
| `LATNUM` | Latitude (decimal) | Displaced ≤2 km urban, ≤5 km rural |
| `LONGNUM` | Longitude (decimal) | Same displacement |
| `URBAN_RURA` | U = Urban, R = Rural | Cross-check with `v025` |
| `ADM1NAME` | State name | |
| `ADM1DHS` | DHS state code | Match to `v024` |
| `DHSREGCO` | DHS region code | |

---

## Section 3: Education (Primary Outcomes)

| Variable | Recode | Type | Description | Notes |
|---|---|---|---|---|
| **`v133`** | IR | integer | Education in single years | **Primary outcome variable**. Ranges 0–20+. Constructed/imputed by DHS. |
| **`v106`** | IR | integer | Highest education level | 0=None, 1=Primary, 2=Secondary, 3=Higher |
| **`v107`** | IR | integer | Highest year of education within level | Combined with v106 to reconstruct v133 |
| **`v149`** | IR | integer | Educational attainment (6 categories) | 0=No education, 1=Incomplete primary, 2=Complete primary, 3=Incomplete secondary, 4=Complete secondary, 5=Higher |
| `v115` | IR | integer | Literacy (reading ability) | 0=Cannot read, 1=Reads parts, 2=Reads whole sentence |
| `v116` | IR | integer | Reads newspaper | |
| `v106_partner` | IR | integer | Partner's education level | Control variable |

**`v133` construction notes**:
- DHS constructs this variable by converting v106 + v107 into years based on country-specific school system
- Cross-check: `v133` should roughly equal `v107` + years in previous levels
- Nigeria: Primary = 6 years, JSS = 3 years, SSS = 3 years, University = 4 years
- Respondents still in school: v133 captures *completed* years — may understate eventual attainment for younger cohorts
- Values > 18 are rare and may indicate data entry errors — inspect distribution

**Cleaning note**: [Add any issues found, e.g., "2003 round: 47 observations with v133 = 97 (don't know) recoded to missing on [date]."]

---

## Section 4: Age and Cohort Variables

| Variable | Recode | Type | Description | Notes |
|---|---|---|---|---|
| **`v012`** | IR | integer | Current age | Women 15–49 |
| `v010` | IR | integer | Year of birth | Constructed from v008 - (v012 × 12). Verify |
| `v011` | IR | integer | Date of birth (CMC) | Century-month code; more precise than v010 |
| `b0`–`b16` | IR | integer | Birth history variables | For women with children |

**Cohort variable construction**:
```python
# Year of birth (approximate from interview year and age)
df['birth_year'] = df['v007'] - df['v012']

# Cohort exposure indicator: was respondent school-age (6-18) during 2009-2020?
# School-age in 2009: born 1991-2003 → age 6 in 2009 if born 2003, age 18 in 2009 if born 1991
df['school_age_during_conflict'] = (
    (df['birth_year'] >= 1991) & (df['birth_year'] <= 2003)
).astype(int)
```

*Refine these cutoffs after examining the data — document final decision in analysis_plan.md.*

---

## Section 5: Household and Socioeconomic Variables

| Variable | Recode | Type | Description | Notes |
|---|---|---|---|---|
| **`v190`** | IR | integer | Wealth index quintile | 1=Poorest, 2=Poorer, 3=Middle, 4=Richer, 5=Richest. **Primary SES control.** |
| `v191` | IR | float | Wealth index factor score | Continuous underlying score; use for robustness |
| `v113` | IR | integer | Source of drinking water | |
| `v116a` | IR | integer | Owns cell phone | |
| `v012_hh_head` | HR | integer | Age of household head | In household recode |
| `v151` | IR | integer | Sex of household head | 1=Male, 2=Female |
| `v152` | IR | integer | Age of household head | |

**Wealth index notes**:
- DHS wealth index is a PCA-based composite of household assets and characteristics
- Not directly comparable across DHS rounds (computed separately per round)
- For cross-round comparisons, use quintile rank or re-compute using pooled PCA
- [Add cleaning decisions here]

---

## Section 6: Religion and Ethnicity (Contextual Controls)

| Variable | Recode | Type | Description | Notes |
|---|---|---|---|---|
| `v130` | IR | integer | Religion | 1=Christianity, 2=Islam, 3=Traditionalist, 6=Other |
| `v131` | IR | integer | Ethnicity | Varies by round; check value labels |

**Notes**: Religion and ethnicity are sensitive control variables. Including them may introduce bad controls (potentially mediated by conflict). Use with caution — document decision in analysis_plan.md.

---

## Section 7: GPS and Spatial Linkage

**Procedure for linking DHS respondents to LGAs**:

1. Load GPS file (`NGGE*.shp`) — contains cluster centroids
2. Load Nigeria LGA shapefile (`nga_lga/`)
3. Spatial join: assign each cluster to the LGA polygon it falls within
4. Merge result to DHS individual data via `DHSCLUST` = `v001`

```python
import geopandas as gpd

# Load files
clusters = gpd.read_file("data/raw/dhs/2018/NGGE7AFL/NGGE7AFL.shp")
lgas = gpd.read_file("data/raw/shapefiles/nga_lga/nga_admbnda_adm2_osgof.shp")

# Ensure same CRS
clusters = clusters.to_crs(lgas.crs)

# Spatial join
cluster_lga = gpd.sjoin(clusters, lgas, how="left", predicate="within")
```

**GPS displacement robustness**: Re-run spatial join with 10 km buffer around each cluster centroid. If multiple LGAs fall within buffer, use nearest centroid. Compare treatment assignment between base and buffered version.

---

## Round-Specific Notes

### 2003 (NGIR4AFL)
- [Add notes when you work with this round]

### 2008 (NGIR5AFL)
- [Add notes when you work with this round]
- This is the last pre-peak-insurgency round — key baseline

### 2013 (NGIR6AFL)
- [Add notes when you work with this round]
- Overlaps with insurgency peak (2013–2015)

### 2018 (NGIR7AFL)
- [Add notes when you work with this round]
- Post-peak; captures displacement effects

---

## Known Data Quality Issues

| Issue | Affected variable | Round(s) | Resolution |
|---|---|---|---|
| [Add as discovered] | | | |
