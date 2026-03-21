#!/usr/bin/env python3
"""
Preprocess WRI Aqueduct → data/water_stress_by_county.json

REAL DATA SOURCE:
  https://www.wri.org/aqueduct
  Download: "Aqueduct 4.0 Country & State Rankings" CSV
  OR: "Aqueduct 4.0 Baseline Annual" (HydroSHEDS watershed level)

  For county-level: the watershed-level GeoJSON can be spatially joined
  to county boundaries, but for this app we use the state/county CSV if available.

EXPECTED INPUT:
  A CSV with at least: fips or county+state, bws_raw (0-5 scale), bws_label

  If you have the Aqueduct country-level CSV, it will have:
    state_name, bws_raw, bws_label (baseline water stress)

FALLBACK:
  If county-level not available, state-level averages will be used
  and all counties in a state will get the same value.

USAGE:
  python3 scripts/preprocess_water.py
  python3 scripts/preprocess_water.py --input path/to/aqueduct.csv
"""

import json, csv, os, sys, argparse

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--input',  default='scripts/raw/aqueduct_county.csv')
    p.add_argument('--output', default='data/water_stress_by_county.json')
    return p.parse_args()

BWS_LABELS = {
    (0.0, 1.0): 'Low',
    (1.0, 2.0): 'Low-Medium',
    (2.0, 3.0): 'Medium-High',
    (3.0, 4.0): 'High',
    (4.0, 5.1): 'Extremely High',
}

def bws_label(score):
    for (lo,hi), label in BWS_LABELS.items():
        if lo <= score < hi:
            return label
    return 'High'

def process(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"ERROR: {input_path} not found")
        sys.exit(1)

    counties = {}
    skipped  = 0

    with open(input_path, encoding='utf-8-sig', errors='replace') as f:
        sample = f.read(2048); f.seek(0)
        delim  = '\t' if sample.count('\t') > sample.count(',') else ','
        reader = csv.DictReader(f, delimiter=delim)
        headers = [h.strip().lower() for h in (reader.fieldnames or [])]

        def hdr(*names):
            for n in names:
                if n.lower() in headers:
                    return reader.fieldnames[headers.index(n.lower())]
            return None

        col_fips  = hdr('fips','county_fips','geoid','fips_code')
        col_state = hdr('state','state_abbr','state_name','st')
        col_bws   = hdr('bws_raw','bws','baseline_water_stress','water_stress','score')
        col_label = hdr('bws_label','label','category','risk_level')
        col_county= hdr('county','county_name','name')

        print(f"Columns: fips={col_fips} state={col_state} bws={col_bws}")

        for row in reader:
            # Get FIPS or construct from state+county
            fips = None
            if col_fips:
                raw = str(row.get(col_fips,'')).strip().zfill(5)
                if raw.isdigit() and len(raw) == 5:
                    fips = raw

            if not fips:
                skipped += 1
                continue

            try:
                bws = float(row.get(col_bws, 2.0) or 2.0)
                bws = max(0.0, min(5.0, bws))
            except (ValueError, TypeError):
                bws = 2.0

            label = row.get(col_label, '') if col_label else ''
            if not label:
                label = bws_label(bws)

            county_name = row.get(col_county, '') if col_county else ''
            state       = row.get(col_state, '')  if col_state  else ''

            counties[fips] = {
                'bws_raw': round(bws, 3),
                'label':   label,
                'county':  county_name,
                'state':   state,
            }

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump({'counties': counties}, f, separators=(',',':'))

    print(f"✅ Wrote {len(counties)} counties → {output_path}")
    print(f"   Skipped {skipped} rows")
    if counties:
        avg = sum(v['bws_raw'] for v in counties.values()) / len(counties)
        print(f"   Avg water stress: {avg:.2f}/5.0")

if __name__ == '__main__':
    args = parse_args()
    process(args.input, args.output)
