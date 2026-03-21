"""
Generate realistic static JSON datasets for HeatGrid.
"""

import json
import math
import random

random.seed(42)

# ---------------------------------------------------------------------------
# Master county definitions
# FIPS -> (name, state_abbr, lat, lng, region)
# Regions: west_arid, west_pacific, mountain, midwest, southeast, northeast, south_central
# ---------------------------------------------------------------------------

COUNTIES = {
    # Major metros (explicitly required)
    "06037": ("Los Angeles, CA", "CA", 34.05, -118.24, "west_arid"),   # Southern CA: warm, drier
    "17031": ("Cook, IL", "IL", 41.84, -87.82, "midwest"),
    "48201": ("Harris, TX", "TX", 29.85, -95.40, "south_central"),
    "04013": ("Maricopa, AZ", "AZ", 33.35, -112.49, "west_arid"),
    "06073": ("San Diego, CA", "CA", 32.72, -116.73, "west_arid"),    # Southern CA
    "48113": ("Dallas, TX", "TX", 32.77, -96.79, "south_central"),
    "53033": ("King, WA", "WA", 47.49, -121.83, "west_pacific"),
    "12086": ("Miami-Dade, FL", "FL", 25.55, -80.63, "southeast"),
    "48439": ("Tarrant, TX", "TX", 32.77, -97.29, "south_central"),
    "06065": ("Riverside, CA", "CA", 33.74, -115.99, "west_pacific"),
    "06085": ("Santa Clara, CA", "CA", 37.23, -121.69, "west_pacific"),
    "48029": ("Bexar, TX", "TX", 29.45, -98.52, "south_central"),
    "12011": ("Broward, FL", "FL", 26.15, -80.44, "southeast"),
    "32003": ("Clark, NV", "NV", 36.21, -115.01, "west_arid"),
    "06001": ("Alameda, CA", "CA", 37.65, -121.92, "west_pacific"),
    "06067": ("Sacramento, CA", "CA", 38.45, -121.34, "west_pacific"),
    "25017": ("Middlesex, MA", "MA", 42.48, -71.39, "northeast"),
    "26163": ("Wayne, MI", "MI", 42.28, -83.26, "midwest"),
    "27053": ("Hennepin, MN", "MN", 44.97, -93.39, "midwest"),
    "41051": ("Multnomah, OR", "OR", 45.55, -122.43, "west_pacific"),
    "08031": ("Denver, CO", "CO", 39.76, -104.88, "mountain"),
    "48453": ("Travis, TX", "TX", 30.22, -97.77, "south_central"),
    "51107": ("Loudoun, VA", "VA", 39.08, -77.64, "northeast"),
    "51059": ("Fairfax, VA", "VA", 38.84, -77.27, "northeast"),
    "24031": ("Montgomery, MD", "MD", 39.14, -77.21, "northeast"),
    "24033": ("Prince George's, MD", "MD", 38.83, -76.84, "northeast"),
    "24510": ("Baltimore City, MD", "MD", 39.29, -76.61, "northeast"),
    "42101": ("Philadelphia, PA", "PA", 40.00, -75.13, "northeast"),
    "42003": ("Allegheny, PA", "PA", 40.47, -79.99, "northeast"),
    "39049": ("Franklin, OH", "OH", 39.96, -82.99, "midwest"),
    "39061": ("Hamilton, OH", "OH", 39.22, -84.55, "midwest"),
    "39035": ("Cuyahoga, OH", "OH", 41.44, -81.68, "midwest"),
    "39153": ("Summit, OH", "OH", 41.12, -81.52, "midwest"),
    "39095": ("Lucas, OH", "OH", 41.59, -83.67, "midwest"),
    "39169": ("Wayne, OH", "OH", 40.82, -81.89, "midwest"),
    "18097": ("Marion, IN", "IN", 39.77, -86.14, "midwest"),
    "18003": ("Allen, IN", "IN", 41.08, -85.07, "midwest"),
    "29510": ("St. Louis City, MO", "MO", 38.64, -90.24, "midwest"),
    "29095": ("Jackson, MO", "MO", 39.00, -94.35, "midwest"),
    "55079": ("Milwaukee, WI", "WI", 43.03, -87.97, "midwest"),
    "55025": ("Dane, WI", "WI", 43.07, -89.41, "midwest"),
    "55133": ("Waukesha, WI", "WI", 43.01, -88.30, "midwest"),
    "01073": ("Jefferson, AL", "AL", 33.55, -86.89, "southeast"),
    "47157": ("Shelby, TN", "TN", 35.18, -89.90, "southeast"),
    "47037": ("Davidson, TN", "TN", 36.17, -86.79, "southeast"),
    "47093": ("Knox, TN", "TN", 35.99, -83.93, "southeast"),
    "37119": ("Mecklenburg, NC", "NC", 35.25, -80.84, "southeast"),
    "37183": ("Wake, NC", "NC", 35.79, -78.64, "southeast"),
    "37063": ("Durham, NC", "NC", 35.99, -78.90, "southeast"),
    "37081": ("Guilford, NC", "NC", 36.07, -79.79, "southeast"),
    "45079": ("Richland, SC", "SC", 34.03, -80.90, "southeast"),
    "45019": ("Charleston, SC", "SC", 32.80, -80.02, "southeast"),
    "13121": ("Fulton, GA", "GA", 33.79, -84.47, "southeast"),
    "13089": ("DeKalb, GA", "GA", 33.77, -84.22, "southeast"),
    "13135": ("Gwinnett, GA", "GA", 33.97, -84.00, "southeast"),
    "12095": ("Orange, FL", "FL", 28.51, -81.37, "southeast"),
    "12057": ("Hillsborough, FL", "FL", 27.97, -82.37, "southeast"),
    "12099": ("Palm Beach, FL", "FL", 26.65, -80.45, "southeast"),
    "12031": ("Duval, FL", "FL", 30.33, -81.66, "southeast"),
    "12103": ("Pinellas, FL", "FL", 27.90, -82.74, "southeast"),
    "12073": ("Leon, FL", "FL", 30.46, -84.28, "southeast"),
    "22033": ("East Baton Rouge, LA", "LA", 30.53, -91.10, "southeast"),
    "22051": ("Jefferson, LA", "LA", 29.83, -90.17, "southeast"),
    "22071": ("Orleans, LA", "LA", 29.95, -90.07, "southeast"),
    "28049": ("Hinds, MS", "MS", 32.27, -90.44, "southeast"),
    "28089": ("Madison, MS", "MS", 32.63, -90.02, "southeast"),
    "05119": ("Pulaski, AR", "AR", 34.77, -92.31, "southeast"),
    "40109": ("Oklahoma, OK", "OK", 35.55, -97.40, "south_central"),
    "40143": ("Tulsa, OK", "OK", 36.12, -95.93, "south_central"),
    "20173": ("Sedgwick, KS", "KS", 37.69, -97.44, "midwest"),
    "20091": ("Johnson, KS", "KS", 38.88, -94.83, "midwest"),
    "31055": ("Douglas, NE", "NE", 41.30, -96.15, "midwest"),
    "31109": ("Lancaster, NE", "NE", 40.79, -96.69, "midwest"),
    "46099": ("Minnehaha, SD", "SD", 43.67, -96.73, "midwest"),
    "46103": ("Pennington, SD", "SD", 44.08, -103.23, "mountain"),
    "27109": ("Olmsted, MN", "MN", 44.02, -92.46, "midwest"),
    "27145": ("Stearns, MN", "MN", 45.54, -94.65, "midwest"),
    "55009": ("Brown, WI", "WI", 44.47, -88.03, "midwest"),
    "55087": ("Outagamie, WI", "WI", 44.41, -88.46, "midwest"),
    "26077": ("Kalamazoo, MI", "MI", 42.24, -85.53, "midwest"),
    "26081": ("Kent, MI", "MI", 43.03, -85.55, "midwest"),
    "26065": ("Ingham, MI", "MI", 42.60, -84.41, "midwest"),
    "26161": ("Washtenaw, MI", "MI", 42.25, -83.93, "midwest"),
    "26049": ("Genesee, MI", "MI", 43.01, -83.71, "midwest"),
    "26099": ("Macomb, MI", "MI", 42.67, -82.92, "midwest"),
    "26125": ("Oakland, MI", "MI", 42.66, -83.38, "midwest"),
    "34025": ("Monmouth, NJ", "NJ", 40.29, -74.16, "northeast"),
    "34003": ("Bergen, NJ", "NJ", 40.96, -74.07, "northeast"),
    "34013": ("Essex, NJ", "NJ", 40.79, -74.25, "northeast"),
    "34017": ("Hudson, NJ", "NJ", 40.73, -74.07, "northeast"),
    "34023": ("Middlesex, NJ", "NJ", 40.44, -74.41, "northeast"),
    "36059": ("Nassau, NY", "NY", 40.73, -73.59, "northeast"),
    "36103": ("Suffolk, NY", "NY", 40.88, -72.83, "northeast"),
    "36119": ("Westchester, NY", "NY", 41.13, -73.77, "northeast"),
    "36055": ("Monroe, NY", "NY", 43.17, -77.60, "northeast"),
    "36067": ("Onondaga, NY", "NY", 43.00, -76.20, "northeast"),
    "36029": ("Erie, NY", "NY", 42.76, -78.85, "northeast"),
    "36001": ("Albany, NY", "NY", 42.60, -73.97, "northeast"),
    "09001": ("Fairfield, CT", "CT", 41.27, -73.38, "northeast"),
    "09003": ("Hartford, CT", "CT", 41.80, -72.73, "northeast"),
    "09009": ("New Haven, CT", "CT", 41.35, -72.90, "northeast"),
    "44007": ("Providence, RI", "RI", 41.82, -71.51, "northeast"),
    "25015": ("Hampshire, MA", "MA", 42.34, -72.67, "northeast"),
    "25027": ("Worcester, MA", "MA", 42.35, -71.97, "northeast"),
    "25009": ("Essex, MA", "MA", 42.65, -70.97, "northeast"),
    "25021": ("Norfolk, MA", "MA", 42.17, -71.19, "northeast"),
    "25005": ("Bristol, MA", "MA", 41.79, -71.09, "northeast"),
    "33015": ("Rockingham, NH", "NH", 43.00, -71.14, "northeast"),
    "23005": ("Cumberland, ME", "ME", 43.82, -70.37, "northeast"),
    "50007": ("Chittenden, VT", "VT", 44.47, -73.09, "northeast"),
    "35001": ("Bernalillo, NM", "NM", 35.06, -106.67, "west_arid"),
    "35013": ("Dona Ana, NM", "NM", 32.35, -106.83, "west_arid"),
    "48141": ("El Paso, TX", "TX", 31.77, -106.42, "west_arid"),
    "48303": ("Lubbock, TX", "TX", 33.61, -101.82, "south_central"),
    "48479": ("Webb, TX", "TX", 27.76, -99.47, "south_central"),
    "48215": ("Hidalgo, TX", "TX", 26.40, -98.18, "south_central"),
    "48355": ("Nueces, TX", "TX", 27.73, -97.55, "south_central"),
    "48245": ("Jefferson, TX", "TX", 30.08, -94.20, "south_central"),
    "48167": ("Galveston, TX", "TX", 29.30, -94.79, "south_central"),
    "48157": ("Fort Bend, TX", "TX", 29.53, -95.77, "south_central"),
    "48085": ("Collin, TX", "TX", 33.19, -96.57, "south_central"),
    "48121": ("Denton, TX", "TX", 33.21, -97.13, "south_central"),
    "48491": ("Williamson, TX", "TX", 30.65, -97.60, "south_central"),
    "48209": ("Hays, TX", "TX", 29.98, -98.05, "south_central"),
    "48423": ("Smith, TX", "TX", 32.37, -95.27, "south_central"),
    "48309": ("McLennan, TX", "TX", 31.55, -97.17, "south_central"),
    "48027": ("Bell, TX", "TX", 31.04, -97.47, "south_central"),
    "48061": ("Cameron, TX", "TX", 26.16, -97.57, "south_central"),
    "04019": ("Pima, AZ", "AZ", 32.00, -111.01, "west_arid"),
    "04021": ("Pinal, AZ", "AZ", 32.91, -111.36, "west_arid"),
    "04025": ("Yavapai, AZ", "AZ", 34.60, -112.47, "west_arid"),
    "04015": ("Mohave, AZ", "AZ", 35.72, -113.75, "west_arid"),
    "04027": ("Yuma, AZ", "AZ", 32.77, -113.92, "west_arid"),
    "04005": ("Coconino, AZ", "AZ", 36.23, -111.75, "west_arid"),
    "04001": ("Apache, AZ", "AZ", 35.40, -109.49, "west_arid"),
    "04017": ("Navajo, AZ", "AZ", 35.79, -110.32, "west_arid"),
    "32031": ("Washoe, NV", "NV", 40.60, -119.80, "west_arid"),
    "32510": ("Carson City, NV", "NV", 39.15, -119.75, "west_arid"),
    "16001": ("Ada, ID", "ID", 43.45, -116.24, "mountain"),
    "16027": ("Canyon, ID", "ID", 43.63, -116.68, "mountain"),
    "16019": ("Bonneville, ID", "ID", 43.38, -112.02, "mountain"),
    "16055": ("Kootenai, ID", "ID", 47.66, -116.73, "mountain"),
    "30111": ("Yellowstone, MT", "MT", 45.78, -108.50, "mountain"),
    "30013": ("Cascade, MT", "MT", 47.45, -111.22, "mountain"),
    "30063": ("Missoula, MT", "MT", 46.92, -114.07, "mountain"),
    "30093": ("Silver Bow, MT", "MT", 45.90, -112.66, "mountain"),
    "30031": ("Gallatin, MT", "MT", 45.68, -111.16, "mountain"),
    "56025": ("Natrona, WY", "WY", 42.96, -106.79, "mountain"),
    "56021": ("Laramie, WY", "WY", 41.31, -105.59, "mountain"),
    "56005": ("Campbell, WY", "WY", 44.25, -105.55, "mountain"),
    "49035": ("Salt Lake, UT", "UT", 40.67, -111.92, "mountain"),
    "49049": ("Utah, UT", "UT", 40.12, -111.66, "mountain"),
    "49057": ("Weber, UT", "UT", 41.26, -111.97, "mountain"),
    "49011": ("Davis, UT", "UT", 41.02, -112.08, "mountain"),
    "49053": ("Washington, UT", "UT", 37.33, -113.53, "west_arid"),
    "49005": ("Cache, UT", "UT", 41.73, -111.75, "mountain"),
    "08041": ("El Paso, CO", "CO", 38.83, -104.52, "mountain"),
    "08069": ("Larimer, CO", "CO", 40.66, -105.46, "mountain"),
    "08123": ("Weld, CO", "CO", 40.56, -104.40, "mountain"),
    "08005": ("Arapahoe, CO", "CO", 39.65, -104.34, "mountain"),
    "08059": ("Jefferson, CO", "CO", 39.59, -105.19, "mountain"),
    "08001": ("Adams, CO", "CO", 39.87, -104.34, "mountain"),
    "08013": ("Boulder, CO", "CO", 40.09, -105.36, "mountain"),
    "08101": ("Pueblo, CO", "CO", 38.18, -104.51, "mountain"),
    "53063": ("Spokane, WA", "WA", 47.62, -117.42, "west_pacific"),
    "53053": ("Pierce, WA", "WA", 47.06, -122.16, "west_pacific"),
    "53061": ("Snohomish, WA", "WA", 47.98, -121.74, "west_pacific"),
    "53011": ("Clark, WA", "WA", 45.79, -122.49, "west_pacific"),
    "53067": ("Thurston, WA", "WA", 47.05, -122.86, "west_pacific"),
    "53073": ("Whatcom, WA", "WA", 48.83, -121.82, "west_pacific"),
    "53077": ("Yakima, WA", "WA", 46.47, -120.51, "west_pacific"),
    "41039": ("Lane, OR", "OR", 43.94, -122.62, "west_pacific"),
    "41047": ("Marion, OR", "OR", 44.90, -122.57, "west_pacific"),
    "41067": ("Washington, OR", "OR", 45.56, -123.08, "west_pacific"),
    "41005": ("Clackamas, OR", "OR", 45.19, -122.22, "west_pacific"),
    "41029": ("Jackson, OR", "OR", 42.42, -122.74, "west_pacific"),
    "41017": ("Deschutes, OR", "OR", 43.91, -121.22, "mountain"),
}

