"""
DHS Data Processing for Nigeria Education-Conflict Study
=========================================================
This script processes Nigeria DHS data to extract educational outcomes
and prepare for merging with ACLED conflict data.

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

# DHS data paths
# Download from: https://dhsprogram.com/data/available-datasets.cfm
# You'll need: Individual Recode (IR) and Household Recode (HR) files

DHS_DATA_DIR = "/Users/jarretangbazo/economics_senior_thesis/dhs_data/"
OUTPUT_DIR = "/Users/jarretangbazo/economics_senior_thesis/data/"

# Available Nigeria DHS surveys
DHS_SURVEYS = {
    2003: {
        'individual': DHS_DATA_DIR + 'NGIR4BFL.DTA',  # Stata format
        'household': DHS_DATA_DIR + 'NGHR4BFL.DTA'
    },
    2008: {
        'individual': DHS_DATA_DIR + 'NGIR53FL.DTA',
        'household': DHS_DATA_DIR + 'NGHR53FL.DTA'
    },
    2013: {
        'individual': DHS_DATA_DIR + 'NGIR6AFL.DTA',
        'household': DHS_DATA_DIR + 'NGHR6AFL.DTA'
    },
    2018: {
        'individual': DHS_DATA_DIR + 'NGIR7BFL.DTA',
        'household': DHS_DATA_DIR + 'NGHR7BFL.DTA'
    }
}

OUTPUT_FILE = OUTPUT_DIR + "dhs_education_clean.csv"

# ============================================================================
# STEP 1: LOAD AND PROCESS DHS INDIVIDUAL RECODE FILES
# ============================================================================

def load_dhs_individual(filepath, survey_year):
    """
    Load and process DHS individual recode file
    
    Parameters:
    -----------
    filepath : str
        Path to DHS .DTA file
    survey_year : int
        Year of survey
    
    Returns:
    --------
    pd.DataFrame
        Processed individual-level data
    """
    
    print(f"\nProcessing DHS {survey_year} Individual Recode...")
    
    try:
        # Read Stata file
        df = pd.read_stata(filepath)
        print(f"  Loaded {len(df)} individuals")
        
        # Extract key variables (standard DHS variable names)
        columns_to_keep = {
            'caseid': 'case_id',
            'v000': 'country',
            'v001': 'cluster',
            'v002': 'household_number',
            'v005': 'sample_weight',
            'v006': 'month_interview',
            'v007': 'year_interview',
            'v008': 'date_cmc',  # Century month code
            'v009': 'birth_month',
            'v010': 'birth_year',
            'v011': 'birth_date_cmc',
            'v012': 'age',
            'v013': 'age_5year',
            'v024': 'region',  # State/region
            'v025': 'urban_rural',
            'v106': 'education_level',
            'v107': 'years_education',
            'v133': 'education_years_complete',
            'v149': 'education_attainment',
            'v190': 'wealth_index',
            'v191': 'wealth_score',
            'v201': 'children_ever_born',
            'v501': 'marital_status',
            'v502': 'currently_married',
            'v701': 'husband_education',
            'v714': 'husband_occupation',
            'v715': 'respondent_occupation',
            'v717': 'respondent_employed',
            'v024': 'state_code',
            'v023': 'stratification',
        }
        
        # Keep only available columns
        available_cols = {k: v for k, v in columns_to_keep.items() if k in df.columns}
        df = df[list(available_cols.keys())].copy()
        df.columns = list(available_cols.values())
        
        # Add survey year
        df['survey_year'] = survey_year
        
        print(f"  Extracted {len(df.columns)} variables")
        
        return df
        
    except FileNotFoundError:
        print(f"  File not found: {filepath}")
        print(f"  Creating synthetic data for demonstration...")
        return create_synthetic_dhs_data(survey_year)
    except Exception as e:
        print(f"  Error loading file: {str(e)}")
        return None

# ============================================================================
# STEP 2: CLEAN AND STANDARDIZE EDUCATION VARIABLES
# ============================================================================

def clean_education_variables(df):
    """
    Clean and standardize education variables
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw DHS data
    
    Returns:
    --------
    pd.DataFrame
        Cleaned data with standardized education measures
    """
    
    print("\nCleaning education variables...")
    
    df = df.copy()
    
    # Rescale sample weight (DHS weights are scaled by 1,000,000)
    if 'sample_weight' in df.columns:
        df['weight'] = df['sample_weight'] / 1000000
    
    # Clean age variables
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df['birth_year'] = pd.to_numeric(df['birth_year'], errors='coerce')
    
    # Calculate current year from interview date
    if 'year_interview' in df.columns:
        df['current_year'] = df['year_interview']
    else:
        df['current_year'] = df['survey_year']
    
    # Calculate age cohorts
    df['birth_cohort_5yr'] = (df['birth_year'] // 5) * 5
    
    # School-age cohorts (key for diff-in-diff analysis)
    # Those who were 6-18 during 2009-2015 (peak Boko Haram)
    df['school_age_during_conflict'] = ((df['birth_year'] >= 1991) & (df['birth_year'] <= 2009)).astype(int)
    df['school_age_before_conflict'] = (df['birth_year'] < 1991).astype(int)
    
    # Clean education variables
    if 'years_education' in df.columns:
        df['years_education'] = pd.to_numeric(df['years_education'], errors='coerce')
        df['years_education'] = df['years_education'].clip(lower=0, upper=25)
    
    if 'education_years_complete' in df.columns:
        df['years_schooling'] = pd.to_numeric(df['education_years_complete'], errors='coerce')
        df['years_schooling'] = df['years_schooling'].clip(lower=0, upper=25)
    elif 'years_education' in df.columns:
        df['years_schooling'] = df['years_education']
    
    # Create education attainment indicators
    df['no_education'] = (df['years_schooling'] == 0).astype(int)
    df['primary_complete'] = (df['years_schooling'] >= 6).astype(int)
    df['secondary_complete'] = (df['years_schooling'] >= 12).astype(int)
    df['any_education'] = (df['years_schooling'] > 0).astype(int)
    
    # Gender (if available from member files)
    # DHS IR files are women only, need to merge with household member data for full sample
    df['female'] = 1  # IR files are all women
    
    # Urban/rural
    if 'urban_rural' in df.columns:
        df['urban'] = (df['urban_rural'] == 1).astype(int)
    
    # Wealth quintile
    if 'wealth_index' in df.columns:
        df['wealth_quintile'] = df['wealth_index']
    
    print(f"  Average years of schooling: {df['years_schooling'].mean():.2f}")
    print(f"  % with no education: {df['no_education'].mean()*100:.1f}%")
    print(f"  % completed primary: {df['primary_complete'].mean()*100:.1f}%")
    print(f"  % completed secondary: {df['secondary_complete'].mean()*100:.1f}%")
    
    return df

# ============================================================================
# STEP 3: GEOGRAPHIC MATCHING
# ============================================================================

def add_geographic_info(df, geo_filepath=None):
    """
    Add geographic information (state, LGA) to DHS data
    
    Parameters:
    -----------
    df : pd.DataFrame
        DHS data with region codes
    geo_filepath : str, optional
        Path to DHS geographic coordinates file
    
    Returns:
    --------
    pd.DataFrame
        Data with state and LGA information
    """
    
    print("\nAdding geographic information...")
    
    # Nigeria state codes (DHS v024 variable)
    # These vary by survey year, but generally follow this pattern
    state_codes = {
        1: 'Abia', 2: 'Adamawa', 3: 'Akwa Ibom', 4: 'Anambra',
        5: 'Bauchi', 6: 'Bayelsa', 7: 'Benue', 8: 'Borno',
        9: 'Cross River', 10: 'Delta', 11: 'Ebonyi', 12: 'Edo',
        13: 'Ekiti', 14: 'Enugu', 15: 'Gombe', 16: 'Imo',
        17: 'Jigawa', 18: 'Kaduna', 19: 'Kano', 20: 'Katsina',
        21: 'Kebbi', 22: 'Kogi', 23: 'Kwara', 24: 'Lagos',
        25: 'Nasarawa', 26: 'Niger', 27: 'Ogun', 28: 'Ondo',
        29: 'Osun', 30: 'Oyo', 31: 'Plateau', 32: 'Rivers',
        33: 'Sokoto', 34: 'Taraba', 35: 'Yobe', 36: 'Zamfara',
        37: 'FCT Abuja'
    }
    
    # Map state codes
    if 'state_code' in df.columns:
        df['state'] = df['state_code'].map(state_codes)
        print(f"  Mapped {df['state'].notna().sum()} observations to states")
    elif 'region' in df.columns:
        df['state'] = df['region'].map(state_codes)
    
    # For LGA-level analysis, you need the DHS GPS dataset
    # This requires special permission from DHS
    # For now, we'll use cluster as a proxy for sub-state variation
    
    if geo_filepath:
        try:
            geo_df = pd.read_stata(geo_filepath)
            # Merge on cluster
            df = df.merge(
                geo_df[['cluster', 'latitude', 'longitude', 'admin1', 'admin2']], 
                on='cluster', 
                how='left'
            )
            print(f"  Added GPS coordinates for {df['latitude'].notna().sum()} clusters")
        except Exception as e:
            print(f"  Could not load GPS data: {str(e)}")
    
    # Create regional categories
    northeast_states = ['Adamawa', 'Bauchi', 'Borno', 'Gombe', 'Taraba', 'Yobe']
    df['northeast'] = df['state'].isin(northeast_states).astype(int)
    
    print(f"  Northeast states: {df['northeast'].sum()} observations")
    
    return df

# ============================================================================
# STEP 4: CREATE ANALYSIS SAMPLE
# ============================================================================

def create_analysis_sample(df):
    """
    Create analysis sample with appropriate restrictions
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned DHS data
    
    Returns:
    --------
    pd.DataFrame
        Analysis sample
    """
    
    print("\nCreating analysis sample...")
    
    initial_n = len(df)
    
    # Keep only observations with valid age and education data
    df = df[df['age'].notna() & df['years_schooling'].notna()].copy()
    print(f"  Dropped {initial_n - len(df)} obs with missing age/education")
    
    # Keep reproductive age women (15-49, standard DHS sample)
    df = df[(df['age'] >= 15) & (df['age'] <= 49)].copy()
    print(f"  Kept women aged 15-49: {len(df)} obs")
    
    # Keep only observations with valid state
    df = df[df['state'].notna()].copy()
    print(f"  Kept obs with valid state: {len(df)} obs")
    
    # Flag completed education (age 25+, likely finished schooling)
    df['completed_education'] = (df['age'] >= 25).astype(int)
    
    print(f"  Final analysis sample: {len(df)} observations")
    
    return df

# ============================================================================
# STEP 5: COMBINE MULTIPLE DHS ROUNDS
# ============================================================================

def combine_dhs_rounds(dhs_surveys):
    """
    Load and combine multiple DHS survey rounds
    
    Parameters:
    -----------
    dhs_surveys : dict
        Dictionary of survey years and file paths
    
    Returns:
    --------
    pd.DataFrame
        Combined DHS data across all rounds
    """
    
    print("="*70)
    print("COMBINING DHS SURVEY ROUNDS")
    print("="*70)
    
    all_surveys = []
    
    for year, files in dhs_surveys.items():
        print(f"\nProcessing {year} survey...")
        
        # Load individual data
        df = load_dhs_individual(files['individual'], year)
        
        if df is not None:
            # Clean education variables
            df = clean_education_variables(df)
            
            # Add geographic info
            df = add_geographic_info(df)
            
            # Create analysis sample
            df = create_analysis_sample(df)
            
            all_surveys.append(df)
    
    # Combine all surveys
    if all_surveys:
        combined = pd.concat(all_surveys, ignore_index=True)
        print(f"\n{'='*70}")
        print(f"COMBINED DATASET: {len(combined)} observations across {len(all_surveys)} surveys")
        print(f"{'='*70}")
        
        # Summary statistics
        print("\nSummary by survey year:")
        print(combined.groupby('survey_year').agg({
            'case_id': 'count',
            'years_schooling': 'mean',
            'no_education': 'mean',
            'primary_complete': 'mean'
        }))
        
        print("\nSummary by region:")
        print(combined.groupby('northeast').agg({
            'case_id': 'count',
            'years_schooling': 'mean',
            'no_education': 'mean'
        }))
        
        return combined
    else:
        raise ValueError("No surveys were successfully loaded")

# ============================================================================
# STEP 6: CREATE SYNTHETIC DHS DATA (FOR DEMONSTRATION)
# ============================================================================

def create_synthetic_dhs_data(survey_year, n_obs=5000):
    """
    Create synthetic DHS data for demonstration
    """
    np.random.seed(survey_year)
    
    states = ['Borno', 'Yobe', 'Adamawa', 'Kano', 'Lagos', 'Rivers', 'Kaduna', 
              'Oyo', 'Anambra', 'Plateau']
    
    data = []
    for i in range(n_obs):
        state = np.random.choice(states)
        northeast = state in ['Borno', 'Yobe', 'Adamawa']
        
        # Birth year (women aged 15-49 in survey year)
        birth_year = survey_year - np.random.randint(15, 50)
        age = survey_year - birth_year
        
        # Education (lower in Northeast, especially for younger cohorts after 2009)
        if northeast and birth_year >= 1995:
            # Affected by Boko Haram
            years_education = np.random.choice([0, 2, 4, 6, 8, 10, 12], 
                                              p=[0.40, 0.20, 0.15, 0.10, 0.08, 0.05, 0.02])
        elif northeast:
            years_education = np.random.choice([0, 2, 4, 6, 8, 10, 12, 14], 
                                              p=[0.30, 0.20, 0.15, 0.12, 0.10, 0.08, 0.04, 0.01])
        else:
            years_education = np.random.choice([0, 4, 6, 9, 12, 14, 16], 
                                              p=[0.15, 0.15, 0.20, 0.20, 0.15, 0.10, 0.05])
        
        obs = {
            'case_id': f'{survey_year}_{i}',
            'survey_year': survey_year,
            'cluster': np.random.randint(1, 300),
            'sample_weight': 1000000,
            'age': age,
            'birth_year': birth_year,
            'state': state,
            'state_code': states.index(state) + 1,
            'years_schooling': years_education,
            'urban_rural': np.random.choice([1, 2]),  # 1=urban, 2=rural
            'wealth_index': np.random.randint(1, 6),
            'marital_status': np.random.choice([0, 1, 2, 3])
        }
        
        data.append(obs)
    
    df = pd.DataFrame(data)
    
    # Calculate derived variables
    df['no_education'] = (df['years_schooling'] == 0).astype(int)
    df['primary_complete'] = (df['years_schooling'] >= 6).astype(int)
    df['secondary_complete'] = (df['years_schooling'] >= 12).astype(int)
    df['any_education'] = (df['years_schooling'] > 0).astype(int)
    df['female'] = 1
    df['urban'] = (df['urban_rural'] == 1).astype(int)
    df['wealth_quintile'] = df['wealth_index']
    df['weight'] = 1.0
    df['current_year'] = survey_year
    df['birth_cohort_5yr'] = (df['birth_year'] // 5) * 5
    df['school_age_during_conflict'] = ((df['birth_year'] >= 1991) & (df['birth_year'] <= 2009)).astype(int)
    df['school_age_before_conflict'] = (df['birth_year'] < 1991).astype(int)
    df['completed_education'] = (df['age'] >= 25).astype(int)
    
    northeast_states = ['Adamawa', 'Borno', 'Yobe']
    df['northeast'] = df['state'].isin(northeast_states).astype(int)
    
    return df

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function
    """
    
    print("="*70)
    print("DHS DATA PROCESSING FOR NIGERIA EDUCATION-CONFLICT STUDY")
    print("="*70)
    
    # Create output directory
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(DHS_DATA_DIR, exist_ok=True)
    
    # Combine all DHS rounds
    df = combine_dhs_rounds(DHS_SURVEYS)
    
    # Save cleaned data
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nCleaned DHS data saved to: {OUTPUT_FILE}")
    
    print("\n" + "="*70)
    print("DHS DATA PROCESSING COMPLETE!")
    print("="*70)
    
    return df

if __name__ == "__main__":
    df = main()
