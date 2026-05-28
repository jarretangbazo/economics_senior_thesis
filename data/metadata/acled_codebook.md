# ACLED Codebook

**Dataset**: Armed Conflict Location & Event Data (ACLED)  
**Coverage**: Nigeria, 2000–2024 (download date: [TBD])  
**ACLED Version**: [Record version when downloading]  
**Source**: https://acleddata.com  
**Last Updated**: March 2026

> This is a working codebook. Add notes, cleaning decisions, and value label discoveries as you work through the data. Bold fields are those used in this analysis.

---

## Key Variables

### Identifiers

| Variable | Type | Description | Notes |
|---|---|---|---|
| `event_id_cnty` | string | Unique event ID per country | Format: `NGR-YYYY-XXXXX` |
| `event_id_no_cnty` | integer | Numeric event ID (global) | Use `event_id_cnty` for merging |
| `data_id` | integer | Internal ACLED database ID | Not needed for analysis |

---

### Date and Time

| Variable | Type | Description | Notes |
|---|---|---|---|
| **`event_date`** | date | Full date of event | Format: YYYY-MM-DD. Extract year/month for aggregation |
| **`year`** | integer | Year of event | Use for annual aggregation |
| `time_precision` | integer | Precision of event date | 1 = exact day, 2 = week, 3 = month. Filter to precision ≤ 2 for most analyses |

---

### Event Classification

| Variable | Type | Description | Values | Notes |
|---|---|---|---|---|
| **`event_type`** | string | Broad event category | See below | Primary classification |
| **`sub_event_type`** | string | Specific event type | See below | Use for targeted subgroup analysis |
| `interaction` | integer | Actor interaction code | See codebook | Encodes which actor types interacted |
| `disorder_type` | string | Disorder category | Political Violence, Demonstrations, Strategic Developments | Added in newer ACLED versions |

**`event_type` values** (as of ACLED v6):
- `Battles` — armed engagement between organized forces
- `Explosions/Remote violence` — IEDs, airstrikes, grenades
- `Violence against civilians` — direct targeting of non-combatants
- `Riots` — collective violence by informal groups
- `Protests` — organized demonstrations (rarely include fatalities)
- `Strategic developments` — HQ establishment, looting, non-violent actions

**`sub_event_type` values** (selected, most relevant for this project):
- `Armed clash` — exchange of fire between armed groups
- `Attack` — one-sided violence or assault
- `Suicide bomb` — suicide bombing event
- `IED/landmine/UVIED` — explosive devices
- `Abduction/forced disappearance` — kidnapping
- `Sexual violence` — [note: undercounted in ACLED]

**Cleaning note**: [Add your decisions here as you work through cleaning, e.g., "Excluded Protests and Riots from conflict exposure measure on [date] — rationale: these rarely involve fatalities and are conceptually distinct from insurgency violence."]

---

### Actors

| Variable | Type | Description | Notes |
|---|---|---|---|
| **`actor1`** | string | Primary actor | Boko Haram appears as multiple labels — see standardization below |
| `assoc_actor_1` | string | Associated group of actor1 | Often faction details |
| **`actor2`** | string | Secondary actor | Military, civilians, etc. |
| `assoc_actor_2` | string | Associated group of actor2 | |
| `inter1` | integer | Actor1 type code | 1=State, 2=Rebel, 3=Political Militia, 4=Communal Militia, 5=Rioters, 6=Protesters, 7=Civilians, 8=External/Other Forces |
| `inter2` | integer | Actor2 type code | Same codes as inter1 |

**Boko Haram Actor Labels** (to standardize during cleaning):
- `Boko Haram`
- `JAS (Jama'atu Ahlis Sunna Lidda'awati wal-Jihad)` — official name
- `ISWAP (Islamic State West Africa Province)` — post-2016 faction
- `Boko Haram - Ansaru` — splinter group

**Cleaning decision**: [Document how you handle factional splits — e.g., "Created binary indicator `boko_haram_event = 1` if actor1 or actor2 contains any of the above labels. ISWAP included after 2016 factional split as it continued targeting education."]

---

### Geography

| Variable | Type | Description | Notes |
|---|---|---|---|
| **`country`** | string | Country name | Should always = "Nigeria" for this analysis |
| **`admin1`** | string | State/province | 36 states + FCT. Check for name inconsistencies |
| **`admin2`** | string | LGA (Local Government Area) | **Primary geographic unit** — used to merge with DHS |
| `admin3` | string | Town/settlement | Often blank |
| `location` | string | Named location of event | City/town/village name |
| `geo_precision` | integer | Geographic precision | 1 = exact location, 2 = town/area, 3 = admin region |
| **`latitude`** | float | Decimal latitude | Check for outliers outside Nigeria bbox |
| **`longitude`** | float | Decimal longitude | Check for outliers |

**Nigeria bounding box** (for outlier check):
- Latitude: 4.0° – 14.0°
- Longitude: 2.7° – 15.0°

**Admin2 cleaning note**: [Document LGA name discrepancies between ACLED and the LGA shapefile here as you find them, e.g., "ACLED uses 'Maiduguri' while shapefile uses 'Maiduguri/Jere Urban' — standardized to shapefile coding."]

---

### Fatalities

| Variable | Type | Description | Notes |
|---|---|---|---|
| **`fatalities`** | integer | Estimated number killed | Conservative lower bound. Treat as floor, not point estimate |

**Fatalities notes**:
- ACLED reports the most conservative available estimate from news sources
- Many events have `fatalities = 0` even when violence occurred (underreporting)
- Distribution is highly right-skewed — use log transformation: `log(1 + fatalities)` for regression
- Check: events with implausibly high fatalities (>500 in single event) — likely mass casualty events; verify with `notes` field

---

### Other Fields

| Variable | Type | Description | Notes |
|---|---|---|---|
| `source` | string | Primary news source | Useful for manual event verification |
| `source_scale` | string | Geographic scale of source | National, Regional, etc. — proxy for reporting quality |
| `notes` | string | Free-text event description | Search this for school attacks: `notes.str.contains("school|teacher|student", case=False)` |
| `timestamp` | datetime | ACLED entry timestamp | Not needed for analysis |

---

## Derived Variables (Created During Cleaning)

Document variables you construct here as you build them:

| Variable | Construction | Script |
|---|---|---|
| `boko_haram_event` | 1 if actor1 or actor2 contains Boko Haram/ISWAP label | `01_acled_clean.py` |
| `lga_year_events` | Count of events per LGA-year | `01_acled_clean.py` |
| `lga_year_fatalities` | Sum of fatalities per LGA-year | `01_acled_clean.py` |
| `lga_total_fatalities_0924` | Cumulative fatalities 2009–2024 per LGA | `01_acled_clean.py` |
| `treated_binary` | 1 if `lga_total_fatalities_0924` > sample median | `03_merge_data.py` |
| `log_fatalities_intensity` | log(1 + `lga_total_fatalities_0924`) | `03_merge_data.py` |
| [Add more as you build them] | | |

---

## Coverage Notes

- **Temporal coverage**: Nigeria events available from 1997; coverage quality improves significantly from ~2009 onward. For pre-2009 baseline conflict exposure, use ACLED but note the sparser reporting.
- **Geographic coverage**: Urban and accessible rural areas better covered than remote Northeast (Sambisa Forest area). Reporting bias is systematic toward areas with journalist/NGO presence.
- **Version updates**: ACLED revises historical events. Pin the download date and version. If you re-download later, check for changes in the 2009–2015 period specifically.
