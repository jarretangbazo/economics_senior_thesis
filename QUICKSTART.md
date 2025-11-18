# Quick Start Guide
## Nigeria Conflict-Education Analysis

**Created: November 2025**

---

## 🎯 What You Have

A complete, production-ready codebase for your undergraduate economics senior thesis analyzing how violent conflict affects educational attainment in Nigeria.

---

## 📦 Files Created

### Main Scripts (Run in Order)
1. **`00_run_all.py`** - Master script that runs everything
2. **`01_acled_download_clean.py`** - Downloads and cleans conflict data
3. **`02_dhs_process.py`** - Processes education survey data
4. **`03_merge_data.py`** - Merges conflict and education data
5. **`04_econometric_analysis.py`** - Runs all regressions and creates figures

### Documentation
- **`README.md`** - Comprehensive guide (16KB) - START HERE!
- **`METHODOLOGY.md`** - Detailed econometric methodology (17KB)
- **`requirements.txt`** - Python package dependencies

### Data Files (Already Created with Synthetic Data)
- `acled_lga_year.csv` - Conflict events by location and year (179KB)
- `dhs_education_clean.csv` - Individual education outcomes (1.7MB)
- `analysis_dataset.csv` - Merged analysis-ready data (2.8MB)
- `state_year_conflict.csv` - State-level conflict summary (5.5KB)

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Up API Credentials

**For ACLED Data** (Real Data):
1. Register at https://developer.acleddata.com/
2. Get your API key
3. Edit `01_acled_download_clean.py` lines 25-26:
```python
ACLED_EMAIL = "your_email@example.com"
ACLED_KEY = "your_api_key_here"
```

**For DHS Data** (Real Data):
1. Register at https://dhsprogram.com/
2. Request Nigeria surveys (2003, 2008, 2013, 2018)
3. Download and place .DTA files in `/home/claude/dhs_data/`

**OR Use Synthetic Data** (For Learning/Testing):
- Skip the above steps
- Code automatically generates realistic synthetic data

### Step 3: Run the Analysis
```bash
# Option A: Run everything at once
python 00_run_all.py

# Option B: Run step by step
python 01_acled_download_clean.py
python 02_dhs_process.py
python 03_merge_data.py
python 04_econometric_analysis.py
```

---

## 📊 What You'll Get

### Console Output
- Detailed regression results with coefficients, standard errors, p-values
- Summary statistics by region and cohort
- Diagnostic tests (parallel trends, robustness checks)

### Figures (in `/home/claude/results/figures/`)
1. **trends_by_cohort.png** - Education trends over time by region
2. **education_distribution.png** - Distribution of education outcomes
3. **did_visual.png** - Classic difference-in-differences visualization

### Analysis Dataset
Ready-to-use CSV with:
- 20,000 individuals (with synthetic data)
- 48 variables including:
  - Education outcomes
  - Conflict exposure measures
  - Control variables
  - Treatment indicators

---

## 🎓 Understanding the Results

### Main Result: The DiD Coefficient

Look for this in the output:
```
northeast_x_post2009: -1.234
Standard Error: 0.456
P-value: 0.007
```

**Interpretation**: 
"Being in the Northeast region AND being school-age during the Boko Haram conflict reduced educational attainment by 1.23 years compared to other regions (p < 0.01)."

### Key Statistics to Report

From Specification 1 (Basic DiD):
- β₃ coefficient (the DiD estimate)
- Standard error
- P-value
- Sample size

From Specification 5 (Event Study):
- Pre-treatment coefficients (should be ≈ 0)
- Post-treatment coefficients (effects over time)

---

## 🔍 Next Steps for Your Thesis

### 1. Run the Code
- Start with synthetic data to understand workflow
- Then get real data for actual thesis

### 2. Understand the Methods
- Read `METHODOLOGY.md` carefully
- Understand each econometric specification
- Know your identification assumptions

