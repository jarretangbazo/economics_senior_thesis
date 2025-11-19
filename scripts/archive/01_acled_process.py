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
import glob
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# Data paths
DATA_DIR = "/Users/jarretangbazo/economics_senior_thesis/data/"
RAW_DATA_DIR = os.path.join(DATA_DIR, "ACLED_raw_by_year")
OUTPUT_DIR = DATA_DIR

# Study parameters
START_YEAR = 1997  # Include pre-conflict period for comparison
END_YEAR = 2019
COUNTRY = "Nigeria"

# Output paths

# ============================================================================
# STEP 1: LOAD ACLED DATA
# ============================================================================

def load_acled_data(raw_data_dir, start_year, end_year):
    """
    Load downloaded ACLED data
    
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
    print(f"Source directory:  {raw_data_dir}")
    
    all_data = []
    
    for year in range(start_year, end_year + 1):
        filename = f"acled_nga_{year}.csv"
        filepath = os.path.join(raw_data_dir, filename)

        if os.path.exists(filepath):
            print(f"    Loading {filename}...")
            try:
                year_df = pd.read_csv(filepath)
                all_data.append(year_df)
                print(f"    Retrieved {len(year_df)} events")
            except Exception as e:
                print(f"    Error loading {filename}: {str(e)}")
                continue
        else:
            print(f"    Warning: {filename} not found, skipping...")

    if all_data:
        df = pd.concat(all_data, ignore_index=True)
        print(f"\nTotal events downloaded: {len(df)}")
        return df
    else:
        raise ValueError("No data was successfully loaded. Check that files exist in the specified directory.")

# ============================================================================
# STEP 2: CLEAN AND PROCESS ACLED DATA
# ============================================================================

def clean_acled_data(df):
    """
    Clean and process ACLED data
    
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
    
    # Convert date columns
    df['event_date'] = pd.to_datetime(df['event_date'])
    df['year'] = df['event_date'].dt.year
    df['month'] = df['event_date'].dt.month
    
    # Convert numeric columns
    df['fatalities'] = pd.to_numeric(df['fatalities'], errors='coerce')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    
    # Clean location names (standardize)
    df['admin1'] = df['admin1'].str.strip().str.title()  # State
    df['admin2'] = df['admin2'].str.strip().str.title()  # LGA
    df['location'] = df['location'].str.strip().str.title()
    
    # Create event type categories
    violent_events = [
        'Battles',
        'Explosions/Remote violence',
        'Violence against civilians'
    ]
    
    df['is_violent'] = df['event_type'].isin(violent_events).astype(int)
    
    # Flag Boko Haram events (multiple possible spellings)
    boko_haram_keywords = ['boko haram', 'jama\'atu ahlis', 'iswap', 'islamic state']
    df['is_boko_haram'] = df['actor1'].str.lower().str.contains('|'.join(boko_haram_keywords), na=False) | \
                           df['actor2'].str.lower().str.contains('|'.join(boko_haram_keywords), na=False)
    df['is_boko_haram'] = df['is_boko_haram'].astype(int)
    
    # Create conflict intensity measure
    df['has_fatalities'] = (df['fatalities'] > 0).astype(int)
    
    print(f"  Total events: {len(df)}")
    print(f"  Violent events: {df['is_violent'].sum()}")
    print(f"  Boko Haram events: {df['is_boko_haram'].sum()}")
    print(f"  Total fatalities: {df['fatalities'].sum()}")
    print(f"  Date range: {df['event_date'].min()} to {df['event_date'].max()}")
    
    return df

# ============================================================================
# STEP 3: AGGREGATE TO LGA-YEAR LEVEL
# ============================================================================