# ---------------------------------------------------------------------------
# Regional parameters
# ---------------------------------------------------------------------------

REGION_PARAMS = {
    "west_arid": {
        "bws_range": (3.0, 5.0),
        "temp_range": (58, 80),
        "hdd_range": (1500, 4500),
        "cdd_range": (1500, 4000),
        "humidity_range": (20, 38),
        "co2": 825,         # TX/AZ mix; override by state below
        "renewable_base": 0.42,
    },
    "west_pacific": {
        "bws_range": (1.5, 3.5),
        "temp_range": (48, 65),
        "hdd_range": (2000, 5500),
        "cdd_range": (200, 900),
        "humidity_range": (60, 80),
        "co2": 600,
        "renewable_base": 0.44,
    },
    "mountain": {
        "bws_range": (2.0, 4.0),
        "temp_range": (42, 58),
        "hdd_range": (5000, 9000),
        "cdd_range": (100, 800),
        "humidity_range": (30, 50),
        "co2": 700,
        "renewable_base": 0.40,
    },
    "midwest": {
        "bws_range": (0.3, 1.5),
        "temp_range": (46, 58),
        "hdd_range": (5000, 8500),
        "cdd_range": (600, 1600),
        "humidity_range": (62, 78),
        "co2": 1050,
        "renewable_base": 0.38,
    },
    "southeast": {
        "bws_range": (0.8, 2.5),
        "temp_range": (62, 76),
        "hdd_range": (800, 3000),
        "cdd_range": (1800, 3500),
        "humidity_range": (70, 85),
        "co2": 870,
        "renewable_base": 0.30,
    },
    "northeast": {
        "bws_range": (0.3, 1.5),
        "temp_range": (44, 56),
        "hdd_range": (4500, 7500),
        "cdd_range": (400, 1200),
        "humidity_range": (62, 76),
        "co2": 550,
        "renewable_base": 0.28,
    },
    "south_central": {
        "bws_range": (1.2, 3.5),
        "temp_range": (62, 74),
        "hdd_range": (1000, 3500),
        "cdd_range": (2000, 3800),
        "humidity_range": (55, 75),
        "co2": 825,
        "renewable_base": 0.40,
    },
}