### 3. Interpret Results
- What is the magnitude of the effect?
- Is it statistically significant?
- Is it robust across specifications?
- What are the mechanisms?

### 4. Write Your Thesis
Suggested structure (40-50 pages):
1. Introduction (5-7 pages)
2. Background & Context (5-7 pages)
3. Literature Review (8-10 pages)
4. Data & Descriptive Statistics (8-10 pages)
5. Empirical Strategy (8-10 pages)
6. Results (10-12 pages)
7. Discussion & Conclusion (5-7 pages)

### 5. Create Tables and Figures
- Use output from scripts
- Create professional-looking tables
- Include all three figures from analysis
- Add a map of Nigeria showing conflict zones

---

## 💡 Tips for Success

### Do's ✅
- Run code multiple times to understand it
- Read every comment in the scripts
- Check your data at each stage
- Test parallel trends assumption carefully
- Be honest about limitations
- Show your work to your advisor early

### Don'ts ❌
- Don't just copy-paste results without understanding
- Don't ignore failed robustness checks
- Don't claim causation without careful identification
- Don't overinterpret marginally significant results
- Don't hide negative findings

---

## 📚 Key Concepts to Master

1. **Difference-in-Differences**
   - What it is: Comparing changes over time between groups
   - Why it works: Differences out confounders
   - Main assumption: Parallel trends

2. **Parallel Trends**
   - What it is: Treatment and control would have same trends absent treatment
   - How to test: Event study, pre-trend analysis
   - What violates it: Differential pre-existing trends

3. **Standard Errors**
   - Why they matter: Determine statistical significance
   - Types: Robust, clustered, bootstrapped
   - When to cluster: Multiple observations per cluster

4. **Fixed Effects**
   - State FE: Controls for time-invariant state characteristics
   - Year FE: Controls for common time trends
   - Two-way FE: Both simultaneously

---

## 🆘 Common Issues and Solutions

### "ACLED API not working"
→ Check your credentials, or use synthetic data

### "DHS files not found"
→ Check file paths, or use synthetic data

### "statsmodels not installed"
→ Run: `pip install statsmodels`

### "Results look weird"
→ Check sample sizes, check for data errors, verify merge

### "I don't understand the coefficient"
→ Read METHODOLOGY.md section on interpretation

---

## 📖 Essential Reading

### Before You Start
1. README.md (this explains everything)
2. METHODOLOGY.md (this explains the econometrics)

### While Writing
1. Angrist & Pischke (2009) - *Mostly Harmless Econometrics*, Chapter 5
2. Cunningham (2021) - *Causal Inference: The Mixtape*, DiD chapter
3. Papers cited in code comments

---

## 🎯 Success Metrics

You know you're on track when:
- [ ] Code runs without errors
- [ ] You understand what each script does
- [ ] You can explain the DiD coefficient
- [ ] You can interpret the event study
- [ ] You understand parallel trends
- [ ] You can discuss limitations
- [ ] Your advisor is impressed!

---

## 📧 Support

### For Technical Issues
1. Check error messages
2. Review troubleshooting section in README
3. Re-read relevant code comments
4. Consult Python/statsmodels documentation

### For Methodological Questions
1. Read METHODOLOGY.md
2. Consult econometrics textbooks
3. Talk to your thesis advisor
4. Post on Cross Validated (stats.stackexchange.com)

---

## 🏆 You're Ready!

You now have everything you need for an excellent senior thesis:
- ✅ Real, policy-relevant research question
- ✅ Rigorous econometric methods
- ✅ Working code with documentation
- ✅ Synthetic data to practice
- ✅ Path to real data
- ✅ Comprehensive methodology guide

**Most Important**: Take your time, understand each step, and be proud of your work. This is challenging research, and you're doing something that matters!

---

**Good luck with your thesis! 🎓📊**

*Remember: A good thesis isn't about perfection—it's about asking an important question, using appropriate methods, being transparent about limitations, and contributing to knowledge.*
