# Critical Bug: Side-by-Side Comparison

## The Problem: Fatal Bug in Fatality Calculations

### ❌ ORIGINAL (INCORRECT) CODE

```python
def aggregate_to_lga_year(df):
    # ... other code ...
    
    lga_year = df.groupby(['admin1', 'admin2', 'year']).agg(
        # ... other aggregations ...
        
        # 🐛 BUG: These lambdas access df.loc with wrong indices
        violent_fatalities=('fatalities', lambda x: x[df.loc[x.index, 'is_violent'] == 1].sum()),
        boko_haram_fatalities=('fatalities', lambda x: x[df.loc[x.index, 'is_boko_haram'] == 1].sum()),
        
        # ... other aggregations ...
    ).reset_index()
```

**Why This Fails:**
1. `groupby()` creates groups with their own indices
2. `x.index` contains indices from the GROUPED data (e.g., [0, 1, 2, ...])
3. `df.loc[x.index, 'is_violent']` tries to find those indices in the ORIGINAL dataframe
4. But the original df has different indices (e.g., [5013031, 5013096, ...])
5. Result: KeyError or misaligned data = **WRONG FATALITY COUNTS**

---

### ✅ FIXED (CORRECT) CODE

```python
def aggregate_to_lga_year(df):
    # ... other code ...
    
    # ✅ FIX: Pre-calculate conditional fatalities BEFORE grouping
    df['violent_fatalities_calc'] = df['fatalities'] * df['is_violent']
    df['boko_haram_fatalities_calc'] = df['fatalities'] * df['is_boko_haram']
    
    lga_year = df.groupby(['admin1', 'admin2', 'year']).agg({
        # ... other aggregations ...
        
        # ✅ Now just sum the pre-calculated columns
        'violent_fatalities_calc': 'sum',
        'boko_haram_fatalities_calc': 'sum',
        
        # ... other aggregations ...
    }).reset_index()
    
    # Rename columns
    lga_year.columns = [
        # ...
        'violent_fatalities',  # ← Gets correct sum now
        'boko_haram_fatalities',  # ← Gets correct sum now
        # ...
    ]
```

**Why This Works:**
1. Calculate `fatalities * is_violent` for each row BEFORE grouping
2. Then just sum those pre-calculated values by group
3. No index confusion, no misalignment
4. Result: **CORRECT FATALITY COUNTS**

---

## Example of the Impact

### Sample Data:
```
Event | LGA    | Year | Fatalities | is_violent | is_boko_haram
1     | Borno  | 2014 | 10         | 1          | 1
2     | Borno  | 2014 | 5          | 1          | 0
3     | Borno  | 2014 | 0          | 0          | 0
4     | Yobe   | 2014 | 20         | 1          | 1
```

### Expected Results:
```
LGA   | Year | total_fatalities | violent_fatalities | boko_haram_fatalities
Borno | 2014 | 15               | 15                 | 10
Yobe  | 2014 | 20               | 20                 | 20
```

### With Original Bug:
```
LGA   | Year | total_fatalities | violent_fatalities | boko_haram_fatalities
Borno | 2014 | 15               | ??? (WRONG)        | ??? (WRONG)
Yobe  | 2014 | 20               | ??? (WRONG)        | ??? (WRONG)
```
The bug would produce KeyErrors or completely incorrect counts.

### With Fix:
```
LGA   | Year | total_fatalities | violent_fatalities | boko_haram_fatalities
Borno | 2014 | 15               | 15 ✓               | 10 ✓
Yobe  | 2014 | 20               | 20 ✓               | 20 ✓
```

---

## Impact on Your Research

If you used the original code:
- ❌ Your violent fatality statistics would be **INCORRECT**
- ❌ Your Boko Haram fatality statistics would be **INCORRECT**
- ❌ Any analysis using these variables would be **UNRELIABLE**
- ❌ Your thesis conclusions could be **WRONG**

With the fixed code:
- ✅ All fatality counts are **ACCURATE**
- ✅ Your analysis is **RELIABLE**
- ✅ Your thesis conclusions are **TRUSTWORTHY**

---

## Action Required

**IMMEDIATELY replace your script with the improved version before proceeding with any analysis.**

Your total fatality counts were likely correct, but the breakdown by violent events and Boko Haram events was wrong.
