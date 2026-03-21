#!/usr/bin/env python3
"""
Master preprocessing script — runs all datasets in order.

PLACE YOUR RAW FILES IN: scripts/raw/
  nces_schools.csv          → from https://nces.ed.gov/ccd/schoolsearch/
  eGRID2023_data.xlsx       → from https://www.epa.gov/egrid/download-data
  aqueduct_country.csv      → from https://www.wri.org/aqueduct (county/state level)
  noaa_normals.csv          → from https://www.ncei.noaa.gov/products/land-based-station/us-climate-normals
  census_counties.csv       → from https://www.census.gov/data/tables/time-series/demo/popest/2020s-counties-total.html
  dc_atlas.csv              → from https://www.osti.gov/biblio/1773498 (IM3 DC Atlas)
  osm_greenhouses.geojson   → from Overpass API: building=greenhouse
  osm_pools.geojson         → from Overpass API: leisure=swimming_pool + access=public

USAGE:
  python3 scripts/preprocess_all.py [--skip-missing]

This script will process whichever files exist and skip missing ones.
"""

import os, sys, subprocess, json

RAW_DIR  = 'scripts/raw'
DATA_DIR = 'data'

STEPS = [
    {
        'name':   'eGRID Subregions',
        'raw':    f'{RAW_DIR}/eGRID2023_data.xlsx',
        'out':    f'{DATA_DIR}/egrid_subregions.json',
        'script': 'scripts/preprocess_egrid.py',
        'note':   'EPA eGRID 2023 — CO2 emission rates by subregion',
    },
    {
        'name':   'NCES Schools',
        'raw':    f'{RAW_DIR}/nces_schools.csv',
        'out':    f'{DATA_DIR}/schools.json',
        'script': 'scripts/preprocess_nces.py',
        'note':   'NCES CCD — ~100K public school locations with lat/lng',
    },
    {
        'name':   'WRI Water Stress',
        'raw':    f'{RAW_DIR}/aqueduct_county.csv',
        'out':    f'{DATA_DIR}/water_stress_by_county.json',
        'script': 'scripts/preprocess_water.py',
        'note':   'WRI Aqueduct 4.0 — baseline water stress by county FIPS',
    },
    {
        'name':   'NOAA Climate Normals',
        'raw':    f'{RAW_DIR}/noaa_normals.csv',
        'out':    f'{DATA_DIR}/climate_by_county.json',
        'script': 'scripts/preprocess_climate.py',
        'note':   'NOAA 1991-2020 normals — HDD, CDD, avg temp by county',
    },
    {
        'name':   'Census Population',
        'raw':    f'{RAW_DIR}/census_counties.csv',
        'out':    f'{DATA_DIR}/population_by_county.json',
        'script': 'scripts/preprocess_census.py',
        'note':   'US Census ACS — population, housing units, density by county FIPS',
    },
    {
        'name':   'IM3 Data Center Atlas',
        'raw':    f'{RAW_DIR}/dc_atlas.csv',
        'out':    f'{DATA_DIR}/existing_dcs.json',
        'script': 'scripts/preprocess_dcs.py',
        'note':   'DOE/PNNL IM3 Atlas — existing US data center locations',
    },
    {
        'name':   'OSM Greenhouses',
        'raw':    f'{RAW_DIR}/osm_greenhouses.geojson',
        'out':    f'{DATA_DIR}/greenhouses.json',
        'script': 'scripts/preprocess_osm.py',
        'args':   ['--type', 'greenhouse'],
        'note':   'OpenStreetMap — building=greenhouse',
    },
    {
        'name':   'OSM Public Pools',
        'raw':    f'{RAW_DIR}/osm_pools.geojson',
        'out':    f'{DATA_DIR}/pools.json',
        'script': 'scripts/preprocess_osm.py',
        'args':   ['--type', 'pool'],
        'note':   'OpenStreetMap — leisure=swimming_pool + access=public',
    },
]

# After all per-dataset processing, this script computes county_scores.json
SCORE_SCRIPT = 'scripts/compute_scores.py'


def main():
    skip_missing = '--skip-missing' in sys.argv
    os.makedirs(RAW_DIR,  exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    print("═" * 60)
    print("  HeatGrid — Data Preprocessing Pipeline")
    print("═" * 60)

    results = []
    for step in STEPS:
        name   = step['name']
        raw    = step['raw']
        out    = step['out']
        script = step['script']

        print(f"\n▶ {name}")
        print(f"  Source: {raw}")
        print(f"  Note:   {step['note']}")

        if not os.path.exists(raw):
            if skip_missing:
                print(f"  ⚠️  Raw file missing — SKIPPING (using existing {out} if present)")
                results.append((name, 'skipped'))
                continue
            else:
                print(f"  ❌ Raw file not found: {raw}")
                print(f"     Run with --skip-missing to skip missing datasets")
                results.append((name, 'missing'))
                continue

        if not os.path.exists(script):
            print(f"  ❌ Script not found: {script}")
            results.append((name, 'no-script'))
            continue

        cmd = [sys.executable, script, '--input', raw, '--output', out]
        if 'args' in step:
            cmd.extend(step['args'])

        ret = subprocess.run(cmd, capture_output=False)
        if ret.returncode == 0:
            size = os.path.getsize(out) if os.path.exists(out) else 0
            print(f"  ✅ Done ({size/1024:.0f} KB)")
            results.append((name, 'ok'))
        else:
            print(f"  ❌ Script failed (exit {ret.returncode})")
            results.append((name, 'failed'))

    # Compute combined county scores
    print(f"\n▶ County Scores (combined)")
    if os.path.exists(SCORE_SCRIPT):
        ret = subprocess.run([sys.executable, SCORE_SCRIPT], capture_output=False)
        if ret.returncode == 0:
            print(f"  ✅ Done")
        else:
            print(f"  ❌ Failed")
    else:
        print(f"  ⚠️  {SCORE_SCRIPT} not found — skipping")

    # Summary
    print("\n═" * 60)
    print("  Summary")
    print("═" * 60)
    for name, status in results:
        icon = {'ok':'✅','skipped':'⚠️ ','missing':'❌','failed':'❌','no-script':'❌'}[status]
        print(f"  {icon} {name}: {status}")

    total_size = sum(
        os.path.getsize(f'{DATA_DIR}/{f}')
        for f in os.listdir(DATA_DIR) if f.endswith('.json')
    ) if os.path.exists(DATA_DIR) else 0
    print(f"\n  Total data size: {total_size/1024:.0f} KB")
    print("\nOpen index.html via: python3 -m http.server 8000")
    print("Then visit:          http://localhost:8000")

if __name__ == '__main__':
    main()
