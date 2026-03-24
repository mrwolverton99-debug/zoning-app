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

s = requests.Session()
s.mount('https://', LegacySSL())

params = {
    "geometry": "-96.60136564,32.85808757",
    "geometryType": "esriGeometryPoint",
    "inSR": "4326",
    "spatialRel": "esriSpatialRelIntersects",
    "outFields": "BASE_ZONE,GDC_ZONING,PD_NUM,BASEZONING",
    "returnGeometry": "false",
    "f": "json"
}

r = s.get(
    "https://maps.garlandtx.gov/arcgis/rest/services/Planning/GarlandZoningWebmap/MapServer/0/query",
    params=params
)
print(r.json())