# Variable Definitions

**Project**: Caught in the Crossfire — Boko Haram Insurgency and Educational Attainment in Northeast Nigeria  
**Last Updated**: March 2026

> This file defines every variable in the final analysis dataset (`data/processed/analysis_dataset.csv`). Add entries as variables are constructed during data cleaning. The source column indicates where the variable originates; the construction column documents any transformation.

---

## Outcome Variables

| Variable name | Label | Type | Range | Source | Construction | Notes |
|---|---|---|---|---|---|---|
| `years_schooling` | Years of schooling completed | continuous | 0–20 | DHS `v133` | Taken directly from DHS; verify against v106+v107 | **Primary outcome** |
| `any_primary` | Completed any primary school | binary | 0/1 | DHS `v106` | 1 if `v106` ≥ 1 | |
| `completed_primary` | Completed primary school | binary | 0/1 | DHS `v149` | 1 if `v149` ≥ 2 | |
| `any_secondary` | Completed any secondary school | binary | 0/1 | DHS `v149` | 1 if `v149` ≥ 3 | |
| `completed_secondary` | Completed secondary school | binary | 0/1 | DHS `v149` | 1 if `v149` ≥ 4 | |
| [Add more as built] | | | | | | |

---

## Treatment / Exposure Variables

| Variable name | Label | Type | Range | Source | Construction | Notes |
|---|---|---|---|---|---|---|
| `treated_binary` | LGA above-median conflict intensity | binary | 0/1 | ACLED | 1 if `lga_total_fatalities_0924` > median across Northern LGAs | Threshold defined before examining outcomes per analysis plan |
| `lga_total_fatalities_0924` | Cumulative ACLED fatalities 2009–2024 | integer | 0–∞ | ACLED | Sum of `fatalities` per LGA, 2009–2024 | |
| `log_fatalities_intensity` | Log fatalities per LGA (continuous treatment) | continuous | 0–∞ | ACLED | `log(1 + lga_total_fatalities_0924)` | |
| `lga_total_events_0924` | Cumulative ACLED events 2009–2024 | integer | 0–∞ | ACLED | Count of events per LGA, 2009–2024 | Robustness alternative to fatalities |
| `bk_fatalities_0924` | Cumulative Boko Haram fatalities 2009–2024 | integer | 0–∞ | ACLED | Sum where `boko_haram_event = 1` | More targeted measure |
| `post_cohort` | Born after 1991 (school-age during conflict) | binary | 0/1 | DHS `v010`/`v007`-`v012` | 1 if birth_year ≥ 1991 | See analysis_plan.md for cohort definition rationale |
| `conflict_exposure` | Interaction term (treated × post) | binary | 0/1 | Derived | `treated_binary × post_cohort` | Main DiD coefficient variable |
| [Add more as built] | | | | | | |

---

## Individual-Level Controls

| Variable name | Label | Type | Values | Source | Notes |
|---|---|---|---|---|---|
| `female` | Female respondent | binary | 0/1 | DHS `v151` or IR file | 1=Female, 0=Male |
| `birth_year` | Respondent birth year | integer | ~1960–2005 | DHS `v007` - `v012` | Approximate; use v011 (CMC) for precision |
| `age` | Age at interview | integer | 15–54 | DHS `v012` | |
| `urban` | Urban residence | binary | 0/1 | DHS `v025` | 1=Urban (DHS code 1), 0=Rural (DHS code 2) |
| `wealth_quintile` | Wealth index quintile | ordinal | 1–5 | DHS `v190` | 1=Poorest, 5=Richest |
| `wealth_score` | Wealth index factor score (continuous) | continuous | — | DHS `v191` | For robustness |
| `dhs_round` | DHS survey round | integer | 2003, 2008, 2013, 2018 | DHS `v007` | Survey round fixed effect |
| [Add more as built] | | | | | | |

---

## Geographic / Administrative Variables

| Variable name | Label | Type | Values | Source | Notes |
|---|---|---|---|---|---|
| `lga_name` | LGA name | string | 774 unique values | Shapefile join | Standardized to shapefile naming convention |
| `lga_code` | LGA numeric code | integer | — | Shapefile join | |
| `state_name` | State name | string | 36 + FCT | DHS v024 + shapefile | |
| `state_code` | DHS state code | integer | — | DHS `v024` | Changes across rounds — use name for merging |
| `geopolitical_zone` | Geopolitical zone | string | NW, NE, NC, SW, SE, SS | Derived from state | Nigeria's 6 geopolitical zones |
| `northeast_dummy` | Northeast zone indicator | binary | 0/1 | Derived | 1 if state in {Borno, Yobe, Adamawa, Bauchi, Gombe, Taraba} |
| `northern_dummy` | Northern Nigeria indicator | binary | 0/1 | Derived | 1 if geopolitical zone in {NW, NE, NC} |
| `dhs_cluster` | DHS cluster ID | integer | — | DHS `v001` | Use for clustering standard errors |
| `cluster_lat` | Cluster latitude (displaced) | float | — | DHS GPS file | Displaced per DHS protocol |
| `cluster_lon` | Cluster longitude (displaced) | float | — | DHS GPS file | Displaced per DHS protocol |

---

## Fixed Effects

| Variable name | Label | Used as FE | Notes |
|---|---|---|---|
| `lga_fe` | LGA fixed effect | Yes | Absorbs time-invariant LGA-level confounders |
| `cohort_fe` | Birth cohort fixed effect | Yes | Absorbs cohort-level confounders |
| `dhs_round_fe` | Survey round fixed effect | Yes (in multi-round specs) | Absorbs survey wave shocks |
| `state_trend` | State × linear time trend | Robustness only | Added to absorb state-level trends |

---

## Variable Construction Log

Document any non-trivial construction decisions here:

| Variable | Decision | Date | Script |
|---|---|---|---|
| `treated_binary` | Threshold = sample median of Northern LGA fatalities, not all-Nigeria median. Rationale: Southern LGAs are structural non-comparators; including them would dilute the threshold. | [Date] | `03_merge_data.py` |
| `post_cohort` | Birth year cutoff = 1991 (18 years old in 2009). Individuals born in 1992+ were ≤17 in 2009 and thus school-age at insurgency onset. | [Date] | `03_merge_data.py` |
| [Add decisions as made] | | | |

---

## Sample Restrictions Log

| Restriction | Obs. dropped | Running N | Date | Script |
|---|---|---|---|---|
| Starting sample (all Nigeria DHS 2008-2018) | — | [TBD] | | |
| Restrict to Northern Nigeria | [TBD] | | | |
| Restrict to ages 18–40 | [TBD] | | | |
| Drop LGAs with <20 DHS obs | [TBD] | | | |
| Drop missing outcome variable | [TBD] | | | |
| **Final analysis sample** | | [TBD] | | |
