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
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "false",
    "resultRecordCount": 5,
    "f": "json"
}

r = s.get(
    "https://maps.garlandtx.gov/arcgis/rest/services/Planning/Long_Range_Plans/MapServer/0/query",
    params=params
)
print(r.json())