def aggregate_to_lga_year(df):
    """
    Aggregate conflict events to LGA-year level
    
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
    
    # Group by state, LGA, and year
    lga_year = df.groupby(['admin1', 'admin2', 'year']).agg(
        # Event counts
        total_events=('event_id_cnty', 'count'),
        violent_events=('is_violent', 'sum'),
        boko_haram_events=('is_boko_haram', 'sum'),
        
        # Fatalities
        total_fatalities=('fatalities', 'sum'),
        violent_fatalities=('fatalities', lambda x: x[df.loc[x.index, 'is_violent'] == 1].sum()),
        boko_haram_fatalities=('fatalities', lambda x: x[df.loc[x.index, 'is_boko_haram'] == 1].sum()),
        
        # Event types
        battles=('event_type', lambda x: (x == 'Battles').sum()),
        explosions=('event_type', lambda x: (x == 'Explosions/Remote violence').sum()),
        violence_civilians=('event_type', lambda x: (x == 'Violence against civilians').sum()),
        
        # Location info (take first occurrence)
        latitude=('latitude', 'first'),
        longitude=('longitude', 'first')
    ).reset_index()
    
    # Rename columns for clarity
    lga_year.columns = ['state', 'lga', 'year', 'total_events', 'violent_events', 
                        'boko_haram_events', 'total_fatalities', 'violent_fatalities',
                        'boko_haram_fatalities', 'battles', 'explosions', 
                        'violence_civilians', 'latitude', 'longitude']
    
    # Create binary indicators for any conflict
    lga_year['any_conflict'] = (lga_year['total_events'] > 0).astype(int)
    lga_year['any_violent_conflict'] = (lga_year['violent_events'] > 0).astype(int)
    lga_year['any_boko_haram'] = (lga_year['boko_haram_events'] > 0).astype(int)
    
    # Create conflict intensity categories (quartiles of violent events)
    # Handle zero violent events separately to avoid binning issues with qcut
    lga_year['conflict_intensity'] = 'No Conflict'

    # For LGAs with any violent events, create quartiles
    nonzero_violent_events = lga_year['violent_events'] > 0
    if nonzero_violent_events.sum() > 0:
        # Create quartiles only for LGAs with conflict
        conflict_quartiles = pd.qcut(
            lga_year.loc[nonzero_violent_events, 'violent_events'],
            q=4,
            labels=['Low', 'Medium', 'High', 'Very High'],
            duplicates='drop'
        )
        lga_year.loc[nonzero_violent_events, 'conflict_intensity'] = conflict_quartiles
    
    # Create treatment indicators (high conflict = top quartile among conflict LGAs)
    lga_year['high_conflict'] = (lga_year['conflict_intensity'] == 'Very High').astype(int)
    
    print(f"  LGA-year observations: {len(lga_year)}")
    print(f"  Unique LGAs: {lga_year['lga'].nunique()}")
    print(f"  Unique states: {lga_year['state'].nunique()}")
    print(f"  Years covered: {lga_year['year'].min()}-{lga_year['year'].max()}")
    
    # Summary statistics
    print("\nConflict exposure summary:")
    print(lga_year.groupby('year')['any_violent_conflict'].sum())
    
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
    lga_year['cum_violent_events'] = lga_year.groupby(['state', 'lga'])['violent_events'].cumsum()
    lga_year['cum_fatalities'] = lga_year.groupby(['state', 'lga'])['total_fatalities'].cumsum()
    lga_year['cum_boko_haram_events'] = lga_year.groupby(['state', 'lga'])['boko_haram_events'].cumsum()
    
    # Years since first violent event
    lga_year['first_violent_year'] = lga_year[lga_year['violent_events'] > 0].groupby(['state', 'lga'])['year'].transform('min')
    lga_year['years_since_first_conflict'] = lga_year['year'] - lga_year['first_violent_year']
    lga_year['years_since_first_conflict'] = lga_year['years_since_first_conflict'].clip(lower=0)
    
    # Ever exposed indicator (useful for treatment definition)
    lga_year['ever_exposed'] = (lga_year['cum_violent_events'] > 0).astype(int)
    
    return lga_year

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function
    """
    
    print("="*70)
    print("ACLED DATA PROCESSING FOR NIGERIA CONFLICT-EDUCATION STUDY")
    print("="*70)
    
    # Define output paths
    ACLED_RAW = os.path.join(OUTPUT_DIR, "acled_nigeria_raw.csv")
    ACLED_CLEAN = os.path.join(OUTPUT_DIR, "acled_nigeria_clean.csv")
    ACLED_LGA_YEAR = os.path.join(OUTPUT_DIR, "acled_lga_year.csv")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Check if raw data directory exists
    if not os.path.exists(RAW_DATA_DIR):
        raise FileNotFoundError(f"Raw data directory not found: {RAW_DATA_DIR}")
    
    # Load local data files
    df_raw = load_acled_data(
        raw_data_dir=RAW_DATA_DIR,
        start_year=START_YEAR,
        end_year=END_YEAR
    )
        
    # Save raw data
    df_raw.to_csv(ACLED_RAW, index=False)
    print(f"\nRaw data saved to: {ACLED_RAW}")
    
    # Clean data
    df_clean = clean_acled_data(df_raw)
    df_clean.to_csv(ACLED_CLEAN, index=False)
    print(f"Clean data saved to: {ACLED_CLEAN}")
    
    # Aggregate to LGA-year
    lga_year = aggregate_to_lga_year(df_clean)
    
    # Add cumulative measures
    lga_year = create_cumulative_exposure(lga_year)
    
    # Save LGA-year data
    lga_year.to_csv(ACLED_LGA_YEAR, index=False)
    print(f"LGA-year data saved to: {ACLED_LGA_YEAR}")
    
    print("\n" + "="*70)
    print("ACLED DATA PROCESSING COMPLETE!")
    print("="*70)
    print("\nOutput files:")
    print(f"  1. {ACLED_RAW}")
    print(f"  2. {ACLED_CLEAN}")
    print(f"  3. {ACLED_LGA_YEAR}")
    
    return lga_year

