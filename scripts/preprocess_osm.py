#!/usr/bin/env python3
"""
Preprocess OpenStreetMap GeoJSON → data/greenhouses.json or data/pools.json

HOW TO GET OSM DATA (Overpass API):
  Run these queries at https://overpass-turbo.eu/ then Export → GeoJSON

  Greenhouses (US):
    [out:json][timeout:180];
    area["ISO3166-1"="US"]->.searchArea;
    (
      way["building"="greenhouse"](area.searchArea);
      relation["building"="greenhouse"](area.searchArea);
    );
    out center tags;

  Public Swimming Pools (US):
    [out:json][timeout:180];
    area["ISO3166-1"="US"]->.searchArea;
    (
      way["leisure"="swimming_pool"]["access"!="private"](area.searchArea);
      node["leisure"="swimming_pool"]["access"!="private"](area.searchArea);
    );
    out center tags;

USAGE:
  python3 scripts/preprocess_osm.py --type greenhouse --input scripts/raw/osm_greenhouses.geojson
  python3 scripts/preprocess_osm.py --type pool       --input scripts/raw/osm_pools.geojson
"""

import json, os, sys, argparse, re

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--type',   required=True, choices=['greenhouse','pool'])
    p.add_argument('--input',  default=None)
    p.add_argument('--output', default=None)
    return p.parse_args()

# Default sqft and heat demand for each type
DEFAULTS = {
    'greenhouse': {
        'sqft':             10_000,
        'heating_kbtu_sqft': 80,       # kBtu/sqft/yr
        'required_temp_c':  40,
        'key':              'greenhouses',
    },
    'pool': {
        'annual_mwh':       350,        # indoor pool default
        'required_temp_c':  28,
        'key':              'pools',
    },
}

US_STATE_ABBRS = {
    'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA',
    'Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA',
    'Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS',
    'Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA',
    'Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT',
    'Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM',
    'New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK',
    'Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC',
    'South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT',
    'Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY',
}

def get_coord(feature):
    geom = feature.get('geometry', {})
    gt   = geom.get('type','')
    c    = geom.get('coordinates',[])
    if gt == 'Point':
        return c[1], c[0]
    if gt == 'Polygon' and c:
        pts   = c[0]
        lat   = sum(p[1] for p in pts) / len(pts)
        lng   = sum(p[0] for p in pts) / len(pts)
        return lat, lng
    if gt == 'MultiPolygon' and c:
        pts   = c[0][0]
        return sum(p[1] for p in pts)/len(pts), sum(p[0] for p in pts)/len(pts)
    # Center point from Overpass
    if 'center' in feature:
        ctr = feature['center']
        return ctr.get('lat',0), ctr.get('lon',0)
    return None, None

def extract_name(tags):
    return (tags.get('name') or tags.get('alt_name') or '').strip() or None

def extract_state(tags):
    addr_state = tags.get('addr:state','')
    if addr_state and len(addr_state) <= 2:
        return addr_state.upper()
    # Try full state name
    for full, abbr in US_STATE_ABBRS.items():
        if full.lower() in addr_state.lower():
            return abbr
    return ''

def extract_city(tags):
    return tags.get('addr:city', tags.get('addr:town', '')).strip()

def process(input_path, output_path, feature_type):
    with open(input_path) as f:
        data = json.load(f)

    # Handle both GeoJSON FeatureCollection and Overpass JSON
    features = []
    if 'features' in data:
        features = data['features']
    elif 'elements' in data:
        # Overpass JSON format
        for el in data['elements']:
            feat = {
                'geometry': {'type':'Point','coordinates':[el.get('lon',el.get('center',{}).get('lon',0)),
                                                            el.get('lat',el.get('center',{}).get('lat',0))]},
                'properties': el.get('tags',{}),
            }
            features.append(feat)

    cfg    = DEFAULTS[feature_type]
    key    = cfg['key']
    items  = []
    skipped = 0

    for i, feat in enumerate(features):
        tags = feat.get('properties') or feat.get('tags') or {}
        lat, lng = get_coord(feat)

        if not lat or not lng:
            skipped += 1; continue
        if not (-180 < lng < -60 and 18 < lat < 72):
            skipped += 1; continue  # Not US

        name   = extract_name(tags) or f'{feature_type.title()} {i+1}'
        state  = extract_state(tags)
        city   = extract_city(tags)

        if feature_type == 'greenhouse':
            # Try to get area from OSM tags
            area_tag = tags.get('area','')
            try:
                sqft = float(re.sub(r'[^\d.]','',area_tag)) * 10.764 if area_tag else cfg['sqft']
            except ValueError:
                sqft = cfg['sqft']

            demand_mwh = round(sqft * cfg['heating_kbtu_sqft'] / 3412, 1)
            items.append({
                'id':   f'g{i:05d}',
                'name': name,
                'lat':  round(lat, 6),
                'lng':  round(lng, 6),
                'city': city, 'state': state,
                'sqft': round(sqft),
                'est_annual_demand_mwh': demand_mwh,
                'required_temp_c': cfg['required_temp_c'],
                'type': 'greenhouse',
            })

        else:  # pool
            pool_type = 'outdoor'
            tags_str  = ' '.join(str(v) for v in tags.values()).lower()
            if any(w in tags_str for w in ['indoor','covered','enclosed','natatorium']):
                pool_type = 'indoor'

            demand = cfg['annual_mwh'] if pool_type == 'indoor' else 180
            items.append({
                'id':   f'p{i:05d}',
                'name': name,
                'lat':  round(lat, 6),
                'lng':  round(lng, 6),
                'city': city, 'state': state,
                'pool_type': pool_type,
                'est_annual_demand_mwh': demand,
                'required_temp_c': cfg['required_temp_c'],
                'type': 'pool',
            })

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump({key: items}, f, separators=(',',':'))

    print(f"✅ Wrote {len(items)} {feature_type}s → {output_path}")
    print(f"   Skipped {skipped} (invalid coords or non-US)")

if __name__ == '__main__':
    args = parse_args()
    inp  = args.input  or f'scripts/raw/osm_{args.type}s.geojson'
    out  = args.output or f'data/{args.type}s.json'
    process(inp, out, args.type)
