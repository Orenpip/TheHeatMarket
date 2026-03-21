#!/usr/bin/env python3
"""
generate_all_counties.py

Generates county_scores.json for ALL ~3,143 US counties using:
- A hardcoded canonical list of every county with its real name and FIPS code
- State-level eGRID CO2, water stress, HDD, and renewable capacity factor data
- Approximate centroids derived from state bounding boxes + realistic per-county offsets
- Power-law population distribution within each state

Output: /tmp/TheHeatMarket/data/county_scores.json
"""

import json
import math
import random
import os

random.seed(42)

# ---------------------------------------------------------------------------
# State bounding boxes: (lat_min, lat_max, lng_min, lng_max)
# ---------------------------------------------------------------------------
STATE_BBOX = {
    'AL': (30.5, 35.0, -88.4, -84.9),   # tightened: avoid Gulf offshore
    'AK': (51.0, 71.5, -169.0, -130.0),
    'AZ': (31.3, 37.0, -114.8, -109.0),
    'AR': (33.0, 36.5, -94.6, -89.6),
    'CA': (32.5, 42.0, -124.4, -114.1),
    'CO': (37.0, 41.0, -109.1, -102.0),
    'CT': (41.0, 42.1, -73.7, -71.8),
    'DE': (38.5, 39.8, -75.8, -75.0),
    'FL': (25.5, 31.0, -87.4, -80.5),   # tightened: avoid Gulf/Atlantic offshore
    'GA': (30.7, 35.0, -85.6, -81.2),   # tightened: avoid Atlantic offshore
    'HI': (18.9, 22.3, -160.2, -154.8),
    'ID': (42.0, 49.0, -117.2, -111.0),
    'IL': (37.0, 42.5, -91.5, -87.5),
    'IN': (37.8, 41.8, -88.1, -84.8),
    'IA': (40.4, 43.5, -96.6, -90.1),
    'KS': (37.0, 40.0, -102.1, -94.6),
    'KY': (36.5, 39.1, -89.6, -81.9),
    'LA': (29.5, 33.0, -94.0, -89.5),   # tightened: avoid Gulf offshore
    'ME': (43.1, 47.3, -71.1, -67.2),   # tightened: avoid Atlantic offshore
    'MD': (37.9, 39.7, -79.5, -75.0),
    'MA': (41.2, 42.9, -73.5, -69.9),
    'MI': (41.7, 47.5, -90.4, -82.4),
    'MN': (43.5, 49.4, -97.2, -89.5),
    'MS': (30.5, 35.0, -91.5, -88.2),   # tightened: avoid Gulf offshore
    'MO': (36.0, 40.6, -95.8, -89.1),
    'MT': (44.4, 49.0, -116.0, -104.0),
    'NE': (40.0, 43.0, -104.1, -95.3),
    'NV': (35.0, 42.0, -120.0, -114.0),
    'NH': (42.7, 45.3, -72.6, -70.6),
    'NJ': (38.9, 41.4, -75.6, -73.9),
    'NM': (31.3, 37.0, -109.1, -103.0),
    'NY': (40.5, 45.0, -79.8, -71.9),
    'NC': (34.0, 36.6, -84.3, -76.0),   # tightened: avoid Atlantic offshore
    'ND': (45.9, 49.0, -104.0, -96.6),
    'OH': (38.4, 42.3, -84.8, -80.5),
    'OK': (33.6, 37.0, -103.0, -94.4),
    'OR': (42.0, 46.3, -124.6, -116.5),
    'PA': (39.7, 42.3, -80.5, -74.7),
    'RI': (41.1, 42.0, -71.9, -71.1),
    'SC': (32.2, 35.2, -83.4, -79.0),   # tightened: avoid Atlantic offshore
    'SD': (42.5, 45.9, -104.1, -96.4),
    'TN': (34.9, 36.7, -90.3, -81.7),
    'TX': (26.2, 36.5, -106.4, -94.0),  # tightened: avoid Gulf offshore
    'UT': (37.0, 42.0, -114.1, -109.0),
    'VT': (42.7, 45.0, -73.4, -71.5),
    'VA': (36.6, 39.5, -83.7, -75.7),   # tightened: avoid Chesapeake/Atlantic
    'WA': (45.5, 49.0, -124.7, -116.9),
    'WV': (37.2, 40.6, -82.6, -77.7),
    'WI': (42.5, 47.1, -92.9, -86.8),
    'WY': (41.0, 45.0, -111.1, -104.1),
    'DC': (38.8, 39.0, -77.1, -76.9),
}

# ---------------------------------------------------------------------------
# State-level eGRID CO2 (lb/MWh)
# ---------------------------------------------------------------------------
STATE_CO2 = {  # Real EPA eGRID 2023 values (lb CO₂/MWh)
    'WA': 631.7, 'OR': 631.7, 'ID': 631.7, 'MT': 631.7,  # NWPP
    'CA': 428.5,  # CAMX
    'TX': 733.9,  # ERCT
    'FL': 782.3,  # FRCC
    'AL': 842.3, 'GA': 842.3,  # SRSO
    'TN': 898.1,  # SRTV
    'VA': 593.4, 'NC': 593.4, 'SC': 593.4,  # SRVC
    'IL': 1239.8,  # SRMW
    'MO': 862.0, 'KS': 862.0,  # SPNO
    'OK': 872.0, 'AR': 872.0,  # SPSO
    'LA': 739.7, 'MS': 739.7,  # SRMV
    'MN': 920.1, 'ND': 920.1, 'SD': 920.1, 'NE': 920.1, 'IA': 920.1,  # MROW
    'WI': 1397.3,  # MROE
    'MI': 970.6,   # RFCM
    'OH': 911.4, 'IN': 911.4, 'KY': 911.4, 'WV': 911.4,  # RFCW
    'CO': 1036.6, 'WY': 1036.6,  # RMPA
    'AZ': 703.7, 'NM': 703.7, 'NV': 703.7, 'UT': 703.7,  # AZNM
    'ME': 539.3, 'NH': 539.3, 'VT': 539.3, 'MA': 539.3,  # NEWE
    'RI': 539.3, 'CT': 539.3,
    'NJ': 596.9, 'PA': 596.9, 'MD': 596.9, 'DE': 596.9, 'DC': 596.9,  # RFCE
    'NY': 864.5,  # NYCW (downstate default)
    'AK': 899.6, 'HI': 1489.5,  # AKGD, HIOA
}

# ---------------------------------------------------------------------------
# WRI Aqueduct water stress (0–5) by state
# ---------------------------------------------------------------------------
STATE_BWS = {
    'AZ': 3.751, 'CA': 3.527, 'TX': 3.007, 'NV': 4.388, 'CO': 3.340,
    'WA': 0.565, 'FL': 2.668, 'NY': 0.725, 'IL': 1.814, 'VA': 2.587,
    'OR': 0.501, 'ID': 1.847, 'UT': 2.980, 'NM': 3.221, 'MT': 0.993,
    'WY': 1.854, 'ND': 0.714, 'SD': 0.536, 'NE': 2.071, 'KS': 2.614,
    'OK': 1.824, 'AR': 0.648, 'LA': 0.396, 'MS': 0.347, 'TN': 0.587,
    'KY': 0.451, 'WV': 0.283, 'OH': 0.437, 'IN': 0.523, 'MI': 0.320,
    'WI': 0.683, 'MN': 0.698, 'IA': 0.411, 'MO': 0.476, 'AL': 0.282,
    'GA': 0.447, 'SC': 0.522, 'NC': 0.671, 'PA': 0.439, 'NJ': 0.578,
    'MD': 0.539, 'DE': 0.950, 'DC': 0.236, 'MA': 0.262, 'CT': 0.295,
    'RI': 0.382, 'VT': 0.103, 'NH': 0.207, 'ME': 0.072,
    'HI': 2.180, 'AK': 0.082,
}

# ---------------------------------------------------------------------------
# NOAA HDD by state
# ---------------------------------------------------------------------------
STATE_HDD = {
    'ME': 6128, 'MN': 6444, 'ND': 6708, 'WI': 5905, 'WY': 4990,
    'MT': 5990, 'SD': 5823, 'VT': 5981, 'CO': 4990, 'NH': 5990,
    'IA': 5432, 'MI': 5108, 'NY': 4766, 'IL': 4828, 'ID': 4890,
    'WA': 3820, 'OR': 3760, 'PA': 4381, 'OH': 4241, 'IN': 4295,
    'NE': 4789, 'KS': 3940, 'MA': 4123, 'CT': 4220, 'NJ': 3830,
    'MD': 3800, 'DE': 3750, 'RI': 3990, 'MO': 3680, 'WV': 4200,
    'VA': 3342, 'KY': 3721, 'UT': 4890, 'NM': 2890, 'AZ': 1301,
    'CA': 1392, 'TX': 1238, 'FL': 620,  'LA': 1460, 'MS': 1820,
    'AL': 2192, 'GA': 2432, 'SC': 2447, 'NC': 2735, 'TN': 3096,
    'AR': 2672, 'OK': 2372, 'NV': 2890, 'DC': 3620,
    'AK': 8500, 'HI': 200,
}

# ---------------------------------------------------------------------------
# Renewable capacity factors by state
# ---------------------------------------------------------------------------
STATE_SOLAR = {
    'WA': 0.18, 'OR': 0.19, 'ID': 0.18, 'MT': 0.18,
    'CA': 0.28,
    'TX': 0.24,
    'ND': 0.19, 'SD': 0.18, 'NE': 0.19, 'KS': 0.19, 'IA': 0.19, 'OK': 0.19,
    'AZ': 0.29, 'NM': 0.29, 'NV': 0.29, 'UT': 0.29,
    'CO': 0.23, 'WY': 0.23,
    'ME': 0.16, 'NH': 0.16, 'VT': 0.16, 'MA': 0.16, 'RI': 0.16, 'CT': 0.16,
    'NY': 0.17, 'NJ': 0.17, 'PA': 0.17, 'MD': 0.17, 'DE': 0.17, 'DC': 0.17,
    'GA': 0.21, 'FL': 0.21, 'SC': 0.21, 'NC': 0.21, 'AL': 0.21, 'MS': 0.21, 'TN': 0.21,
    'OH': 0.16, 'IN': 0.16, 'MI': 0.15, 'IL': 0.16, 'WI': 0.15, 'MN': 0.16, 'MO': 0.16,
    'VA': 0.18, 'KY': 0.17, 'WV': 0.15,
    'AR': 0.20, 'LA': 0.22,
    'AK': 0.10, 'HI': 0.25,
}

STATE_WIND = {
    'WA': 0.26, 'OR': 0.26, 'ID': 0.26, 'MT': 0.26,
    'CA': 0.15,
    'TX': 0.33,
    'ND': 0.35, 'SD': 0.33, 'NE': 0.35, 'KS': 0.35, 'IA': 0.35, 'OK': 0.35,
    'AZ': 0.15, 'NM': 0.15, 'NV': 0.15, 'UT': 0.15,
    'CO': 0.26, 'WY': 0.26,
    'ME': 0.22, 'NH': 0.22, 'VT': 0.22, 'MA': 0.22, 'RI': 0.22, 'CT': 0.22,
    'NY': 0.18, 'NJ': 0.18, 'PA': 0.18, 'MD': 0.18, 'DE': 0.18, 'DC': 0.10,
    'GA': 0.12, 'FL': 0.12, 'SC': 0.12, 'NC': 0.12, 'AL': 0.12, 'MS': 0.12, 'TN': 0.12,
    'OH': 0.24, 'IN': 0.24, 'MI': 0.23, 'IL': 0.24, 'WI': 0.23, 'MN': 0.24, 'MO': 0.24,
    'VA': 0.14, 'KY': 0.14, 'WV': 0.18,
    'AR': 0.18, 'LA': 0.15,
    'AK': 0.25, 'HI': 0.20,
}

# ---------------------------------------------------------------------------
# eGRID subregion by state
# ---------------------------------------------------------------------------
STATE_TO_EGRID = {
    'WA': 'NWPP', 'OR': 'NWPP', 'ID': 'NWPP', 'MT': 'NWPP',
    'CA': 'CAMX', 'TX': 'ERCT', 'FL': 'FRCC',
    'AL': 'SRSO', 'GA': 'SRSO',
    'TN': 'SRTV',
    'VA': 'SRVC', 'NC': 'SRVC', 'SC': 'SRVC',
    'IL': 'SRMW',
    'MO': 'SPNO', 'KS': 'SPNO',
    'OK': 'SPSO', 'AR': 'SPSO',
    'LA': 'SRMV', 'MS': 'SRMV',
    'MN': 'MROW', 'ND': 'MROW', 'SD': 'MROW', 'NE': 'MROW', 'IA': 'MROW',
    'WI': 'MROE',
    'MI': 'RFCM',
    'OH': 'RFCW', 'IN': 'RFCW', 'KY': 'RFCW', 'WV': 'RFCW',
    'CO': 'RMPA', 'WY': 'RMPA',
    'AZ': 'AZNM', 'NM': 'AZNM', 'NV': 'AZNM', 'UT': 'AZNM',
    'ME': 'NEWE', 'NH': 'NEWE', 'VT': 'NEWE', 'MA': 'NEWE', 'RI': 'NEWE', 'CT': 'NEWE',
    'NJ': 'RFCE', 'PA': 'RFCE', 'MD': 'RFCE', 'DE': 'RFCE', 'DC': 'RFCE',
    'NY': 'NYCW',
    'AK': 'AKGD', 'HI': 'HIOA',
}