def create_synthetic_acled_data():
    """
    Create synthetic ACLED data for demonstration purposes
    (Remove this when you have real API credentials)
    """
    np.random.seed(42)
    
    states = ['Borno', 'Yobe', 'Adamawa', 'Kano', 'Lagos', 'Rivers', 'Kaduna']
    lgas_per_state = 10
    
    data = []
    event_id = 1
    
    for year in range(2000, 2025):
        for state in states:
            for lga_num in range(lgas_per_state):
                lga = f"{state} LGA {lga_num+1}"
                
                # More conflict in Northeast after 2009
                if state in ['Borno', 'Yobe', 'Adamawa'] and year >= 2009:
                    n_events = np.random.poisson(10)
                else:
                    n_events = np.random.poisson(2)
                
                for _ in range(n_events):
                    event = {
                        'event_id_cnty': f'NGA{event_id}',
                        'event_date': f'{year}-{np.random.randint(1,13):02d}-{np.random.randint(1,29):02d}',
                        'year': year,
                        'event_type': np.random.choice([
                            'Battles', 'Violence against civilians', 
                            'Explosions/Remote violence', 'Protests', 'Riots'
                        ]),
                        'admin1': state,
                        'admin2': lga,
                        'location': f'{lga} Town',
                        'latitude': np.random.uniform(4, 14),
                        'longitude': np.random.uniform(3, 15),
                        'fatalities': np.random.choice([0, 0, 0, 1, 2, 3, 5, 10, 20], p=[0.3, 0.2, 0.15, 0.15, 0.1, 0.05, 0.03, 0.01, 0.01]),
                        'actor1': 'Boko Haram' if (state in ['Borno', 'Yobe'] and year >= 2009 and np.random.random() > 0.5) else 'Other Actor',
                        'actor2': 'Military Forces of Nigeria'
                    }
                    data.append(event)
                    event_id += 1
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    try:
        lga_year = main()
    except FileNotFoundError as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nPlease check that your raw data files are in the correct location:")
        print(f"  Expected location: {RAW_DATA_DIR}")
        print(f"  Expected files: acled_nga_1997.csv through acled_nga_2019.csv")
    except Exception as e:
        print(f"\n✗ Error in ACLED processing: {str(e)}")
        raise