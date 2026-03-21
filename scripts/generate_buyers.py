import json
import random
import math

random.seed(42)

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def jitter(base, spread):
    return round(base + random.uniform(-spread, spread), 6)

def zpad(n, width=3):
    return str(n).zfill(width)

# ─────────────────────────────────────────────
# 1. schools.json
# ─────────────────────────────────────────────

CITY_CONFIGS = [
    ("New York City",  "NY", 40.70, -74.00, 0.30, 60),
    ("Los Angeles",    "CA", 34.05,-118.25, 0.30, 50),
    ("Chicago",        "IL", 41.85, -87.65, 0.20, 40),
    ("Houston",        "TX", 29.76, -95.37, 0.20, 30),
    ("Phoenix",        "AZ", 33.45,-112.07, 0.20, 25),
    ("Philadelphia",   "PA", 39.95, -75.17, 0.15, 20),
    ("San Antonio",    "TX", 29.43, -98.49, 0.20, 20),
    ("Dallas",         "TX", 32.78, -96.80, 0.20, 25),
    ("San Jose",       "CA", 37.34,-121.89, 0.15, 15),
    ("Austin",         "TX", 30.27, -97.74, 0.20, 20),
    ("Jacksonville",   "FL", 30.33, -81.66, 0.20, 15),
    ("Fort Worth",     "TX", 32.75, -97.33, 0.15, 15),
    ("Columbus",       "OH", 39.96, -82.99, 0.15, 15),
    ("Charlotte",      "NC", 35.23, -80.84, 0.15, 15),
    ("Indianapolis",   "IN", 39.77, -86.16, 0.15, 15),
    ("San Francisco",  "CA", 37.77,-122.42, 0.10, 15),
    ("Seattle",        "WA", 47.61,-122.33, 0.20, 20),
    ("Denver",         "CO", 39.74,-104.98, 0.15, 15),
    ("Nashville",      "TN", 36.17, -86.78, 0.15, 15),
    ("Boston",         "MA", 42.36, -71.06, 0.15, 20),
    ("Detroit",        "MI", 42.33, -83.05, 0.15, 15),
    ("Portland",       "OR", 45.52,-122.68, 0.15, 15),
    ("Atlanta",        "GA", 33.75, -84.39, 0.15, 20),
    ("Miami",          "FL", 25.77, -80.19, 0.20, 20),
]

PRESIDENTS = [
    "Jefferson","Lincoln","Washington","Roosevelt","Kennedy","Madison","Monroe",
    "Adams","Jackson","Grant","Eisenhower","Reagan","Wilson","Truman","Harrison",
    "McKinley","Garfield","Cleveland","Pierce","Polk","Tyler","Fillmore","Harding",
    "Coolidge","Hoover","Nixon","Ford","Carter","Clinton","Obama",
]
HISTORICAL = [
    "Martin Luther King Jr.","Frederick Douglass","Harriet Tubman","Benjamin Franklin",
    "Susan B. Anthony","Cesar Chavez","Thurgood Marshall","Rosa Parks","John Muir",
    "Amelia Earhart","Neil Armstrong","Helen Keller","George Washington Carver",
    "Booker T. Washington","Jane Addams","Clara Barton","Thomas Edison","Marie Curie",
]
DIRECTIONS = ["North","South","East","West","Central","Eastside","Westside","Northside","Southside"]
NEIGHBORHOODS = [
    "Riverside","Lakeside","Hillcrest","Oakwood","Maplewood","Pinecrest","Brookside",
    "Meadowbrook","Fairview","Greenfield","Sunnydale","Crestwood","Highland","Valley",
    "Creekside","Elmwood","Cedarwood","Willowbrook","Springdale","Stonegate","Parkview",
    "Ridgewood","Clearwater","Harborview","Bayview","Lakeview","Mountainview",
]
SAINTS = [
    "St. Patrick","St. Mary","St. Joseph","St. Michael","St. John","St. Peter",
    "St. Francis","St. Catherine","St. Thomas","St. Anthony","St. Elizabeth",
    "St. Anne","St. Paul","St. Luke","St. Mark","St. Matthew","St. James",
]
LEVELS = ["elementary","middle","high"]

