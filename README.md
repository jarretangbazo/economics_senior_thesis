# Impact of Violent Conflict on Educational Attainment in Nigeria

## Undergraduate Economics Senior Thesis Project

This repository contains all the code and documentation needed to conduct a rigorous econometric analysis of how violent conflict (particularly the Boko Haram insurgency) has affected educational outcomes in Nigeria.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Research Question](#research-question)
3. [Data Sources](#data-sources)
4. [Methodology](#methodology)
5. [Setup Instructions](#setup-instructions)
6. [Running the Analysis](#running-the-analysis)
7. [File Structure](#file-structure)
8. [Output Interpretation](#output-interpretation)
9. [Troubleshooting](#troubleshooting)

---

## Project Overview

This project examines how exposure to violent conflict during school-age years affects educational attainment in Nigeria. Using a difference-in-differences (DiD) approach, we compare educational outcomes between:

- **Treatment group**: Individuals in conflict-affected areas (primarily Northeastern Nigeria)
- **Control group**: Individuals in less-affected regions
- **Time dimension**: Cohorts who were school-age before vs. during the Boko Haram insurgency (2009-present)

### Key Features

- Uses publicly available data (ACLED + DHS)
- Implements rigorous econometric methods (DiD, event studies, robustness checks)
- Includes detailed code documentation and comments
- Produces publication-quality figures

---

## Research Question

**Main Question**: How has violent conflict in Nigeria affected educational attainment?

**Specific Hypotheses**:
1. Individuals exposed to conflict during school-age years (6-18) complete fewer years of schooling
2. Effects are larger in the Northeast (epicenter of Boko Haram insurgency)
3. Effects vary by gender, urban/rural location, and household wealth

---

## Data Sources

### 1. ACLED (Armed Conflict Location & Event Data)

- **What**: Geocoded conflict events with dates, locations, and fatalities
- **Coverage**: Nigeria, 2000-present
- **URL**: https://developer.acleddata.com/
- **What you need**: Email and API key

### 2. DHS (Demographic and Health Surveys)

- **What**: Individual-level household survey data with education outcomes
- **Surveys Used**: Nigeria 2003, 2008, 2013, 2018
- **URL**: https://dhsprogram.com/data/
- **What you need**: Research project description and intended use

**Files to Download**:
- Individual Recode (IR) files: `NGIR*.DTA`
- Household Recode (HR) files: `NGHR*.DTA`
- Format: Stata (.DTA) files

---

## Methodology

### Identification Strategy: Difference-in-Differences

**The Model**:

```
Education_i = β₀ + β₁(Northeast_i) + β₂(Post2009_i) + β₃(Northeast × Post2009) + X_i + ε_i
```

Where:
- `Education_i`: Years of schooling for individual i
- `Northeast_i`: Indicator for living in Northeast region
- `Post2009_i`: Indicator for being school-age during Boko Haram era
- `β₃`: The difference-in-differences estimate (our main coefficient of interest)
- `X_i`: Control variables (age, wealth, urban/rural, state fixed effects)

### Key Assumptions

1. **Parallel Trends**: Education trends in Northeast and other regions would have been parallel absent the conflict
   - Tested using: Event study specification (pre-trends analysis)
   
2. **No Spillovers**: Conflict doesn't systematically affect control regions
   - Addressed by: State fixed effects, sensitivity analysis

3. **No Compositional Changes**: Selection into treatment not driven by education
   - Mitigated by: Using birth cohorts (predetermined treatment)

### Alternative Specifications

We implement multiple specifications for robustness:

1. **Basic DiD**: Simple 2x2 comparison
2. **DiD with Controls**: Add individual and household characteristics
3. **DiD with State FE**: Absorb all time-invariant state characteristics
4. **Continuous Treatment**: Use conflict intensity instead of binary treatment
5. **Event Study**: Test parallel trends and examine dynamic effects
6. **Heterogeneity Analysis**: Examine effects by subgroups

---

## Setup Instructions

### 1. System Requirements

- **Python**: 3.7 or higher
- **Storage**: 2GB for data files

### 2. Install Required Packages

```bash
# Required packages
pip install pandas numpy scipy matplotlib seaborn

# For econometric analysis
pip install statsmodels

# Optional but recommended
pip install linearmodels  # For panel data models
pip install jupyter       # For interactive exploration
```

### 3. Register for Data Access

#### ACLED Registration

1. Go to https://developer.acleddata.com/
2. Create account (instant)
3. Navigate to "My API Keys"
4. Copy your email and API key
5. Update in `01_acled_download_clean.py`:

```python
ACLED_EMAIL = "your_email@example.com"
ACLED_KEY = "your_api_key_here"
```

#### DHS Registration

1. Go to https://dhsprogram.com/data/new-user-registration.cfm
2. Create account
3. Submit data request for Nigeria surveys
4. Download approval typically within 24 hours
5. Download the following files:
   - NGIR4BFL.DTA (2003 Individual Recode)
   - NGIR5AFL.DTA (2008 Individual Recode)
   - NGIR6AFL.DTA (2013 Individual Recode)
   - NGIR7BFL.DTA (2018 Individual Recode)
6. Place files in: `/home/claude/dhs_data/`

**Note**: If you can't access DHS data, the code will automatically generate synthetic data for demonstration purposes.

### 4. Directory Structure

The code will create this structure automatically:

```
/home/claude/
├── 00_run_all.py                    # Master script
├── 01_acled_download_clean.py       # ACLED data processing
├── 02_dhs_process.py                # DHS data processing
├── 03_merge_data.py                 # Merge datasets
├── 04_econometric_analysis.py       # Run analysis
├── data/                            # Data files (created)
│   ├── acled_nigeria_raw.csv
│   ├── acled_nigeria_clean.csv
│   ├── acled_lga_year.csv
│   ├── dhs_education_clean.csv
│   └── analysis_dataset.csv
├── dhs_data/                        # DHS raw files (you create)
│   ├── NGIR4BFL.DTA
│   ├── NGIR5AFL.DTA
│   ├── NGIR6AFL.DTA
│   └── NGIR7BFL.DTA
└── results/                         # Results (created)
    └── figures/
        ├── trends_by_cohort.png
        ├── education_distribution.png
        └── did_visual.png
```

---

## ▶️ Running the Analysis

### Option 1: Run Complete Pipeline (Recommended)

```bash
python 00_run_all.py
```

This runs all steps in sequence:
1. Downloads and cleans ACLED data
2. Processes DHS data
3. Merges datasets
4. Runs econometric analysis
5. Creates figures

**Time**: 10-30 minutes depending on data size

### Option 2: Run Individual Scripts

Run each script in order:

```bash
# Step 1: Download ACLED data
python 01_acled_download_clean.py

# Step 2: Process DHS data
python 02_dhs_process.py

# Step 3: Merge datasets
python 03_merge_data.py

# Step 4: Run analysis
python 04_econometric_analysis.py
```

### Option 3: Interactive Analysis (Advanced)

```bash
jupyter notebook
# Open and run each script in Jupyter for interactive exploration
```

---

## 📁 File Structure

### Scripts

| File | Purpose | Input | Output |
|------|---------|-------|--------|
| `00_run_all.py` | Master script, runs everything | None | All outputs |
| `01_acled_download_clean.py` | Download & clean conflict data | ACLED API | `acled_lga_year.csv` |
| `02_dhs_process.py` | Process education data | DHS .DTA files | `dhs_education_clean.csv` |
| `03_merge_data.py` | Merge conflict & education | Both datasets | `analysis_dataset.csv` |
| `04_econometric_analysis.py` | Run regressions | Analysis dataset | Regression results & figures |

### Key Variables in Final Dataset

**Outcome Variables**:
- `years_schooling`: Years of completed schooling (0-20)
- `no_education`: Binary indicator for zero education
- `primary_complete`: Binary indicator for completing primary (6+ years)
- `secondary_complete`: Binary indicator for completing secondary (12+ years)

**Treatment Variables**:
- `northeast`: Binary indicator for Northeast region
- `post_boko_haram`: Binary indicator for post-2009 birth cohorts
- `northeast_x_post2009`: Interaction term (DiD estimator)
- `conflict_exposure_school_age`: Continuous measure of conflict intensity
- `violent_events_school_age`: Count of violent events during school age
- `years_exposed_school_age`: Number of years exposed to conflict

**Control Variables**:
- `age`: Current age (15-49)
- `birth_year`: Year of birth
- `urban`: Binary indicator for urban residence
- `wealth_quintile`: Household wealth quintile (1-5)
- `state`: State of residence
- `survey_year`: DHS survey year

---

## 📈 Output Interpretation

### Regression Results

The main coefficient of interest is **β₃** (the DiD estimate) from this model:

```
Years_Schooling = β₀ + β₁(Northeast) + β₂(Post2009) + β₃(Northeast × Post2009) + Controls
```

**Interpretation**:
- β₃ = -1.5 means: Being in the Northeast and school-age during Boko Haram is associated with 1.5 fewer years of schooling
- If p < 0.05: Result is statistically significant at 5% level
- 95% CI: Range of plausible effect sizes

### Figures

1. **trends_by_cohort.png**: 
   - Shows education levels over time by region
   - Visual test of parallel trends assumption
   - Look for divergence after 2009

2. **education_distribution.png**:
   - Histograms of education by treatment status
   - Shows full distribution, not just means

3. **did_visual.png**:
   - Classic 2x2 DiD visualization
   - Clearly shows the treatment effect

### Example Results Interpretation

```
Coefficient on Northeast × Post2009: -1.234
Standard Error: 0.456
P-value: 0.007
95% CI: [-2.128, -0.340]
```

**Write-up**:
"Using a difference-in-differences approach, I find that exposure to the Boko Haram insurgency during school-age years reduced educational attainment by 1.23 years (SE: 0.46, p = 0.007). This effect is statistically significant at the 1% level and robust to the inclusion of state fixed effects and individual controls."

---

## 🔧 Troubleshooting

### Common Issues

#### 1. ACLED API not working

**Error**: `"API request failed: 401"`

**Solution**:
- Verify your email and API key are correct
- Check you've registered at https://developer.acleddata.com/
- Make sure you've updated the credentials in the script

**Workaround**: The script automatically creates synthetic data if API fails

---

#### 2. DHS files not found

**Error**: `"File not found: NGIR*.DTA"`

**Solution**:
- Verify files are in `/home/claude/dhs_data/`
- Check file names exactly match (case-sensitive)
- Ensure files are unzipped

**Workaround**: Script automatically creates synthetic DHS data for demonstration

---

#### 3. Statsmodels not installed

**Error**: `"No module named 'statsmodels'"`

**Solution**:
```bash
pip install statsmodels
```

---

#### 4. Memory error

**Error**: `"MemoryError"`

**Solution**:
- Reduce sample size in merge script
- Use smaller birth cohort range
- Close other applications

---

#### 5. Results don't match expectations

**Check**:
1. Are you using real or synthetic data?
2. Did all scripts run successfully?
3. Check sample sizes in output
4. Verify merge was successful

---

## 📚 Additional Resources

### Recommended Reading

**Difference-in-Differences**:
- Angrist & Pischke (2009). *Mostly Harmless Econometrics*. Chapter 5.
- Cunningham (2021). *Causal Inference: The Mixtape*. Chapter on DiD.

**Conflict and Education Literature**:
- Akresh & de Walque (2011). "Armed Conflict and Schooling" (*World Bank Economic Review*)
- Chamarbagwala & Morán (2011). "The human capital consequences of civil war" (*JDE*)
- Dabalen & Paul (2014). "Estimating the Effects of Conflict on Education in Côte d'Ivoire" (*JDE*)

**Nigeria-Specific**:
- Adetula et al. (2016). "Boko Haram Insurgency and the Counter-Terrorism Policy"
- Chiluwa & Chiluwa (2020). "Education in the Time of Boko Haram"

### Online Resources

- **ACLED Methodology**: https://acleddata.com/resources/methodology/
- **DHS Methodology**: https://dhsprogram.com/methodology/
- **Statsmodels Docs**: https://www.statsmodels.org/
- **Python for Economists**: https://python.quantecon.org/

---

## ✍️ Using These Results in Your Thesis

### Thesis Structure Recommendation

1. **Introduction** (5-7 pages)
   - Motivation: Why this matters
   - Research question
   - Preview of findings
   - Contribution to literature

2. **Background** (5-7 pages)
   - Nigeria context
   - Boko Haram insurgency timeline
   - Education system structure
   - Regional variation

3. **Literature Review** (8-10 pages)
   - Conflict and education globally
   - Mechanisms: displacement, school destruction, teacher flight, household shocks
   - Nigeria-specific studies

4. **Data** (8-10 pages)
   - ACLED: conflict data description
   - DHS: education data description
   - Sample construction
   - Descriptive statistics (use figures from analysis)
   - Discuss limitations

5. **Empirical Strategy** (8-10 pages)
   - Difference-in-differences framework
   - Identification assumptions
   - Parallel trends discussion (use event study results)
   - Potential threats to validity

6. **Results** (10-12 pages)
   - Main DiD estimates
   - Robustness checks
   - Heterogeneity analysis
   - Magnitude interpretation

7. **Discussion & Conclusion** (5-7 pages)
   - Summary of findings
   - Policy implications
   - Limitations
   - Future research directions

### Tables to Include

1. **Table 1**: Summary statistics by region and cohort
2. **Table 2**: Main DiD results (basic + controls + FE)
3. **Table 3**: Alternative outcomes (primary completion, secondary completion)
4. **Table 4**: Heterogeneity results (by gender, urban/rural, wealth)
5. **Table 5**: Robustness checks (placebo tests, alternative treatments)

### Figures to Include

1. **Figure 1**: Map of conflict intensity by region
2. **Figure 2**: Education trends over time (from code)
3. **Figure 3**: Event study graph (parallel trends test)
4. **Figure 4**: DiD visual (from code)

---

## 🤝 Citation

If you use this code, please cite:

```
[Your Name] (2025). "Impact of Violent Conflict on Educational Attainment in Nigeria."
Undergraduate Senior Thesis, [Your University], Economics Department.
```

**Data Sources**:
```
ACLED (2025). Armed Conflict Location & Event Data Project. 
www.acleddata.com

ICF (2018). Demographic and Health Surveys (Various) [Datasets]. 
Funded by USAID. Rockville, Maryland: ICF [Distributor].
```

---

## 📝 License

This code is provided for educational purposes. Feel free to modify and adapt for your own research.

---

## 💡 Tips for Success

1. **Start Early**: Data download and approval can take time
2. **Keep Notes**: Document any data cleaning decisions you make
3. **Replicate First**: Run all code as-is before making changes
4. **Understand Each Step**: Don't just run code - understand what it does
5. **Talk to Your Advisor**: Share preliminary results early and often
6. **Check Assumptions**: Really think through whether DiD assumptions hold
7. **Be Honest**: Acknowledge limitations in your thesis
8. **Think Causally**: Always ask "what else could explain this pattern?"

---

## 🆘 Getting Help

If you run into issues:

1. Check error messages carefully
2. Review the troubleshooting section above
3. Read code comments for clarification
4. Consult your thesis advisor
5. Post on econometrics forums (Cross Validated, Economics Stack Exchange)

---

## 📧 Contact

For questions about this code:
- Review the documentation above
- Check code comments
- Consult with your thesis advisor
- Refer to methodology papers cited above

---

**Good luck with your thesis! 🎓**

Remember: This is rigorous, impactful research on an important policy question. Take your time, be thorough, and be proud of your work.
