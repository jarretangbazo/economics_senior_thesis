"""
Econometric Analysis: Impact of Violent Conflict on Educational Attainment
===========================================================================
This script implements difference-in-differences and other causal inference
approaches to estimate the impact of violent conflict in Nigeria on education.

Author: Jarret Angbazo
Date: November 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Statistical packages
try:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from statsmodels.iolib.summary2 import summary_col
    HAS_STATSMODELS = True
except ImportError:
    print("Warning: statsmodels not installed. Install with: pip install statsmodels")
    HAS_STATSMODELS = False

try:
    from linearmodels.panel import PanelOLS
    from linearmodels import IV2SLS
    HAS_LINEARMODELS = True
except ImportError:
    print("Warning: linearmodels not installed. Install with: pip install linearmodels")
    HAS_LINEARMODELS = False

# ============================================================================
# CONFIGURATION
# ============================================================================

DATA_DIR = "/users/jarretangbazo/economics_senior_thesis/data/"
OUTPUT_DIR = "/users/jarretangbazo/economics_senior_thesis/results/"
FIGURES_DIR = OUTPUT_DIR + "figures/"

INPUT_FILE = DATA_DIR + "analysis_dataset.csv"

# ============================================================================
# STEP 1: LOAD DATA AND PREPARE FOR ANALYSIS
# ============================================================================

def load_analysis_data():
    """
    Load and prepare analysis dataset
    """
    
    print("="*70)
    print("LOADING ANALYSIS DATA")
    print("="*70)
    
    df = pd.read_csv(INPUT_FILE)
    print(f"\nLoaded {len(df)} observations")
    print(f"Variables: {len(df.columns)}")
    
    # Keep only observations with complete data for main analysis
    analysis_vars = ['years_schooling', 'age', 'state', 'birth_year', 
                     'northeast', 'post_boko_haram', 'weight']
    
    df_complete = df.dropna(subset=analysis_vars)
    print(f"Complete cases for main analysis: {len(df_complete)}")
    
    return df_complete

# ============================================================================
# SPECIFICATION 1: BASIC DIFFERENCE-IN-DIFFERENCES
# ============================================================================

def run_basic_did(df):
    """
    Basic Difference-in-Differences specification
    
    Model: 
    Education_i = β0 + β1*Northeast + β2*Post2009 + β3*(Northeast × Post2009) + ε
    
    β3 is the DiD estimate
    """
    
    print("\n" + "="*70)
    print("SPECIFICATION 1: BASIC DIFFERENCE-IN-DIFFERENCES")
    print("="*70)
    
    # Create the dataset for this specification
    df_did = df.copy()
    
    # Outcome: years of schooling
    y = df_did['years_schooling']
    
    # Treatment: Northeast region
    # Time: Post-2009 cohort (school age during Boko Haram)
    X = df_did[['northeast', 'post_boko_haram']]
    X['northeast_x_post'] = df_did['northeast'] * df_did['post_boko_haram']
    X['const'] = 1
    
    # Weights
    weights = df_did['weight']
    
    if HAS_STATSMODELS:
        # Run weighted OLS
        model = sm.WLS(y, X[['const', 'northeast', 'post_boko_haram', 'northeast_x_post']], 
                       weights=weights)
        results = model.fit(cov_type='HC1')  # Heteroskedasticity-robust SE
        
        print("\nBasic DiD Results:")
        print(results.summary())
        
        # Interpret the coefficient
        did_coef = results.params['northeast_x_post']
        did_se = results.bse['northeast_x_post']
        did_pval = results.pvalues['northeast_x_post']
        
        print("\n" + "-"*70)
        print("INTERPRETATION:")
        print(f"DiD Estimate: {did_coef:.3f} years")
        print(f"Standard Error: {did_se:.3f}")
        print(f"P-value: {did_pval:.3f}")
        print(f"95% CI: [{did_coef - 1.96*did_se:.3f}, {did_coef + 1.96*did_se:.3f}]")
        
        if did_pval < 0.05:
            print(f"\nThe Boko Haram conflict reduced educational attainment")
            print(f"in the Northeast by {abs(did_coef):.2f} years (p < 0.05)")
        else:
            print(f"\nNo statistically significant effect detected (p = {did_pval:.3f})")
        print("-"*70)
        
        return results
    else:
        print("Statsmodels not available. Showing manual calculation:")
        
        # Manual DiD calculation
        ne_post = df_did[(df_did['northeast']==1) & (df_did['post_boko_haram']==1)]['years_schooling'].mean()
        ne_pre = df_did[(df_did['northeast']==1) & (df_did['post_boko_haram']==0)]['years_schooling'].mean()
        other_post = df_did[(df_did['northeast']==0) & (df_did['post_boko_haram']==1)]['years_schooling'].mean()
        other_pre = df_did[(df_did['northeast']==0) & (df_did['post_boko_haram']==0)]['years_schooling'].mean()
        
        did = (ne_post - ne_pre) - (other_post - other_pre)
        
        print(f"\nManual DiD calculation:")
        print(f"Northeast, Post: {ne_post:.2f}")
        print(f"Northeast, Pre: {ne_pre:.2f}")
        print(f"Other regions, Post: {other_post:.2f}")
        print(f"Other regions, Pre: {other_pre:.2f}")
        print(f"\nDiD Estimate: {did:.3f} years")
        
        return None

# ============================================================================
# SPECIFICATION 2: DiD WITH CONTROLS
# ============================================================================

def run_did_with_controls(df):
    """
    Difference-in-Differences with control variables
    
    Model:
    Education_i = β0 + β1*Northeast + β2*Post2009 + β3*(NE × Post) 
                + β4*Age + β5*Urban + β6*Wealth + State FE + ε
    """
    
    print("\n" + "="*70)
    print("SPECIFICATION 2: DiD WITH CONTROL VARIABLES")
    print("="*70)
    
    if not HAS_STATSMODELS:
        print("Statsmodels required for this specification")
        return None
    
    # Prepare formula
    formula = '''years_schooling ~ northeast + post_boko_haram + northeast_x_post2009 + 
                 age + C(wealth_quintile) + urban + C(survey_year)'''
    
    # Run regression
    try:
        model = smf.wls(formula, data=df, weights=df['weight'])
        results = model.fit(cov_type='HC1')
        
        print("\nDiD with Controls Results:")
        print(results.summary())
        
        return results
    except Exception as e:
        print(f"Error running regression: {str(e)}")
        print("Running simplified version...")
        
        # Simplified version without categorical variables
        df['northeast_x_post'] = df['northeast'] * df['post_boko_haram']
        formula_simple = 'years_schooling ~ northeast + post_boko_haram + northeast_x_post + age'
        
        model = smf.wls(formula_simple, data=df, weights=df['weight'])
        results = model.fit(cov_type='HC1')
        
        print(results.summary())
        return results

# ============================================================================
# SPECIFICATION 3: DiD WITH STATE FIXED EFFECTS
# ============================================================================

def run_did_with_state_fe(df):
    """
    Difference-in-Differences with state fixed effects
    
    This absorbs all time-invariant state characteristics
    """
    
    print("\n" + "="*70)
    print("SPECIFICATION 3: DiD WITH STATE FIXED EFFECTS")
    print("="*70)
    
    if not HAS_STATSMODELS:
        print("Statsmodels required for this specification")
        return None
    
    # Create interaction term
    df = df.copy()
    df['northeast_x_post'] = df['northeast'] * df['post_boko_haram']
    
    # Formula with state fixed effects
    formula = '''years_schooling ~ northeast_x_post + post_boko_haram + 
                 age + urban + C(state)'''
    
    try:
        model = smf.wls(formula, data=df, weights=df['weight'])
        results = model.fit(cov_type='cluster', cov_kwds={'groups': df['state']})
        
        print("\nDiD with State FE (clustered SE by state):")
        print(results.summary())
        
        return results
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# ============================================================================
# SPECIFICATION 4: CONTINUOUS TREATMENT (CONFLICT INTENSITY)
# ============================================================================

def run_continuous_treatment(df):
    """
    Use continuous measure of conflict intensity instead of binary treatment
    
    Model:
    Education_i = β0 + β1*ConflictIntensity + Controls + State FE + ε
    """
    
    print("\n" + "="*70)
    print("SPECIFICATION 4: CONTINUOUS CONFLICT INTENSITY")
    print("="*70)
    
    if not HAS_STATSMODELS:
        print("Statsmodels required for this specification")
        return None
    
    # Focus on cohorts that were school-age during data period
    df_analysis = df[df['birth_year'] >= 1985].copy()
    
    print(f"\nAnalysis sample: {len(df_analysis)} observations")
    print(f"Mean conflict exposure: {df_analysis['conflict_exposure_school_age'].mean():.2f}")
    
    # Formula
    formula = '''years_schooling ~ conflict_exposure_school_age + 
                 age + urban + C(state) + C(survey_year)'''
    
    try:
        model = smf.wls(formula, data=df_analysis, weights=df_analysis['weight'])
        results = model.fit(cov_type='cluster', cov_kwds={'groups': df_analysis['state']})
        
        print("\nContinuous Treatment Results:")
        print(results.summary())
        
        # Interpret coefficient
        coef = results.params['conflict_exposure_school_age']
        se = results.bse['conflict_exposure_school_age']
        
        print("\n" + "-"*70)
        print("INTERPRETATION:")
        print(f"A one-unit increase in conflict intensity during school age")
        print(f"is associated with {coef:.3f} years change in education (SE: {se:.3f})")
        print("-"*70)
        
        return results
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# ============================================================================
# SPECIFICATION 5: EVENT STUDY (DYNAMIC EFFECTS)
# ============================================================================

def run_event_study(df):
    """
    Event study specification to test parallel trends assumption
    
    Estimates effects for each birth cohort relative to reference cohort
    """
    
    print("\n" + "="*70)
    print("SPECIFICATION 5: EVENT STUDY (PARALLEL TRENDS TEST)")
    print("="*70)
    
    if not HAS_STATSMODELS:
        print("Statsmodels required for this specification")
        return None
    
    # Create cohort indicators relative to 1990 (just before Boko Haram)
    df = df.copy()
    df['cohort_relative'] = df['birth_year'] - 1990
    
    # Create interaction terms for each cohort (exclude reference year)
    cohort_years = sorted(df['cohort_relative'].unique())
    
    # Remove reference cohort (1990 = 0)
    reference_cohort = 0
    cohort_years = [c for c in cohort_years if c != reference_cohort]
    
    # Create interactions
    for cohort in cohort_years:
        df[f'northeast_x_cohort_{cohort}'] = df['northeast'] * (df['cohort_relative'] == cohort)
    
    # Build formula
    interaction_terms = ' + '.join([f'northeast_x_cohort_{c}' for c in cohort_years])
    formula = f'years_schooling ~ {interaction_terms} + age + urban + C(birth_year) + C(state)'
    
    print(f"\nEstimating event study with {len(cohort_years)} cohort interactions...")
    
    try:
        model = smf.wls(formula, data=df, weights=df['weight'])
        results = model.fit(cov_type='cluster', cov_kwds={'groups': df['state']})
        
        print("\nEvent Study Results (selected coefficients):")
        
        # Extract and display interaction coefficients
        event_study_coefs = {}
        for cohort in cohort_years:
            param_name = f'northeast_x_cohort_{cohort}'
            if param_name in results.params:
                event_study_coefs[cohort] = {
                    'coef': results.params[param_name],
                    'se': results.bse[param_name],
                    'pval': results.pvalues[param_name]
                }
        
        # Display in table format
        print("\nCohort | Coefficient | Std Error | P-value")
        print("-" * 50)
        for cohort in sorted(event_study_coefs.keys()):
            coef = event_study_coefs[cohort]['coef']
            se = event_study_coefs[cohort]['se']
            pval = event_study_coefs[cohort]['pval']
            sig = '***' if pval < 0.01 else '**' if pval < 0.05 else '*' if pval < 0.10 else ''
            print(f"{1990+cohort:4d}   | {coef:10.3f}  | {se:8.3f}  | {pval:6.3f} {sig}")
        
        print("\n" + "-"*70)
        print("PARALLEL TRENDS TEST:")
        print("Pre-treatment coefficients (birth cohorts before 1991) should be")
        print("statistically indistinguishable from zero if parallel trends holds.")
        print("-"*70)
        
        return results, event_study_coefs
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None

# ============================================================================
# SPECIFICATION 6: HETEROGENEITY ANALYSIS
# ============================================================================

def run_heterogeneity_analysis(df):
    """
    Examine heterogeneous effects by:
    - Urban vs Rural
    - Wealth quintile
    - Age cohorts
    """
    
    print("\n" + "="*70)
    print("SPECIFICATION 6: HETEROGENEITY ANALYSIS")
    print("="*70)
    
    if not HAS_STATSMODELS:
        print("Statsmodels required for this specification")
        return None
    
    results_dict = {}
    
    # 1. Urban vs Rural
    print("\n1. URBAN VS RURAL:")
    print("-" * 40)
    
    for urban_status in [0, 1]:
        label = "Urban" if urban_status == 1 else "Rural"
        df_subset = df[df['urban'] == urban_status].copy()
        df_subset['northeast_x_post'] = df_subset['northeast'] * df_subset['post_boko_haram']
        
        formula = 'years_schooling ~ northeast + post_boko_haram + northeast_x_post + age'
        
        try:
            model = smf.wls(formula, data=df_subset, weights=df_subset['weight'])
            results = model.fit(cov_type='HC1')
            
            did_coef = results.params['northeast_x_post']
            did_se = results.bse['northeast_x_post']
            did_pval = results.pvalues['northeast_x_post']
            
            print(f"\n{label}:")
            print(f"  N = {len(df_subset)}")
            print(f"  DiD Coefficient: {did_coef:.3f} ({did_se:.3f})")
            print(f"  P-value: {did_pval:.3f}")
            
            results_dict[f'urban_{urban_status}'] = results
        except:
            print(f"  Error running {label} regression")
    
    # 2. By Wealth Quintile
    print("\n\n2. BY WEALTH QUINTILE:")
    print("-" * 40)
    
    for quintile in [1, 2, 3, 4, 5]:
        df_subset = df[df['wealth_quintile'] == quintile].copy()
        df_subset['northeast_x_post'] = df_subset['northeast'] * df_subset['post_boko_haram']
        
        formula = 'years_schooling ~ northeast + post_boko_haram + northeast_x_post + age'
        
        try:
            model = smf.wls(formula, data=df_subset, weights=df_subset['weight'])
            results = model.fit(cov_type='HC1')
            
            did_coef = results.params['northeast_x_post']
            did_se = results.bse['northeast_x_post']
            
            print(f"\nQuintile {quintile}:")
            print(f"  N = {len(df_subset)}")
            print(f"  DiD Coefficient: {did_coef:.3f} ({did_se:.3f})")
            
            results_dict[f'wealth_q{quintile}'] = results
        except:
            print(f"  Error running Quintile {quintile} regression")
    
    return results_dict

# ============================================================================
# ROBUSTNESS CHECKS
# ============================================================================

def run_robustness_checks(df):
    """
    Various robustness checks:
    1. Alternative outcomes (primary completion, secondary completion)
    2. Alternative treatment definitions
    3. Alternative control groups
    4. Placebo tests
    """
    
    print("\n" + "="*70)
    print("ROBUSTNESS CHECKS")
    print("="*70)
    
    if not HAS_STATSMODELS:
        print("Statsmodels required")
        return None
    
    df = df.copy()
    df['northeast_x_post'] = df['northeast'] * df['post_boko_haram']
    
    robustness_results = {}
    
    # 1. Alternative Outcomes
    print("\n1. ALTERNATIVE OUTCOMES:")
    print("-" * 40)
    
    outcomes = {
        'years_schooling': 'Years of Schooling',
        'primary_complete': 'Primary Completion',
        'secondary_complete': 'Secondary Completion',
        'no_education': 'No Education'
    }
    
    for outcome_var, outcome_label in outcomes.items():
        formula = f'{outcome_var} ~ northeast + post_boko_haram + northeast_x_post + age + urban'
        
        try:
            model = smf.wls(formula, data=df, weights=df['weight'])
            results = model.fit(cov_type='HC1')
            
            did_coef = results.params['northeast_x_post']
            did_se = results.bse['northeast_x_post']
            did_pval = results.pvalues['northeast_x_post']
            
            print(f"\n{outcome_label}:")
            print(f"  DiD Coefficient: {did_coef:.4f} ({did_se:.4f}), p={did_pval:.3f}")
            
            robustness_results[outcome_var] = results
        except Exception as e:
            print(f"  Error: {str(e)}")
    
    # 2. Alternative Treatment: Boko Haram specific
    print("\n\n2. BOKO HARAM SPECIFIC EXPOSURE:")
    print("-" * 40)
    
    df['any_bh_x_post'] = df['any_boko_haram_exposure'] * df['post_boko_haram']
    formula = 'years_schooling ~ any_boko_haram_exposure + post_boko_haram + any_bh_x_post + age + urban'
    
    try:
        model = smf.wls(formula, data=df, weights=df['weight'])
        results = model.fit(cov_type='HC1')
        
        print(results.summary())
        robustness_results['boko_haram_specific'] = results
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # 3. Placebo Test: Use pre-conflict cohorts only
    print("\n\n3. PLACEBO TEST (Pre-conflict cohorts):")
    print("-" * 40)
    print("Testing for differential trends before conflict began...")
    
    df_placebo = df[df['birth_year'] < 1985].copy()
    df_placebo['pseudo_post'] = (df_placebo['birth_year'] >= 1980).astype(int)
    df_placebo['placebo_treatment'] = df_placebo['northeast'] * df_placebo['pseudo_post']
    
    formula = 'years_schooling ~ northeast + pseudo_post + placebo_treatment + age'
    
    try:
        model = smf.wls(formula, data=df_placebo, weights=df_placebo['weight'])
        results = model.fit(cov_type='HC1')
        
        placebo_coef = results.params['placebo_treatment']
        placebo_pval = results.pvalues['placebo_treatment']
        
        print(f"  Placebo DiD Coefficient: {placebo_coef:.4f}")
        print(f"  P-value: {placebo_pval:.3f}")
        
        if placebo_pval > 0.10:
            print("  ✓ PASS: No differential trends detected (p > 0.10)")
        else:
            print("  ✗ WARNING: Potential pre-treatment differential trends")
        
        robustness_results['placebo'] = results
    except Exception as e:
        print(f"Error: {str(e)}")
    
    return robustness_results

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_visualizations(df, output_dir):
    """
    Create key visualizations for the analysis
    """
    
    print("\n" + "="*70)
    print("CREATING VISUALIZATIONS")
    print("="*70)
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)
    
    # 1. Trends in education by region and cohort
    print("\n1. Creating trends plot...")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Calculate means by birth year and region
    trends = df.groupby(['birth_year', 'northeast'])['years_schooling'].mean().reset_index()
    
    for region in [0, 1]:
        region_data = trends[trends['northeast'] == region]
        label = "Northeast" if region == 1 else "Other Regions"
        ax.plot(region_data['birth_year'], region_data['years_schooling'], 
                marker='o', linewidth=2, label=label)
    
    # Add vertical line for Boko Haram start
    ax.axvline(x=1991, color='red', linestyle='--', linewidth=2, 
               label='School entry of 2009 conflict-affected cohort')
    
    ax.set_xlabel('Birth Year', fontsize=12)
    ax.set_ylabel('Years of Schooling', fontsize=12)
    ax.set_title('Educational Attainment by Birth Cohort and Region', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir + 'trends_by_cohort.png', dpi=300, bbox_inches='tight')
    print(f"  Saved: {output_dir}trends_by_cohort.png")
    plt.close()
    
    # 2. Distribution of education by treatment status
    print("2. Creating distribution plot...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Pre-conflict
    df_pre = df[df['post_boko_haram'] == 0]
    for region in [0, 1]:
        region_data = df_pre[df_pre['northeast'] == region]['years_schooling']
        label = "Northeast" if region == 1 else "Other Regions"
        axes[0].hist(region_data, bins=range(0, 20), alpha=0.6, label=label, density=True)
    
    axes[0].set_xlabel('Years of Schooling')
    axes[0].set_ylabel('Density')
    axes[0].set_title('Pre-Conflict Cohorts')
    axes[0].legend()
    
    # Post-conflict
    df_post = df[df['post_boko_haram'] == 1]
    for region in [0, 1]:
        region_data = df_post[df_post['northeast'] == region]['years_schooling']
        label = "Northeast" if region == 1 else "Other Regions"
        axes[1].hist(region_data, bins=range(0, 20), alpha=0.6, label=label, density=True)
    
    axes[1].set_xlabel('Years of Schooling')
    axes[1].set_ylabel('Density')
    axes[1].set_title('Post-Conflict Cohorts')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig(output_dir + 'education_distribution.png', dpi=300, bbox_inches='tight')
    print(f"  Saved: {output_dir}education_distribution.png")
    plt.close()
    
    # 3. Mean comparison (DiD visual)
    print("3. Creating DiD visual...")
    
    means = df.groupby(['northeast', 'post_boko_haram'])['years_schooling'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    for region in [0, 1]:
        region_data = means[means['northeast'] == region]
        label = "Northeast" if region == 1 else "Other Regions"
        x = region_data['post_boko_haram']
        y = region_data['years_schooling']
        ax.plot(x, y, marker='o', markersize=12, linewidth=3, label=label)
    
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Pre-Conflict\nCohorts', 'Post-Conflict\nCohorts'], fontsize=11)
    ax.set_ylabel('Mean Years of Schooling', fontsize=12)
    ax.set_title('Difference-in-Differences: Visual Representation', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir + 'did_visual.png', dpi=300, bbox_inches='tight')
    print(f"  Saved: {output_dir}did_visual.png")
    plt.close()
    
    print("\nAll visualizations created!")

# ============================================================================
# MAIN ANALYSIS PIPELINE
# ============================================================================

def main():
    """
    Run complete econometric analysis
    """
    
    print("="*70)
    print("ECONOMETRIC ANALYSIS: CONFLICT AND EDUCATION IN NIGERIA")
    print("="*70)
    
    # Create output directories
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)
    
    # Load data
    df = load_analysis_data()
    
    # Run all specifications
    all_results = {}
    
    # 1. Basic DiD
    all_results['basic_did'] = run_basic_did(df)
    
    # 2. DiD with controls
    all_results['did_controls'] = run_did_with_controls(df)
    
    # 3. DiD with state FE
    all_results['did_state_fe'] = run_did_with_state_fe(df)
    
    # 4. Continuous treatment
    all_results['continuous'] = run_continuous_treatment(df)
    
    # 5. Event study
    all_results['event_study'], event_coefs = run_event_study(df)
    
    # 6. Heterogeneity
    all_results['heterogeneity'] = run_heterogeneity_analysis(df)
    
    # 7. Robustness checks
    all_results['robustness'] = run_robustness_checks(df)
    
    # 8. Create visualizations
    create_visualizations(df, FIGURES_DIR)
    
    # Save results summary
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print(f"\nResults saved to: {OUTPUT_DIR}")
    print(f"Figures saved to: {FIGURES_DIR}")
    
    return all_results

if __name__ == "__main__":
    results = main()