# State-level CO2 overrides (lbs/MWh approximate)
STATE_CO2 = {
    "WA": 635, "OR": 635, "ID": 635,
    "CA": 520,
    "TX": 825,
    "FL": 900,
    "NY": 550, "MA": 550, "CT": 550, "RI": 550, "NH": 550, "VT": 550, "ME": 550,
    "NJ": 550, "PA": 550, "MD": 550, "VA": 550, "DE": 550,
    "IL": 1050, "OH": 1050, "MI": 1050, "WI": 1050, "MN": 1050,
    "IN": 1050, "MO": 1050, "KS": 1050, "NE": 1050, "SD": 1050, "ND": 1050,
    "AL": 870, "GA": 870, "SC": 870, "NC": 870, "TN": 870, "MS": 870,
    "AR": 870, "LA": 870,
    "OK": 825, "AZ": 825, "NM": 825,
    "NV": 700, "UT": 700, "CO": 700, "MT": 700, "WY": 700, "ID": 635,
}

# Population data (realistic approximations)
POPULATION_DATA = {
    "06037": (10014009, 3501458, 2344, 34.05, -118.24),
    "17031": (5275541, 2173344, 5672, 41.84, -87.82),
    "48201": (4731145, 1764497, 2843, 29.85, -95.40),
    "04013": (4485414, 1871576, 475, 33.35, -112.49),
    "06073": (3338330, 1176544, 811, 32.72, -116.73),
    "48113": (2613539, 1030406, 3719, 32.77, -96.79),
    "53033": (2269675, 919922, 986, 47.49, -121.83),
    "12086": (2716940, 1050220, 1413, 25.55, -80.63),
    "48439": (2110640, 817823, 2279, 32.77, -97.29),
    "06065": (2457590, 837305, 312, 33.74, -115.99),
    "06085": (1927852, 672225, 1747, 37.23, -121.69),
    "48029": (2009324, 762613, 1454, 29.45, -98.52),
    "12011": (1952778, 759320, 1649, 26.15, -80.44),
    "32003": (2266715, 922047, 568, 36.21, -115.01),
    "06001": (1682353, 637070, 2123, 37.65, -121.92),
    "06067": (1585055, 604684, 1618, 38.45, -121.34),
    "25017": (1632002, 610229, 1907, 42.48, -71.39),
    "26163": (1749343, 715120, 3373, 42.28, -83.26),
    "27053": (1281565, 545433, 1989, 44.97, -93.39),
    "41051": (815428, 352091, 1801, 45.55, -122.43),
    "08031": (715878, 317872, 4493, 39.76, -104.88),
    "48453": (1290188, 531344, 804, 30.22, -97.77),
    "51107": (420959, 152219, 1036, 39.08, -77.64),
    "51059": (1150309, 418454, 3085, 38.84, -77.27),
    "24031": (1062061, 393248, 2074, 39.14, -77.21),
    "24033": (967201, 335519, 1799, 38.83, -76.84),
    "24510": (585708, 253978, 7671, 39.29, -76.61),
    "42101": (1576251, 673896, 11683, 40.00, -75.13),
    "42003": (1218452, 533867, 1648, 40.47, -79.99),
    "39049": (1323807, 568714, 3023, 39.96, -82.99),
    "39061": (826518, 360714, 2131, 39.22, -84.55),
    "39035": (1264817, 550948, 2877, 41.44, -81.68),
    "39153": (541228, 235841, 1459, 41.12, -81.52),
    "39095": (436490, 190210, 935, 41.59, -83.67),
    "39169": (139909, 60234, 230, 40.82, -81.89),
    "18097": (964582, 406612, 2243, 39.77, -86.14),
    "18003": (385810, 164521, 1015, 41.08, -85.07),
    "29510": (308626, 151124, 5210, 38.64, -90.24),
    "29095": (714034, 294103, 1455, 39.00, -94.35),
    "55079": (945726, 394321, 3881, 43.03, -87.97),
    "55025": (561504, 231413, 425, 43.07, -89.41),
    "55133": (404198, 163321, 875, 43.01, -88.30),
    "01073": (674721, 283415, 793, 33.55, -86.89),
    "47157": (929744, 380209, 1371, 35.18, -89.90),
    "47037": (715884, 311022, 1282, 36.17, -86.79),
    "47093": (478971, 204321, 878, 35.99, -83.93),
    "37119": (1110356, 450211, 1055, 35.25, -80.84),
    "37183": (1129410, 462104, 1255, 35.79, -78.64),
    "37063": (324734, 138012, 902, 35.99, -78.90),
    "37081": (541299, 222414, 729, 36.07, -79.79),
    "45079": (415759, 175621, 512, 34.03, -80.90),
    "45019": (411406, 177321, 278, 32.80, -80.02),
    "13121": (1066710, 458201, 1959, 33.79, -84.47),
    "13089": (764382, 308012, 2847, 33.77, -84.22),
    "13135": (957062, 369043, 2037, 33.97, -84.00),
    "12095": (1429908, 568921, 1321, 28.51, -81.37),
    "12057": (1459762, 601204, 1362, 27.97, -82.37),
    "12099": (1496770, 638412, 727, 26.65, -80.45),
    "12031": (995318, 419204, 1109, 30.33, -81.66),
    "12103": (974996, 453021, 3476, 27.90, -82.74),
    "12073": (294071, 123412, 383, 30.46, -84.28),
    "22033": (456781, 184321, 512, 30.53, -91.10),
    "22051": (432552, 178214, 1897, 29.83, -90.17),
    "22071": (383997, 190321, 2082, 29.95, -90.07),
    "28049": (229926, 94321, 280, 32.27, -90.44),
    "28089": (107046, 42321, 183, 32.63, -90.02),
    "05119": (399125, 167321, 532, 34.77, -92.31),
    "40109": (796292, 334021, 1168, 35.55, -97.40),
    "40143": (669279, 280412, 948, 36.12, -95.93),
    "20173": (523824, 215321, 600, 37.69, -97.44),
    "20091": (609863, 237412, 1384, 38.88, -94.83),
    "31055": (576858, 234321, 1459, 41.30, -96.15),
    "31109": (319090, 129321, 327, 40.79, -96.69),
    "46099": (197214, 83012, 190, 43.67, -96.73),
    "46103": (113775, 51012, 25, 44.08, -103.23),
    "27109": (158293, 67412, 235, 44.02, -92.46),
    "27145": (159,    67000, 65, 45.54, -94.65),  # placeholder fixed below
    "55009": (264542, 108321, 452, 44.47, -88.03),
    "55087": (187885, 77412, 368, 44.41, -88.46),
    "26077": (265066, 110321, 423, 42.24, -85.53),
    "26081": (643140, 264021, 1062, 43.03, -85.55),
    "26065": (292406, 120321, 484, 42.60, -84.41),
    "26161": (372258, 153021, 540, 42.25, -83.93),
    "26049": (405813, 168321, 747, 43.01, -83.71),
    "26099": (881217, 354021, 1769, 42.67, -82.92),
    "26125": (1274395, 508321, 1477, 42.66, -83.38),
    "34025": (643615, 250321, 1318, 40.29, -74.16),
    "34003": (955732, 340321, 3918, 40.96, -74.07),
    "34013": (863728, 320321, 6286, 40.79, -74.25),
    "34017": (724854, 257321, 13440, 40.73, -74.07),
    "34023": (863162, 307021, 2692, 40.44, -74.41),
    "36059": (1395774, 501321, 4622, 40.73, -73.59),
    "36103": (1525920, 551321, 1696, 40.88, -72.83),
    "36119": (1004457, 362321, 2165, 41.13, -73.77),
    "36055": (744248, 311321, 1768, 43.17, -77.60),
    "36067": (476516, 201321, 751, 43.00, -76.20),
    "36029": (918702, 394321, 1406, 42.76, -78.85),
    "36001": (314848, 138321, 806, 42.60, -73.97),
    "09001": (973383, 364321, 1452, 41.27, -73.38),
    "09003": (898977, 361321, 1148, 41.80, -72.73),
    "09009": (864835, 349321, 1400, 41.35, -72.90),
    "44007": (663001, 266321, 1518, 41.82, -71.51),
    "25015": (161355, 66321, 321, 42.34, -72.67),
    "25027": (838318, 326321, 849, 42.35, -71.97),
    "25009": (789034, 305321, 1248, 42.65, -70.97),
    "25021": (706775, 273021, 1724, 42.17, -71.19),
    "25005": (565217, 224021, 1337, 41.79, -71.09),
    "33015": (307086, 128321, 480, 43.00, -71.14),
    "23005": (296214, 128321, 322, 43.82, -70.37),
    "50007": (168323, 73321, 400, 44.47, -73.09),
    "35001": (679121, 277321, 661, 35.06, -106.67),
    "35013": (218195, 88321, 98, 32.35, -106.83),
    "48141": (865657, 306321, 821, 31.77, -106.42),
    "48303": (314193, 126321, 165, 33.61, -101.82),
    "48479": (266772, 97321, 90, 27.76, -99.47),
    "48215": (870781, 264321, 670, 26.40, -98.18),
    "48355": (346534, 141321, 399, 27.73, -97.55),
    "48245": (252273, 105321, 373, 30.08, -94.20),
    "48167": (342139, 149321, 676, 29.30, -94.79),
    "48157": (811688, 290321, 979, 29.53, -95.77),
    "48085": (1005146, 370321, 2132, 33.19, -96.57),
    "48121": (906422, 341321, 920, 33.21, -97.13),
    "48491": (609017, 223321, 609, 30.65, -97.60),
    "48209": (263959, 102321, 252, 29.98, -98.05),
    "48423": (234769, 97321, 175, 32.37, -95.27),
    "48309": (264004, 106321, 155, 31.55, -97.17),
    "48027": (362924, 138321, 268, 31.04, -97.47),
    "48061": (423163, 151321, 588, 26.16, -97.57),
    "04019": (1066454, 419321, 97, 32.00, -111.01),
    "04021": (446902, 175321, 83, 32.91, -111.36),
    "04025": (245883, 112321, 15, 34.60, -112.47),
    "04015": (213267, 97321, 6, 35.72, -113.75),
    "04027": (213787, 88321, 40, 32.77, -113.92),
    "04005": (145101, 68321, 4, 36.23, -111.75),
    "04001": (72125, 27321, 3, 35.40, -109.49),
    "04017": (109926, 43321, 5, 35.79, -110.32),
    "32031": (469587, 193321, 125, 40.60, -119.80),
    "32510": (58639, 27321, 878, 39.15, -119.75),
    "16001": (486492, 188321, 309, 43.45, -116.24),
    "16027": (231799, 88321, 127, 43.63, -116.68),
    "16019": (119429, 46321, 65, 43.38, -112.02),
    "16055": (171362, 72321, 115, 47.66, -116.73),
    "30111": (159798, 68321, 48, 45.78, -108.50),
    "30013": (83012, 36321, 42, 47.45, -111.22),
    "30063": (119600, 52321, 65, 46.92, -114.07),
    "30093": (34915, 15321, 36, 45.90, -112.66),
    "30031": (118960, 50321, 42, 45.68, -111.16),
    "56025": (75450, 31321, 10, 42.96, -106.79),
    "56021": (99500, 41321, 22, 41.31, -105.59),
    "56005": (46341, 18321, 6, 44.25, -105.55),
    "49035": (1160437, 413321, 1386, 40.67, -111.92),
    "49049": (636235, 229321, 429, 40.12, -111.66),
    "49057": (256828, 97321, 428, 41.26, -111.97),
    "49011": (363392, 128321, 851, 41.02, -112.08),
    "49053": (180279, 71321, 80, 37.33, -113.53),
    "49005": (128289, 47321, 92, 41.73, -111.75),
    "08041": (720403, 289321, 244, 38.83, -104.52),
    "08069": (359066, 144321, 163, 40.66, -105.46),
    "08123": (322571, 127321, 59, 40.56, -104.40),
    "08005": (656590, 264321, 2313, 39.65, -104.34),
    "08059": (582881, 233321, 844, 39.59, -105.19),
    "08001": (519672, 203321, 1507, 39.87, -104.34),
    "08013": (330758, 138321, 437, 40.09, -105.36),
    "08101": (168424, 70321, 145, 38.18, -104.51),
    "53063": (522798, 215321, 282, 47.62, -117.42),
    "53053": (921173, 359321, 464, 47.06, -122.16),
    "53061": (827957, 320321, 376, 47.98, -121.74),
    "53011": (503320, 194321, 548, 45.79, -122.49),
    "53067": (290536, 119321, 282, 47.05, -122.86),
    "53073": (229247, 95321, 93, 48.83, -121.82),
    "53077": (250873, 101321, 63, 46.47, -120.51),
    "41039": (382971, 160321, 86, 43.94, -122.62),
    "41047": (345920, 140321, 180, 44.90, -122.57),
    "41067": (616074, 243321, 545, 45.56, -123.08),
    "41005": (428204, 173321, 148, 45.19, -122.22),
    "41029": (220944, 95321, 78, 42.42, -122.74),
    "41017": (198253, 88321, 40, 43.91, -121.22),
}

