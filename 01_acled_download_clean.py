"""
ACLED Data Download and Cleaning for Nigeria Conflict Analysis
===============================================================
This script downloads ACLED data for Nigeria and creates conflict exposure measures
at the LGA (Local Government Area) level.

Author: Jarret Angbazo
Date: November 2025
"""

import pandas as pd
import numpy as np
import requests
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# ACLED API credentials (get yours at: https://developer.acleddata.com/)
# After registering, replace these with your actual credentials
ACLED_EMAIL = "jarretangbazo@gmail.com"
ACLED_KEY = "your_api_key_here"

# Study parameters
START_YEAR = 2000  # Include pre-conflict period for comparison
END_YEAR = 2024
COUNTRY = "Nigeria"

# Output paths
OUTPUT_DIR = "/users/jarretangbazo/economics_senior_thesis/data/"
ACLED_RAW = OUTPUT_DIR + "acled_nigeria_raw.csv"
ACLED_CLEAN = OUTPUT_DIR + "acled_nigeria_clean.csv"
ACLED_LGA_YEAR = OUTPUT_DIR + "acled_lga_year.csv"

# ============================================================================
# STEP 1: DOWNLOAD ACLED DATA
# ============================================================================

def download_acled_data(email, api_key, country, start_year, end_year):
    """
    Download ACLED data via API
    
    Parameters:
    -----------
    email : str
        Your ACLED registered email
    api_key : str
        Your ACLED API key
    country : str
        Country name
    start_year : int
        Start year for data
    end_year : int
        End year for data
    
    Returns:
    --------
    pd.DataFrame
        Raw ACLED data
    """
    
    print(f"Downloading ACLED data for {country} ({start_year}-{end_year})...")
    
    # ACLED API endpoint
    base_url = "https://api.acleddata.com/acled/read"
    
    all_data = []
    
    for year in range(start_year, end_year + 1):
        print(f"  Downloading year {year}...")
        
        params = {
            'key': api_key,
            'email': email,
            'country': country,
            'year': year,
            'limit': 0  # No limit, get all events
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if 'data' in data:
                year_df = pd.DataFrame(data['data'])
                all_data.append(year_df)
                print(f"    Retrieved {len(year_df)} events")
            else:
                print(f"    No data returned for {year}")
                
        except Exception as e:
            print(f"    Error downloading {year}: {str(e)}")
            continue
    
    if all_data:
        df = pd.concat(all_data, ignore_index=True)
        print(f"\nTotal events downloaded: {len(df)}")
        return df
    else:
        raise ValueError("No data was successfully downloaded")

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
    lga_year['conflict_intensity'] = pd.qcut(
        lga_year['violent_events'], 
        q=4, 
        labels=['None/Low', 'Medium', 'High', 'Very High'],
        duplicates='drop'
    )
    
    # Create treatment indicators (high conflict = top quartile)
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
    
    # Create output directory
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Check if credentials are set
    if ACLED_EMAIL == "your_email@example.com" or ACLED_KEY == "your_api_key_here":
        print("\n" + "!"*70)
        print("WARNING: Please set your ACLED API credentials!")
        print("1. Register at: https://developer.acleddata.com/")
        print("2. Replace ACLED_EMAIL and ACLED_KEY at the top of this script")
        print("!"*70)
        
        # For demonstration, create synthetic data
        print("\nCreating synthetic data for demonstration...")
        df_raw = create_synthetic_acled_data()
    else:
        # Download real data
        df_raw = download_acled_data(
            email=ACLED_EMAIL,
            api_key=ACLED_KEY,
            country=COUNTRY,
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
    lga_year = main()
