#!/usr/bin/env python3
"""
Compute county_scores.json from all preprocessed datasets.

Run AFTER all preprocess_*.py scripts have been run.
This joins climate, water, population, and eGRID data by county FIPS
and computes the 5-component sustainability score for each county.
The output is used to render the heatmap on the map.

USAGE:
  python3 scripts/compute_scores.py
"""

import json, os, math

DATA = 'data'

def clamp(v, mn, mx): return max(mn, min(mx, v))
def norm(v, mn, mx):  return clamp((v - mn) / (mx - mn), 0, 1)

# Map state abbr → eGRID subregion code
STATE_TO_EGRID = {
    'WA':'NWPP','OR':'NWPP','ID':'NWPP','MT':'NWPP',
    'CA':'CAMX','TX':'ERCT','FL':'FRCC',
    'AL':'SRSO','GA':'SRSO',
    'TN':'SRTV',
    'VA':'SRVC','NC':'SRVC','SC':'SRVC',
    'IL':'SRMW',
    'MO':'SPNO','KS':'SPNO',
    'OK':'SPSO','AR':'SPSO',
    'LA':'SRMV','MS':'SRMV',
    'MN':'MROW','ND':'MROW','SD':'MROW','NE':'MROW','IA':'MROW',
    'WI':'MROE',
    'MI':'RFCM',
    'OH':'RFCW','IN':'RFCW','KY':'RFCW','WV':'RFCW',
    'CO':'RMPA','WY':'RMPA',
    'AZ':'AZNM','NM':'AZNM','NV':'AZNM','UT':'AZNM',
    'ME':'NEWE','NH':'NEWE','VT':'NEWE','MA':'NEWE','RI':'NEWE','CT':'NEWE',
    'NJ':'RFCE','PA':'RFCE','MD':'RFCE','DE':'RFCE','DC':'RFCE',
    'NY':'NYCW',
    # Upstate NY counties (FIPS prefix 36, lat > 42.5) → NYUP handled below
}

# Renewable capacity factors by state
SOLAR_CF = {'WA':0.18,'OR':0.19,'CA':0.28,'AZ':0.30,'NV':0.30,'NM':0.28,'TX':0.24,'FL':0.22,
            'NY':0.16,'MA':0.16,'CT':0.15,'GA':0.20,'AL':0.20,'SC':0.21,'NC':0.20,'VA':0.18,
            'MD':0.17,'PA':0.16,'OH':0.15,'MI':0.15,'IN':0.16,'IL':0.16,'MN':0.17,'WI':0.16,
            'IA':0.17,'MO':0.17,'KS':0.20,'NE':0.19,'OK':0.21,'CO':0.23,'UT':0.26,'MT':0.19,
            'ID':0.18,'WY':0.20,'ND':0.17,'SD':0.18,'TN':0.19,'KY':0.17,'LA':0.22,'MS':0.21,
            'AR':0.20,'ME':0.16,'NH':0.16,'VT':0.15,'RI':0.16,'WV':0.15,'DE':0.16,'NJ':0.16,'DC':0.14}
WIND_CF  = {'WA':0.25,'OR':0.27,'CA':0.15,'AZ':0.13,'NV':0.14,'NM':0.20,'TX':0.33,'FL':0.12,
            'NY':0.20,'MA':0.18,'CT':0.16,'GA':0.12,'AL':0.12,'SC':0.12,'NC':0.16,'VA':0.14,
            'MD':0.16,'PA':0.18,'OH':0.18,'MI':0.22,'IN':0.22,'IL':0.24,'MN':0.30,'WI':0.24,
            'IA':0.38,'MO':0.24,'KS':0.36,'NE':0.34,'OK':0.35,'CO':0.25,'UT':0.18,'MT':0.25,
            'ID':0.20,'WY':0.30,'ND':0.35,'SD':0.33,'TN':0.12,'KY':0.14,'LA':0.15,'MS':0.14,
            'AR':0.18,'ME':0.27,'NH':0.20,'VT':0.24,'RI':0.22,'WV':0.18,'DE':0.16,'NJ':0.18,'DC':0.10}

def load_json(path, fallback=None):
    if not os.path.exists(path):
        print(f"  WARNING: {path} not found — using fallback")
        return fallback or {}
    with open(path) as f:
        return json.load(f)

