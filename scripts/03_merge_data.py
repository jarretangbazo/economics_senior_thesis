"""
Merge ACLED and DHS Data for Conflict-Education Analysis
==========================================================
This script merges conflict exposure data with individual education outcomes.

Author: Jarret Angbazo
Date: November 2025
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

DATA_DIR = "/Users/jarretangbazo/economics_senior_thesis/data/"

# Input files
ACLED_FILE = DATA_DIR + "acled_lga_year.csv"
DHS_FILE = DATA_DIR + "dhs_education_clean.csv"

# Output file
MERGED_FILE = DATA_DIR + "analysis_dataset.csv"

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================

def load_data():
    """
    Load ACLED and DHS data
    """
    
    print("="*70)
    print("LOADING DATA")
    print("="*70)
    
    # Load ACLED conflict data
    print("\nLoading ACLED data...")
    acled = pd.read_csv(ACLED_FILE)
    print(f"  ACLED observations: {len(acled)}")
    print(f"  Years: {acled['year'].min()}-{acled['year'].max()}")
    print(f"  Unique LGAs: {acled['lga'].nunique()}")
    
    # Load DHS education data
    print("\nLoading DHS data...")
    dhs = pd.read_csv(DHS_FILE)
    print(f"  DHS observations: {len(dhs)}")
    print(f"  Survey years: {sorted(dhs['survey_year'].unique())}")
    print(f"  Birth years: {dhs['birth_year'].min()}-{dhs['birth_year'].max()}")
    
    return acled, dhs

# ============================================================================
# STEP 2: STANDARDIZE STATE NAMES
# ============================================================================

def standardize_state_names(df, state_col='state'):
    """
    Standardize state names for merging
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with state column
    state_col : str
        Name of state column
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with standardized state names
    """
    
    df = df.copy()
    
    # Clean state names
    df[state_col] = df[state_col].str.strip().str.title()
    
    # Handle common variations
    state_mapping = {
        'Fct Abuja': 'FCT',
        'Fct': 'FCT',
        'Federal Capital Territory': 'FCT',
        'Nassarawa': 'Nasarawa',
        'Rivers State': 'Rivers',
        'Lagos State': 'Lagos'
    }
    
    df[state_col] = df[state_col].replace(state_mapping)
    
    return df

# ============================================================================
# STEP 3: CALCULATE CONFLICT EXPOSURE FOR EACH INDIVIDUAL
# ============================================================================

def calculate_conflict_exposure(dhs, acled):
    """
    Calculate conflict exposure for each DHS respondent based on their
    state of residence and age during conflict periods
    
    Parameters:
    -----------
    dhs : pd.DataFrame
        DHS individual data
    acled : pd.DataFrame
        ACLED state-year level data
    
    Returns:
    --------
    pd.DataFrame
        DHS data with conflict exposure measures
    """
    
    print("\n" + "="*70)
    print("CALCULATING CONFLICT EXPOSURE")
    print("="*70)
    
    # Standardize state names in both datasets
    dhs = standardize_state_names(dhs, 'state')
    acled = standardize_state_names(acled, 'state')
    
    # Aggregate ACLED to state-year level (since DHS typically only has state IDs)
    print("\nAggregating conflict data to state-year level...")
    state_year_conflict = acled.groupby(['state', 'year']).agg({
        'total_events': 'sum',
        'violent_events': 'sum',
        'boko_haram_events': 'sum',
        'total_fatalities': 'sum',
        'violent_fatalities': 'sum',
        'boko_haram_fatalities': 'sum',
        'any_violent_conflict': 'max',
        'any_boko_haram': 'max'
    }).reset_index()
    
    print(f"  State-year observations: {len(state_year_conflict)}")
    
    # For each individual, calculate conflict exposure during school-age years
    # School age: 6-18 years old
    
    print("\nCalculating individual conflict exposure...")
    
    dhs['conflict_exposure_school_age'] = 0.0
    dhs['violent_events_school_age'] = 0
    dhs['boko_haram_events_school_age'] = 0
    dhs['years_exposed_school_age'] = 0
    dhs['exposed_during_school_age'] = 0
    
    # This is computationally intensive, so we'll do it efficiently
    # Create a list to store exposure for each individual
    exposure_data = []
    
    for idx, person in dhs.iterrows():
        state = person['state']
        birth_year = person['birth_year']
        
        if pd.isna(state) or pd.isna(birth_year):
            exposure_data.append({
                'idx': idx,
                'conflict_exposure_school_age': 0,
                'violent_events_school_age': 0,
                'boko_haram_events_school_age': 0,
                'years_exposed_school_age': 0,
                'exposed_during_school_age': 0
            })
            continue
        
        # School age years: when person was 6-18
        school_start_year = birth_year + 6
        school_end_year = birth_year + 18
        
        # Get conflict in this state during school years
        state_conflict = state_year_conflict[
            (state_year_conflict['state'] == state) &
            (state_year_conflict['year'] >= school_start_year) &
            (state_year_conflict['year'] <= school_end_year)
        ]
        
        if len(state_conflict) > 0:
            violent_events = state_conflict['violent_events'].sum()
            boko_haram_events = state_conflict['boko_haram_events'].sum()
            years_exposed = (state_conflict['any_violent_conflict'] > 0).sum()
            exposed = int(violent_events > 0)
            
            # Intensity measure: events per school-age year
            years_in_data = len(state_conflict)
            exposure_intensity = violent_events / max(years_in_data, 1)
        else:
            violent_events = 0
            boko_haram_events = 0
            years_exposed = 0
            exposed = 0
            exposure_intensity = 0
        
        exposure_data.append({
            'idx': idx,
            'conflict_exposure_school_age': exposure_intensity,
            'violent_events_school_age': violent_events,
            'boko_haram_events_school_age': boko_haram_events,
            'years_exposed_school_age': years_exposed,
            'exposed_during_school_age': exposed
        })
    
    # Convert to DataFrame and merge back
    exposure_df = pd.DataFrame(exposure_data)
    
    for col in ['conflict_exposure_school_age', 'violent_events_school_age', 
                'boko_haram_events_school_age', 'years_exposed_school_age', 
                'exposed_during_school_age']:
        dhs[col] = exposure_df[col].values
    
    print(f"\n  Individuals with any conflict exposure: {dhs['exposed_during_school_age'].sum()}")
    print(f"  Mean violent events during school age: {dhs['violent_events_school_age'].mean():.2f}")
    print(f"  Mean years exposed: {dhs['years_exposed_school_age'].mean():.2f}")
    
    return dhs, state_year_conflict

# ============================================================================
# STEP 4: CREATE TREATMENT AND CONTROL GROUPS
# ============================================================================

def create_treatment_groups(df):
    """
    Create treatment and control group indicators for diff-in-diff analysis
    
    Parameters:
    -----------
    df : pd.DataFrame
        Merged data with conflict exposure
    
    Returns:
    --------
    pd.DataFrame
        Data with treatment indicators
    """
    
    print("\n" + "="*70)
    print("CREATING TREATMENT GROUPS")
    print("="*70)
    
    df = df.copy()
    
    # Define treatment: high conflict exposure during school age
    # Use top quartile of conflict exposure
    exposure_quartiles = df['conflict_exposure_school_age'].quantile([0.5, 0.75, 0.9])
    
    print(f"\nConflict exposure distribution:")
    print(f"  50th percentile: {exposure_quartiles[0.5]:.2f}")
    print(f"  75th percentile: {exposure_quartiles[0.75]:.2f}")
    print(f"  90th percentile: {exposure_quartiles[0.9]:.2f}")
    
    # Treatment definitions
    df['high_conflict'] = (df['conflict_exposure_school_age'] > exposure_quartiles[0.75]).astype(int)
    df['medium_conflict'] = ((df['conflict_exposure_school_age'] > exposure_quartiles[0.5]) & 
                             (df['conflict_exposure_school_age'] <= exposure_quartiles[0.75])).astype(int)
    df['low_conflict'] = (df['conflict_exposure_school_age'] <= exposure_quartiles[0.5]).astype(int)
    
    # Alternative treatment: any Boko Haram exposure
    df['any_boko_haram_exposure'] = (df['boko_haram_events_school_age'] > 0).astype(int)
    
    # Cohort definitions for diff-in-diff
    # Post-treatment cohorts: those who were school age during 2009-2020 (Boko Haram period)
    df['post_boko_haram'] = ((df['birth_year'] >= 1991) & (df['birth_year'] <= 2014)).astype(int)
    df['pre_boko_haram'] = (df['birth_year'] < 1991).astype(int)
    
    # Regional treatment (Northeast states most affected)
    northeast_states = ['Adamawa', 'Bauchi', 'Borno', 'Gombe', 'Taraba', 'Yobe']
    df['northeast'] = df['state'].isin(northeast_states).astype(int)
    
    print(f"\nTreatment group sizes:")
    print(f"  High conflict: {df['high_conflict'].sum()} ({df['high_conflict'].mean()*100:.1f}%)")
    print(f"  Medium conflict: {df['medium_conflict'].sum()} ({df['medium_conflict'].mean()*100:.1f}%)")
    print(f"  Low conflict: {df['low_conflict'].sum()} ({df['low_conflict'].mean()*100:.1f}%)")
    print(f"\n  Any Boko Haram exposure: {df['any_boko_haram_exposure'].sum()} ({df['any_boko_haram_exposure'].mean()*100:.1f}%)")
    print(f"\n  Northeast region: {df['northeast'].sum()} ({df['northeast'].mean()*100:.1f}%)")
    print(f"  Post-Boko Haram cohorts: {df['post_boko_haram'].sum()} ({df['post_boko_haram'].mean()*100:.1f}%)")
    
    # Create interaction term for diff-in-diff
    df['northeast_x_post2009'] = df['northeast'] * df['post_boko_haram']
    df['high_conflict_x_post2009'] = df['high_conflict'] * df['post_boko_haram']
    
    return df

# ============================================================================
# STEP 5: CREATE ANALYSIS VARIABLES
# ============================================================================

def create_analysis_variables(df):
    """
    Create additional variables for analysis
    
    Parameters:
    -----------
    df : pd.DataFrame
        Merged data
    
    Returns:
    --------
    pd.DataFrame
        Data with analysis variables
    """
    
    print("\n" + "="*70)
    print("CREATING ANALYSIS VARIABLES")
    print("="*70)
    
    df = df.copy()
    
    # Age categories
    df['age_group'] = pd.cut(df['age'], 
                             bins=[15, 20, 25, 30, 35, 40, 45, 50],
                             labels=['15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49'])
    
    # Birth cohort categories (5-year bins)
    df['cohort_group'] = pd.cut(df['birth_year'],
                                bins=[1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010],
                                labels=['1970-74', '1975-79', '1980-84', '1985-89', 
                                       '1990-94', '1995-99', '2000-04', '2005-09'])
    
    # School attendance during key conflict years
    df['school_age_2009_2015'] = ((df['birth_year'] >= 1991) & (df['birth_year'] <= 2009)).astype(int)
    
    # Control variables
    if 'wealth_quintile' in df.columns:
        df['wealth_q1'] = (df['wealth_quintile'] == 1).astype(int)
        df['wealth_q2'] = (df['wealth_quintile'] == 2).astype(int)
        df['wealth_q3'] = (df['wealth_quintile'] == 3).astype(int)
        df['wealth_q4'] = (df['wealth_quintile'] == 4).astype(int)
        df['wealth_q5'] = (df['wealth_quintile'] == 5).astype(int)
    
    # Create state fixed effects coding
    df['state_code'] = df['state'].astype('category').cat.codes
    
    # Create year fixed effects
    df['survey_year_code'] = df['survey_year'].astype('category').cat.codes
    
    print(f"  Created age groups, cohorts, and control variables")
    print(f"  Sample size: {len(df)}")
    
    return df

# ============================================================================
# STEP 6: SUMMARY STATISTICS
# ============================================================================

def print_summary_statistics(df):
    """
    Print summary statistics for merged dataset
    """
    
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)
    
    # Overall statistics
    print("\nOverall sample:")
    print(f"  N = {len(df)}")
    print(f"  Mean age: {df['age'].mean():.1f} (SD: {df['age'].std():.1f})")
    print(f"  Mean years of schooling: {df['years_schooling'].mean():.2f} (SD: {df['years_schooling'].std():.2f})")
    print(f"  % with no education: {df['no_education'].mean()*100:.1f}%")
    print(f"  % completed primary: {df['primary_complete'].mean()*100:.1f}%")
    print(f"  % completed secondary: {df['secondary_complete'].mean()*100:.1f}%")
    
    # By conflict exposure
    print("\n\nBy conflict exposure:")
    summary_by_conflict = df.groupby('high_conflict').agg({
        'case_id': 'count',
        'years_schooling': 'mean',
        'no_education': 'mean',
        'primary_complete': 'mean',
        'secondary_complete': 'mean'
    }).round(3)
    summary_by_conflict.columns = ['N', 'Mean Years School', 'No Education', 
                                   'Primary Complete', 'Secondary Complete']
    print(summary_by_conflict)
    
    # By region
    print("\n\nBy region (Northeast vs other):")
    summary_by_region = df.groupby('northeast').agg({
        'case_id': 'count',
        'years_schooling': 'mean',
        'no_education': 'mean',
        'violent_events_school_age': 'mean'
    }).round(3)
    summary_by_region.columns = ['N', 'Mean Years School', 'No Education', 
                                 'Violent Events During School Age']
    print(summary_by_region)
    
    # By cohort
    print("\n\nBy birth cohort:")
    summary_by_cohort = df.groupby('post_boko_haram').agg({
        'case_id': 'count',
        'years_schooling': 'mean',
        'no_education': 'mean',
        'violent_events_school_age': 'mean'
    }).round(3)
    summary_by_cohort.columns = ['N', 'Mean Years School', 'No Education', 
                                 'Violent Events During School Age']
    print(summary_by_cohort)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function
    """
    
    print("="*70)
    print("MERGING ACLED AND DHS DATA")
    print("="*70)
    
    # Load data
    acled, dhs = load_data()
    
    # Calculate conflict exposure for each individual
    dhs, state_year_conflict = calculate_conflict_exposure(dhs, acled)
    
    # Create treatment groups
    dhs = create_treatment_groups(dhs)
    
    # Create analysis variables
    dhs = create_analysis_variables(dhs)
    
    # Print summary statistics
    print_summary_statistics(dhs)
    
    # Save merged dataset
    print(f"\n{'='*70}")
    print("SAVING ANALYSIS DATASET")
    print(f"{'='*70}")
    
    dhs.to_csv(MERGED_FILE, index=False)
    print(f"\nAnalysis dataset saved to: {MERGED_FILE}")
    print(f"Observations: {len(dhs)}")
    print(f"Variables: {len(dhs.columns)}")
    
    # Also save state-year conflict data for reference
    state_year_file = DATA_DIR + "state_year_conflict.csv"
    state_year_conflict.to_csv(state_year_file, index=False)
    print(f"State-year conflict data saved to: {state_year_file}")
    
    print("\n" + "="*70)
    print("MERGE COMPLETE!")
    print("="*70)
    
    return dhs

if __name__ == "__main__":
    df = main()
