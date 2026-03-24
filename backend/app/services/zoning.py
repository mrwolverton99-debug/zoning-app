import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

class LegacySSL(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.set_ciphers('DEFAULT')
        ctx.check_hostname = False
        ctx.verify_mode = 0
        kwargs['ssl_context'] = ctx
        super().init_poolmanager(*args, **kwargs)

def get_session():
    s = requests.Session()
    s.mount('https://', LegacySSL())
    return s

ADDRESS_URL = "https://maps.garlandtx.gov/arcgis/rest/services/Planning/GarlandZoningWebmap/MapServer/3/query"
ZONING_URL = "https://maps.garlandtx.gov/arcgis/rest/services/Planning/GarlandZoningWebmap/MapServer/0/query"
FLUM_URL = "https://maps.garlandtx.gov/arcgis/rest/services/Planning/GarlandZoningWebmap/MapServer/1/query"

def get_parcel_zoning(address: str):
    s = get_session()

    # Step 1: address to coordinates
    addr_params = {
        "where": f"FULL_ADDRESS = '{address.upper()}'",
        "outFields": "FULL_ADDRESS,LAT,LONG,GDS_TAXACCTNO,PARCELID",
        "resultRecordCount": 1,
        "f": "json"
    }
    addr_resp = s.get(ADDRESS_URL, params=addr_params)
    addr_data = addr_resp.json()
    features = addr_data.get("features", [])
    if not features:
        return None

    attrs = features[0]["attributes"]
    lat = attrs["LAT"]
    lng = attrs["LONG"]

    # Step 2: coordinates to zoning
    zone_params = {
        "geometry": f"{lng},{lat}",
        "geometryType": "esriGeometryPoint",
        "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "BASE_ZONE,GDC_ZONING,PD_NUM,BASEZONING",
        "returnGeometry": "false",
        "f": "json"
    }
    zone_resp = s.get(ZONING_URL, params=zone_params)
    zone_data = zone_resp.json()
    zone_features = zone_data.get("features", [])
    if not zone_features:
        return None

    z = zone_features[0]["attributes"]
    base_zone = z.get("BASE_ZONE") or ""
    is_pd = "PD" in base_zone.upper()

    # Step 3: coordinates to FLUM
    flum_params = {
        "geometry": f"{lng},{lat}",
        "geometryType": "esriGeometryPoint",
        "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "SUB_CATEGO,CATEGORY",
        "returnGeometry": "false",
        "f": "json"
    }
    flum_resp = s.get(FLUM_URL, params=flum_params)
    flum_data = flum_resp.json()
    flum_features = flum_data.get("features", [])
    flum_designation = None
    flum_category = None
    if flum_features:
        flum_designation = flum_features[0]["attributes"].get("SUB_CATEGO")
        flum_category = flum_features[0]["attributes"].get("CATEGORY")

    gdc_zoning = z.get("GDC_ZONING") or ""
    pd_num = z.get("PD_NUM", "").strip() or None
    has_existing_sup = gdc_zoning.startswith("S ") and not is_pd
    existing_sup_num = gdc_zoning if has_existing_sup else None

    return {
        "base_zone": base_zone,
        "gdc_zoning": gdc_zoning,
        "pd_num": pd_num,
        "has_existing_sup": has_existing_sup,
        "existing_sup_num": existing_sup_num,
        "lat": lat,
        "lng": lng,
        "is_planned_development": is_pd,
        "requires_manual_review": is_pd,
        "flum_designation": flum_designation,
        "flum_category": flum_category,
    }