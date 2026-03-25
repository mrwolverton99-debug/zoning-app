# City configurations for multi-city support
# Each city defines its GIS endpoints, district codes, data paths, and bounding box

CITIES = {
    "garland": {
        "name": "City of Garland, TX",
        "display_name": "Garland, TX",
        "state": "TX",
        "timezone": "America/Chicago",

        # Bounding box for geocoder validation [min_lat, max_lat, min_lng, max_lng]
        "bounds": [32.85, 33.05, -96.75, -96.55],

        # DCAD data file
        "dcad_file": "data/ACCOUNT_INFO.CSV",
        "dcad_city_filter": "GARLAND (DALLAS CO)",

        # Land use matrix CSVs
        "matrix_file": "data/garland_land_use_matrix.csv",
        "dt_matrix_file": "data/garland_dt_land_use_matrix.csv",

        # GIS endpoints
        "gis": {
            "address": "https://maps.garlandtx.gov/arcgis/rest/services/Planning/GarlandZoningWebmap/MapServer/3/query",
            "zoning":  "https://maps.garlandtx.gov/arcgis/rest/services/Planning/GarlandZoningWebmap/MapServer/0/query",
            "flum":    "https://maps.garlandtx.gov/arcgis/rest/services/Planning/GarlandZoningWebmap/MapServer/1/query",
            "dao":     "https://maps.garlandtx.gov/arcgis/rest/services/Planning/GarlandZoningWebmap/MapServer/6/query",
        },

        # Districts that have sub-district detection
        "subdistricts": {
            "DT": ["DS", "DH", "U", "IR", "SC"],
        },

        # Planning department contact
        "planning_phone": "972-205-2454",
        "planning_email": "planning@garlandtx.gov",
        "planning_url": "https://www.garlandtx.gov/3316/Zoning",

        # Geocoder search suffix
        "geocoder_suffix": "Garland, TX 75040",
    }
}

DEFAULT_CITY = "garland"


def get_city(city_key: str = None) -> dict:
    key = city_key or DEFAULT_CITY
    if key not in CITIES:
        raise ValueError(f"Unknown city: {key}")
    return CITIES[key]


def get_city_keys() -> list:
    return list(CITIES.keys())