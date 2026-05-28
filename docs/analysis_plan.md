# Pre-Registered Analysis Plan

**Project**: Education Under Fire: Conflict Exposure and Educational Attainment in Northern Nigeria  
**Author**: Jarret Angbazo  
**Date Written**: March 3, 2026
**Status**: [ ] Draft  [ ] Finalized  [ ] Pre-registered (AEA RCT Registry / OSF)

---

## 1. Research Questions

**Primary question**: Did exposure to the Boko Haram insurgency reduce educational attainment among individuals who were school-age during the conflict period?

**Secondary questions**:
1. Are effects larger for girls than boys?
2. Are effects larger in the Northeast (conflict epicenter) versus other Northern regions?
3. Are effects larger for poorer households?
4. Are effects larger in rural areas?
5. Do effects differ by ethnicity or religion?
6. Is there evidence of catch-up (attenuating effects for younger cohorts)?

---

## 2. Hypotheses

**H1 (Primary)**: Individuals who were school-age (ages 6–18) during periods of high conflict intensity in their birth region will complete fewer years of schooling than similar individuals from the same region born before the insurgency, or from less-affected regions.

*Direction*: Negative. Both supply-side (school destruction, teacher displacement) and demand-side (household income shocks, safety concerns) mechanisms predict reduced attainment.

**H2 (Gender heterogeneity)**: The negative effect of conflict exposure on educational attainment is larger for girls than boys.

*Direction*: Girls ≥ boys in magnitude. Mechanisms: greater safety concerns for girls, gender-based targeting by Boko Haram, household prioritization of boys' schooling under resource constraints.

**H3 (Intensity dose-response)**: Effects are increasing in conflict intensity (fatalities per capita, event count).

*Direction*: Monotonically negative with intensity. Falsification: near-zero effects in low-intensity LGAs.

**H4 (Wealth heterogeneity)**: Effects are larger for households in lower wealth quintiles.

*Direction*: Wealthier households can better substitute (private schools, relocation, tutoring); poorer households cannot buffer the shock.

**H5 (Regional heterogeneity)**: Effects are largest in Borno, Yobe, and Adamawa states and attenuate with distance from the insurgency epicenter.

*Direction*: Northeast > North Central > South.

---

## 3. Identification Strategy

### 3.1 Design

