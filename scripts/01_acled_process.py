"""
ACLED Data Download and Cleaning for Nigeria Conflict Analysis
===============================================================
This script processes ACLED data for Nigeria and creates conflict exposure measures
at the LGA (Local Government Area) level.

Author: Jarret Angbazo
Date: November 2025
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# ACLED data
# Download from: https://acleddata.com
# You'll need: Account and ACLED API

# Data paths
DATA_DIR = "/Users/jarretangbazo/economics_senior_thesis/data/"
RAW_DATA_DIR = os.path.join(DATA_DIR, "ACLED_raw_by_year")
OUTPUT_DIR = DATA_DIR

# Study parameters
START_YEAR = 1997   # Include pre-conflict period for comparison
END_YEAR = 2019
COUNTRY = "Nigeria"

# Required columns - validate data has these
REQUIRED_COLUMNS = [
    'event_id_cnty', 'event_date', 'event_type', 'admin1', 'admin2',
    'location', 'latitude', 'longitude', 'fatalities', 'actor1', 'actor2'
]

# ============================================================================
# STEP 1: LOAD ACLED DATA
# ============================================================================

# Data downloaded: JUN-06_2019
def load_acled_data(raw_data_dir, start_year, end_year):
    """
    Load downloaded ACLED data with validation
    
    Parameters:
    -----------
    raw_data_dir : str
        Directory containing the CSV files
    start_year : int
        Start year for data
    end_year : int
        End year for data
    
    Returns:
    --------
    pd.DataFrame
        Raw ACLED data
    """
    
    print(f"Loading ACLED data for Nigeria ({start_year}-{end_year})...")
    print(f"Source directory: {raw_data_dir}")
    
    all_data = []
    missing_files = []
    
    for year in range(start_year, end_year + 1):
        filename = f"acled_nga_{year}.csv"
        filepath = os.path.join(raw_data_dir, filename)

        if os.path.exists(filepath):
            print(f"  Loading {filename}...", end=" ")
            try:
                year_df = pd.read_csv(filepath, low_memory=False)
                
                # Validate required columns exist
                missing_cols = [col for col in REQUIRED_COLUMNS if col not in year_df.columns]
                if missing_cols:
                    print(f"  WARNING: Missing columns {missing_cols}")
                else:
                    all_data.append(year_df)
                    print(f"✓ {len(year_df)} events")
                    
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                continue
        else:
            missing_files.append(filename)
            print(f"    {filename} not found")

    if missing_files:
        print(f"\n Missing {len(missing_files)} file(s): {', '.join(missing_files[:5])}")
        if len(missing_files) > 5:
            print(f"    ... and {len(missing_files) - 5} more")
    
    if all_data:
        df = pd.concat(all_data, ignore_index=True)
        print(f"\n✓ Total events loaded: {len(df):,}")
        print(f"  Years represented: {sorted(df['year'].unique())}")
        return df
    else:
        raise ValueError(
            "No data was successfully loaded. "
            f"Check that files exist in: {raw_data_dir}"
        )

# ============================================================================
# STEP 2: CLEAN AND PROCESS ACLED DATA
# ============================================================================

def clean_acled_data(df):
    """
    Clean and process ACLED data with validation
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw ACLED data
    
    Returns:
    --------
    pd.DataFrame
        Cleaned ACLED data
    """
    
    print("\nCleaning ACLED data...")
    
    # Create a copy
    df = df.copy()
    original_length = len(df)
    
    # Convert date columns with error handling
    print("  Processing dates...", end=" ")
    df['event_date'] = pd.to_datetime(df['event_date'], errors='coerce')
    
    # Check for invalid dates
    invalid_dates = df['event_date'].isna().sum()
    if invalid_dates > 0:
        print(f"  {invalid_dates} invalid dates found")
        df = df.dropna(subset=['event_date'])
    else:
        print("✓")
    
    df['year'] = df['event_date'].dt.year
    df['month'] = df['event_date'].dt.month
    
    # Convert numeric columns
    print("  Processing numeric columns...", end=" ")
    df['fatalities'] = pd.to_numeric(df['fatalities'], errors='coerce').fillna(0)
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    print("✓")
    
    # Clean location names (standardize)
    print("  Standardizing location names...", end=" ")
    df['admin1'] = df['admin1'].str.strip().str.title()  # State
    df['admin2'] = df['admin2'].fillna('Unknown').str.strip().str.title()  # LGA
    df['location'] = df['location'].str.strip().str.title()
    print("✓")
    
    # Create event type categories
    print("  Categorizing event types...", end=" ")
    violent_events = [
        'Battles',
        'Explosions/Remote violence',
        'Violence against civilians'
    ]
    
    df['is_violent'] = df['event_type'].isin(violent_events).astype(int)
    print("✓")
    
    # Flag Boko Haram events (multiple possible spellings)
    print("  Identifying Boko Haram events...", end=" ")
    boko_haram_keywords = ['boko haram', 'jama\'atu ahlis', 'iswap', 'islamic state']
    
    # Handle potential missing values in actor columns
    df['actor1'] = df['actor1'].fillna('')
    df['actor2'] = df['actor2'].fillna('')
    
    df['is_boko_haram'] = (
        df['actor1'].str.lower().str.contains('|'.join(boko_haram_keywords), na=False) | 
        df['actor2'].str.lower().str.contains('|'.join(boko_haram_keywords), na=False)
    ).astype(int)
    print("✓")
    
    # Create conflict intensity measure
    df['has_fatalities'] = (df['fatalities'] > 0).astype(int)
    
    # Remove rows with missing critical location data
    before_drop = len(df)
    df = df.dropna(subset=['admin1', 'admin2'])
    dropped = before_drop - len(df)
    
    print(f"\n  Data Quality Summary:")
    print(f"    Original events: {original_length:,}")
    print(f"    After cleaning: {len(df):,}")
    if dropped > 0:
        print(f"    Dropped (missing locations): {dropped:,}")
    print(f"    Violent events: {df['is_violent'].sum():,} ({df['is_violent'].mean()*100:.1f}%)")
    print(f"    Boko Haram events: {df['is_boko_haram'].sum():,} ({df['is_boko_haram'].mean()*100:.1f}%)")
    print(f"    Events with fatalities: {df['has_fatalities'].sum():,} ({df['has_fatalities'].mean()*100:.1f}%)")
    print(f"    Total fatalities: {df['fatalities'].sum():,.0f}")
    print(f"    Date range: {df['event_date'].min().strftime('%Y-%m-%d')} to {df['event_date'].max().strftime('%Y-%m-%d')}")
    
    return df

# ============================================================================
# STEP 3: AGGREGATE TO LGA-YEAR LEVEL
# ============================================================================

def aggregate_to_lga_year(df):
    """
    Aggregate conflict events to LGA-year level
    
    FIXED: Previous version had a critical bug in fatality calculations
    that would cause KeyError. Now uses proper groupby aggregation.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned ACLED data
    
    Returns:
    --------
    pd.DataFrame
        LGA-year level conflict measures
    """
    
    print("\nAggregating to LGA-year level...")
    
    # First, create helper columns for conditional aggregation
    df['violent_fatalities_calc'] = df['fatalities'] * df['is_violent']
    df['boko_haram_fatalities_calc'] = df['fatalities'] * df['is_boko_haram']
    
    # Group by state, LGA, and year
    lga_year = df.groupby(['admin1', 'admin2', 'year']).agg({
        # Event counts
        'event_id_cnty': 'count',
        'is_violent': 'sum',
        'is_boko_haram': 'sum',
        
        # Fatalities (FIXED: Now uses pre-calculated columns)
        'fatalities': 'sum',
        'violent_fatalities_calc': 'sum',
        'boko_haram_fatalities_calc': 'sum',
        
        # Event types
        'event_type': [
            lambda x: (x == 'Battles').sum(),
            lambda x: (x == 'Explosions/Remote violence').sum(),
            lambda x: (x == 'Violence against civilians').sum()
        ],
        
        # Location info (take first occurrence)
        'latitude': 'first',
        'longitude': 'first'
    }).reset_index()
    
    # Flatten column names
    lga_year.columns = [
        'state', 'lga', 'year', 
        'total_events', 'violent_events', 'boko_haram_events',
        'total_fatalities', 'violent_fatalities', 'boko_haram_fatalities',
        'battles', 'explosions', 'violence_civilians',
        'latitude', 'longitude'
    ]
    
    # Create binary indicators for any conflict
    lga_year['any_conflict'] = (lga_year['total_events'] > 0).astype(int)
    lga_year['any_violent_conflict'] = (lga_year['violent_events'] > 0).astype(int)
    lga_year['any_boko_haram'] = (lga_year['boko_haram_events'] > 0).astype(int)
    
    # Create conflict intensity categories
    # IMPROVED: Better handling of zero-inflation
    print("  Creating conflict intensity categories...", end=" ")
    lga_year['conflict_intensity'] = 'No Conflict'
    
    # For LGAs with any violent events, create quartiles
    has_conflict = lga_year['violent_events'] > 0
    if has_conflict.sum() > 0:
        try:
            # Create quartiles only for LGAs with conflict
            conflict_quartiles = pd.qcut(
                lga_year.loc[has_conflict, 'violent_events'],
                q=4,
                labels=False,
                duplicates='drop'
            )
            # Map numeric bins to labels
            n_bins = conflict_quartiles.max() + 1
            if n_bins == 4:
                label_map = {0: 'Low', 1: 'Medium', 2: 'High', 3: 'Very High'}
            elif n_bins == 3:
                label_map = {0: 'Low', 1: 'Medium', 2: 'High'}
            elif n_bins == 2:
                label_map = {0: 'Low', 1: 'High'}
            else:
                label_map = {i: f'Level {i+1}' for i in range(int(n_bins))}
            
            lga_year.loc[has_conflict, 'conflict_intensity'] = conflict_quartiles.map(label_map)
            print("✓")
        except ValueError as e:
            # If quartiles can't be created (e.g., too few unique values)
            print(f"  Using terciles instead")
            conflict_terciles = pd.qcut(
                lga_year.loc[has_conflict, 'violent_events'],
                q=3,
                labels=False,
                duplicates='drop'
            )
            # Map numeric bins to labels
            n_bins = conflict_terciles.max() + 1
            if n_bins == 3:
                label_map = {0: 'Low', 1: 'Medium', 2: 'High'}
            elif n_bins == 2:
                label_map = {0: 'Low', 1: 'High'}
            else:
                label_map = {i: f'Level {i+1}' for i in range(int(n_bins))}
            
            lga_year.loc[has_conflict, 'conflict_intensity'] = conflict_terciles.map(label_map)
    else:
        print("  No violent conflict found")
    
    # Create treatment indicators
    lga_year['high_conflict'] = (
        lga_year['conflict_intensity'].isin(['Very High', 'High'])
    ).astype(int)
    
    print(f"\n  LGA-Year Summary:")
    print(f"    Total observations: {len(lga_year):,}")
    print(f"    Unique LGAs: {lga_year['lga'].nunique():,}")
    print(f"    Unique states: {lga_year['state'].nunique():,}")
    print(f"    Years covered: {lga_year['year'].min()}-{lga_year['year'].max()}")
    print(f"    LGA-years with any conflict: {lga_year['any_conflict'].sum():,} ({lga_year['any_conflict'].mean()*100:.1f}%)")
    print(f"    LGA-years with violent conflict: {lga_year['any_violent_conflict'].sum():,} ({lga_year['any_violent_conflict'].mean()*100:.1f}%)")
    
    # Show conflict intensity distribution
    print(f"\n  Conflict Intensity Distribution:")
    intensity_counts = lga_year['conflict_intensity'].value_counts().sort_index()
    for intensity, count in intensity_counts.items():
        pct = (count / len(lga_year)) * 100
        print(f"    {intensity}: {count:,} ({pct:.1f}%)")
    
    return lga_year

# ============================================================================
# STEP 4: CREATE CUMULATIVE EXPOSURE MEASURES
# ============================================================================

def create_cumulative_exposure(lga_year):
    """
    Create cumulative conflict exposure measures
    
    Parameters:
    -----------
    lga_year : pd.DataFrame
        LGA-year level data
    
    Returns:
    --------
    pd.DataFrame
        Data with cumulative exposure measures
    """
    
    print("\nCreating cumulative exposure measures...")
    
    # Sort data
    lga_year = lga_year.sort_values(['state', 'lga', 'year'])
    
    # Calculate cumulative measures by LGA
    print("  Computing cumulative statistics...", end=" ")
    lga_year['cum_violent_events'] = lga_year.groupby(['state', 'lga'])['violent_events'].cumsum()
    lga_year['cum_fatalities'] = lga_year.groupby(['state', 'lga'])['total_fatalities'].cumsum()
    lga_year['cum_boko_haram_events'] = lga_year.groupby(['state', 'lga'])['boko_haram_events'].cumsum()
    print("✓")
    
    # Years since first violent event
    print("  Calculating conflict duration measures...", end=" ")
    lga_year['first_violent_year'] = lga_year[lga_year['violent_events'] > 0].groupby(
        ['state', 'lga']
    )['year'].transform('min')
    lga_year['years_since_first_conflict'] = lga_year['year'] - lga_year['first_violent_year']
    lga_year['years_since_first_conflict'] = lga_year['years_since_first_conflict'].clip(lower=0)
    print("✓")
    
    # Ever exposed indicator (useful for treatment definition)
    lga_year['ever_exposed'] = (lga_year['cum_violent_events'] > 0).astype(int)
    
    print(f"\n  Cumulative Exposure Summary:")
    print(f"    LGAs ever exposed to violent conflict: {lga_year.groupby(['state', 'lga'])['ever_exposed'].max().sum():,}")
    print(f"    Max cumulative violent events (single LGA): {lga_year['cum_violent_events'].max():,.0f}")
    print(f"    Max cumulative fatalities (single LGA): {lga_year['cum_fatalities'].max():,.0f}")
    
    return lga_year

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function
    """
    
    print("=" * 70)
    print("ACLED DATA PROCESSING FOR NIGERIA CONFLICT ANALYSIS")
    print("=" * 70)
    print(f"Processing years {START_YEAR}-{END_YEAR}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Define output paths
    ACLED_RAW = os.path.join(OUTPUT_DIR, "acled_nigeria_raw.csv")
    ACLED_CLEAN = os.path.join(OUTPUT_DIR, "acled_nigeria_clean.csv")
    ACLED_LGA_YEAR = os.path.join(OUTPUT_DIR, "acled_lga_year.csv")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Check if raw data directory exists
    if not os.path.exists(RAW_DATA_DIR):
        raise FileNotFoundError(
            f"Raw data directory not found: {RAW_DATA_DIR}\n"
            f"Please create the directory and add your ACLED CSV files."
        )
    
    try:
        # Load local data files
        df_raw = load_acled_data(
            raw_data_dir=RAW_DATA_DIR,
            start_year=START_YEAR,
            end_year=END_YEAR
        )
        
        # Save combined raw data
        print(f"\nSaving combined raw data...", end=" ")
        df_raw.to_csv(ACLED_RAW, index=False)
        print(f"✓\n  Location: {ACLED_RAW}")
        
        # Clean data
        df_clean = clean_acled_data(df_raw)
        print(f"\nSaving clean data...", end=" ")
        df_clean.to_csv(ACLED_CLEAN, index=False)
        print(f"✓\n  Location: {ACLED_CLEAN}")
        
        # Aggregate to LGA-year
        lga_year = aggregate_to_lga_year(df_clean)
        
        # Add cumulative measures
        lga_year = create_cumulative_exposure(lga_year)
        
        # Save LGA-year data
        print(f"\nSaving LGA-year aggregated data...", end=" ")
        lga_year.to_csv(ACLED_LGA_YEAR, index=False)
        print(f"✓\n  Location: {ACLED_LGA_YEAR}")
        
        print("\n" + "=" * 70)
        print("ACLED DATA PROCESSING COMPLETE!")
        print("=" * 70)
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nOutput files created:")
        print(f"  1. {ACLED_RAW}")
        print(f"  2. {ACLED_CLEAN}")
        print(f"  3. {ACLED_LGA_YEAR}")
        print("\nNext steps:")
        print("  - Review the conflict intensity distribution")
        print("  - Check for any data quality warnings above")
        print("  - Proceed with merging to DHS or other survey data")
        print("=" * 70)
        
        return lga_year
        
    except Exception as e:
        print(f"\n{'=' * 70}")
        print("ERROR IN PROCESSING")
        print(f"{'=' * 70}")
        raise

if __name__ == "__main__":
    try:
        lga_year = main()
    except FileNotFoundError as e:
        print(f"\n✗ File Error: {str(e)}")
        print(f"\nExpected location: {RAW_DATA_DIR}")
        print(f"Expected files: acled_nga_{START_YEAR}.csv through acled_nga_{END_YEAR}.csv")
    except Exception as e:
        print(f"\n✗ Error in ACLED processing: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