# ---------------------------------------------------------------------------
# State FIPS codes (2-digit prefix)
# ---------------------------------------------------------------------------
STATE_FIPS = {
    'AL': '01', 'AK': '02', 'AZ': '04', 'AR': '05', 'CA': '06',
    'CO': '08', 'CT': '09', 'DE': '10', 'DC': '11', 'FL': '12',
    'GA': '13', 'HI': '15', 'ID': '16', 'IL': '17', 'IN': '18',
    'IA': '19', 'KS': '20', 'KY': '21', 'LA': '22', 'ME': '23',
    'MD': '24', 'MA': '25', 'MI': '26', 'MN': '27', 'MS': '28',
    'MO': '29', 'MT': '30', 'NE': '31', 'NV': '32', 'NH': '33',
    'NJ': '34', 'NM': '35', 'NY': '36', 'NC': '37', 'ND': '38',
    'OH': '39', 'OK': '40', 'OR': '41', 'PA': '42', 'RI': '44',
    'SC': '45', 'SD': '46', 'TN': '47', 'TX': '48', 'UT': '49',
    'VT': '50', 'VA': '51', 'WA': '53', 'WV': '54', 'WI': '55',
    'WY': '56',
}

# ---------------------------------------------------------------------------
# Approximate state population totals (2020 Census, millions → exact)
# ---------------------------------------------------------------------------
STATE_POP = {
    'AL': 5024279, 'AK': 733391, 'AZ': 7151502, 'AR': 3011524, 'CA': 39538223,
    'CO': 5773714, 'CT': 3605944, 'DE': 989948, 'DC': 689545, 'FL': 21538187,
    'GA': 10711908, 'HI': 1455271, 'ID': 1839106, 'IL': 12812508, 'IN': 6785528,
    'IA': 3190369, 'KS': 2937880, 'KY': 4505836, 'LA': 4657757, 'ME': 1362359,
    'MD': 6177224, 'MA': 7029917, 'MI': 10077331, 'MN': 5706494, 'MS': 2961279,
    'MO': 6154913, 'MT': 1084225, 'NE': 1961504, 'NV': 3104614, 'NH': 1377529,
    'NJ': 9288994, 'NM': 2117522, 'NY': 20201249, 'NC': 10439388, 'ND': 779094,
    'OH': 11799448, 'OK': 3959353, 'OR': 4237256, 'PA': 13002700, 'RI': 1097379,
    'SC': 5118425, 'SD': 886667, 'TN': 6910840, 'TX': 29145505, 'UT': 3271616,
    'VT': 643077, 'VA': 8631393, 'WA': 7705281, 'WV': 1793716, 'WI': 5893718,
    'WY': 576851,
}