**Difference-in-differences (DiD)** exploiting variation in:
- **Time**: Pre- vs. post-2009 (Boko Haram's founding/onset of violence)
- **Space**: High-conflict vs. low-conflict LGAs (defined by ACLED event counts or fatalities per capita)

**Key assumption**: In the absence of the insurgency, educational attainment trends in high- and low-conflict LGAs would have been parallel (parallel trends assumption).

### 3.2 Primary Specification

**Unit of observation**: Individual *i* from LGA *l* in birth cohort *c*

```
Y_ilc = α + β(TreatedLGA_l × PostCohort_c) + γ_l + δ_c + X_ilc'Θ + ε_ilc
```

Where:
- `Y_ilc` = years of schooling completed (primary outcome)
- `TreatedLGA_l` = 1 if LGA *l* experienced above-median conflict intensity during 2009–2020
- `PostCohort_c` = 1 if cohort *c* was school-age (6–18) during the conflict period
- `γ_l` = LGA fixed effects (absorb all time-invariant LGA-level confounders)
- `δ_c` = Cohort fixed effects (absorb all cohort-level confounders)
- `X_ilc` = Individual/household controls (wealth index, urban/rural, gender)
- `β` = DiD coefficient of interest

**Standard errors**: Clustered at the LGA level (treatment level). Robustness: two-way clustering by LGA and cohort.

### 3.3 Alternative/Extended Specifications

**Continuous treatment** (intensity measure):
```
Y_ilc = α + β(ConflictIntensity_l × PostCohort_c) + γ_l + δ_c + X_ilc'Θ + ε_ilc
```
Where `ConflictIntensity_l` = log(1 + fatalities per capita in LGA *l*, 2009–2020)

**Event study** (to test pre-trends and trace dynamic effects):
```
Y_ilc = α + Σ_τ β_τ (TreatedLGA_l × CohortDummy_τ) + γ_l + δ_c + X_ilc'Θ + ε_ilc
```
Plot β_τ coefficients — should be near zero for pre-2009 cohorts and negative for post-2009 cohorts.

**Stacked DiD** (if using multiple DHS rounds as a panel-like structure):
- Follow Cengiz et al. (2019) / Baker et al. (2022) methodology
- Construct cohort-specific clean comparison groups to address heterogeneous treatment timing concerns

### 3.4 Cohort Definition

| Cohort | Birth years | School-age during... | Treatment status |
|---|---|---|---|
| Pre-insurgency | 1975–1991 | 1981–2009 | Control (not school-age during conflict) |
| Partially exposed | 1992–1997 | 1998–2015 | Partial (school-age at onset) |
| Fully exposed | 1998–2005 | 2004–2023 | Full (entirely school-age during conflict) |

*Exact cutoffs to be determined by DHS age distribution and conflict timeline — document final decision here.*

---

## 4. Outcome Variables

**Primary outcome**:
- `years_schooling` — constructed from DHS `v133` (education in single years); range 0–20

**Secondary outcomes**:
- `any_primary` — 1 if completed any primary school (v106 ≥ 1)
- `completed_primary` — 1 if completed primary school
- `any_secondary` — 1 if completed any secondary school
- `completed_secondary` — 1 if completed secondary school
- `currently_enrolled` — 1 if currently attending school (for school-age sub-sample)

**Outcome construction pre-committed**: Primary outcome is continuous years of schooling. Binary completion variables are secondary. We will not switch to a binary outcome as the primary outcome based on results.

---

## 5. Treatment Variable Construction

**Binary treatment** (pre-committed threshold): LGA is "treated" if cumulative conflict fatalities per 10,000 population during 2009–2020 exceed the **sample median** among Northern Nigerian LGAs. This threshold is defined before examining outcomes.

**Continuous treatment** (intensity): log(1 + total ACLED fatalities in LGA, 2009–2020). Robustness: log(1 + total ACLED events), log(1 + Battle events only), log(1 + Violence Against Civilians events only).

**Spatial assignment**: Each DHS respondent is assigned to an LGA using the spatial join of DHS GPS cluster coordinates and the Nigeria LGA shapefile. DHS cluster GPS displacement (up to 5 km rural) introduces measurement error — test robustness using a 10 km buffer.

---

## 6. Control Variables

All controls entered as pre-committed:
- Gender (male/female)
- Urban/rural
- Wealth index quintile (DHS v190)
- Survey round fixed effects (if pooling across rounds)
- State × year fixed effects (as robustness — absorbs state-level time trends)
- Ethnicity/Religion

We will **not** include any post-treatment controls (e.g., current employment, migration status) that could be outcomes of conflict exposure themselves (bad controls problem).

---

## 7. Sample Restrictions

**Base sample**:
- Nigeria DHS respondents from 2008, 2013, and 2018 rounds
- Age 18–40 at time of survey (old enough to have completed primary school)
- Northern Nigeria only (6 geopolitical zones: NW, NE, NC — or refine to core ACLED treatment states)

**Exclusions** (pre-committed):
- Respondents under 18 (may still be enrolled; left-censored outcome)
- Respondents over 45 (less reliable conflict exposure assignment for early cohorts)
- LGAs with fewer than 20 DHS observations (insufficient statistical power; document count)

**Final sample size**: To be documented once data is merged.

---

## 8. Heterogeneity Analysis

Pre-committed subgroup analyses (family-wise error rate correction via Bonferroni or Holm-Bonferroni):

1. **Gender**: Estimate separately for women and men; test H[0]: β_female = β_male
2. **Wealth quintile**: Bottom 40% vs. top 60%
3. **Urban/rural**: Separate estimates for urban and rural DHS clusters
4. **Northeast vs. other North**: Borno/Yobe/Adamawa vs. remaining Northern states
5. **Conflict type**: Restrict ACLED to "Violence Against Civilians" events; test if effects differ from all-events measure
6. **Ethnicity/religion controls**: Boko Haram's targeting wasn't spatially random. Areas with higher Muslim populations are differentially targeted but also have pre-existing differences in girls' education norms. Our conflict exposure measure may absorb this pre-existing cultural variation if this isn't controlled for.

---

## 9. Parallel Trends Validation

**Event study plot**: Estimate β_τ for each birth cohort relative to baseline (pre-insurgency cohorts). Pre-trend coefficients should be statistically indistinguishable from zero.

**Placebo test 1**: Re-run analysis using Southern Nigerian LGAs where Boko Haram was absent. Expect zero effect.

**Placebo test 2**: Use a fake treatment onset year (e.g., 2003, 2006) to confirm no spurious effects in pre-period.

**Falsification test**: Replace educational attainment with an outcome that *should not* be affected by conflict (e.g., birth year, or a pre-determined characteristic). Expect zero effect.

---

## 10. Robustness Checks

All robustness checks are secondary to the primary specification:

1. **Alternative treatment threshold**: Top tercile instead of above-median for binary treatment
2. **Alternative conflict measure**: Event count instead of fatalities per capita
3. **Alternative spatial unit**: State-level treatment instead of LGA-level
4. **Standard error clustering**: Two-way clustering (LGA + cohort) vs. state-level clustering
5. **Control for pre-existing trends**: Include state × linear trend interactions
6. **GPS displacement buffer**: Expand assignment radius to 10 km for rural clusters
7. **Balanced cohort panel**: Restrict to cohorts with observations in all pre/post periods
8. **DHS round fixed effects**: Include survey round FE to absorb round-specific shocks
9. **Stacked DiD**: Address potential Callaway-Sant'Anna / Sun-Abraham heterogeneous treatment concerns

---

## 11. Deviations from This Plan

| Deviation | Original plan | What was done | Rationale |
|---|---|---|---|
| | | | |

---

## 12. Pre-Registration

Before finalizing analysis, register this plan at:
- **AEA RCT Registry** (https://www.socialscienceregistry.org) — preferred for economics
- **OSF** (https://osf.io) — alternative, broader audience

Registration date: [ ] Not yet registered

Registration link: [to be filled in]


---

## 13. Distance to conflict
Exposure to conflict.
I will use distance to conflict as an exposure variable. As the crow flies distance, while tempting, is not the best metric to use as it may not account for certain geographical features that may make the effective distance between a household and a conflict incidence larger. As an example, a household that is 10 km away from a conflict location may be further than a second household that is 15 km away from the same conflict location if the first household is separated from the conflict location by a deep canyon or dense forest while the second household is connected to the conflict area via roads.

We will implement this exposure variable into our analysis as follows:
1. Pull ACLED data with event coordinates filtered to Boko Haram events during our study period
2. Download **Malaria Atlas Project's 2019 global travel time to cities** friction raster for Nigeria. This incorporates roads, terrain, land cover, and walking speed into a single friction surface. It has solid coverage even for Nigeria.
3. For each household, compute least-cost cumulative travel time to the nearest ACLED conflict event using the friction raster
4. Run the educational outcome regressions using that travel time measure as the exposure variable
5. Compare results to the naive haversine distance specification as a robustness check. This combines haversine distance + the **SRTM terrain ruggedness index**.  

**NOTE**: DHS displaces households (especially rural households) by up to 10 km randomly for privacy reasons. As such, it may be preferable to aggregate the conflict exposure measure to the cluster level as opposed to the household level or use a radius-based measure that is less sensitive to the 10 km jitter. LSMS-ISA Nigeria doesn't have the same displacement issue and gives actual coordinates so this may be preferable.