def main():
    print("Computing county scores...")

    # Load all datasets
    egrid_data = load_json(f'{DATA}/egrid_subregions.json', {'subregions':[]})
    climate_d  = load_json(f'{DATA}/climate_by_county.json',  {'counties':{}})
    water_d    = load_json(f'{DATA}/water_stress_by_county.json', {'counties':{}})
    pop_d      = load_json(f'{DATA}/population_by_county.json',   {'counties':{}})

    # Build eGRID lookup: code → co2_lbs_per_mwh
    egrid_co2 = {s['code']: s['co2_lbs_per_mwh'] for s in egrid_data.get('subregions', [])}
    print(f"  eGRID subregions loaded: {len(egrid_co2)}")

    # Normalize county data to dict format
    def to_dict(data_obj, key='counties'):
        val = data_obj.get(key, {})
        if isinstance(val, list):
            return {item['fips']: item for item in val if 'fips' in item}
        return val

    climate = to_dict(climate_d)
    water   = to_dict(water_d)
    pop     = to_dict(pop_d)

    # Union of all known FIPS
    all_fips = set(climate.keys()) | set(water.keys()) | set(pop.keys())
    print(f"  Counties to score: {len(all_fips)}")

    county_scores = []
    for fips in sorted(all_fips):
        clim = climate.get(fips, {})
        wat  = water.get(fips, {})
        pu   = pop.get(fips, {})

        avg_temp_f   = clim.get('avg_temp_f', 55)
        hdd          = clim.get('hdd', 4000)
        cdd          = clim.get('cdd', 2000)
        avg_humidity = clim.get('avg_humidity', 60)
        bws_raw      = wat.get('bws_raw', 2.0)
        bws_label    = wat.get('label', 'Medium')
        housing_units = pu.get('housing_units', 50000)
        density      = pu.get('density_per_sqmi', 300)
        pop_count    = pu.get('pop', 100000)
        lat          = pu.get('lat') or clim.get('lat') or wat.get('lat')
        lng          = pu.get('lng') or clim.get('lng') or wat.get('lng')
        county_name  = pu.get('county_name','') or wat.get('county','') or fips
        state        = pu.get('state','') or wat.get('state','') or fips[:2]

        if not lat or not lng:
            continue  # Can't plot without coordinates

        # Determine eGRID region and CO2 rate
        egrid_code = STATE_TO_EGRID.get(state, 'RFCE')
        # Upstate NY special case
        if state == 'NY' and lat and lat > 42.5:
            egrid_code = 'NYUP'
        co2 = egrid_co2.get(egrid_code, 850)

        solar = SOLAR_CF.get(state, 0.18)
        wind  = WIND_CF.get(state, 0.18)

        # Scoring (PRD formulas)
        grid      = (1 - norm(co2, 400, 1450)) * 100
        water_s   = (1 - norm(bws_raw, 0, 5)) * 100
        climate_s = norm(clamp(95 - avg_temp_f, 0, 65), 0, 65) * 50 \
                  + norm(clamp(90 - avg_humidity, 0, 70), 0, 70) * 50
        renewable = norm(solar + wind, 0.15, 0.60) * 100
        heat_d    = norm(hdd * housing_units / 1_000_000, 0.5, 18) * 100

        total = 0.25*grid + 0.25*water_s + 0.20*climate_s + 0.10*renewable + 0.20*heat_d

        county_scores.append({
            'fips':  fips,
            'county': county_name,
            'state':  state,
            'lat':    round(lat, 5),
            'lng':    round(lng, 5),
            # Scores
            'total':     round(total, 1),
            'grid':      round(grid, 1),
            'water':     round(water_s, 1),
            'climate':   round(climate_s, 1),
            'renewable': round(renewable, 1),
            'heat':      round(heat_d, 1),
            # Raw detail fields (used in score card)
            'co2_lbs_per_mwh': co2,
            'egrid':           egrid_code,
            'bws_raw':         round(bws_raw, 3),
            'bws_label':       bws_label,
            'avg_temp_f':      round(avg_temp_f, 1),
            'hdd':             round(hdd),
            'cdd':             round(cdd),
            'avg_humidity':    round(avg_humidity),
            'solar_cf':        solar,
            'wind_cf':         wind,
            'housing_units':   housing_units,
            'density_per_sqmi': density,
            'pop':             pop_count,
        })

    # Sort by total score descending
    county_scores.sort(key=lambda x: x['total'], reverse=True)

    out_path = f'{DATA}/county_scores.json'
    with open(out_path, 'w') as f:
        json.dump({'counties': county_scores}, f, separators=(',',':'))

    scores = [c['total'] for c in county_scores]
    print(f"✅ Wrote {len(county_scores)} county scores → {out_path}")
    print(f"   Score range: {min(scores):.1f} – {max(scores):.1f}, mean: {sum(scores)/len(scores):.1f}")
    print(f"   Top 5: {[(c['county']+', '+c['state'], round(c['total'])) for c in county_scores[:5]]}")

if __name__ == '__main__':
    main()