def school_name(level):
    choice = random.randint(0, 3)
    if choice == 0:
        figure = random.choice(PRESIDENTS + HISTORICAL)
        ltype = {"elementary":"Elementary School","middle":"Middle School","high":"High School"}[level]
        return f"{figure} {ltype}"
    elif choice == 1:
        direction = random.choice(DIRECTIONS)
        ltype = {"elementary":"Elementary School","middle":"Middle School","high":"High School"}[level]
        return f"{direction} {ltype}"
    elif choice == 2:
        hood = random.choice(NEIGHBORHOODS)
        ltype = random.choice(["Academy","Preparatory School","Learning Center","Charter School"])
        return f"{hood} {ltype}"
    else:
        saint = random.choice(SAINTS)
        ltype = {"elementary":"Elementary","middle":"Middle School","high":"High School"}[level]
        return f"{saint}'s {ltype}"

def make_school(idx, city, state, lat, lng):
    level = random.choice(LEVELS)
    if level == "elementary":
        students = random.randint(200, 600)
        sqft_per = 150
    elif level == "middle":
        students = random.randint(400, 900)
        sqft_per = 160
    else:
        students = random.randint(800, 2500)
        sqft_per = 175

    est_sqft = students * sqft_per
    est_annual_heating_kbtu = round(est_sqft * 27.6)
    est_annual_heating_cost_usd = round(est_annual_heating_kbtu / 3412 * 48.15)

    return {
        "id": f"s{zpad(idx)}",
        "name": school_name(level),
        "lat": lat,
        "lng": lng,
        "students": students,
        "level": level,
        "est_sqft": est_sqft,
        "est_annual_heating_kbtu": est_annual_heating_kbtu,
        "est_annual_heating_cost_usd": est_annual_heating_cost_usd,
        "city": city,
        "state": state,
        "required_temp_c": 65,
        "type": "school",
    }

schools = []
idx = 1
for city, state, base_lat, base_lng, spread, count in CITY_CONFIGS:
    for _ in range(count):
        lat = jitter(base_lat, spread)
        lng = jitter(base_lng, spread)
        schools.append(make_school(idx, city, state, lat, lng))
        idx += 1

with open("/tmp/TheHeatMarket/data/schools.json", "w") as f:
    json.dump({"schools": schools}, f, indent=2)

print(f"schools.json: {len(schools)} entries")

# ─────────────────────────────────────────────
# 2. greenhouses.json
# ─────────────────────────────────────────────

GH_CLUSTERS = [
    ("Salinas",          "CA", [(36.5, 36.9), (-121.5, -121.8)], 15),
    ("Holland",          "MI", [(42.7, 42.9), (-86.1, -86.3)],  10),
    ("El Centro",        "CA", [(32.7, 32.9), (-115.5, -115.7)],  8),
    ("Leamington",       "OH", [(41.2, 41.5), (-84.0, -84.5)],   8),
    ("Rochester",        "NY", [(42.8, 43.2), (-77.5, -78.5)],   8),
    ("Lima",             "OH", [(40.7, 41.1), (-83.5, -84.2)],   8),
    ("Pueblo",           "CO", [(37.5, 38.3),(-104.5,-105.5)],   5),
    ("Rio Grande Valley","TX", [(26.1, 26.5), (-97.5, -98.2)],   8),
    ("Homestead",        "FL", [(25.3, 25.6), (-80.4, -80.6)],   8),
    ("Vancouver",        "WA", [(45.5, 47.0),(-122.0,-123.0)],   5),
]

GH_NAMES = [
    "Sunnyside","Green Valley","Harvest Moon","Blooming Fields","Fresh Roots",
    "Verdant Acres","Golden Sun","Pacific Bloom","Prairie Flower","Emerald Grove",
    "Crystal Spring","Morning Dew","Sunrise Farms","Redwood","Coastal","Heritage",
    "Summit","Clearwater","Frontier","Pioneer","Meadow","Alpine","Valley View",
    "Horizon","Riverside","Lakewood","Pinecrest","Canyon","Springhill","Willow Creek",
]

STATE_LOOKUP = {
    "Salinas": "CA","Holland": "MI","El Centro": "CA","Leamington": "OH",
    "Rochester": "NY","Lima": "OH","Pueblo": "CO","Rio Grande Valley": "TX",
    "Homestead": "FL","Vancouver": "WA",
}

