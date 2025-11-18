# Detailed Econometric Methodology
## Impact of Violent Conflict on Educational Attainment in Nigeria

---

## Table of Contents

1. [Theoretical Framework](#theoretical-framework)
2. [Identification Strategy](#identification-strategy)
3. [Econometric Specifications](#econometric-specifications)
4. [Identification Assumptions](#identification-assumptions)
5. [Robustness Checks](#robustness-checks)
6. [Potential Limitations](#potential-limitations)
7. [Extensions and Future Work](#extensions)

---

## 1. Theoretical Framework

### How Conflict Affects Education: Theoretical Channels

**Direct Effects**:
1. **School Destruction**: Physical destruction of schools, reducing supply
2. **Teacher Flight**: Teachers flee conflict zones, reducing quality
3. **Student Displacement**: Families flee, interrupting schooling
4. **Mortality and Injury**: Direct casualties reduce school attendance

**Indirect Effects**:
1. **Household Income Shocks**: Conflict reduces income → reduced education investment
2. **Opportunity Costs**: Child labor more valuable during conflict
3. **Security Concerns**: Parents keep children home due to safety fears
4. **Psychological Trauma**: PTSD and trauma affect learning capacity
5. **Expectations**: Reduced returns to education in conflict zones

### The Boko Haram Context

**Timeline**:
- **2002-2008**: Early organization formation, low-intensity activity
- **2009**: Boko Haram uprising, government crackdown begins
- **2009-2014**: Escalating insurgency in Northeast Nigeria
- **2014-2015**: Peak violence, territorial control
- **2015-present**: Ongoing insurgency, international intervention

**Geographic Concentration**:
- **Epicenter**: Borno, Yobe, Adamawa states (Northeast)
- **Secondary**: Bauchi, Gombe, Plateau, Kaduna
- **Spillover**: Occasional attacks in other regions

**Educational Impact Mechanisms in Nigeria**:
1. **Direct Attacks on Schools**: Boko Haram specifically targeted schools (name means "Western education is forbidden")
2. **Teacher Assassination**: Targeted killing of educators
3. **Student Kidnapping**: Mass abductions (Chibok girls, 2014)
4. **Displacement**: 2+ million internally displaced persons
5. **Poverty**: Economic disruption in Northeast

---

## 2. Identification Strategy

### Why Difference-in-Differences?

**The Fundamental Problem of Causal Inference**:
- We want to know: What would education outcomes in the Northeast have been *without* conflict?
- This counterfactual is unobserved

**DiD Solution**:
- Use changes in other regions as the counterfactual
- Assumes trends would have been parallel absent treatment

### Treatment and Control Groups

**Treatment Group** (Two Dimensions):
1. **Geographic**: Northeast region (Borno, Yobe, Adamawa, Gombe, Bauchi, Taraba)
2. **Temporal**: Birth cohorts who were school-age during 2009-2020

**Control Group**:
1. **Geographic**: Other Nigerian regions
2. **Temporal**: Birth cohorts who completed school before 2009

**Key Identification Advantage**:
- Treatment is based on birth year → predetermined, not chosen
- Reduces selection concerns

### The DiD Logic

```
Effect = [Northeast_Post - Northeast_Pre] - [Other_Post - Other_Pre]
       = Δ_Northeast - Δ_Other
```

This differences out:
- Time-invariant differences between regions (β₁)
- Common time trends affecting all regions (β₂)

---

## 3. Econometric Specifications

### Specification 1: Basic 2x2 DiD

**Equation**:
```
Y_i = β₀ + β₁·Northeast_i + β₂·Post_i + β₃·(Northeast_i × Post_i) + ε_i
```

**Variables**:
- Y_i: Years of schooling for individual i
- Northeast_i: 1 if lives in Northeast, 0 otherwise
- Post_i: 1 if born after 1991 (school-age during conflict), 0 otherwise
- β₃: The DiD estimate (treatment effect)

**Standard Errors**:
- Heteroskedasticity-robust (White/Huber)
- Or cluster by state (if sufficient clusters)

**Interpretation**:
- β₁: Baseline difference between Northeast and other regions
- β₂: Common trend for all regions (cohort effects)
- β₃: **Additional effect of being in Northeast AND exposed to conflict**

**Advantages**: Simple, transparent, easy to interpret

**Limitations**: No controls for confounders

---

### Specification 2: DiD with Individual Controls

**Equation**:
```
Y_i = β₀ + β₁·Northeast_i + β₂·Post_i + β₃·(Northeast_i × Post_i) 
      + X_i'γ + ε_i
```

**Additional Controls (X_i)**:
- Age (continuous)
- Urban residence indicator
- Wealth quintile fixed effects
- Survey year fixed effects

**Why Include Controls?**
- Improves precision (reduces residual variance)
- Controls for compositional changes
- Not strictly necessary for unbiasedness if parallel trends holds

**Standard Errors**:
- Clustered by state (accounts for within-state correlation)

---

### Specification 3: DiD with State Fixed Effects

**Equation**:
```
Y_i = β₃·(Northeast_i × Post_i) + β₂·Post_i + X_i'γ + α_s + ε_i
```

Where:
- α_s: State fixed effects
- Note: Northeast_i is absorbed by state FE

**What This Controls For**:
- All time-invariant state characteristics
- Historical differences in education systems
- Cultural factors
- Geographic features
- Economic development levels

**Identification**:
- Within-state variation only
- Comparing same states over time
- More demanding specification

**Trade-off**:
- Reduces bias from state-level confounders
- But reduces statistical power (fewer degrees of freedom)

---

### Specification 4: Continuous Treatment Intensity

**Equation**:
```
Y_i = β₁·ConflictIntensity_i + X_i'γ + α_s + τ_t + ε_i
```

Where:
- ConflictIntensity_i: Violent events per year during school age in individual's state
- τ_t: Survey year fixed effects

**Advantages**:
- Uses full variation in conflict exposure
- More efficient (exploits continuous variation)
- Can examine dose-response relationship

**Interpretation**:
- β₁: Effect of one additional violent event per year during school age
- Example: β₁ = -0.05 → 10 events/year → -0.5 years schooling

---

### Specification 5: Event Study (Dynamic DiD)

**Equation**:
```
Y_i = Σ_(k≠-1) β_k·(Northeast_i × Cohort_k) + X_i'γ + α_s + τ_t + ε_i
```

Where:
- Cohort_k: Indicators for birth year relative to conflict start
- k = -10, -9, ..., -2, 0, 1, ..., 10 (omit k = -1 as reference)

**Purpose**:
1. **Test Parallel Trends**: Pre-treatment β_k should be ≈ 0
2. **Dynamic Effects**: Shows how effects evolve over time
3. **Anticipation Effects**: Detects if effects started before conflict

**Graphical Test**:
- Plot β_k against k
- Pre-period (k < 0): Should be flat around zero
- Post-period (k ≥ 0): Can be non-zero

**Example Interpretation**:
```
β_-3 = 0.1  (p=0.6)  ← No pre-trend
β_-2 = -0.05 (p=0.8) ← No pre-trend
β_0  = -0.4  (p=0.03) ← Immediate effect
β_1  = -0.8  (p=0.01) ← Growing effect
β_2  = -1.2  (p=0.00) ← Larger effect
```

---

### Specification 6: Triple Differences (DDD)

**Equation** (if data permits):
```
Y_igs = β₇·(NE_s × Post_g × Female_i) + ... + ε_igs
```

**Purpose**: 
- Examine heterogeneous effects by gender
- β₇ = differential effect for girls in Northeast post-conflict

**Interpretation**:
- If β₇ < 0: Girls affected more than boys
- If β₇ > 0: Boys affected more than girls

---

## 4. Identification Assumptions

### A. Parallel Trends Assumption (CRITICAL)

**Statement**: 
In the absence of treatment, educational outcomes in the Northeast and other regions would have followed parallel trends.

**Formal**:
```
E[Y_Northeast,1 - Y_Northeast,0 | Northeast=1] = E[Y_Other,1 - Y_Other,0 | Other=1]
```

**Why It's Critical**:
- This is the KEY assumption for DiD
- If violated, DiD estimates are biased
- Cannot be directly tested (counterfactual is unobserved)

**Tests**:
1. **Visual Inspection**: Plot pre-treatment trends
2. **Event Study**: Test if pre-treatment coefficients = 0
3. **Placebo Test**: Run DiD on pre-treatment period only

**What Could Violate It?**
- Northeast already on different trajectory before conflict
- Other region-specific shocks happening simultaneously
- Differential impacts of national policies by region

**Evidence Supporting Parallel Trends**:
- Similar trends in 1990s and early 2000s
- Event study shows no pre-trends
- Robust to different control groups

---

### B. No Anticipation

**Statement**: 
Treatment effects don't begin before actual conflict exposure.

**Why It Matters**:
- If people migrate before conflict, treatment assignment is endogenous
- Pre-conflict changes could bias estimates

**Tests**:
- Check for effects in cohorts too old to be affected
- Examine migration patterns
- Event study: no effects before t=0

---

### C. Stable Unit Treatment Value Assumption (SUTVA)

**Statement**:
1. No spillovers between units
2. Treatment is well-defined and uniform

**Potential Violations**:
1. **Spillovers to control regions**:
   - IDPs moving to other regions
   - Economic ripple effects
   - Media coverage affecting all regions

2. **Treatment heterogeneity**:
   - Conflict intensity varies within Northeast
   - Different types of conflict (bombings vs. battles)

**How We Address It**:
- State fixed effects reduce spillover concerns
- Continuous treatment captures heterogeneity
- Sensitivity analysis: drop border states

---

### D. Exogeneity of Treatment Timing

**Statement**: 
Conflict onset (2009) not caused by education trends.

**Why It's Plausible**:
- Boko Haram driven by political/religious factors
- Not caused by education system changes
- Timing determined by external events

**Potential Concern**:
- Education quality already declining → frustration → conflict
- This would violate assumption

**Evidence**:
- Historical accounts point to political triggers
- Pre-trends test shows no divergence before 2009

---

## 5. Robustness Checks

### A. Alternative Outcome Measures

**Purpose**: Ensure results not driven by measurement of education

**Tests**:
1. **Primary completion** (binary)
2. **Secondary completion** (binary)
3. **Any education** (binary)
4. **Literacy** (if available)

**Expected Pattern**:
- All outcomes should show consistent direction
- Magnitude will differ (mechanical - different scales)

---

### B. Alternative Treatment Definitions

**Purpose**: Test if results robust to treatment definition

**Variations**:
1. **Geographic**: 
   - Core Northeast only (Borno, Yobe, Adamawa)
   - Extended Northeast (add Bauchi, Gombe)
   - Remove border states

2. **Temporal**:
   - Earlier cutoff (2008)
   - Later cutoff (2010)
   - Continuous age at exposure

3. **Intensity**:
   - Top quartile vs. bottom quartile
   - Continuous conflict measure
   - Boko Haram events only vs. all violence

**Interpretation**:
- Consistent results → robust
- Sensitive results → investigate why

---

### C. Alternative Control Groups

**Purpose**: Ensure results not driven by control group selection

**Tests**:
1. **Geographic**:
   - Northern states only (more similar)
   - All other states
   - Exclude Lagos/Abuja (outliers)

2. **Temporal**:
   - Older cohorts only (finished school by 2000)
   - Multiple pre-treatment cohorts

**Expectation**:
- Similar results → robust
- Varying results → selection concerns

---

### D. Placebo Tests

**Purpose**: Test for spurious correlations

**Test 1: Placebo Treatment Time**
```
Run DiD on pre-conflict cohorts only:
- "Treat": 1980-1985 cohorts
- "Control": 1970-1975 cohorts
- Should find no effect
```

**Test 2: Placebo Geography**
```
Run DiD with fake "Northeast":
- Randomly assign states to treatment
- Repeat 1000 times
- True effect should be in tail of distribution
```

**Test 3: Irrelevant Outcomes**
```
Run DiD on outcomes that shouldn't be affected:
- Height (predetermined)
- Sex ratio (predetermined)
- Should find no effect
```

---

### E. Sample Restrictions

**Purpose**: Test sensitivity to sample definition

**Tests**:
1. **Age restrictions**:
   - 25+ only (completed education)
   - 30+ only (definitely completed)
   - 20-40 (balanced sample)

2. **Urban/Rural**:
   - Urban only
   - Rural only
   - Should effects differ?

3. **Cohort balance**:
   - Equal-sized pre/post windows
   - Symmetric around 2009

---

### F. Inference and Standard Errors

**Purpose**: Ensure significance isn't spurious

**Variations**:
1. **Heteroskedasticity-robust** (baseline)
2. **Cluster by state** (if N_states > 20)
3. **Cluster by state-survey** 
4. **Bootstrap** (1000 replications)
5. **Randomization inference** (permutation test)

**Expectation**:
- True effects robust to SE specification
- P-values may change slightly

---

## 6. Potential Limitations

### A. Selection Bias

**Concern**: Migration in response to conflict

**Evidence**:
- ~2 million IDPs in Northeast
- Many moved to other regions

**Implications**:
- Treatment group: Loses higher-SES individuals (negative selection)
- Control group: Gains some conflict-exposed individuals (dilutes contrast)
- **Direction of bias**: Probably underestimates true effect

**Mitigation**:
- Focus on completed education (age 25+)
- State fixed effects capture some migration
- Note limitation in thesis

---

### B. Measurement Error

**Concerns**:
1. **Education**: Self-reported years may have error
   - Classical measurement error → attenuation bias
   
2. **Conflict exposure**: 
   - ACLED may miss some events
   - State-level measure misses within-state variation

**Implications**:
- Likely biases toward zero (underestimates effects)
- Measurement error in treatment less concerning with binary variable

---

### C. Unobserved Confounders

**What could bias estimates?**

1. **Contemporaneous shocks**:
   - Oil price changes affecting North differently
   - Federal education policy changes
   - Health shocks (e.g., epidemics)

2. **Spillover effects**:
   - Military spending diverted from social services
   - National economic impacts of conflict

**Mitigation**:
- State fixed effects control for state-specific shocks
- Survey year FE control for national time trends
- Discuss in limitations section

---

### D. Generalizability

**Questions**:
1. Do results apply to other conflicts?
2. Do results apply to men? (DHS samples women)
3. Do results apply to other education measures?

**Honest Answer**: 
- Results specific to Boko Haram context
- Education effects may differ from other conflicts
- Gender effects may differ
- These are useful, policy-relevant findings despite limited generalizability

---

## 7. Extensions and Future Work

### Potential Extensions for Undergraduate Thesis

1. **Mechanisms Analysis**:
   - Test specific channels (school closure, displacement, etc.)
   - Requires additional data on schools/displacement

2. **Long-run Effects**:
   - As more data becomes available, examine longer-term impacts
   - Compare cohorts 5, 10 years post-conflict

3. **Intergenerational Effects**:
   - Do affected individuals have fewer/less educated children?
   - Requires fertility data

4. **Economic Outcomes**:
   - Employment, wages, wealth
   - Link education effects to economic well-being

---

### Advanced Extensions (Graduate Work)

1. **Structural Model**:
   - Model household education investment decisions under conflict
   - Estimate deeper parameters

2. **Instrumental Variables**:
   - Distance to Boko Haram strongholds as IV
   - Requires exogeneity assumption

3. **Regression Discontinuity**:
   - If there's a sharp geographic boundary
   - Unlikely in this context

4. **Machine Learning**:
   - Predict which individuals most affected
   - Heterogeneous treatment effects (causal forests)

---

## Summary: What Makes This a Strong Senior Thesis?

✅ **Real data**: Uses actual policy-relevant data sources
✅ **Rigorous methods**: Implements standard econometric techniques correctly
✅ **Clear identification**: Well-defined treatment and control groups
✅ **Transparency**: Tests assumptions explicitly
✅ **Robustness**: Multiple specifications and sensitivity checks
✅ **Policy relevance**: Directly informs education and conflict policy
✅ **Appropriate scope**: Ambitious but feasible for undergraduate work

---

## Key Takeaways for Your Thesis

1. **Be Clear About Assumptions**: 
   - Don't hide behind jargon
   - State what you're assuming and why it's plausible

2. **Test Parallel Trends**:
   - This is the most important assumption
   - Event study is your best friend

3. **Show Robustness**:
   - One specification is never enough
   - Show your result holds up to reasonable alternatives

4. **Acknowledge Limitations**:
   - Every study has limitations
   - Being upfront about them shows maturity

5. **Tell a Story**:
   - Don't just report coefficients
   - Explain what they mean substantively

---

**Good luck! This is challenging but rewarding work.**
