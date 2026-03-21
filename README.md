# HeatGrid

**A two-sided web platform for data center sustainability siting and waste heat monetization.**

HeatGrid helps city planners, data center developers, and community organizations:
- **Side A** — Score any US location for sustainable data center siting (grid carbon, water stress, climate, renewables, local heat demand)
- **Side B** — Discover nearby schools, greenhouses, and pools that can buy the DC's waste heat, with full ROI analysis

The two sides are interlocked: more heat buyers nearby → higher heat demand score → better overall siting score.

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/Orenpip/TheHeatMarket.git
cd TheHeatMarket

# 2. Serve locally (required — fetch() doesn't work over file://)
python3 -m http.server 8000

# 3. Open in browser
open http://localhost:8000
```

> **No build step. No dependencies to install.** The app runs entirely in the browser via CDN scripts.

---

## Data Pipeline

The `data/` folder ships with **synthetic but geographically realistic** placeholder data. To run with **real datasets**, place raw files in `scripts/raw/` and run the preprocessing pipeline:

```bash
mkdir -p scripts/raw

# Place your downloaded files:
#   scripts/raw/nces_schools.csv          ← NCES CCD School Locations
#   scripts/raw/eGRID2023_data.xlsx       ← EPA eGRID 2023
#   scripts/raw/aqueduct_county.csv       ← WRI Aqueduct 4.0
#   scripts/raw/noaa_normals.csv          ← NOAA Climate Normals
#   scripts/raw/census_counties.csv       ← US Census county population
#   scripts/raw/dc_atlas.csv             ← IM3/PNNL Data Center Atlas
#   scripts/raw/osm_greenhouses.geojson  ← OpenStreetMap greenhouses
#   scripts/raw/osm_pools.geojson        ← OpenStreetMap public pools

# Run all preprocessing (skips any missing files)
python3 scripts/preprocess_all.py --skip-missing
```

### Data Sources

| Dataset | Source | URL |
|---|---|---|
| Grid Carbon (eGRID 2023) | EPA | https://www.epa.gov/egrid/download-data |
| Water Stress | WRI Aqueduct 4.0 | https://www.wri.org/aqueduct |
| Climate (HDD/CDD) | NOAA Normals 1991–2020 | https://www.ncei.noaa.gov/products/land-based-station/us-climate-normals |
| County Population | US Census ACS | https://www.census.gov/data/ |
| School Locations | NCES CCD | https://nces.ed.gov/ccd/schoolsearch/ |
| Data Center Atlas | DOE/PNNL IM3 | https://www.osti.gov/biblio/1773498 |
| Greenhouses / Pools | OpenStreetMap | https://overpass-turbo.eu/ |

### Individual Scripts

```bash
python3 scripts/preprocess_nces.py   --input scripts/raw/nces_schools.csv
python3 scripts/preprocess_egrid.py  --input scripts/raw/eGRID2023_data.xlsx
python3 scripts/preprocess_water.py  --input scripts/raw/aqueduct_county.csv
python3 scripts/preprocess_osm.py    --type greenhouse --input scripts/raw/osm_greenhouses.geojson
python3 scripts/preprocess_osm.py    --type pool       --input scripts/raw/osm_pools.geojson
python3 scripts/compute_scores.py    # joins all datasets → county_scores.json
```

---

## Scoring Formula

```
SUSTAINABILITY_SCORE =
    0.25 × grid_carbon_score     (lower CO₂/MWh → higher score)
  + 0.25 × water_stress_score    (lower water stress → higher score)
  + 0.20 × climate_score         (cooler + drier → lower cooling load)
  + 0.10 × renewable_score       (higher solar+wind CF → higher score)
  + 0.20 × heat_demand_score     (more HDD × housing density → higher score)
                                  ↑ boosted by actual heat buyer discovery (Side B interlock)
```

All components normalized to 0–100. CO₂ values from **EPA eGRID 2023** (real data).

---

## Heat Economics

```
DC heat available = capacity_MW × 8,760 hrs × 80% recovery rate
Pipe loss        = 1.5% per km
Buyer savings    = deliverable_MWh × ($48.15 gas − $20 DC heat − pump_cost) / MWh
Pump cost        = needed if buyer_temp > DC_output_temp (45°C air / 55°C liquid)
                   pump cost = $0.12/kWh ÷ COP 3.5 × 1000 = $34.3/MWh
Infrastructure   = pipe_distance × $1,000/m + $50K heat exchanger + $200K pump (if needed)
Payback          = infrastructure_cost / annual_savings
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Map | MapLibre GL JS 4.7 (free, no token) + OpenFreeMap tiles |
| Framework | React 18 (UMD via CDN) + Babel standalone |
| Styling | Tailwind CSS (CDN) + custom CSS |
| Typography | Fraunces (serif) + Space Mono (mono) via Google Fonts |
| Data | Static JSON files, all scoring client-side |
| Backend | **None** — single HTML file |

---

## File Structure

```
TheHeatMarket/
├── index.html                    ← Main app (open this)
├── data/
│   ├── egrid_subregions.json     ← EPA eGRID 2023 CO₂ rates (real values)
│   ├── county_scores.json        ← Pre-computed heatmap scores per county
│   ├── schools.json              ← School buyer locations
│   ├── greenhouses.json          ← Greenhouse buyer locations
│   ├── pools.json                ← Public pool buyer locations
│   ├── existing_dcs.json         ← Existing data center locations
│   ├── climate_by_county.json    ← HDD, CDD, temp, humidity by county
│   ├── water_stress_by_county.json ← WRI Aqueduct water stress by county
│   └── population_by_county.json ← Census population + housing units
├── scripts/
│   ├── preprocess_all.py         ← Master pipeline runner
│   ├── preprocess_nces.py        ← NCES schools → schools.json
│   ├── preprocess_egrid.py       ← EPA eGRID → egrid_subregions.json
│   ├── preprocess_water.py       ← WRI Aqueduct → water_stress.json
│   ├── preprocess_osm.py         ← OSM GeoJSON → greenhouses/pools.json
│   └── compute_scores.py         ← Joins all data → county_scores.json
└── claude-code/                  ← Claude Code configuration
```

---

## Design

Industrial-editorial aesthetic. Clean, data-dense, trustworthy.

- **Background:** `#f5f0e8` (warm off-white)
- **Side A accent:** `#1a5cff` (blue — data, trust)
- **Side B accent:** `#d4380d` (warm red-orange — heat, community)
- **Headings:** Fraunces (serif)
- **Data/labels:** Space Mono (monospace)

---

## Context

US data centers consumed **183 TWh** of electricity in 2024 (~4% of national consumption), projected to grow 133% by 2030. ~90% becomes waste heat, dumped to atmosphere.

Europe has dozens of operational data-center-to-district-heating projects. The US has approximately zero at scale.

HeatGrid is a platform to change that.