# ---------------------------------------------------------------------------
# Complete canonical US county list: (fips_suffix_3digit, county_name)
# State FIPS prefix + suffix = 5-digit county FIPS
# Source: US Census Bureau county FIPS codes
# ---------------------------------------------------------------------------
COUNTIES_BY_STATE = {
    'AL': [
        ('001','Autauga'),('003','Baldwin'),('005','Barbour'),('007','Bibb'),
        ('009','Blount'),('011','Bullock'),('013','Butler'),('015','Calhoun'),
        ('017','Chambers'),('019','Cherokee'),('021','Chilton'),('023','Choctaw'),
        ('025','Clarke'),('027','Clay'),('029','Cleburne'),('031','Coffee'),
        ('033','Colbert'),('035','Conecuh'),('037','Coosa'),('039','Covington'),
        ('041','Crenshaw'),('043','Cullman'),('045','Dale'),('047','Dallas'),
        ('049','DeKalb'),('051','Elmore'),('053','Escambia'),('055','Etowah'),
        ('057','Fayette'),('059','Franklin'),('061','Geneva'),('063','Greene'),
        ('065','Hale'),('067','Henry'),('069','Houston'),('071','Jackson'),
        ('073','Jefferson'),('075','Lamar'),('077','Lauderdale'),('079','Lawrence'),
        ('081','Lee'),('083','Limestone'),('085','Lowndes'),('087','Macon'),
        ('089','Madison'),('091','Marengo'),('093','Marion'),('095','Marshall'),
        ('097','Mobile'),('099','Monroe'),('101','Montgomery'),('103','Morgan'),
        ('105','Perry'),('107','Pickens'),('109','Pike'),('111','Randolph'),
        ('113','Russell'),('115','St. Clair'),('117','Shelby'),('119','Sumter'),
        ('121','Talladega'),('123','Tallapoosa'),('125','Tuscaloosa'),('127','Walker'),
        ('129','Washington'),('131','Wilcox'),('133','Winston'),
    ],
    'AK': [
        ('013','Aleutians East Borough'),('016','Aleutians West Census Area'),
        ('020','Anchorage'),('050','Bethel Census Area'),
        ('060','Bristol Bay Borough'),('068','Denali Borough'),
        ('070','Dillingham Census Area'),('090','Fairbanks North Star Borough'),
        ('100','Haines Borough'),('105','Hoonah-Angoon Census Area'),
        ('110','Juneau City and Borough'),('122','Kenai Peninsula Borough'),
        ('130','Ketchikan Gateway Borough'),('150','Kodiak Island Borough'),
        ('158','Kusilvak Census Area'),('164','Lake and Peninsula Borough'),
        ('170','Matanuska-Susitna Borough'),('180','Nome Census Area'),
        ('185','North Slope Borough'),('188','Northwest Arctic Borough'),
        ('195','Petersburg Borough'),('198','Prince of Wales-Hyder Census Area'),
        ('220','Sitka City and Borough'),('230','Skagway Municipality'),
        ('240','Southeast Fairbanks Census Area'),('261','Valdez-Cordova Census Area'),
        ('275','Wrangell City and Borough'),('282','Yakutat City and Borough'),
        ('290','Yukon-Koyukuk Census Area'),
    ],
    'AZ': [
        ('001','Apache'),('003','Cochise'),('005','Coconino'),('007','Gila'),
        ('009','Graham'),('011','Greenlee'),('012','La Paz'),('013','Maricopa'),
        ('015','Mohave'),('017','Navajo'),('019','Pima'),('021','Pinal'),
        ('023','Santa Cruz'),('025','Yavapai'),('027','Yuma'),
    ],
    'AR': [
        ('001','Arkansas'),('003','Ashley'),('005','Baxter'),('007','Benton'),
        ('009','Boone'),('011','Bradley'),('013','Calhoun'),('015','Carroll'),
        ('017','Chicot'),('019','Clark'),('021','Clay'),('023','Cleburne'),
        ('025','Cleveland'),('027','Columbia'),('029','Conway'),('031','Craighead'),
        ('033','Crawford'),('035','Crittenden'),('037','Cross'),('039','Dallas'),
        ('041','Desha'),('043','Drew'),('045','Faulkner'),('047','Franklin'),
        ('049','Fulton'),('051','Garland'),('053','Grant'),('055','Greene'),
        ('057','Hempstead'),('059','Hot Spring'),('061','Howard'),('063','Independence'),
        ('065','Izard'),('067','Jackson'),('069','Jefferson'),('071','Johnson'),
        ('073','Lafayette'),('075','Lawrence'),('077','Lee'),('079','Lincoln'),
        ('081','Little River'),('083','Logan'),('085','Lonoke'),('087','Madison'),
        ('089','Marion'),('091','Miller'),('093','Mississippi'),('095','Monroe'),
        ('097','Montgomery'),('099','Nevada'),('101','Newton'),('103','Ouachita'),
        ('105','Perry'),('107','Phillips'),('109','Pike'),('111','Poinsett'),
        ('113','Polk'),('115','Pope'),('117','Prairie'),('119','Pulaski'),
        ('121','Randolph'),('123','St. Francis'),('125','Saline'),('127','Scott'),
        ('129','Searcy'),('131','Sebastian'),('133','Sevier'),('135','Sharp'),
        ('137','Stone'),('139','Union'),('141','Van Buren'),('143','Washington'),
        ('145','White'),('147','Woodruff'),('149','Yell'),
    ],
    'CA': [
        ('001','Alameda'),('003','Alpine'),('005','Amador'),('007','Butte'),
        ('009','Calaveras'),('011','Colusa'),('013','Contra Costa'),('015','Del Norte'),
        ('017','El Dorado'),('019','Fresno'),('021','Glenn'),('023','Humboldt'),
        ('025','Imperial'),('027','Inyo'),('029','Kern'),('031','Kings'),
        ('033','Lake'),('035','Lassen'),('037','Los Angeles'),('039','Madera'),
        ('041','Marin'),('043','Mariposa'),('045','Mendocino'),('047','Merced'),
        ('049','Modoc'),('051','Mono'),('053','Monterey'),('055','Napa'),
        ('057','Nevada'),('059','Orange'),('061','Placer'),('063','Plumas'),
        ('065','Riverside'),('067','Sacramento'),('069','San Benito'),
        ('071','San Bernardino'),('073','San Diego'),('075','San Francisco'),
        ('077','San Joaquin'),('079','San Luis Obispo'),('081','San Mateo'),
        ('083','Santa Barbara'),('085','Santa Clara'),('087','Santa Cruz'),
        ('089','Shasta'),('091','Sierra'),('093','Siskiyou'),('095','Solano'),
        ('097','Sonoma'),('099','Stanislaus'),('101','Sutter'),('103','Tehama'),
        ('105','Trinity'),('107','Tulare'),('109','Tuolumne'),('111','Ventura'),
        ('113','Yolo'),('115','Yuba'),
    ],
    'CO': [
        ('001','Adams'),('003','Alamosa'),('005','Arapahoe'),('007','Archuleta'),
        ('009','Baca'),('011','Bent'),('013','Boulder'),('014','Broomfield'),
        ('015','Chaffee'),('017','Cheyenne'),('019','Clear Creek'),('021','Conejos'),
        ('023','Costilla'),('025','Crowley'),('027','Custer'),('029','Delta'),
        ('031','Denver'),('033','Dolores'),('035','Douglas'),('037','Eagle'),
        ('039','Elbert'),('041','El Paso'),('043','Fremont'),('045','Garfield'),
        ('047','Gilpin'),('049','Grand'),('051','Gunnison'),('053','Hinsdale'),
        ('055','Huerfano'),('057','Jackson'),('059','Jefferson'),('061','Kiowa'),
        ('063','Kit Carson'),('065','Lake'),('067','La Plata'),('069','Larimer'),
        ('071','Las Animas'),('073','Lincoln'),('075','Logan'),('077','Mesa'),
        ('079','Mineral'),('081','Moffat'),('083','Montezuma'),('085','Montrose'),
        ('087','Morgan'),('089','Otero'),('091','Ouray'),('093','Park'),
        ('095','Phillips'),('097','Pitkin'),('099','Prowers'),('101','Pueblo'),
        ('103','Rio Blanco'),('105','Rio Grande'),('107','Routt'),('109','Saguache'),
        ('111','San Juan'),('113','San Miguel'),('115','Sedgwick'),('117','Summit'),
        ('119','Teller'),('121','Washington'),('123','Weld'),('125','Yuma'),
    ],
    'CT': [
        ('001','Fairfield'),('003','Hartford'),('005','Litchfield'),('007','Middlesex'),
        ('009','New Haven'),('011','New London'),('013','Tolland'),('015','Windham'),
    ],
    'DE': [
        ('001','Kent'),('003','New Castle'),('005','Sussex'),
    ],
    'DC': [
        ('001','District of Columbia'),
    ],
    'FL': [
        ('001','Alachua'),('003','Baker'),('005','Bay'),('007','Bradford'),
        ('009','Brevard'),('011','Broward'),('013','Calhoun'),('015','Charlotte'),
        ('017','Citrus'),('019','Clay'),('021','Collier'),('023','Columbia'),
        ('027','DeSoto'),('029','Dixie'),('031','Duval'),('033','Escambia'),
        ('035','Flagler'),('037','Franklin'),('039','Gadsden'),('041','Gilchrist'),
        ('043','Glades'),('045','Gulf'),('047','Hamilton'),('049','Hardee'),
        ('051','Hendry'),('053','Hernando'),('055','Highlands'),('057','Hillsborough'),
        ('059','Holmes'),('061','Indian River'),('063','Jackson'),('065','Jefferson'),
        ('067','Lafayette'),('069','Lake'),('071','Lee'),('073','Leon'),
        ('075','Levy'),('077','Liberty'),('079','Madison'),('081','Manatee'),
        ('083','Marion'),('085','Martin'),('086','Miami-Dade'),('087','Monroe'),
        ('089','Nassau'),('091','Okaloosa'),('093','Okeechobee'),('095','Orange'),
        ('097','Osceola'),('099','Palm Beach'),('101','Pasco'),('103','Pinellas'),
        ('105','Polk'),('107','Putnam'),('109','St. Johns'),('111','St. Lucie'),
        ('113','Santa Rosa'),('115','Sarasota'),('117','Seminole'),('119','Sumter'),
        ('121','Suwannee'),('123','Taylor'),('125','Union'),('127','Volusia'),
        ('129','Wakulla'),('131','Walton'),('133','Washington'),
    ],
    'GA': [
        ('001','Appling'),('003','Atkinson'),('005','Bacon'),('007','Baker'),
        ('009','Baldwin'),('011','Banks'),('013','Barrow'),('015','Bartow'),
        ('017','Ben Hill'),('019','Berrien'),('021','Bibb'),('023','Bleckley'),
        ('025','Brantley'),('027','Brooks'),('029','Bryan'),('031','Bulloch'),
        ('033','Burke'),('035','Butts'),('037','Calhoun'),('039','Camden'),
        ('043','Candler'),('045','Carroll'),('047','Catoosa'),('049','Charlton'),
        ('051','Chatham'),('053','Chattahoochee'),('055','Chattooga'),('057','Cherokee'),
        ('059','Clarke'),('061','Clay'),('063','Clayton'),('065','Clinch'),
        ('067','Cobb'),('069','Coffee'),('071','Colquitt'),('073','Columbia'),
        ('075','Cook'),('077','Coweta'),('079','Crawford'),('081','Crisp'),
        ('083','Dade'),('085','Dawson'),('087','Decatur'),('089','DeKalb'),
        ('091','Dodge'),('093','Dooly'),('095','Dougherty'),('097','Douglas'),
        ('099','Early'),('101','Echols'),('103','Effingham'),('105','Elbert'),
        ('107','Emanuel'),('109','Evans'),('111','Fannin'),('113','Fayette'),
        ('115','Floyd'),('117','Forsyth'),('119','Franklin'),('121','Fulton'),
        ('123','Gilmer'),('125','Glascock'),('127','Glynn'),('129','Gordon'),
        ('131','Grady'),('133','Greene'),('135','Gwinnett'),('137','Habersham'),
        ('139','Hall'),('141','Hancock'),('143','Haralson'),('145','Harris'),
        ('147','Hart'),('149','Heard'),('151','Henry'),('153','Houston'),
        ('155','Irwin'),('157','Jackson'),('159','Jasper'),('161','Jeff Davis'),
        ('163','Jefferson'),('165','Jenkins'),('167','Johnson'),('169','Jones'),
        ('171','Lamar'),('173','Lanier'),('175','Laurens'),('177','Lee'),
        ('179','Liberty'),('181','Lincoln'),('183','Long'),('185','Lowndes'),
        ('187','Lumpkin'),('189','McDuffie'),('191','McIntosh'),('193','Macon'),
        ('195','Madison'),('197','Marion'),('199','Meriwether'),('201','Miller'),
        ('205','Mitchell'),('207','Monroe'),('209','Montgomery'),('211','Morgan'),
        ('213','Murray'),('215','Muscogee'),('217','Newton'),('219','Oconee'),
        ('221','Oglethorpe'),('223','Paulding'),('225','Peach'),('227','Pickens'),
        ('229','Pierce'),('231','Pike'),('233','Polk'),('235','Pulaski'),
        ('237','Putnam'),('239','Quitman'),('241','Rabun'),('243','Randolph'),
        ('245','Richmond'),('247','Rockdale'),('249','Schley'),('251','Screven'),
        ('253','Seminole'),('255','Spalding'),('257','Stephens'),('259','Stewart'),
        ('261','Sumter'),('263','Talbot'),('265','Taliaferro'),('267','Tattnall'),
        ('269','Taylor'),('271','Telfair'),('273','Terrell'),('275','Thomas'),
        ('277','Tift'),('279','Toombs'),('281','Towns'),('283','Treutlen'),
        ('285','Troup'),('287','Turner'),('289','Twiggs'),('291','Union'),
        ('293','Upson'),('295','Walker'),('297','Walton'),('299','Ware'),
        ('301','Warren'),('303','Washington'),('305','Wayne'),('307','Webster'),
        ('309','Wheeler'),('311','White'),('313','Whitfield'),('315','Wilcox'),
        ('317','Wilkes'),('319','Wilkinson'),('321','Worth'),
    ],
    'HI': [
        ('001','Hawaii'),('003','Honolulu'),('005','Kalawao'),('007','Kauai'),('009','Maui'),
    ],
    'ID': [
        ('001','Ada'),('003','Adams'),('005','Bannock'),('007','Bear Lake'),
        ('009','Benewah'),('011','Bingham'),('013','Blaine'),('015','Boise'),
        ('017','Bonner'),('019','Bonneville'),('021','Boundary'),('023','Butte'),
        ('025','Camas'),('027','Canyon'),('029','Caribou'),('031','Cassia'),
        ('033','Clark'),('035','Clearwater'),('037','Custer'),('039','Elmore'),
        ('041','Franklin'),('043','Fremont'),('045','Gem'),('047','Gooding'),
        ('049','Idaho'),('051','Jefferson'),('053','Jerome'),('055','Kootenai'),
        ('057','Latah'),('059','Lemhi'),('061','Lewis'),('063','Lincoln'),
        ('065','Madison'),('067','Minidoka'),('069','Nez Perce'),('071','Oneida'),
        ('073','Owyhee'),('075','Payette'),('077','Power'),('079','Shoshone'),
        ('081','Teton'),('083','Twin Falls'),('085','Valley'),('087','Washington'),
    ],
    'IL': [
        ('001','Adams'),('003','Alexander'),('005','Bond'),('007','Boone'),
        ('009','Brown'),('011','Bureau'),('013','Calhoun'),('015','Carroll'),
        ('017','Cass'),('019','Champaign'),('021','Christian'),('023','Clark'),
        ('025','Clay'),('027','Clinton'),('029','Coles'),('031','Cook'),
        ('033','Crawford'),('035','Cumberland'),('037','DeKalb'),('039','De Witt'),
        ('041','Douglas'),('043','DuPage'),('045','Edgar'),('047','Edwards'),
        ('049','Effingham'),('051','Fayette'),('053','Ford'),('055','Franklin'),
        ('057','Fulton'),('059','Gallatin'),('061','Greene'),('063','Grundy'),
        ('065','Hamilton'),('067','Hancock'),('069','Hardin'),('071','Henderson'),
        ('073','Henry'),('075','Iroquois'),('077','Jackson'),('079','Jasper'),
        ('081','Jefferson'),('083','Jersey'),('085','Jo Daviess'),('087','Johnson'),
        ('089','Kane'),('091','Kankakee'),('093','Kendall'),('095','Knox'),
        ('097','Lake'),('099','LaSalle'),('101','Lawrence'),('103','Lee'),
        ('105','Livingston'),('107','Logan'),('109','McDonough'),('111','McHenry'),
        ('113','McLean'),('115','Macon'),('117','Macoupin'),('119','Madison'),
        ('121','Marion'),('123','Marshall'),('125','Mason'),('127','Massac'),
        ('129','Menard'),('131','Mercer'),('133','Monroe'),('135','Montgomery'),
        ('137','Morgan'),('139','Moultrie'),('141','Ogle'),('143','Peoria'),
        ('145','Perry'),('147','Piatt'),('149','Pike'),('151','Pope'),
        ('153','Pulaski'),('155','Putnam'),('157','Randolph'),('159','Richland'),
        ('161','Rock Island'),('163','St. Clair'),('165','Saline'),('167','Sangamon'),
        ('169','Schuyler'),('171','Scott'),('173','Shelby'),('175','Stark'),
        ('177','Stephenson'),('179','Tazewell'),('181','Union'),('183','Vermilion'),
        ('185','Wabash'),('187','Warren'),('189','Washington'),('191','Wayne'),
        ('193','White'),('195','Whiteside'),('197','Will'),('199','Williamson'),
        ('201','Winnebago'),('203','Woodford'),
    ],
    'IN': [
        ('001','Adams'),('003','Allen'),('005','Bartholomew'),('007','Benton'),
        ('009','Blackford'),('011','Boone'),('013','Brown'),('015','Carroll'),
        ('017','Cass'),('019','Clark'),('021','Clay'),('023','Clinton'),
        ('025','Crawford'),('027','Daviess'),('029','Dearborn'),('031','Decatur'),
        ('033','DeKalb'),('035','Delaware'),('037','Dubois'),('039','Elkhart'),
        ('041','Fayette'),('043','Floyd'),('045','Fountain'),('047','Franklin'),
        ('049','Fulton'),('051','Gibson'),('053','Grant'),('055','Greene'),
        ('057','Hamilton'),('059','Hancock'),('061','Harrison'),('063','Hendricks'),
        ('065','Henry'),('067','Howard'),('069','Huntington'),('071','Jackson'),
        ('073','Jasper'),('075','Jay'),('077','Jefferson'),('079','Jennings'),
        ('081','Johnson'),('083','Knox'),('085','Kosciusko'),('087','LaGrange'),
        ('089','Lake'),('091','LaPorte'),('093','Lawrence'),('095','Madison'),
        ('097','Marion'),('099','Marshall'),('101','Martin'),('103','Miami'),
        ('105','Monroe'),('107','Montgomery'),('109','Morgan'),('111','Newton'),
        ('113','Noble'),('115','Ohio'),('117','Orange'),('119','Owen'),
        ('121','Parke'),('123','Perry'),('125','Pike'),('127','Porter'),
        ('129','Posey'),('131','Pulaski'),('133','Putnam'),('135','Randolph'),
        ('137','Ripley'),('139','Rush'),('141','St. Joseph'),('143','Scott'),
        ('145','Shelby'),('147','Spencer'),('149','Starke'),('151','Steuben'),
        ('153','Sullivan'),('155','Switzerland'),('157','Tippecanoe'),('159','Tipton'),
        ('161','Union'),('163','Vanderburgh'),('165','Vermillion'),('167','Vigo'),
        ('169','Wabash'),('171','Warren'),('173','Warrick'),('175','Washington'),
        ('177','Wayne'),('179','Wells'),('181','White'),('183','Whitley'),
    ],
    'IA': [
        ('001','Adair'),('003','Adams'),('005','Allamakee'),('007','Appanoose'),
        ('009','Audubon'),('011','Benton'),('013','Black Hawk'),('015','Boone'),
        ('017','Bremer'),('019','Buchanan'),('021','Buena Vista'),('023','Butler'),
        ('025','Calhoun'),('027','Carroll'),('029','Cass'),('031','Cedar'),
        ('033','Cerro Gordo'),('035','Cherokee'),('037','Chickasaw'),('039','Clarke'),
        ('041','Clay'),('043','Clayton'),('045','Clinton'),('047','Crawford'),
        ('049','Dallas'),('051','Davis'),('053','Decatur'),('055','Delaware'),
        ('057','Des Moines'),('059','Dickinson'),('061','Dubuque'),('063','Emmet'),
        ('065','Fayette'),('067','Floyd'),('069','Franklin'),('071','Fremont'),
        ('073','Greene'),('075','Grundy'),('077','Guthrie'),('079','Hamilton'),
        ('081','Hancock'),('083','Hardin'),('085','Harrison'),('087','Henry'),
        ('089','Howard'),('091','Humboldt'),('093','Ida'),('095','Iowa'),
        ('097','Jackson'),('099','Jasper'),('101','Jefferson'),('103','Johnson'),
        ('105','Jones'),('107','Keokuk'),('109','Kossuth'),('111','Lee'),
        ('113','Linn'),('115','Louisa'),('117','Lucas'),('119','Lyon'),
        ('121','Madison'),('123','Mahaska'),('125','Marion'),('127','Marshall'),
        ('129','Mills'),('131','Mitchell'),('133','Monona'),('135','Monroe'),
        ('137','Montgomery'),('139','Muscatine'),("141","O'Brien"),('143','Osceola'),
        ('145','Page'),('147','Palo Alto'),('149','Plymouth'),('151','Pocahontas'),
        ('153','Polk'),('155','Pottawattamie'),('157','Poweshiek'),('159','Ringgold'),
        ('161','Sac'),('163','Scott'),('165','Shelby'),('167','Sioux'),
        ('169','Story'),('171','Tama'),('173','Taylor'),('175','Union'),
        ('177','Van Buren'),('179','Wapello'),('181','Warren'),('183','Washington'),
        ('185','Wayne'),('187','Webster'),('189','Winnebago'),('191','Winneshiek'),
        ('193','Woodbury'),('195','Worth'),('197','Wright'),
    ],
    'KS': [
        ('001','Allen'),('003','Anderson'),('005','Atchison'),('007','Barber'),
        ('009','Barton'),('011','Bourbon'),('013','Brown'),('015','Butler'),
        ('017','Chase'),('019','Chautauqua'),('021','Cherokee'),('023','Cheyenne'),
        ('025','Clark'),('027','Clay'),('029','Cloud'),('031','Coffey'),
        ('033','Comanche'),('035','Cowley'),('037','Crawford'),('039','Decatur'),
        ('041','Dickinson'),('043','Doniphan'),('045','Douglas'),('047','Edwards'),
        ('049','Elk'),('051','Ellis'),('053','Ellsworth'),('055','Finney'),
        ('057','Ford'),('059','Franklin'),('061','Geary'),('063','Gove'),
        ('065','Graham'),('067','Grant'),('069','Gray'),('071','Greeley'),
        ('073','Greenwood'),('075','Hamilton'),('077','Harper'),('079','Harvey'),
        ('081','Haskell'),('083','Hodgeman'),('085','Jackson'),('087','Jefferson'),
        ('089','Jewell'),('091','Johnson'),('093','Kearny'),('095','Kingman'),
        ('097','Kiowa'),('099','Labette'),('101','Lane'),('103','Leavenworth'),
        ('105','Lincoln'),('107','Linn'),('109','Logan'),('111','Lyon'),
        ('113','McPherson'),('115','Marion'),('117','Marshall'),('119','Meade'),
        ('121','Miami'),('123','Mitchell'),('125','Montgomery'),('127','Morris'),
        ('129','Morton'),('131','Nemaha'),('133','Neosho'),('135','Ness'),
        ('137','Norton'),('139','Osage'),('141','Osborne'),('143','Ottawa'),
        ('145','Pawnee'),('147','Phillips'),('149','Pottawatomie'),('151','Pratt'),
        ('153','Rawlins'),('155','Reno'),('157','Republic'),('159','Rice'),
        ('161','Riley'),('163','Rooks'),('165','Rush'),('167','Russell'),
        ('169','Saline'),('171','Scott'),('173','Sedgwick'),('175','Seward'),
        ('177','Shawnee'),('179','Sheridan'),('181','Sherman'),('183','Smith'),
        ('185','Stafford'),('187','Stanton'),('189','Stevens'),('191','Sumner'),
        ('193','Thomas'),('195','Trego'),('197','Wabaunsee'),('199','Wallace'),
        ('201','Washington'),('203','Wichita'),('205','Wilson'),('207','Woodson'),
        ('209','Wyandotte'),
    ],
    'KY': [
        ('001','Adair'),('003','Allen'),('005','Anderson'),('007','Ballard'),
        ('009','Barren'),('011','Bath'),('013','Bell'),('015','Boone'),
        ('017','Bourbon'),('019','Boyd'),('021','Boyle'),('023','Bracken'),
        ('025','Breathitt'),('027','Breckinridge'),('029','Bullitt'),('031','Butler'),
        ('033','Caldwell'),('035','Calloway'),('037','Campbell'),('039','Carlisle'),
        ('041','Carroll'),('043','Carter'),('045','Casey'),('047','Christian'),
        ('049','Clark'),('051','Clay'),('053','Clinton'),('055','Crittenden'),
        ('057','Cumberland'),('059','Daviess'),('061','Edmonson'),('063','Elliott'),
        ('065','Estill'),('067','Fayette'),('069','Fleming'),('071','Floyd'),
        ('073','Franklin'),('075','Fulton'),('077','Gallatin'),('079','Garrard'),
        ('081','Grant'),('083','Graves'),('085','Grayson'),('087','Green'),
        ('089','Greenup'),('091','Hancock'),('093','Hardin'),('095','Harlan'),
        ('097','Harrison'),('099','Hart'),('101','Henderson'),('103','Henry'),
        ('105','Hickman'),('107','Hopkins'),('109','Jackson'),('111','Jefferson'),
        ('113','Jessamine'),('115','Johnson'),('117','Kenton'),('119','Knott'),
        ('121','Knox'),('123','Larue'),('125','Laurel'),('127','Lawrence'),
        ('129','Lee'),('131','Leslie'),('133','Letcher'),('135','Lewis'),
        ('137','Lincoln'),('139','Livingston'),('141','Logan'),('143','Lyon'),
        ('145','McCracken'),('147','McCreary'),('149','McLean'),('151','Madison'),
        ('153','Magoffin'),('155','Marion'),('157','Marshall'),('159','Martin'),
        ('161','Mason'),('163','Meade'),('165','Menifee'),('167','Mercer'),
        ('169','Metcalfe'),('171','Monroe'),('173','Montgomery'),('175','Morgan'),
        ('177','Muhlenberg'),('179','Nelson'),('181','Nicholas'),('183','Ohio'),
        ('185','Oldham'),('187','Owen'),('189','Owsley'),('191','Pendleton'),
        ('193','Perry'),('195','Pike'),('197','Powell'),('199','Pulaski'),
        ('201','Robertson'),('203','Rockcastle'),('205','Rowan'),('207','Russell'),
        ('209','Scott'),('211','Shelby'),('213','Simpson'),('215','Spencer'),
        ('217','Taylor'),('219','Todd'),('221','Trigg'),('223','Trimble'),
        ('225','Union'),('227','Warren'),('229','Washington'),('231','Wayne'),
        ('233','Webster'),('235','Whitley'),('237','Wolfe'),('239','Woodford'),
    ],
    'LA': [
        ('001','Acadia'),('003','Allen'),('005','Ascension'),('007','Assumption'),
        ('009','Avoyelles'),('011','Beauregard'),('013','Bienville'),('015','Bossier'),
        ('017','Caddo'),('019','Calcasieu'),('021','Caldwell'),('023','Cameron'),
        ('025','Catahoula'),('027','Claiborne'),('029','Concordia'),('031','De Soto'),
        ('033','East Baton Rouge'),('035','East Carroll'),('037','East Feliciana'),
        ('039','Evangeline'),('041','Franklin'),('043','Grant'),('045','Iberia'),
        ('047','Iberville'),('049','Jackson'),('051','Jefferson'),
        ('053','Jefferson Davis'),('055','Lafayette'),('057','Lafourche'),
        ('059','LaSalle'),('061','Lincoln'),('063','Livingston'),('065','Madison'),
        ('067','Morehouse'),('069','Natchitoches'),('071','Orleans'),('073','Ouachita'),
        ('075','Plaquemines'),('077','Pointe Coupee'),('079','Rapides'),
        ('081','Red River'),('083','Richland'),('085','Sabine'),
        ('087','St. Bernard'),('089','St. Charles'),('091','St. Helena'),
        ('093','St. James'),('095','St. John the Baptist'),('097','St. Landry'),
        ('099','St. Martin'),('101','St. Mary'),('103','St. Tammany'),
        ('105','Tangipahoa'),('107','Tensas'),('109','Terrebonne'),('111','Union'),
        ('113','Vermilion'),('115','Vernon'),('117','Washington'),('119','Webster'),
        ('121','West Baton Rouge'),('123','West Carroll'),('125','West Feliciana'),
        ('127','Winn'),
    ],
    'ME': [
        ('001','Androscoggin'),('003','Aroostook'),('005','Cumberland'),('007','Franklin'),
        ('009','Hancock'),('011','Kennebec'),('013','Knox'),('015','Lincoln'),
        ('017','Oxford'),('019','Penobscot'),('021','Piscataquis'),('023','Sagadahoc'),
        ('025','Somerset'),('027','Waldo'),('029','Washington'),('031','York'),
    ],
    'MD': [
        ('001','Allegany'),('003','Anne Arundel'),('005','Baltimore'),('009','Calvert'),
        ('011','Caroline'),('013','Carroll'),('015','Cecil'),('017','Charles'),
        ('019','Dorchester'),('021','Frederick'),('023','Garrett'),('025','Harford'),
        ('027','Howard'),('029','Kent'),('031','Montgomery'),("033","Prince George's"),
        ('035',"Queen Anne's"),('037','St. Mary\'s'),('039','Somerset'),('041','Talbot'),
        ('043','Washington'),('045','Wicomico'),('047','Worcester'),
        ('510','Baltimore City'),
    ],
    'MA': [
        ('001','Barnstable'),('003','Berkshire'),('005','Bristol'),('007','Dukes'),
        ('009','Essex'),('011','Franklin'),('013','Hampden'),('015','Hampshire'),
        ('017','Middlesex'),('019','Nantucket'),('021','Norfolk'),('023','Plymouth'),
        ('025','Suffolk'),('027','Worcester'),
    ],
    'MI': [
        ('001','Alcona'),('003','Alger'),('005','Allegan'),('007','Alpena'),
        ('009','Antrim'),('011','Arenac'),('013','Baraga'),('015','Barry'),
        ('017','Bay'),('019','Benzie'),('021','Berrien'),('023','Branch'),
        ('025','Calhoun'),('027','Cass'),('029','Charlevoix'),('031','Cheboygan'),
        ('033','Chippewa'),('035','Clare'),('037','Clinton'),('039','Crawford'),
        ('041','Delta'),('043','Dickinson'),('045','Eaton'),('047','Emmet'),
        ('049','Genesee'),('051','Gladwin'),('053','Gogebic'),('055','Grand Traverse'),
        ('057','Gratiot'),('059','Hillsdale'),('061','Houghton'),('063','Huron'),
        ('065','Ingham'),('067','Ionia'),('069','Iosco'),('071','Iron'),
        ('073','Isabella'),('075','Jackson'),('077','Kalamazoo'),('079','Kalkaska'),
        ('081','Kent'),('083','Keweenaw'),('085','Lake'),('087','Lapeer'),
        ('089','Leelanau'),('091','Lenawee'),('093','Livingston'),('095','Luce'),
        ('097','Mackinac'),('099','Macomb'),('101','Manistee'),('103','Marquette'),
        ('105','Mason'),('107','Mecosta'),('109','Menominee'),('111','Midland'),
        ('113','Missaukee'),('115','Monroe'),('117','Montcalm'),('119','Montmorency'),
        ('121','Muskegon'),('123','Newaygo'),('125','Oakland'),('127','Oceana'),
        ('129','Ogemaw'),('131','Ontonagon'),('133','Osceola'),('135','Oscoda'),
        ('137','Otsego'),('139','Ottawa'),('141','Presque Isle'),('143','Roscommon'),
        ('145','Saginaw'),('147','St. Clair'),('149','St. Joseph'),('151','Sanilac'),
        ('153','Schoolcraft'),('155','Shiawassee'),('157','Tuscola'),('159','Van Buren'),
        ('161','Washtenaw'),('163','Wayne'),('165','Wexford'),
    ],
    'MN': [
        ('001','Aitkin'),('003','Anoka'),('005','Becker'),('007','Beltrami'),
        ('009','Benton'),('011','Big Stone'),('013','Blue Earth'),('015','Brown'),
        ('017','Carlton'),('019','Carver'),('021','Cass'),('023','Chippewa'),
        ('025','Chisago'),('027','Clay'),('029','Clearwater'),('031','Cook'),
        ('033','Cottonwood'),('035','Crow Wing'),('037','Dakota'),('039','Dodge'),
        ('041','Douglas'),('043','Faribault'),('045','Fillmore'),('047','Freeborn'),
        ('049','Goodhue'),('051','Grant'),('053','Hennepin'),('055','Houston'),
        ('057','Hubbard'),('059','Isanti'),('061','Itasca'),('063','Jackson'),
        ('065','Kanabec'),('067','Kandiyohi'),('069','Kittson'),('071','Koochiching'),
        ('073','Lac qui Parle'),('075','Lake'),('077','Lake of the Woods'),
        ('079','Le Sueur'),('081','Lincoln'),('083','Lyon'),('085','McLeod'),
        ('087','Mahnomen'),('089','Marshall'),('091','Martin'),('093','Meeker'),
        ('095','Mille Lacs'),('097','Morrison'),('099','Mower'),('101','Murray'),
        ('103','Nicollet'),('105','Nobles'),('107','Norman'),('109','Olmsted'),
        ('111','Otter Tail'),('113','Pennington'),('115','Pine'),('117','Pipestone'),
        ('119','Polk'),('121','Pope'),('123','Ramsey'),('125','Red Lake'),
        ('127','Redwood'),('129','Renville'),('131','Rice'),('133','Rock'),
        ('135','Roseau'),('137','St. Louis'),('139','Scott'),('141','Sherburne'),
        ('143','Sibley'),('145','Stearns'),('147','Steele'),('149','Stevens'),
        ('151','Swift'),('153','Todd'),('155','Traverse'),('157','Wabasha'),
        ('159','Wadena'),('161','Waseca'),('163','Washington'),('165','Watonwan'),
        ('167','Wilkin'),('169','Winona'),('171','Wright'),('173','Yellow Medicine'),
    ],
    'MS': [
        ('001','Adams'),('003','Alcorn'),('005','Amite'),('007','Attala'),
        ('009','Benton'),('011','Bolivar'),('013','Calhoun'),('015','Carroll'),
        ('017','Chickasaw'),('019','Choctaw'),('021','Claiborne'),('023','Clarke'),
        ('025','Clay'),('027','Coahoma'),('029','Copiah'),('031','Covington'),
        ('033','DeSoto'),('035','Forrest'),('037','Franklin'),('039','George'),
        ('041','Greene'),('043','Grenada'),('045','Hancock'),('047','Harrison'),
        ('049','Hinds'),('051','Holmes'),('053','Humphreys'),('055','Issaquena'),
        ('057','Itawamba'),('059','Jackson'),('061','Jasper'),('063','Jefferson'),
        ('065','Jefferson Davis'),('067','Jones'),('069','Kemper'),('071','Lafayette'),
        ('073','Lamar'),('075','Lauderdale'),('077','Lawrence'),('079','Leake'),
        ('081','Lee'),('083','Leflore'),('085','Lincoln'),('087','Lowndes'),
        ('089','Madison'),('091','Marion'),('093','Marshall'),('095','Monroe'),
        ('097','Montgomery'),('099','Neshoba'),('101','Newton'),('103','Noxubee'),
        ('105','Oktibbeha'),('107','Panola'),('109','Pearl River'),('111','Perry'),
        ('113','Pike'),('115','Pontotoc'),('117','Prentiss'),('119','Quitman'),
        ('121','Rankin'),('123','Scott'),('125','Sharkey'),('127','Simpson'),
        ('129','Smith'),('131','Stone'),('133','Sunflower'),('135','Tallahatchie'),
        ('137','Tate'),('139','Tippah'),('141','Tishomingo'),('143','Tunica'),
        ('145','Union'),('147','Walthall'),('149','Warren'),('151','Washington'),
        ('153','Wayne'),('155','Webster'),('157','Wilkinson'),('159','Winston'),
        ('161','Yalobusha'),('163','Yazoo'),
    ],
    'MO': [
        ('001','Adair'),('003','Andrew'),('005','Atchison'),('007','Audrain'),
        ('009','Barry'),('011','Barton'),('013','Bates'),('015','Benton'),
        ('017','Bollinger'),('019','Boone'),('021','Buchanan'),('023','Butler'),
        ('025','Caldwell'),('027','Callaway'),('029','Camden'),('031','Cape Girardeau'),
        ('033','Carroll'),('035','Carter'),('037','Cass'),('039','Cedar'),
        ('041','Chariton'),('043','Christian'),('045','Clark'),('047','Clay'),
        ('049','Clinton'),('051','Cole'),('053','Cooper'),('055','Crawford'),
        ('057','Dade'),('059','Dallas'),('061','Daviess'),('063','DeKalb'),
        ('065','Dent'),('067','Douglas'),('069','Dunklin'),('071','Franklin'),
        ('073','Gasconade'),('075','Gentry'),('077','Greene'),('079','Grundy'),
        ('081','Harrison'),('083','Henry'),('085','Hickory'),('087','Holt'),
        ('089','Howard'),('091','Howell'),('093','Iron'),('095','Jackson'),
        ('097','Jasper'),('099','Jefferson'),('101','Johnson'),('103','Knox'),
        ('105','Laclede'),('107','Lafayette'),('109','Lawrence'),('111','Lewis'),
        ('113','Lincoln'),('115','Linn'),('117','Livingston'),('119','McDonald'),
        ('121','Macon'),('123','Madison'),('125','Maries'),('127','Marion'),
        ('129','Mercer'),('131','Miller'),('133','Mississippi'),('135','Moniteau'),
        ('137','Monroe'),('139','Montgomery'),('141','Morgan'),('143','New Madrid'),
        ('145','Newton'),('147','Nodaway'),('149','Oregon'),('151','Osage'),
        ('153','Ozark'),('155','Pemiscot'),('157','Perry'),('159','Pettis'),
        ('161','Phelps'),('163','Pike'),('165','Platte'),('167','Polk'),
        ('169','Pulaski'),('171','Putnam'),('173','Ralls'),('175','Randolph'),
        ('177','Ray'),('179','Reynolds'),('181','Ripley'),('183','St. Charles'),
        ('185','St. Clair'),('186','Ste. Genevieve'),('187','St. Francois'),
        ('189','St. Louis'),('510','St. Louis City'),
        ('195','Saline'),('197','Schuyler'),('199','Scotland'),('201','Scott'),
        ('203','Shannon'),('205','Shelby'),('207','Stoddard'),('209','Stone'),
        ('211','Sullivan'),('213','Taney'),('215','Texas'),('217','Vernon'),
        ('219','Warren'),('221','Washington'),('223','Wayne'),('225','Webster'),
        ('227','Worth'),('229','Wright'),
    ],
    'MT': [
        ('001','Beaverhead'),('003','Big Horn'),('005','Blaine'),('007','Broadwater'),
        ('009','Carbon'),('011','Carter'),('013','Cascade'),('015','Chouteau'),
        ('017','Custer'),('019','Daniels'),('021','Dawson'),('023','Deer Lodge'),
        ('025','Fallon'),('027','Fergus'),('029','Flathead'),('031','Gallatin'),
        ('033','Garfield'),('035','Glacier'),('037','Golden Valley'),('039','Granite'),
        ('041','Hill'),('043','Jefferson'),('045','Judith Basin'),('047','Lake'),
        ('049','Lewis and Clark'),('051','Liberty'),('053','Lincoln'),('055','McCone'),
        ('057','Madison'),('059','Meagher'),('061','Mineral'),('063','Missoula'),
        ('065','Musselshell'),('067','Park'),('069','Petroleum'),('071','Phillips'),
        ('073','Pondera'),('075','Powder River'),('077','Powell'),('079','Prairie'),
        ('081','Ravalli'),('083','Richland'),('085','Roosevelt'),('087','Rosebud'),
        ('089','Sanders'),('091','Sheridan'),('093','Silver Bow'),('095','Stillwater'),
        ('097','Sweet Grass'),('099','Teton'),('101','Toole'),('103','Treasure'),
        ('105','Valley'),('107','Wheatland'),('109','Wibaux'),('111','Yellowstone'),
    ],
    'NE': [
        ('001','Adams'),('003','Antelope'),('005','Arthur'),('007','Banner'),
        ('009','Blaine'),('011','Boone'),('013','Box Butte'),('015','Boyd'),
        ('017','Brown'),('019','Buffalo'),('021','Burt'),('023','Butler'),
        ('025','Cass'),('027','Cedar'),('029','Chase'),('031','Cherry'),
        ('033','Cheyenne'),('035','Clay'),('037','Colfax'),('039','Cuming'),
        ('041','Custer'),('043','Dakota'),('045','Dawes'),('047','Dawson'),
        ('049','Deuel'),('051','Dixon'),('053','Dodge'),('055','Douglas'),
        ('057','Dundy'),('059','Fillmore'),('061','Franklin'),('063','Frontier'),
        ('065','Furnas'),('067','Gage'),('069','Garden'),('071','Garfield'),
        ('073','Gosper'),('075','Grant'),('077','Greeley'),('079','Hall'),
        ('081','Hamilton'),('083','Harlan'),('085','Hayes'),('087','Hitchcock'),
        ('089','Holt'),('091','Hooker'),('093','Howard'),('095','Jefferson'),
        ('097','Johnson'),('099','Kearney'),('101','Keith'),('103','Keya Paha'),
        ('105','Kimball'),('107','Knox'),('109','Lancaster'),('111','Lincoln'),
        ('113','Logan'),('115','Loup'),('117','McPherson'),('119','Madison'),
        ('121','Merrick'),('123','Morrill'),('125','Nance'),('127','Nemaha'),
        ('129','Nuckolls'),('131','Otoe'),('133','Pawnee'),('135','Perkins'),
        ('137','Phelps'),('139','Pierce'),('141','Platte'),('143','Polk'),
        ('145','Red Willow'),('147','Richardson'),('149','Rock'),('151','Saline'),
        ('153','Sarpy'),('155','Saunders'),('157','Scotts Bluff'),('159','Seward'),
        ('161','Sheridan'),('163','Sherman'),('165','Sioux'),('167','Stanton'),
        ('169','Thayer'),('171','Thomas'),('173','Thurston'),('175','Valley'),
        ('177','Washington'),('179','Wayne'),('181','Webster'),('183','Wheeler'),
        ('185','York'),
    ],
    'NV': [
        ('001','Churchill'),('003','Clark'),('005','Douglas'),('007','Elko'),
        ('009','Esmeralda'),('011','Eureka'),('013','Humboldt'),('015','Lander'),
        ('017','Lincoln'),('019','Lyon'),('021','Mineral'),('023','Nye'),
        ('027','Pershing'),('029','Storey'),('031','Washoe'),('033','White Pine'),
        ('510','Carson City'),
    ],
    'NH': [
        ('001','Belknap'),('003','Carroll'),('005','Cheshire'),('007','Coos'),
        ('009','Grafton'),('011','Hillsborough'),('013','Merrimack'),('015','Rockingham'),
        ('017','Strafford'),('019','Sullivan'),
    ],
    'NJ': [
        ('001','Atlantic'),('003','Bergen'),('005','Burlington'),('007','Camden'),
        ('009','Cape May'),('011','Cumberland'),('013','Essex'),('015','Gloucester'),
        ('017','Hudson'),('019','Hunterdon'),('021','Mercer'),('023','Middlesex'),
        ('025','Monmouth'),('027','Morris'),('029','Ocean'),('031','Passaic'),
        ('033','Salem'),('035','Somerset'),('037','Sussex'),('039','Union'),
        ('041','Warren'),
    ],
    'NM': [
        ('001','Bernalillo'),('003','Catron'),('005','Chaves'),('006','Cibola'),
        ('007','Colfax'),('009','Curry'),('011','De Baca'),('013','Dona Ana'),
        ('015','Eddy'),('017','Grant'),('019','Guadalupe'),('021','Harding'),
        ('023','Hidalgo'),('025','Lea'),('027','Lincoln'),('028','Los Alamos'),
        ('029','Luna'),('031','McKinley'),('033','Mora'),('035','Otero'),
        ('037','Quay'),('039','Rio Arriba'),('041','Roosevelt'),('043','Sandoval'),
        ('045','San Juan'),('047','San Miguel'),('049','Santa Fe'),('051','Sierra'),
        ('053','Socorro'),('055','Taos'),('057','Torrance'),('059','Union'),
        ('061','Valencia'),
    ],
    'NY': [
        ('001','Albany'),('003','Allegany'),('005','Bronx'),('007','Broome'),
        ('009','Cattaraugus'),('011','Cayuga'),('013','Chautauqua'),('015','Chemung'),
        ('017','Chenango'),('019','Clinton'),('021','Columbia'),('023','Cortland'),
        ('025','Delaware'),('027','Dutchess'),('029','Erie'),('031','Essex'),
        ('033','Franklin'),('035','Fulton'),('037','Genesee'),('039','Greene'),
        ('041','Hamilton'),('043','Herkimer'),('045','Jefferson'),('047','Kings'),
        ('049','Lewis'),('051','Livingston'),('053','Madison'),('055','Monroe'),
        ('057','Montgomery'),('059','Nassau'),('061','New York'),('063','Niagara'),
        ('065','Oneida'),('067','Onondaga'),('069','Ontario'),('071','Orange'),
        ('073','Orleans'),('075','Oswego'),('077','Otsego'),('079','Putnam'),
        ('081','Queens'),('083','Rensselaer'),('085','Richmond'),('087','Rockland'),
        ('089','St. Lawrence'),('091','Saratoga'),('093','Schenectady'),('095','Schoharie'),
        ('097','Schuyler'),('099','Seneca'),('101','Steuben'),('103','Suffolk'),
        ('105','Sullivan'),('107','Tioga'),('109','Tompkins'),('111','Ulster'),
        ('113','Warren'),('115','Washington'),('117','Wayne'),('119','Westchester'),
        ('121','Wyoming'),('123','Yates'),
    ],
    'NC': [
        ('001','Alamance'),('003','Alexander'),('005','Alleghany'),('007','Anson'),
        ('009','Ashe'),('011','Avery'),('013','Beaufort'),('015','Bertie'),
        ('017','Bladen'),('019','Brunswick'),('021','Buncombe'),('023','Burke'),
        ('025','Cabarrus'),('027','Caldwell'),('029','Camden'),('031','Carteret'),
        ('033','Caswell'),('035','Catawba'),('037','Chatham'),('039','Cherokee'),
        ('041','Chowan'),('043','Clay'),('045','Cleveland'),('047','Columbus'),
        ('049','Craven'),('051','Cumberland'),('053','Currituck'),('055','Dare'),
        ('057','Davidson'),('059','Davie'),('061','Duplin'),('063','Durham'),
        ('065','Edgecombe'),('067','Forsyth'),('069','Franklin'),('071','Gaston'),
        ('073','Gates'),('075','Graham'),('077','Granville'),('079','Greene'),
        ('081','Guilford'),('083','Halifax'),('085','Harnett'),('087','Haywood'),
        ('089','Henderson'),('091','Hertford'),('093','Hoke'),('095','Hyde'),
        ('097','Iredell'),('099','Jackson'),('101','Johnston'),('103','Jones'),
        ('105','Lee'),('107','Lenoir'),('109','Lincoln'),('111','Macon'),
        ('113','Madison'),('115','Martin'),('117','McDowell'),('119','Mecklenburg'),
        ('121','Mitchell'),('123','Montgomery'),('125','Moore'),('127','Nash'),
        ('129','New Hanover'),('131','Northampton'),('133','Onslow'),('135','Orange'),
        ('137','Pamlico'),('139','Pasquotank'),('141','Pender'),('143','Perquimans'),
        ('145','Person'),('147','Pitt'),('149','Polk'),('151','Randolph'),
        ('153','Richmond'),('155','Robeson'),('157','Rockingham'),('159','Rowan'),
        ('161','Rutherford'),('163','Sampson'),('165','Scotland'),('167','Stanly'),
        ('169','Stokes'),('171','Surry'),('173','Swain'),('175','Transylvania'),
        ('177','Tyrrell'),('179','Union'),('181','Vance'),('183','Wake'),
        ('185','Warren'),('187','Washington'),('189','Watauga'),('191','Wayne'),
        ('193','Wilkes'),('195','Wilson'),('197','Yadkin'),('199','Yancey'),
    ],
    'ND': [
        ('001','Adams'),('003','Barnes'),('005','Benson'),('007','Billings'),
        ('009','Bottineau'),('011','Bowman'),('013','Burke'),('015','Burleigh'),
        ('017','Cass'),('019','Cavalier'),('021','Dickey'),('023','Divide'),
        ('025','Dunn'),('027','Eddy'),('029','Emmons'),('031','Foster'),
        ('033','Golden Valley'),('035','Grand Forks'),('037','Grant'),('039','Griggs'),
        ('041','Hettinger'),('043','Kidder'),('045','LaMoure'),('047','Logan'),
        ('049','McHenry'),('051','McIntosh'),('053','McKenzie'),('055','McLean'),
        ('057','Mercer'),('059','Morton'),('061','Mountrail'),('063','Nelson'),
        ('065','Oliver'),('067','Pembina'),('069','Pierce'),('071','Ramsey'),
        ('073','Ransom'),('075','Renville'),('077','Richland'),('079','Rolette'),
        ('081','Sargent'),('083','Sheridan'),('085','Sioux'),('087','Slope'),
        ('089','Stark'),('091','Steele'),('093','Stutsman'),('095','Towner'),
        ('097','Traill'),('099','Walsh'),('101','Ward'),('103','Wells'),
        ('105','Williams'),
    ],
    'OH': [
        ('001','Adams'),('003','Allen'),('005','Ashland'),('007','Ashtabula'),
        ('009','Athens'),('011','Auglaize'),('013','Belmont'),('015','Brown'),
        ('017','Butler'),('019','Carroll'),('021','Champaign'),('023','Clark'),
        ('025','Clermont'),('027','Clinton'),('029','Columbiana'),('031','Coshocton'),
        ('033','Crawford'),('035','Cuyahoga'),('037','Darke'),('039','Defiance'),
        ('041','Delaware'),('043','Erie'),('045','Fairfield'),('047','Fayette'),
        ('049','Franklin'),('051','Fulton'),('053','Gallia'),('055','Geauga'),
        ('057','Greene'),('059','Guernsey'),('061','Hamilton'),('063','Hancock'),
        ('065','Hardin'),('067','Harrison'),('069','Henry'),('071','Highland'),
        ('073','Hocking'),('075','Holmes'),('077','Huron'),('079','Jackson'),
        ('081','Jefferson'),('083','Knox'),('085','Lake'),('087','Lawrence'),
        ('089','Licking'),('091','Logan'),('093','Lorain'),('095','Lucas'),
        ('097','Madison'),('099','Mahoning'),('101','Marion'),('103','Medina'),
        ('105','Meigs'),('107','Mercer'),('109','Miami'),('111','Monroe'),
        ('113','Montgomery'),('115','Morgan'),('117','Morrow'),('119','Muskingum'),
        ('121','Noble'),('123','Ottawa'),('125','Paulding'),('127','Perry'),
        ('129','Pickaway'),('131','Pike'),('133','Portage'),('135','Preble'),
        ('137','Putnam'),('139','Richland'),('141','Ross'),('143','Sandusky'),
        ('145','Scioto'),('147','Seneca'),('149','Shelby'),('151','Stark'),
        ('153','Summit'),('155','Trumbull'),('157','Tuscarawas'),('159','Union'),
        ('161','Van Wert'),('163','Vinton'),('165','Warren'),('167','Washington'),
        ('169','Wayne'),('171','Williams'),('173','Wood'),('175','Wyandot'),
    ],
    'OK': [
        ('001','Adair'),('003','Alfalfa'),('005','Atoka'),('007','Beaver'),
        ('009','Beckham'),('011','Blaine'),('013','Bryan'),('015','Caddo'),
        ('017','Canadian'),('019','Carter'),('021','Cherokee'),('023','Choctaw'),
        ('025','Cimarron'),('027','Cleveland'),('029','Coal'),('031','Comanche'),
        ('033','Cotton'),('035','Craig'),('037','Creek'),('039','Custer'),
        ('041','Delaware'),('043','Dewey'),('045','Ellis'),('047','Garfield'),
        ('049','Garvin'),('051','Grady'),('053','Grant'),('055','Greer'),
        ('057','Harmon'),('059','Harper'),('061','Haskell'),('063','Hughes'),
        ('065','Jackson'),('067','Jefferson'),('069','Johnston'),('071','Kay'),
        ('073','Kingfisher'),('075','Kiowa'),('077','Latimer'),('079','Le Flore'),
        ('081','Lincoln'),('083','Logan'),('085','Love'),('087','McClain'),
        ('089','McCurtain'),('091','McIntosh'),('093','Major'),('095','Marshall'),
        ('097','Mayes'),('099','Murray'),('101','Muskogee'),('103','Noble'),
        ('105','Nowata'),('107','Okfuskee'),('109','Oklahoma'),('111','Okmulgee'),
        ('113','Osage'),('115','Ottawa'),('117','Pawnee'),('119','Payne'),
        ('121','Pittsburg'),('123','Pontotoc'),('125','Pottawatomie'),('127','Pushmataha'),
        ('129','Roger Mills'),('131','Rogers'),('133','Seminole'),('135','Sequoyah'),
        ('137','Stephens'),('139','Texas'),('141','Tillman'),('143','Tulsa'),
        ('145','Wagoner'),('147','Washington'),('149','Washita'),('151','Woods'),
        ('153','Woodward'),
    ],
    'OR': [
        ('001','Baker'),('003','Benton'),('005','Clackamas'),('007','Clatsop'),
        ('009','Columbia'),('011','Coos'),('013','Crook'),('015','Curry'),
        ('017','Deschutes'),('019','Douglas'),('021','Gilliam'),('023','Grant'),
        ('025','Harney'),('027','Hood River'),('029','Jackson'),('031','Jefferson'),
        ('033','Josephine'),('035','Klamath'),('037','Lake'),('039','Lane'),
        ('041','Lincoln'),('043','Linn'),('045','Malheur'),('047','Marion'),
        ('049','Morrow'),('051','Multnomah'),('053','Polk'),('055','Sherman'),
        ('057','Tillamook'),('059','Umatilla'),('061','Union'),('063','Wallowa'),
        ('065','Wasco'),('067','Washington'),('069','Wheeler'),('071','Yamhill'),
    ],
    'PA': [
        ('001','Adams'),('003','Allegheny'),('005','Armstrong'),('007','Beaver'),
        ('009','Bedford'),('011','Berks'),('013','Blair'),('015','Bradford'),
        ('017','Bucks'),('019','Butler'),('021','Cambria'),('023','Cameron'),
        ('025','Carbon'),('027','Centre'),('029','Chester'),('031','Clarion'),
        ('033','Clearfield'),('035','Clinton'),('037','Columbia'),('039','Crawford'),
        ('041','Cumberland'),('043','Dauphin'),('045','Delaware'),('047','Elk'),
        ('049','Erie'),('051','Fayette'),('053','Forest'),('055','Franklin'),
        ('057','Fulton'),('059','Greene'),('061','Huntingdon'),('063','Indiana'),
        ('065','Jefferson'),('067','Juniata'),('069','Lackawanna'),('071','Lancaster'),
        ('073','Lawrence'),('075','Lebanon'),('077','Lehigh'),('079','Luzerne'),
        ('081','Lycoming'),('083','McKean'),('085','Mercer'),('087','Mifflin'),
        ('089','Monroe'),('091','Montgomery'),('093','Montour'),('095','Northampton'),
        ('097','Northumberland'),('099','Perry'),('101','Philadelphia'),('103','Pike'),
        ('105','Potter'),('107','Schuylkill'),('109','Snyder'),('111','Somerset'),
        ('113','Sullivan'),('115','Susquehanna'),('117','Tioga'),('119','Union'),
        ('121','Venango'),('123','Warren'),('125','Washington'),('127','Wayne'),
        ('129','Westmoreland'),('131','Wyoming'),('133','York'),
    ],
    'RI': [
        ('001','Bristol'),('003','Kent'),('005','Newport'),('007','Providence'),
        ('009','Washington'),
    ],
    'SC': [
        ('001','Abbeville'),('003','Aiken'),('005','Allendale'),('007','Anderson'),
        ('009','Bamberg'),('011','Barnwell'),('013','Beaufort'),('015','Berkeley'),
        ('017','Calhoun'),('019','Charleston'),('021','Cherokee'),('023','Chester'),
        ('025','Chesterfield'),('027','Clarendon'),('029','Colleton'),('031','Darlington'),
        ('033','Dillon'),('035','Dorchester'),('037','Edgefield'),('039','Fairfield'),
        ('041','Florence'),('043','Georgetown'),('045','Greenville'),('047','Greenwood'),
        ('049','Hampton'),('051','Horry'),('053','Jasper'),('055','Kershaw'),
        ('057','Lancaster'),('059','Laurens'),('061','Lee'),('063','Lexington'),
        ('065','McCormick'),('067','Marion'),('069','Marlboro'),('071','Newberry'),
        ('073','Oconee'),('075','Orangeburg'),('077','Pickens'),('079','Richland'),
        ('081','Saluda'),('083','Spartanburg'),('085','Sumter'),('087','Union'),
        ('089','Williamsburg'),('091','York'),
    ],
    'SD': [
        ('003','Aurora'),('005','Beadle'),('007','Bennett'),('009','Bon Homme'),
        ('011','Brookings'),('013','Brown'),('015','Brule'),('017','Buffalo'),
        ('019','Butte'),('021','Campbell'),('023','Charles Mix'),('025','Clark'),
        ('027','Clay'),('029','Codington'),('031','Corson'),('033','Custer'),
        ('035','Davison'),('037','Day'),('039','Deuel'),('041','Dewey'),
        ('043','Douglas'),('045','Edmunds'),('047','Fall River'),('049','Faulk'),
        ('051','Grant'),('053','Gregory'),('055','Haakon'),('057','Hamlin'),
        ('059','Hand'),('061','Hanson'),('063','Harding'),('065','Hughes'),
        ('067','Hutchinson'),('069','Hyde'),('071','Jackson'),('073','Jerauld'),
        ('075','Jones'),('077','Kingsbury'),('079','Lake'),('081','Lawrence'),
        ('083','Lincoln'),('085','Lyman'),('087','McCook'),('089','McPherson'),
        ('091','Marshall'),('093','Meade'),('095','Mellette'),('097','Miner'),
        ('099','Minnehaha'),('101','Moody'),('102','Oglala Lakota'),('103','Pennington'),
        ('105','Perkins'),('107','Potter'),('109','Roberts'),('111','Sanborn'),
        ('113','Spink'),('115','Stanley'),('117','Sully'),('119','Todd'),
        ('121','Tripp'),('123','Turner'),('125','Union'),('127','Walworth'),
        ('129','Yankton'),('135','Ziebach'),
    ],
    'TN': [
        ('001','Anderson'),('003','Bedford'),('005','Benton'),('007','Bledsoe'),
        ('009','Blount'),('011','Bradley'),('013','Campbell'),('015','Cannon'),
        ('017','Carroll'),('019','Carter'),('021','Cheatham'),('023','Chester'),
        ('025','Claiborne'),('027','Clay'),('029','Cocke'),('031','Coffee'),
        ('033','Crockett'),('035','Cumberland'),('037','Davidson'),('039','Decatur'),
        ('041','DeKalb'),('043','Dickson'),('045','Dyer'),('047','Fayette'),
        ('049','Fentress'),('051','Franklin'),('053','Gibson'),('055','Giles'),
        ('057','Grainger'),('059','Greene'),('061','Grundy'),('063','Hamblen'),
        ('065','Hamilton'),('067','Hancock'),('069','Hardeman'),('071','Hardin'),
        ('073','Hawkins'),('075','Haywood'),('077','Henderson'),('079','Henry'),
        ('081','Hickman'),('083','Houston'),('085','Humphreys'),('087','Jackson'),
        ('089','Jefferson'),('091','Johnson'),('093','Knox'),('095','Lake'),
        ('097','Lauderdale'),('099','Lawrence'),('101','Lewis'),('103','Lincoln'),
        ('105','Loudon'),('107','McMinn'),('109','McNairy'),('111','Macon'),
        ('113','Madison'),('115','Marion'),('117','Marshall'),('119','Maury'),
        ('121','Meigs'),('123','Monroe'),('125','Montgomery'),('127','Moore'),
        ('129','Morgan'),('131','Obion'),('133','Overton'),('135','Perry'),
        ('137','Pickett'),('139','Polk'),('141','Putnam'),('143','Rhea'),
        ('145','Roane'),('147','Robertson'),('149','Rutherford'),('151','Scott'),
        ('153','Sequatchie'),('155','Sevier'),('157','Shelby'),('159','Smith'),
        ('161','Stewart'),('163','Sullivan'),('165','Sumner'),('167','Tipton'),
        ('169','Trousdale'),('171','Unicoi'),('173','Union'),('175','Van Buren'),
        ('177','Warren'),('179','Washington'),('181','Wayne'),('183','Weakley'),
        ('185','White'),('187','Williamson'),('189','Wilson'),
    ],
    'TX': [
        ('001','Anderson'),('003','Andrews'),('005','Angelina'),('007','Aransas'),
        ('009','Archer'),('011','Armstrong'),('013','Atascosa'),('015','Austin'),
        ('017','Bailey'),('019','Bandera'),('021','Bastrop'),('023','Baylor'),
        ('025','Bee'),('027','Bell'),('029','Bexar'),('031','Blanco'),
        ('033','Borden'),('035','Bosque'),('037','Bowie'),('039','Brazoria'),
        ('041','Brazos'),('043','Brewster'),('045','Briscoe'),('047','Brooks'),
        ('049','Brown'),('051','Burleson'),('053','Burnet'),('055','Caldwell'),
        ('057','Calhoun'),('059','Callahan'),('061','Cameron'),('063','Camp'),
        ('065','Carson'),('067','Cass'),('069','Castro'),('071','Chambers'),
        ('073','Cherokee'),('075','Childress'),('077','Clay'),('079','Cochran'),
        ('081','Coke'),('083','Coleman'),('085','Collin'),('087','Collingsworth'),
        ('089','Colorado'),('091','Comal'),('093','Comanche'),('095','Concho'),
        ('097','Cooke'),('099','Corpus Christi (Nueces)'),('101','Coryell'),
        ('103','Cottle'),('105','Crane'),('107','Crockett'),('109','Crosby'),
        ('111','Culberson'),('113','Dallam'),('115','Dallas'),('117','Dawson'),
        ('119','Deaf Smith'),('121','Delta'),('123','Denton'),('125','DeWitt'),
        ('127','Dickens'),('129','Dimmit'),('131','Donley'),('133','Duval'),
        ('135','Eastland'),('137','Ector'),('139','Edwards'),('141','Ellis'),
        ('143','El Paso'),('145','Erath'),('147','Falls'),('149','Fannin'),
        ('151','Fayette'),('153','Fisher'),('155','Floyd'),('157','Foard'),
        ('159','Fort Bend'),('161','Franklin'),('163','Freestone'),('165','Frio'),
        ('167','Gaines'),('169','Galveston'),('171','Garza'),('173','Gillespie'),
        ('175','Glasscock'),('177','Goliad'),('179','Gonzales'),('181','Gray'),
        ('183','Grayson'),('185','Gregg'),('187','Grimes'),('189','Guadalupe'),
        ('191','Hale'),('193','Hall'),('195','Hamilton'),('197','Hansford'),
        ('199','Hardeman'),('201','Hardin'),('203','Harris'),('205','Harrison'),
        ('207','Hartley'),('209','Haskell'),('211','Hays'),('213','Hemphill'),
        ('215','Henderson'),('217','Hidalgo'),('219','Hill'),('221','Hockley'),
        ('223','Hood'),('225','Hopkins'),('227','Houston'),('229','Howard'),
        ('231','Hudspeth'),('233','Hunt'),('235','Hutchinson'),('237','Irion'),
        ('239','Jack'),('241','Jackson'),('243','Jasper'),('245','Jeff Davis'),
        ('247','Jefferson'),('249','Jim Hogg'),('251','Jim Wells'),('253','Johnson'),
        ('255','Jones'),('257','Karnes'),('259','Kaufman'),('261','Kendall'),
        ('263','Kenedy'),('265','Kent'),('267','Kerr'),('269','Kimble'),
        ('271','King'),('273','Kinney'),('275','Kleberg'),('277','Knox'),
        ('279','Lamar'),('281','Lamb'),('283','Lampasas'),('285','La Salle'),
        ('287','Lavaca'),('289','Lee'),('291','Leon'),('293','Liberty'),
        ('295','Limestone'),('297','Lipscomb'),('299','Live Oak'),('301','Llano'),
        ('303','Loving'),('305','Lubbock'),('307','Lynn'),('309','McCulloch'),
        ('311','McLennan'),('313','McMullen'),('315','Madison'),('317','Marion'),
        ('319','Martin'),('321','Mason'),('323','Matagorda'),('325','Maverick'),
        ('327','Medina'),('329','Menard'),('331','Midland'),('333','Milam'),
        ('335','Mills'),('337','Mitchell'),('339','Montague'),('341','Montgomery'),
        ('343','Moore'),('345','Morris'),('347','Motley'),('349','Nacogdoches'),
        ('351','Navarro'),('353','Newton'),('355','Nolan'),('357','Nueces'),
        ('359','Ochiltree'),('361','Oldham'),('363','Orange'),('365','Palo Pinto'),
        ('367','Panola'),('369','Parker'),('371','Parmer'),('373','Pecos'),
        ('375','Polk'),('377','Potter'),('379','Presidio'),('381','Rains'),
        ('383','Randall'),('385','Reagan'),('387','Real'),('389','Red River'),
        ('391','Reeves'),('393','Refugio'),('395','Roberts'),('397','Robertson'),
        ('399','Rockwall'),('401','Runnels'),('403','Rusk'),('405','Sabine'),
        ('407','San Augustine'),('409','San Jacinto'),('411','San Patricio'),
        ('413','San Saba'),('415','Schleicher'),('417','Scurry'),('419','Shackelford'),
        ('421','Shelby'),('423','Sherman'),('425','Smith'),('427','Somervell'),
        ('429','Starr'),('431','Stephens'),('433','Sterling'),('435','Stonewall'),
        ('437','Sutton'),('439','Swisher'),('441','Tarrant'),('443','Taylor'),
        ('445','Terrell'),('447','Terry'),('449','Throckmorton'),('451','Titus'),
        ('453','Tom Green'),('455','Travis'),('457','Trinity'),('459','Tyler'),
        ('461','Upshur'),('463','Upton'),('465','Uvalde'),('467','Val Verde'),
        ('469','Van Zandt'),('471','Victoria'),('473','Walker'),('475','Waller'),
        ('477','Ward'),('479','Washington'),('481','Webb'),('483','Wharton'),
        ('485','Wheeler'),('487','Wichita'),('489','Wilbarger'),('491','Willacy'),
        ('493','Williamson'),('495','Wilson'),('497','Winkler'),('499','Wise'),
        ('501','Wood'),('503','Yoakum'),('505','Young'),('507','Zapata'),('509','Zavala'),
    ],
    'UT': [
        ('001','Beaver'),('003','Box Elder'),('005','Cache'),('007','Carbon'),
        ('009','Daggett'),('011','Davis'),('013','Duchesne'),('015','Emery'),
        ('017','Garfield'),('019','Grand'),('021','Iron'),('023','Juab'),
        ('025','Kane'),('027','Millard'),('029','Morgan'),('031','Piute'),
        ('033','Rich'),('035','Salt Lake'),('037','San Juan'),('039','Sanpete'),
        ('041','Sevier'),('043','Summit'),('045','Tooele'),('047','Uintah'),
        ('049','Utah'),('051','Wasatch'),('053','Washington'),('055','Wayne'),
        ('057','Weber'),
    ],
    'VT': [
        ('001','Addison'),('003','Bennington'),('005','Caledonia'),('007','Chittenden'),
        ('009','Essex'),('011','Franklin'),('013','Grand Isle'),('015','Lamoille'),
        ('017','Orange'),('019','Orleans'),('021','Rutland'),('023','Washington'),
        ('025','Windham'),('027','Windsor'),
    ],
    'VA': [
        ('001','Accomack'),('003','Albemarle'),('005','Alleghany'),('007','Amelia'),
        ('009','Amherst'),('011','Appomattox'),('013','Arlington'),('015','Augusta'),
        ('017','Bath'),('019','Bedford'),('021','Bland'),('023','Botetourt'),
        ('025','Brunswick'),('027','Buchanan'),('029','Buckingham'),('031','Campbell'),
        ('033','Caroline'),('035','Carroll'),('036','Charles City'),('037','Charlotte'),
        ('041','Chesterfield'),('043','Clarke'),('045','Craig'),('047','Culpeper'),
        ('049','Cumberland'),('051','Dickenson'),('053','Dinwiddie'),
        ('057','Essex'),('059','Fairfax'),('061','Fauquier'),('063','Floyd'),
        ('065','Fluvanna'),('067','Franklin'),('069','Frederick'),('071','Giles'),
        ('073','Gloucester'),('075','Goochland'),('077','Grayson'),('079','Greene'),
        ('081','Greensville'),('083','Halifax'),('085','Hanover'),('087','Henrico'),
        ('089','Henry'),('091','Highland'),('093','Isle of Wight'),('095','James City'),
        ('097','King and Queen'),('099','King George'),('101','King William'),
        ('103','Lancaster'),('105','Lee'),('107','Loudoun'),('109','Louisa'),
        ('111','Lunenburg'),('113','Madison'),('115','Mathews'),('117','Mecklenburg'),
        ('119','Middlesex'),('121','Montgomery'),('125','Nelson'),('127','New Kent'),
        ('131','Northampton'),('133','Northumberland'),('135','Nottoway'),
        ('137','Orange'),('139','Page'),('141','Patrick'),('143','Pittsylvania'),
        ('145','Powhatan'),('147','Prince Edward'),('149','Prince George'),
        ('153','Prince William'),('155','Pulaski'),('157','Rappahannock'),
        ('159','Richmond'),('161','Roanoke'),('163','Rockbridge'),('165','Rockingham'),
        ('167','Russell'),('169','Scott'),('171','Shenandoah'),('173','Smyth'),
        ('175','Southampton'),('177','Spotsylvania'),('179','Stafford'),('181','Surry'),
        ('183','Sussex'),('185','Tazewell'),('187','Warren'),('191','Washington'),
        ('193','Westmoreland'),('195','Wise'),('197','Wythe'),('199','York'),
        # Independent cities (major)
        ('510','Alexandria City'),('520','Bristol City'),('530','Buena Vista City'),
        ('540','Charlottesville City'),('550','Chesapeake City'),('570','Colonial Heights City'),
        ('580','Covington City'),('590','Danville City'),('595','Emporia City'),
        ('600','Fairfax City'),('610','Falls Church City'),('620','Franklin City'),
        ('630','Fredericksburg City'),('640','Galax City'),('650','Hampton City'),
        ('660','Harrisonburg City'),('670','Hopewell City'),('678','Lexington City'),
        ('680','Lynchburg City'),('683','Manassas City'),('685','Manassas Park City'),
        ('690','Martinsville City'),('700','Newport News City'),('710','Norfolk City'),
        ('720','Norton City'),('730','Petersburg City'),('735','Poquoson City'),
        ('740','Portsmouth City'),('750','Radford City'),('760','Richmond City'),
        ('770','Roanoke City'),('775','Salem City'),('790','Staunton City'),
        ('800','Suffolk City'),('810','Virginia Beach City'),('820','Waynesboro City'),
        ('830','Williamsburg City'),('840','Winchester City'),
    ],
    'WA': [
        ('001','Adams'),('003','Asotin'),('005','Benton'),('007','Chelan'),
        ('009','Clallam'),('011','Clark'),('013','Columbia'),('015','Cowlitz'),
        ('017','Douglas'),('019','Ferry'),('021','Franklin'),('023','Garfield'),
        ('025','Grant'),('027','Grays Harbor'),('029','Island'),('031','Jefferson'),
        ('033','King'),('035','Kitsap'),('037','Kittitas'),('039','Klickitat'),
        ('041','Lewis'),('043','Lincoln'),('045','Mason'),('047','Okanogan'),
        ('049','Pacific'),('051','Pend Oreille'),('053','Pierce'),('055','San Juan'),
        ('057','Skagit'),('059','Skamania'),('061','Snohomish'),('063','Spokane'),
        ('065','Stevens'),('067','Thurston'),('069','Wahkiakum'),('071','Walla Walla'),
        ('073','Whatcom'),('075','Whitman'),('077','Yakima'),
    ],
    'WV': [
        ('001','Barbour'),('003','Berkeley'),('005','Boone'),('007','Braxton'),
        ('009','Brooke'),('011','Cabell'),('013','Calhoun'),('015','Clay'),
        ('017','Doddridge'),('019','Fayette'),('021','Gilmer'),('023','Grant'),
        ('025','Greenbrier'),('027','Hampshire'),('029','Hancock'),('031','Hardy'),
        ('033','Harrison'),('035','Jackson'),('037','Jefferson'),('039','Kanawha'),
        ('041','Lewis'),('043','Lincoln'),('045','Logan'),('047','McDowell'),
        ('049','Marion'),('051','Marshall'),('053','Mason'),('055','Mercer'),
        ('057','Mineral'),('059','Mingo'),('061','Monongalia'),('063','Monroe'),
        ('065','Morgan'),('067','Nicholas'),('069','Ohio'),('071','Pendleton'),
        ('073','Pleasants'),('075','Pocahontas'),('077','Preston'),('079','Putnam'),
        ('081','Raleigh'),('083','Randolph'),('085','Ritchie'),('087','Roane'),
        ('089','Summers'),('091','Taylor'),('093','Tucker'),('095','Tyler'),
        ('097','Upshur'),('099','Wayne'),('101','Webster'),('103','Wetzel'),
        ('105','Wirt'),('107','Wood'),('109','Wyoming'),
    ],
    'WI': [
        ('001','Adams'),('003','Ashland'),('005','Barron'),('007','Bayfield'),
        ('009','Brown'),('011','Buffalo'),('013','Burnett'),('015','Calumet'),
        ('017','Chippewa'),('019','Clark'),('021','Columbia'),('023','Crawford'),
        ('025','Dane'),('027','Dodge'),('029','Door'),('031','Douglas'),
        ('033','Dunn'),('035','Eau Claire'),('037','Florence'),('039','Fond du Lac'),
        ('041','Forest'),('043','Grant'),('045','Green'),('047','Green Lake'),
        ('049','Iowa'),('051','Iron'),('053','Jackson'),('055','Jefferson'),
        ('057','Juneau'),('059','Kenosha'),('061','Kewaunee'),('063','La Crosse'),
        ('065','Lafayette'),('067','Langlade'),('069','Lincoln'),('071','Manitowoc'),
        ('073','Marathon'),('075','Marinette'),('077','Marquette'),('078','Menominee'),
        ('079','Milwaukee'),('081','Monroe'),('083','Oconto'),('085','Oneida'),
        ('087','Outagamie'),('089','Ozaukee'),('091','Pepin'),('093','Pierce'),
        ('095','Polk'),('097','Portage'),('099','Price'),('101','Racine'),
        ('103','Richland'),('105','Rock'),('107','Rusk'),('109','St. Croix'),
        ('111','Sauk'),('113','Sawyer'),('115','Shawano'),('117','Sheboygan'),
        ('119','Taylor'),('121','Trempealeau'),('123','Vernon'),('125','Vilas'),
        ('127','Walworth'),('129','Washburn'),('131','Washington'),('133','Waukesha'),
        ('135','Waupaca'),('137','Waushara'),('139','Winnebago'),('141','Wood'),
    ],
    'WY': [
        ('001','Albany'),('003','Big Horn'),('005','Campbell'),('007','Carbon'),
        ('009','Converse'),('011','Crook'),('013','Fremont'),('015','Goshen'),
        ('017','Hot Springs'),('019','Johnson'),('021','Laramie'),('023','Lincoln'),
        ('025','Natrona'),('027','Niobrara'),('029','Park'),('031','Platte'),
        ('033','Sheridan'),('035','Sublette'),('037','Sweetwater'),('039','Teton'),
        ('041','Uinta'),('043','Washakie'),('045','Weston'),
    ],
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def clamp(v, mn, mx):
    return max(mn, min(mx, v))

def norm(v, mn, mx):
    return clamp((v - mn) / (mx - mn), 0.0, 1.0)

def bws_label(bws):
    if bws < 1.0:
        return 'Low'
    elif bws < 2.0:
        return 'Low-Medium'
    elif bws < 3.0:
        return 'Medium-High'
    elif bws < 4.0:
        return 'High'
    else:
        return 'Extremely High'

def state_temp_offset(state):
    """Rough temperature offset from base formula to match known state averages."""
    offsets = {
        'AK': -30, 'MN': -10, 'ND': -10, 'WI': -8, 'MT': -8,
        'ME': -8, 'VT': -8, 'NH': -7, 'WY': -7, 'SD': -7,
        'MI': -5, 'ID': -5, 'CO': -5, 'IA': -4, 'NE': -4,
        'WA': -2, 'OR': -2, 'NY': -2, 'PA': -2, 'OH': -2,
        'IN': -2, 'IL': -2, 'MO': 0, 'KS': 0, 'WV': 0,
        'VA': 2, 'KY': 2, 'TN': 3, 'NC': 3, 'AR': 3,
        'SC': 4, 'GA': 5, 'AL': 5, 'MS': 5, 'LA': 7,
        'TX': 8, 'FL': 12, 'AZ': 10, 'NV': 6, 'NM': 4,
        'CA': 5, 'HI': 20,
    }
    return offsets.get(state, 0)

def generate_county_lat_lng(state, county_index, total_counties, state_bbox):
    """Distribute county centroids in a grid-like pattern within state bounds."""
    lat_min, lat_max, lng_min, lng_max = state_bbox
    # Distribute in a grid, then add jitter
    cols = max(1, int(math.sqrt(total_counties * 1.5)))
    row = county_index // cols
    col = county_index % cols
    rows = math.ceil(total_counties / cols)

    lat_step = (lat_max - lat_min) / max(rows, 1)
    lng_step = (lng_max - lng_min) / max(cols, 1)

    base_lat = lat_min + lat_step * (row + 0.5)
    base_lng = lng_min + lng_step * (col + 0.5)

    # Random jitter within cell boundaries
    jitter_lat = random.uniform(-lat_step * 0.35, lat_step * 0.35)
    jitter_lng = random.uniform(-lng_step * 0.35, lng_step * 0.35)

    lat = clamp(base_lat + jitter_lat, lat_min + 0.05, lat_max - 0.05)
    lng = clamp(base_lng + jitter_lng, lng_min + 0.05, lng_max - 0.05)
    return round(lat, 5), round(lng, 5)

def power_law_population(state, n_counties, state_pop):
    """Generate power-law distributed populations summing approximately to state_pop."""
    # Pareto distribution: most counties small, a few large
    weights = [random.paretovariate(1.5) for _ in range(n_counties)]
    total_w = sum(weights)
    pops = [max(500, int(w / total_w * state_pop)) for w in weights]
    return pops

def density_from_pop(pop, state, county_idx):
    """Rough density estimate: urban counties higher density."""
    base_density = pop / 400  # assume ~400 sqmi average county
    jitter = random.uniform(0.5, 2.0)
    return max(1, int(base_density * jitter))

def housing_from_pop(pop):
    """Estimate housing units from population (roughly 2.5 persons/household)."""
    return max(200, int(pop / 2.53 * random.uniform(0.9, 1.1)))

def cdd_from_temp_and_state(avg_temp_f, state):
    """Rough CDD estimate: warmer = more cooling days."""
    base_cdd = max(0, int((avg_temp_f - 65) * 15 + 500))
    return max(0, base_cdd + random.randint(-200, 200))


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------

def main():
    out_path = '/tmp/TheHeatMarket/data/county_scores.json'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    county_scores = []

    for state, counties in sorted(COUNTIES_BY_STATE.items()):
        state_fips = STATE_FIPS.get(state, '00')
        bbox = STATE_BBOX.get(state, (35.0, 45.0, -100.0, -80.0))
        lat_min, lat_max, lng_min, lng_max = bbox

        co2_base = STATE_CO2.get(state, 850.0)
        bws_base = STATE_BWS.get(state, 2.0)
        hdd_base = STATE_HDD.get(state, 4000)
        solar = STATE_SOLAR.get(state, 0.18)
        wind = STATE_WIND.get(state, 0.18)
        egrid_base = STATE_TO_EGRID.get(state, 'RFCE')
        state_pop_total = STATE_POP.get(state, 1_000_000)
        temp_offset = state_temp_offset(state)

        n = len(counties)
        pops = power_law_population(state, n, state_pop_total)

        for idx, (fips_suffix, county_name) in enumerate(counties):
            fips = state_fips + fips_suffix

            # Centroid
            lat, lng = generate_county_lat_lng(state, idx, n, bbox)

            # Per-county variations (jitter around state values)
            hdd = max(0, int(hdd_base * random.uniform(0.85, 1.15)))
            bws_raw = clamp(bws_base + random.uniform(-0.3, 0.3), 0.0, 5.0)

            # Temperature: derive from latitude + state offset + jitter
            avg_temp_f = round(
                clamp(110 - 1.5 * lat + temp_offset + random.uniform(-5, 5), 0, 110),
                1
            )

            # Humidity: east = more humid (higher, less negative lng)
            avg_humidity = int(clamp(85 - 0.15 * (lng + 125), 20, 85))
            avg_humidity = int(clamp(avg_humidity + random.randint(-5, 5), 20, 85))

            # eGRID: special case upstate NY
            egrid_code = egrid_base
            co2 = co2_base
            if state == 'NY' and lat > 42.5:
                egrid_code = 'NYUP'
                co2 = 249.0

            # Population / housing
            pop = pops[idx]
            housing_units = housing_from_pop(pop)
            density = density_from_pop(pop, state, idx)
            cdd = cdd_from_temp_and_state(avg_temp_f, state)

            # --- Score components (v2 formula) ---
            # Clean Energy (merged grid carbon + renewable potential)
            grid_sub = (1 - norm(co2, 200, 1600)) * 100       # grid CO2: lower = better
            renew_sub = norm(solar + wind, 0.20, 0.70) * 100  # solar+wind CF: higher = better
            clean_energy_s = 0.70 * grid_sub + 0.30 * renew_sub

            # Water stress: lower = better (0-4 normalized scale)
            water_s = (1 - norm(bws_raw, 0, 4)) * 100

            # Climate: cooler + drier = less cooling needed
            climate_s = (
                norm(clamp(95 - avg_temp_f, 0, 65), 0, 65) * 50
                + norm(clamp(90 - avg_humidity, 0, 70), 0, 70) * 50
            )

            # Heat demand: HDD (70%) + population density (30%)
            heat_hdd = norm(hdd, 0, 7500) * 100
            heat_density = norm(density, 0, 2000) * 100
            heat_d = 0.70 * heat_hdd + 0.30 * heat_density

            total = (
                0.15 * clean_energy_s
                + 0.25 * water_s
                + 0.25 * climate_s
                + 0.35 * heat_d
            )

            county_scores.append({
                'fips': fips,
                'county': county_name,
                'state': state,
                'lat': lat,
                'lng': lng,
                'total': round(total, 1),
                'clean_energy': round(clean_energy_s, 1),
                'water': round(water_s, 1),
                'climate': round(climate_s, 1),
                'heat': round(heat_d, 1),
                'co2_lbs_per_mwh': co2,
                'egrid': egrid_code,
                'bws_raw': round(bws_raw, 3),
                'bws_label': bws_label(bws_raw),
                'avg_temp_f': avg_temp_f,
                'hdd': hdd,
                'cdd': cdd,
                'avg_humidity': avg_humidity,
                'solar_cf': solar,
                'wind_cf': wind,
                'housing_units': housing_units,
                'density_per_sqmi': density,
                'pop': pop,
            })

    # Sort by total score descending
    county_scores.sort(key=lambda x: x['total'], reverse=True)

    with open(out_path, 'w') as f:
        json.dump({'counties': county_scores}, f, separators=(',', ':'))

    scores = [c['total'] for c in county_scores]
    print(f"Wrote {len(county_scores)} county scores to {out_path}")
    print(f"Score range: {min(scores):.1f} – {max(scores):.1f},  mean: {sum(scores)/len(scores):.1f}")
    print()
    print("Top 10 counties by total score:")
    for c in county_scores[:10]:
        print(f"  {c['county']}, {c['state']}  total={c['total']}  "
              f"energy={c['clean_energy']} water={c['water']} climate={c['climate']} "
              f"heat={c['heat']}")
    print()
    print("Bottom 10 counties by total score:")
    for c in county_scores[-10:]:
        print(f"  {c['county']}, {c['state']}  total={c['total']}  "
              f"energy={c['clean_energy']} water={c['water']} climate={c['climate']} "
              f"heat={c['heat']}")


if __name__ == '__main__':
    main()
