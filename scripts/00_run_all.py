"""
MASTER SCRIPT: Complete Analysis Pipeline
==========================================
This script runs the entire analysis from data download to final results.
* Run after setting up ACLED API credentials and downloading DHS data.

Author: Jarret Angbazo
Date: November 2025
"""

import os
import sys
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

# Directory setup
BASE_DIR = "/Users/jarretangbazo/economics_senior_thesis/"
DATA_DIR = BASE_DIR + "data/"
RESULTS_DIR = BASE_DIR + "results/"
FIGURES_DIR = RESULTS_DIR + "figures/"

# Create directories
for directory in [DATA_DIR, RESULTS_DIR, FIGURES_DIR]:
    os.makedirs(directory, exist_ok=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70 + "\n")

def print_step(step_num, step_name):
    """Print step header"""
    print("\n" + "-"*70)
    print(f"STEP {step_num}: {step_name}")
    print("-"*70)

def check_file_exists(filepath, description):
    """Check if required file exists"""
    if os.path.exists(filepath):
        print(f"✓ Found {description}: {filepath}")
        return True
    else:
        print(f"✗ Missing {description}: {filepath}")
        return False

# ============================================================================
# MAIN PIPELINE
# ============================================================================

def run_pipeline():
    """
    Execute complete analysis pipeline
    """
    
    print_header("NIGERIA CONFLICT & EDUCATION ANALYSIS PIPELINE")
    
    start_time = datetime.now()
    print(f"Analysis started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # ========================================================================
    # STEP 1: ACLED Data
    # ========================================================================
    
    print_step(1, "DOWNLOAD AND CLEAN ACLED CONFLICT DATA")
    
    print("\nRunning: 01_acled_download_clean.py")
    print("-" * 40)
    
    try:
        exec(open('01_acled_download_clean.py').read())
        print("\n✓ ACLED data processing complete!")
        
        # Check output
        acled_file = DATA_DIR + "acled_lga_year.csv"
        if check_file_exists(acled_file, "ACLED LGA-year data"):
            import pandas as pd
            acled = pd.read_csv(acled_file)
            print(f"  - {len(acled)} LGA-year observations")
            print(f"  - {acled['year'].min()}-{acled['year'].max()}")
        
    except Exception as e:
        print(f"\n✗ Error in ACLED processing: {str(e)}")
        print("Please check your ACLED API credentials")
        return False
    
    # ========================================================================
    # STEP 2: DHS Data
    # ========================================================================
    
    print_step(2, "PROCESS DHS EDUCATION DATA")
    
    print("\nRunning: 02_dhs_process.py")
    print("-" * 40)
    
    try:
        exec(open('02_dhs_process.py').read())
        print("\n✓ DHS data processing complete!")
        
        # Check output
        dhs_file = DATA_DIR + "dhs_education_clean.csv"
        if check_file_exists(dhs_file, "DHS cleaned data"):
            import pandas as pd
            dhs = pd.read_csv(dhs_file)
            print(f"  - {len(dhs)} individual observations")
            print(f"  - {dhs['survey_year'].unique()} survey years")
        
    except Exception as e:
        print(f"\n✗ Error in DHS processing: {str(e)}")
        print("This is expected if you haven't downloaded DHS data yet")
        print("The script creates synthetic data for demonstration")
    
    # ========================================================================
    # STEP 3: Merge Data
    # ========================================================================
    
    print_step(3, "MERGE ACLED AND DHS DATA")
    
    print("\nRunning: 03_merge_data.py")
    print("-" * 40)
    
    try:
        exec(open('03_merge_data.py').read())
        print("\n✓ Data merge complete!")
        
        # Check output
        merged_file = DATA_DIR + "analysis_dataset.csv"
        if check_file_exists(merged_file, "Analysis dataset"):
            import pandas as pd
            merged = pd.read_csv(merged_file)
            print(f"  - {len(merged)} observations in analysis sample")
            print(f"  - {len(merged.columns)} variables")
            print(f"  - {merged['exposed_during_school_age'].sum()} individuals exposed to conflict")
        
    except Exception as e:
        print(f"\n✗ Error in merging: {str(e)}")
        return False
    
    # ========================================================================
    # STEP 4: Econometric Analysis
    # ========================================================================
    
    print_step(4, "RUN ECONOMETRIC ANALYSIS")
    
    print("\nRunning: 04_econometric_analysis.py")
    print("-" * 40)
    
    try:
        exec(open('04_econometric_analysis.py').read())
        print("\n✓ Econometric analysis complete!")
        
        # Check outputs
        if os.path.exists(FIGURES_DIR):
            figures = os.listdir(FIGURES_DIR)
            print(f"  - Created {len(figures)} figures in {FIGURES_DIR}")
        
    except Exception as e:
        print(f"\n✗ Error in analysis: {str(e)}")
        print("Make sure statsmodels is installed: pip install statsmodels")
        return False
    
    # ========================================================================
    # COMPLETION
    # ========================================================================
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print_header("PIPELINE COMPLETE!")
    
    print(f"Started:  {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Finished: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration}")
    
    print("\n" + "="*70)
    print("OUTPUT FILES:")
    print("="*70)
    print(f"\nData files (in {DATA_DIR}):")
    print("  - acled_nigeria_raw.csv")
    print("  - acled_nigeria_clean.csv")
    print("  - acled_lga_year.csv")
    print("  - dhs_education_clean.csv")
    print("  - analysis_dataset.csv")
    print("  - state_year_conflict.csv")
    
    print(f"\nFigures (in {FIGURES_DIR}):")
    print("  - trends_by_cohort.png")
    print("  - education_distribution.png")
    print("  - did_visual.png")
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("\n1. Review the figures in", FIGURES_DIR)
    print("2. Examine coefficient estimates in console output above")
    print("3. Write up results in your thesis")
    print("4. Consider additional robustness checks")
    print("5. Discuss with your advisor")
    
    return True

# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    
    print("\n" + "="*70)
    print("IMPORTANT NOTES BEFORE RUNNING:")
    print("="*70)
    print("\n1. ACLED API Credentials:")
    print("   - Register at: https://developer.acleddata.com/")
    print("   - Update credentials in 01_acled_download_clean.py")
    
    print("\n2. DHS Data:")
    print("   - Request access at: https://dhsprogram.com/")
    print("   - Download Nigeria surveys (2003, 2008, 2013, 2018)")
    print("   - Place .DTA files in:", DATA_DIR + "dhs_data/")
    print("   - Or use synthetic data for demonstration")
    
    print("\n3. Required Packages:")
    print("   pip install pandas numpy statsmodels matplotlib seaborn scipy")
    print("   pip install linearmodels  # Optional, for panel data models")
    
    print("\n" + "="*70)
    
    # Ask for confirmation
    response = input("\nReady to run pipeline? (y/n): ")
    
    if response.lower() == 'y':
        success = run_pipeline()
        
        if success:
            sys.exit(0)
        else:
            print("\n⚠ Pipeline completed with errors. Review messages above.")
            sys.exit(1)
    else:
        print("\nPipeline cancelled. Run this script when you're ready!")
        sys.exit(0)