greenhouses = []
idx = 1
used_names = set()

for city, state, (lat_range, lng_range), count in GH_CLUSTERS:
    for _ in range(count):
        lat = round(random.uniform(lat_range[0], lat_range[1]), 6)
        lng = round(random.uniform(lng_range[0], lng_range[1]), 6)
        sqft = random.randint(8000, 80000)
        est_annual_demand_mwh = round(sqft * 80 / 3412)

        base = random.choice(GH_NAMES)
        name = f"{base} Greenhouse"
        # ensure uniqueness with counter suffix
        candidate = name
        suffix = 2
        while candidate in used_names:
            candidate = f"{base} Greenhouse {suffix}"
            suffix += 1
        used_names.add(candidate)

        greenhouses.append({
            "id": f"g{zpad(idx)}",
            "name": candidate,
            "lat": lat,
            "lng": lng,
            "sqft": sqft,
            "city": city,
            "state": state,
            "est_annual_demand_mwh": est_annual_demand_mwh,
            "required_temp_c": 40,
            "type": "greenhouse",
        })
        idx += 1

with open("/tmp/TheHeatMarket/data/greenhouses.json", "w") as f:
    json.dump({"greenhouses": greenhouses}, f, indent=2)

print(f"greenhouses.json: {len(greenhouses)} entries")

# ─────────────────────────────────────────────
# 3. pools.json
# ─────────────────────────────────────────────

POOL_CITIES = [
    ("Seattle",       "WA", 47.61, -122.33, 0.10, 4),
    ("Portland",      "OR", 45.52, -122.68, 0.10, 3),
    ("San Francisco", "CA", 37.77, -122.42, 0.08, 3),
    ("Los Angeles",   "CA", 34.05, -118.25, 0.15, 5),
    ("Denver",        "CO", 39.74, -104.98, 0.10, 3),
    ("Phoenix",       "AZ", 33.45, -112.07, 0.15, 3),
    ("Dallas",        "TX", 32.78,  -96.80, 0.12, 3),
    ("Houston",       "TX", 29.76,  -95.37, 0.12, 3),
    ("Chicago",       "IL", 41.85,  -87.65, 0.12, 4),
    ("Minneapolis",   "MN", 44.98,  -93.27, 0.10, 2),
    ("Detroit",       "MI", 42.33,  -83.05, 0.10, 2),
    ("Columbus",      "OH", 39.96,  -82.99, 0.10, 2),
    ("Indianapolis",  "IN", 39.77,  -86.16, 0.10, 2),
    ("Nashville",     "TN", 36.17,  -86.78, 0.10, 2),
    ("Atlanta",       "GA", 33.75,  -84.39, 0.10, 2),
    ("Miami",         "FL", 25.77,  -80.19, 0.12, 3),
    ("Boston",        "MA", 42.36,  -71.06, 0.10, 3),
    ("New York City", "NY", 40.70,  -74.00, 0.15, 5),
    ("Philadelphia",  "PA", 39.95,  -75.17, 0.10, 2),
    ("Charlotte",     "NC", 35.23,  -80.84, 0.10, 2),
    ("Austin",        "TX", 30.27,  -97.74, 0.10, 2),
]

POOL_ADJECTIVES = [
    "Downtown","Northside","Southside","Eastside","Westside","Central","Community",
    "Heritage","Lakeside","Riverfront","Metro","Olympic","Regional","Municipal",
    "Sunrise","Sunset","Highland","Valley","Brookside","Creekside",
]
POOL_SUFFIXES = [
    "Aquatic Center","Community Pool","Recreation Center Pool",
    "Swim Center","Natatorium","Family Aquatic Center","Sports Complex Pool",
]

pools = []
idx = 1
used_pool_names = set()

