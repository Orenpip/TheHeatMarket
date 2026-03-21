#!/usr/bin/env python3
"""
Preprocess NCES School Locations → data/schools.json

REAL DATA SOURCE:
  https://nces.ed.gov/ccd/schoolsearch/
  Download: "Public School Characteristics" or "CCD School Locations & Geoassignments"
  File format: CSV with headers

EXPECTED INPUT FILE:
  scripts/raw/nces_schools.csv
  (or pass --input path/to/file.csv)

KEY COLUMNS NCES USES (may vary by year):
  NCESSCH   - unique school ID
  SCH_NAME  - school name
  LSTATE    - state abbreviation
  LCITY     - city
  LAT       - latitude
  LON       - longitude
  MEMBER    - total membership (students)
  LEVEL     - school level code:
              1=Primary, 2=Middle, 3=High, 4=Other/Combined
              (some years use: Elementary, Middle, High as strings)

USAGE:
  python3 scripts/preprocess_nces.py
  python3 scripts/preprocess_nces.py --input path/to/nces.csv --output data/schools.json
"""

import json
import csv
import argparse
import os
import sys

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--input',  default='scripts/raw/nces_schools.csv')
    p.add_argument('--output', default='data/schools.json')
    p.add_argument('--limit',  type=int, default=0, help='Max schools (0=all)')
    return p.parse_args()

# EIA average heating intensity: 27.6 kBtu/sqft/year for education buildings
HEATING_INTENSITY_KBTU_SQFT = 27.6

# Gas heating cost: ~$12/MMBtu at 85% boiler efficiency → $48.15/MWh
GAS_COST_PER_MWH = 48.15

# sqft per student by level
SQFT_PER_STUDENT = {
    'elementary': 150,
    'middle':     160,
    'high':       175,
    'other':      160,
}

# Required heat temp for space heating + domestic hot water
REQUIRED_TEMP_C = 65

def detect_level(level_raw):
    """Normalize NCES level codes/strings to elementary/middle/high/other."""
    if not level_raw:
        return 'other'
    s = str(level_raw).strip().lower()
    if s in ('1', 'primary', 'elementary', 'pk', 'k'):
        return 'elementary'
    if s in ('2', 'middle', 'junior', 'jh'):
        return 'middle'
    if s in ('3', 'high', 'secondary', 'senior'):
        return 'high'
    return 'other'

def detect_column(headers, candidates):
    """Find first matching column name (case-insensitive)."""
    hl = [h.strip().lower() for h in headers]
    for c in candidates:
        if c.lower() in hl:
            return headers[hl.index(c.lower())]
    return None

def process_nces(input_path, output_path, limit=0):
    if not os.path.exists(input_path):
        print(f"ERROR: Input file not found: {input_path}")
        print("Download from: https://nces.ed.gov/ccd/schoolsearch/")
        sys.exit(1)

    schools = []
    skipped = 0

    with open(input_path, encoding='utf-8-sig', errors='replace') as f:
        # Try to detect delimiter
        sample = f.read(4096)
        f.seek(0)
        delimiter = '\t' if sample.count('\t') > sample.count(',') else ','
        reader = csv.DictReader(f, delimiter=delimiter)
        headers = reader.fieldnames or []

        # Detect column names (NCES changes them across years)
        col_id   = detect_column(headers, ['NCESSCH','SCHID','NCESID','SCHOOL_ID'])
        col_name = detect_column(headers, ['SCH_NAME','SCHNAM','NAME','SCHOOL_NAME'])
        col_state= detect_column(headers, ['LSTATE','STABB','STATE','ST'])
        col_city = detect_column(headers, ['LCITY','CITY','MCITY'])
        col_lat  = detect_column(headers, ['LAT','LATITUDE','Y'])
        col_lon  = detect_column(headers, ['LON','LONGITUDE','X','LNG'])
        col_stu  = detect_column(headers, ['MEMBER','TOTAL_STUDENTS','STUDENTS','ENROLLMENT','MEMBERSCH'])
        col_lvl  = detect_column(headers, ['LEVEL','SCH_TYPE','SCHLEVEL','LEVEL_CODE'])

        print(f"Detected columns: id={col_id} name={col_name} lat={col_lat} lon={col_lon} students={col_stu} level={col_lvl}")
        missing = [c for c,v in [('lat',col_lat),('lon',col_lon),('name',col_name)] if v is None]
        if missing:
            print(f"WARNING: Could not detect columns: {missing}")
            print(f"Available headers: {headers[:20]}")

        for i, row in enumerate(reader):
            if limit and len(schools) >= limit:
                break

            try:
                lat = float(row.get(col_lat,'') or 0)
                lng = float(row.get(col_lon,'') or 0)
            except (ValueError, TypeError):
                skipped += 1
                continue

            # Filter invalid coords (must be continental US approx)
            if not (-180 < lng < -60 and 18 < lat < 72):
                skipped += 1
                continue

            name     = row.get(col_name,'').strip() or 'Unknown School'
            state    = row.get(col_state,'').strip()
            city     = row.get(col_city,'').strip()
            level    = detect_level(row.get(col_lvl,'') if col_lvl else '')
            school_id = row.get(col_id, f's{i:06d}').strip()

            try:
                students = int(float(row.get(col_stu,'') or 0))
            except (ValueError, TypeError):
                students = 300  # fallback average

            if students <= 0:
                students = 300

            sqft_per = SQFT_PER_STUDENT.get(level, 160)
            est_sqft = students * sqft_per
            heating_kbtu = est_sqft * HEATING_INTENSITY_KBTU_SQFT
            heating_mwh  = heating_kbtu / 3412
            heating_cost = round(heating_mwh * GAS_COST_PER_MWH)

            schools.append({
                'id':   school_id,
                'name': name,
                'lat':  round(lat, 6),
                'lng':  round(lng, 6),
                'city': city,
                'state': state,
                'students':   students,
                'level':      level,
                'est_sqft':   est_sqft,
                'est_annual_heating_kbtu': round(heating_kbtu),
                'est_annual_demand_mwh':   round(heating_mwh, 1),
                'est_annual_heating_cost_usd': heating_cost,
                'required_temp_c': REQUIRED_TEMP_C,
                'type': 'school',
            })

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump({'schools': schools}, f, separators=(',', ':'))

    print(f"✅ Wrote {len(schools):,} schools → {output_path}")
    print(f"   Skipped {skipped:,} rows (invalid coords or missing data)")
    if schools:
        states = len(set(s['state'] for s in schools))
        print(f"   {states} states covered")
        print(f"   Sample: {schools[0]['name']} in {schools[0]['city']}, {schools[0]['state']}")

if __name__ == '__main__':
    args = parse_args()
    process_nces(args.input, args.output, args.limit)
