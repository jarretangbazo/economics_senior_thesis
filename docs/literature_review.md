# Literature Review Notes

**Project**: Education Under Fire: Conflict Exposure and Educational Attainment in Northern Nigeria  
**Last Updated**: March 2026

---

## Themes Index

1. [Conflict and Education (Core Literature)](#1-conflict-and-education-core-literature)
2. [Boko Haram and Nigeria Context](#2-boko-haram-and-nigeria-context)
3. [Difference-in-Differences and Causal Identification](#3-difference-in-differences-and-causal-identification)
4. [Mechanisms: Supply vs. Demand](#4-mechanisms-supply-vs-demand)
5. [Gender and Conflict](#5-gender-and-conflict)
6. [Long-Run Human Capital Effects](#6-long-run-human-capital-effects)
7. [Data and Measurement](#7-data-and-measurement)
8. [Nigeria Education System Background](#8-nigeria-education-system-background)

---

## 1. Conflict and Education (Core Literature)

### ★ Leone, Pastore & Molla (2019) — *Journal of Development Economics*
**Full citation**: Leone, T., Pastore, F., & Molla, G. (2019). Education is Forbidden: The Effect of the Boko Haram Conflict on Education in North-East Nigeria. *Journal of Development Economics*, 141, 102249.

**Method**: Difference-in-differences using DHS data and ACLED conflict events. Exposure assigned at state level.

**Data**: Nigeria DHS 2008, 2013; ACLED Nigeria.

**Core finding**: Boko Haram insurgency reduced years of schooling by approximately 0.9–1.4 years for affected cohorts in Northeast Nigeria. Effects concentrated among girls.

**Takeaways for your thesis**:
- Most directly comparable paper to yours; cite prominently in intro and lit review
- Their state-level exposure measure may miss within-state variation — your LGA-level measure is an improvement
- Replicate their baseline spec as a validity check before extending
- Their data ends in 2013; extending to 2018 DHS is a contribution
- Check if they address DHS GPS displacement issue

**Gaps this paper creates for you**: Limited geographic granularity (state vs. LGA); no pre-trend analysis published; no wealth heterogeneity.

---

### ★ Akresh & de Walque (2008) — *World Bank Policy Research Working Paper*
**Full citation**: Akresh, R., & de Walque, D. (2008). Armed Conflict and Schooling: Evidence from the 1994 Rwandan Genocide. *World Bank Policy Research Working Paper 4606*.

**Method**: DiD comparing exposed vs. non-exposed cohorts using post-genocide DHS data.

**Core finding**: Genocide reduced primary school completion by 15 percentage points. Effects larger for those who were school-age during the conflict.

**Takeaways**:
- Foundational paper for cohort-based DiD in conflict/education; cite as methodological precedent
- Shows how to use DHS to construct retrospective cohort exposure — adapt their cohort definition logic

---

### ★ Shemyakina (2011) — *Journal of Development Economics*
**Full citation**: Shemyakina, O. (2011). The Effect of Armed Conflict on Accumulation of Schooling: Results from Tajikistan. *Journal of Development Economics*, 95(2), 186–200.

**Method**: DiD using household survey data; variation in conflict intensity across districts.

**Core finding**: Girls in conflict-affected districts had significantly lower schooling completion; boys less affected.

**Takeaways**:
- Key precedent for gender heterogeneity hypothesis (H2)
- Tajikistan context shares features with Northern Nigeria (patriarchal norms, conservative gender attitudes)
- Reference when motivating gender analysis

---

### Swee (2015) — *Journal of Development Economics*
**Full citation**: Swee, E. L. (2015). On War and Schooling Attainment: The Case of Bosnia and Herzegovina. *Journal of Development Economics*, 113, 24–36.

**Method**: Cohort-based DiD exploiting within-country variation in conflict intensity.

**Core finding**: War reduced schooling by 0.5 years on average; effects heterogeneous by ethnicity and pre-war conditions.

**Takeaways**:
- Good model for heterogeneity analysis structure
- Shows how to handle varying conflict intensity rather than binary exposure

---

### Justino & Verwimp (2013) — *Journal of Development Economics*
**Full citation**: Justino, P., & Verwimp, P. (2013). Poverty Dynamics, Violent Conflict, and Convergence in Rwanda. *Review of Income and Wealth*, 59(1), 66–90.

**Takeaways**:
- Not directly on education but framework for how conflict affects household investment decisions (poverty dynamics)
- Useful for mechanism discussion (Section 3.2)

---

## 2. Boko Haram and Nigeria Context

### ★ Afzal (2020) — Brookings Institution Report
**Full citation**: Afzal, N. (2020). Education and Boko Haram in Nigeria. *Brookings Institution Center for Middle East Policy*.

**URL**: https://www.brookings.edu/wp-content/uploads/2020/04/FP_20200507_nigeria_boko_haram_afzal.pdf

**Core content**:
- Name "Boko Haram" = "Western education is forbidden" in Hausa/Arabic
- Group explicitly targeted schools, teachers, and students (600+ teachers killed 2009–2022)
- 1,400 schools destroyed; 13.2 million out-of-school children attributed to insurgency
- Northern Nigeria has structurally lower education baseline than South — exacerbated by conflict
- Al-majiri (Quranic school) system historically dominant; tension with Western schooling

**Takeaways**:
- Essential context for introduction and motivation (Section 1)
- Explains the *ideological* mechanism (not just tactical disruption) — important for mechanism discussion
- Provides concrete statistics for intro paragraphs

---

### ★ Olashore et al. (2016) — *African Human Rights Law Journal*
**Full citation**: Olashore, A., Akanni, O., Fela-Thomas, A., & Kinnear, J. (2016). Impact of the Boko Haram insurgency on the child's right to education in Nigeria. *African Human Rights Law Journal*, 16(1), 645–669.

**Key statistics**:
- 314 children killed 2012–2014 in school attacks
- 84% of IDPs displaced specifically by Boko Haram
- Borno state: 64% of all Nigerian IDPs

**Takeaways**:
- Concrete statistics for magnitude of disruption — cite in introduction
- Legal framing useful for policy implications section

---

### Campbell & Harwood (2018) — Council on Foreign Relations
**Full citation**: Campbell, J., & Harwood, A. (2018). *Boko Haram: Origins, Challenges, and Responses*. Council on Foreign Relations Policy Innovation Memorandum No. 66.

**Takeaways**:
- Background on Boko Haram founding, ideology, and geographic evolution
- Useful for Chapter 4 (Context and Background)
- Explains factional splits (ISWAP) — note for data cleaning (actor label standardization)

---

## 3. Difference-in-Differences and Causal Identification

### ★ Angrist & Pischke (2009) — *Mostly Harmless Econometrics*
**Citation**: Angrist, J. D., & Pischke, J. S. (2009). *Mostly Harmless Econometrics: An Empiricist's Companion*. Princeton University Press.

**Relevant chapters**: Ch. 5 (DiD), Ch. 3 (regression anatomy), Ch. 8 (IV)

**Takeaways**:
- Primary methodological reference; cite Chapter 5 when describing DiD design
- Use their notation for two-way fixed effects specification

---

### ★ Callaway & Sant'Anna (2021) — *Journal of Econometrics*
**Full citation**: Callaway, B., & Sant'Anna, P. H. C. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics*, 225(2), 200–230.

**Core finding**: Standard TWFE DiD estimator can produce misleading results under heterogeneous treatment effects across cohorts. Proposes cohort-time average treatment effects as an alternative.

**Takeaways**:
- Relevant if you use multiple DHS rounds as a panel
- May need to implement their estimator as robustness; Python package `csdid` or R package `did`
- Discuss in robustness section; reassures readers you're aware of recent DiD literature

---

### Sun & Abraham (2021) — *Journal of Econometrics*
**Full citation**: Sun, L., & Abraham, S. (2021). Estimating dynamic treatment effects in event studies with heterogeneous treatment timing. *Journal of Econometrics*, 225(2), 175–199.

**Takeaways**:
- Complementary to Callaway & Sant'Anna; cite both
- "Interaction-weighted estimator" as alternative to standard event study

---

### Baker et al. (2022) — *Journal of Financial Economics*
**Full citation**: Baker, A. C., Larcker, D. F., & Wang, C. C. Y. (2022). How much should we trust staggered difference-in-differences estimates? *Journal of Financial Economics*, 144(2), 370–395.

**Takeaways**:
- Stacked DiD as practical solution to heterogeneous DiD issues
- Cite when describing robustness check approach

---

## 4. Mechanisms: Supply vs. Demand

### ★ Shemyakina (2011) [also in Section 1]
- Documents both supply (school closure) and demand (household safety concerns) mechanisms

### Merrouche (2011) — *Journal of African Economies*
**Full citation**: Merrouche, O. (2011). The long term educational cost of war: Evidence from landmine contamination in Cambodia. *Journal of African Economies*, 20(2), 208–225.

**Takeaways**:
- Good model for isolating supply-side mechanism using school destruction data
- Suggests using school reconstruction data as falsification — may be relevant if you can get UBEC data

---

### Blattman & Miguel (2010) — *Journal of Economic Literature*
**Full citation**: Blattman, C., & Miguel, E. (2010). Civil War. *Journal of Economic Literature*, 48(1), 3–57.

**Takeaways**:
- Comprehensive review of civil conflict's economic consequences
- Essential cite for general motivation ("cost of conflict" literature)
- Read Section IV on economic impacts

---

## 5. Gender and Conflict

### ★ Shemyakina (2011) [see Section 1]

### Justino (2011) — *IDS Working Paper*
**Full citation**: Justino, P. (2011). Violent conflict and human capital accumulation. *IDS Working Paper 2011*(379).

**Takeaways**:
- Reviews gender-differentiated effects of conflict on human capital
- Useful for H2 motivation

---

## 6. Long-Run Human Capital Effects

### Akresh, Bhalotra, Leone & Osili (2012) — *American Economic Review P&P*
**Full citation**: Akresh, R., Bhalotra, S., Leone, M., & Osili, U. O. (2012). War and stature: Growing up during the Nigerian civil war. *American Economic Review: Papers & Proceedings*, 102(3), 273–77.

**Takeaways**:
- Uses Nigeria specifically — cite for within-country precedent
- Shows height-for-age affected by Nigerian civil war — analogous mechanism to education
- Reinforces that conflict has lasting human capital effects in Nigeria context

---

## 7. Data and Measurement

### ★ Raleigh et al. (2010) — *Journal of Peace Research*
**Full citation**: Raleigh, C., Linke, A., Hegre, H., & Karlsen, J. (2010). Introducing ACLED: An Armed Conflict Location and Event Dataset. *Journal of Peace Research*, 47(5), 651–660.

**Takeaways**:
- Primary methodological citation for ACLED data; cite in data section
- Note ACLED coverage limitations discussed in paper

---

### Burgert et al. (2013) — DHS Spatial Analysis Report
**Full citation**: Burgert, C. R., Colston, J., Roy, T., & Zachary, B. (2013). Geographic displacement procedure and georeferenced data release policy for the Demographic and Health Surveys. *DHS Spatial Analysis Reports No. 7*.

**Takeaways**:
- Official DHS documentation of GPS displacement procedure (up to 5 km rural, 2 km urban)
- Cite when describing measurement error concern in data section
- Guides robustness check design (10 km buffer)

---

## 8. Nigeria Education System Background

### Lewin (2009) — *Comparative Education Review*
**Full citation**: Lewin, K. M. (2009). Access to education in sub-Saharan Africa: Patterns, problems and possibilities. *Comparative Education*, 45(2), 151–174.

**Takeaways**:
- Context on sub-Saharan Africa education systems; cite for comparative framing
- North-South educational disparities in Nigeria fit broader SSA patterns

---

### [Add more as you read]

---

## Papers to Read (Queue)

- [ ] Alderman, Hoddinott & Kinsey (2006) — Long-term consequences of early childhood malnutrition (*Oxford Economic Papers*) — for mechanism discussion
- [ ] Chamarbagwala & Moran (2011) — Guatemala education and civil conflict (*JDE*)
- [ ] Valente (2014) — Nepal and armed conflict education (*JDE*)
- [ ] Krishnaswamy (2023) — any recent updates on Boko Haram and education?
- [ ] UNHCR / UNOCHA Nigeria situation reports for conflict timeline documentation