for city, state, base_lat, base_lng, spread, count in POOL_CITIES:
    for _ in range(count):
        lat = jitter(base_lat, spread)
        lng = jitter(base_lng, spread)
        pool_type = random.choices(["indoor","outdoor"], weights=[0.8, 0.2])[0]
        est_annual_demand_mwh = 350 if pool_type == "indoor" else 180

        adj = random.choice(POOL_ADJECTIVES)
        suf = random.choice(POOL_SUFFIXES)
        name = f"{city} {adj} {suf}"
        candidate = name
        suffix = 2
        while candidate in used_pool_names:
            candidate = f"{name} {suffix}"
            suffix += 1
        used_pool_names.add(candidate)

        pools.append({
            "id": f"p{zpad(idx)}",
            "name": candidate,
            "lat": lat,
            "lng": lng,
            "city": city,
            "state": state,
            "pool_type": pool_type,
            "est_annual_demand_mwh": est_annual_demand_mwh,
            "required_temp_c": 28,
            "type": "pool",
        })
        idx += 1

with open("/tmp/TheHeatMarket/data/pools.json", "w") as f:
    json.dump({"pools": pools}, f, indent=2)

print(f"pools.json: {len(pools)} entries")

# ─────────────────────────────────────────────
# 4. existing_dcs.json
# ─────────────────────────────────────────────

DC_CLUSTERS = [
    # (city, state, lat_range, lng_range, count, capacity_range, operators)
    ("Ashburn",    "VA", (39.00, 39.10), (-77.40, -77.60), 12, (20, 120)),
    ("Dallas",     "TX", (32.80, 33.00), (-96.80, -97.10),  6, (15,  80)),
    ("Santa Clara","CA", (37.30, 37.40),(-121.90,-122.00),  5, (20,  90)),
    ("Chicago",    "IL", (41.80, 42.00), (-87.90, -88.10),  4, (10,  60)),
    ("Phoenix",    "AZ", (33.40, 33.60),(-111.90,-112.20),  4, (15,  70)),
    ("Atlanta",    "GA", (33.70, 33.90), (-84.30, -84.60),  3, (20,  80)),
    ("Quincy",     "WA", (47.20, 47.80),(-119.80,-122.30),  4, (30, 100)),
    ("Secaucus",   "NJ", (40.70, 40.90), (-74.00, -74.20),  4, (15,  75)),
    ("Denver",     "CO", (39.70, 39.80),(-104.90,-105.05),  2, (10,  50)),
    ("Portland",   "OR", (45.50, 45.55),(-122.60,-122.75),  2, (10,  45)),
    ("Minneapolis","MN", (44.95, 45.00), (-93.20, -93.35),  2, (10,  40)),
    ("Boston",     "MA", (42.33, 42.40), (-71.00, -71.15),  2, (15,  55)),
]

DC_OPERATORS = [
    "Equinix","Digital Realty","CyrusOne","QTS Realty","Switch","CoreSite",
    "Flexential","DataBank","Evoque","H5 Data Centers","Vantage Data Centers",
    "Iron Mountain","Aligned Energy","Stack Infrastructure","NTT Global Data Centers",
    "Cologix","Zayo","Centersquare","RagingWire","T5 Data Centers",
]

def dc_name(city, n):
    styles = [
        f"{city} Data Hub {n}",
        f"{city} Compute Center {n}",
        f"{city} Cloud Campus {n}",
        f"{city} Colocation Facility {n}",
        f"{city} Data Center {n}",
    ]
    return random.choice(styles)

data_centers = []
idx = 1
for city, state, lat_range, lng_range, count, cap_range in DC_CLUSTERS:
    city_counter = 1
    for _ in range(count):
        lat = round(random.uniform(lat_range[0], lat_range[1]), 6)
        lng = round(random.uniform(lng_range[0], lng_range[1]), 6)
        capacity = random.randint(cap_range[0], cap_range[1])
        operator = random.choice(DC_OPERATORS)

        data_centers.append({
            "id": f"dc{zpad(idx)}",
            "name": dc_name(city, city_counter),
            "lat": lat,
            "lng": lng,
            "city": city,
            "state": state,
            "est_capacity_mw": capacity,
            "operator": operator,
        })
        idx += 1
        city_counter += 1

with open("/tmp/TheHeatMarket/data/existing_dcs.json", "w") as f:
    json.dump({"data_centers": data_centers}, f, indent=2)

print(f"existing_dcs.json: {len(data_centers)} entries")

# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
print("\nAll files written to /tmp/TheHeatMarket/data/")
print(f"  schools:      {len(schools)}")
print(f"  greenhouses:  {len(greenhouses)}")
print(f"  pools:        {len(pools)}")
print(f"  data_centers: {len(data_centers)}")