# Fix the Stearns MN population entry that had a typo
POPULATION_DATA["27145"] = (159,    67000, 65, 45.54, -94.65)
POPULATION_DATA["27145"] = (161448, 67412, 65, 45.54, -94.65)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def lerp(lo, hi, t):
    return lo + (hi - lo) * t

def jitter(v, pct=0.08):
    """Add small random jitter."""
    return v * (1 + random.uniform(-pct, pct))

def get_bws_label(raw):
    if raw < 1.0:
        return "Low"
    elif raw < 2.0:
        return "Low-Medium"
    elif raw < 3.0:
        return "Medium-High"
    elif raw < 4.0:
        return "High"
    else:
        return "Extremely High"

def generate_county_data():
    water_counties = {}
    climate_counties = {}
    population_counties = {}
    scores_counties = {}

    for fips, (name, state, lat, lng, region) in COUNTIES.items():
        params = REGION_PARAMS[region]

        # --- Water Stress ---
        bws_lo, bws_hi = params["bws_range"]
        bws_raw = round(jitter(random.uniform(bws_lo, bws_hi), 0.05), 2)
        water_counties[fips] = {
            "bws_raw": bws_raw,
            "label": get_bws_label(bws_raw),
            "county": name,
        }

        # --- Climate ---
        temp_lo, temp_hi = params["temp_range"]
        hdd_lo, hdd_hi = params["hdd_range"]
        cdd_lo, cdd_hi = params["cdd_range"]
        hum_lo, hum_hi = params["humidity_range"]

        avg_temp_f = round(jitter(random.uniform(temp_lo, temp_hi), 0.03), 1)
        hdd = int(jitter(random.uniform(hdd_lo, hdd_hi), 0.05))
        cdd = int(jitter(random.uniform(cdd_lo, cdd_hi), 0.05))
        avg_humidity = int(jitter(random.uniform(hum_lo, hum_hi), 0.04))
        climate_counties[fips] = {
            "avg_temp_f": avg_temp_f,
            "hdd": hdd,
            "cdd": cdd,
            "avg_humidity": avg_humidity,
        }

        # --- Population ---
        if fips in POPULATION_DATA:
            pop, housing_units, density, plat, plng = POPULATION_DATA[fips]
        else:
            pop = random.randint(50000, 500000)
            housing_units = int(pop / random.uniform(2.4, 2.9))
            density = random.randint(50, 2000)
            plat, plng = lat, lng

        population_counties[fips] = {
            "pop": pop,
            "housing_units": housing_units,
            "density_per_sqmi": density,
            "lat": plat,
            "lng": plng,
        }

        # --- Scores ---
        co2 = STATE_CO2.get(state, params["co2"])
        grid_carbon_score = round(
            100 - clamp((co2 - 600) / (1800 - 600), 0, 1) * 100, 1
        )

        water_stress_score = round(
            100 - clamp(bws_raw / 5, 0, 1) * 100, 1
        )

        climate_score = round(
            clamp((95 - avg_temp_f) / 65, 0, 1) * 50
            + clamp((90 - avg_humidity) / 70, 0, 1) * 50,
            1,
        )

        renewable_base = params["renewable_base"]
        # Add small state-level jitter
        renewable_raw = jitter(renewable_base, 0.10)
        renewable_score = round(clamp(renewable_raw / 0.50, 0, 1) * 100, 1)

        heat_demand_score = round(
            clamp(
                (hdd * housing_units / 1_000_000 - 1) / 19,
                0, 1
            ) * 100,
            1,
        )

        total_score = round(
            0.25 * grid_carbon_score
            + 0.25 * water_stress_score
            + 0.20 * climate_score
            + 0.10 * renewable_score
            + 0.20 * heat_demand_score,
            1,
        )

        scores_counties[fips] = {
            "lat": plat,
            "lng": plng,
            "county": name,
            "grid_carbon_score": grid_carbon_score,
            "water_stress_score": water_stress_score,
            "climate_score": climate_score,
            "renewable_score": renewable_score,
            "heat_demand_score": heat_demand_score,
            "total_score": total_score,
        }

    return water_counties, climate_counties, population_counties, scores_counties


def main():
    import os
    data_dir = "/tmp/TheHeatMarket/data"
    os.makedirs(data_dir, exist_ok=True)

    water, climate, population, scores = generate_county_data()

    files = {
        "water_stress_by_county.json": {"counties": water},
        "climate_by_county.json": {"counties": climate},
        "population_by_county.json": {"counties": population},
        "county_scores.json": {"counties": scores},
    }

    for filename, data in files.items():
        path = os.path.join(data_dir, filename)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        county_count = len(data["counties"])
        print(f"Wrote {path} ({county_count} counties)")

    print(f"\nTotal counties defined: {len(COUNTIES)}")
    print("Done.")


if __name__ == "__main__":
    main()
