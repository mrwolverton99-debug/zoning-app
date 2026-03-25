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
ZONING_URL  = "https://maps.garlandtx.gov/arcgis/rest/services/Planning/GarlandZoningWebmap/MapServer/0/query"
FLUM_URL    = "https://maps.garlandtx.gov/arcgis/rest/services/Planning/GarlandZoningWebmap/MapServer/1/query"
DAO_URL     = "https://maps.garlandtx.gov/arcgis/rest/services/Planning/GarlandZoningWebmap/MapServer/6/query"

# ---------------------------------------------------------------------------
# Downtown sub-district polygons
# Format: { code: [ [lng, lat], ... ] }  — one list per polygon patch.
# DS, DH: 1 patch each. IR: 2 patches (north + south). SC: 3 patches.
# U: 1 patch (large outer district).
# Boundaries drawn in geojson.io by user, March 2026.
# Check order DS→DH→SC→IR→U ensures smaller/inner districts win over larger.
# ---------------------------------------------------------------------------
_DT_POLYGONS = {
    "DS": [
        [(-96.6377717159665,  32.91389399239365),
         (-96.63777588862271, 32.91333703029484),
         (-96.63838092376187, 32.91335104196254),
         (-96.63838926907435, 32.912685485279155),
         (-96.63778840659099, 32.91268198233557),
         (-96.6378009245597,  32.91221608966093),
         (-96.6363822214745,  32.912212586699496),
         (-96.63631545897651, 32.91264695289627),
         (-96.6359399199246,  32.91331951570655),
         (-96.63651574647096, 32.91332652154237),
         (-96.63651157381472, 32.91389399239365),
         (-96.6377717159665,  32.91389399239365)],
    ],
    "DH": [
        [(-96.63993045671948, 32.91614156172274),
         (-96.64012370987737, 32.91560851996728),
         (-96.64016972253368, 32.91515272809377),
         (-96.64023414025328, 32.911799881844644),
         (-96.63624024166104, 32.91172262582566),
         (-96.63247640635232, 32.91698360665045),
         (-96.63531998852946, 32.916520096672286),
         (-96.63783227957936, 32.91620336345754),
         (-96.63993045671948, 32.91614156172274)],
    ],
    "SC": [
        # West strip (along railroad, north section)
        [(-96.64805998947952, 32.91393670039781),
         (-96.64859791121278, 32.91384834800168),
         (-96.64863299306496, 32.91235125232923),
         (-96.64973222443189, 32.912370886534376),
         (-96.64975561233356, 32.91100629888942),
         (-96.6492074290543,  32.910996603652166),
         (-96.64922020961555, 32.909764850709195),
         (-96.64912262351957, 32.90967845343093),
         (-96.64909279085067, 32.90900567263067),
         (-96.64879888536441, 32.90898954369513),
         (-96.64866602503558, 32.908623051581586),
         (-96.64866982104513, 32.90820238050304),
         (-96.64851798066903, 32.908062156365546),
         (-96.64817946843843, 32.907982192933076),
         (-96.64814536189417, 32.90821533293153),
         (-96.6473445758711,  32.9082187455888),
         (-96.64626960343547, 32.90821884303692),
         (-96.646292670327,   32.90899899755604),
         (-96.64806439183558, 32.90901386109809),
         (-96.64805998947952, 32.91393670039781)],
        # South middle strip
        [(-96.64149290217716, 32.908997862009215),
         (-96.64148231609471, 32.90852090455765),
         (-96.63938627177214, 32.90852090455765),
         (-96.63877410787833, 32.908515693513664),
         (-96.63851429203446, 32.90895467012753),
         (-96.63782578004772, 32.90895194357131),
         (-96.63782134498405, 32.90849216423088),
         (-96.6372618702368,  32.90848090590919),
         (-96.63718787196318, 32.908316897155956),
         (-96.63616647404076, 32.90832585219262),
         (-96.6361529619898,  32.90897623453648),
         (-96.64149290217716, 32.908997862009215)],
        # East strip
        [(-96.63077743863609, 32.91701598039286),
         (-96.63074483191298, 32.90887795414892),
         (-96.62999355059057, 32.90886320557965),
         (-96.63001119174321, 32.91112355372991),
         (-96.62886059510014, 32.911121444071256),
         (-96.62891784745551, 32.911270976941694),
         (-96.62983022770302, 32.91168765361965),
         (-96.62951668718541, 32.91198596923063),
         (-96.62922822990964, 32.91210880477843),
         (-96.62878927318542, 32.912396590251504),
         (-96.62860950995564, 32.912558030472965),
         (-96.62953759431858, 32.91327429884859),
         (-96.62972592510079, 32.91329406166662),
         (-96.62978870202846, 32.91689740840435),
         (-96.63077743863609, 32.91701598039286)],
    ],
    "IR": [
        # North patch
        [(-96.6434163786108,  32.9144642527954),
         (-96.64492477326054, 32.91443306384346),
         (-96.64497678686907, 32.913827995996755),
         (-96.6465669171901,  32.913834233830286),
         (-96.64661893079865, 32.91276131992652),
         (-96.64423373531748, 32.91273013037454),
         (-96.6442188742863,  32.913597195831116),
         (-96.64343123964159, 32.913422535846905),
         (-96.6434163786108,  32.9144642527954)],
        # South patch (L-shaped)
        [(-96.64660266628009, 32.91190361977239),
         (-96.64662604324947, 32.91096737215186),
         (-96.64421022619848, 32.91092488425076),
         (-96.6442348896325,  32.90903218625071),
         (-96.64266019549636, 32.90904405419988),
         (-96.64266656239026, 32.9099500652046),
         (-96.64345605729086, 32.9099500652046),
         (-96.64346732228832, 32.912219010514775),
         (-96.64418359790317, 32.91219763037924),
         (-96.64418937794179, 32.91215602066248),
         (-96.64660235042484, 32.91213306653516),
         (-96.64660266628009, 32.91190361977239)],
    ],
    "U": [
        [(-96.63076943110751, 32.920891158778474),
         (-96.6327523899668,  32.920883143342735),
         (-96.63412835471829, 32.920861211537556),
         (-96.6341489969395,  32.92093052165137),
         (-96.63512176160454, 32.92091969195016),
         (-96.63613011404675, 32.92092504132832),
         (-96.63882485750551, 32.92095234164621),
         (-96.6395139368975,  32.92095681501951),
         (-96.63956762374123, 32.91715203003487),
         (-96.63982833616423, 32.91630004718483),
         (-96.63995960491127, 32.91613897241797),
         (-96.64405684530523, 32.9161759141774),
         (-96.64419481916853, 32.91444848375549),
         (-96.64544655116131, 32.914331927165975),
         (-96.64806219542417, 32.913944847702766),
         (-96.6480586823496,  32.90899391140057),
         (-96.63078944236429, 32.908890595906385),
         (-96.63076943110751, 32.920891158778474)],
    ],
}

# Smaller/inner districts checked before larger/outer ones
_DT_CHECK_ORDER = ["DS", "DH", "SC", "IR", "U"]


def _point_in_polygon(lat: float, lng: float, polygon: list) -> bool:
    """Ray casting point-in-polygon. polygon is list of (lng, lat) tuples."""
    n = len(polygon)
    inside = False
    x, y = lng, lat
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def detect_dt_subdistrict(lat: float, lng: float) -> str | None:
    """
    Returns 'DS', 'DH', 'SC', 'IR', or 'U' for the given coordinates,
    or None if the point falls outside all defined sub-district polygons.
    """
    for code in _DT_CHECK_ORDER:
        for polygon in _DT_POLYGONS[code]:
            if _point_in_polygon(lat, lng, polygon):
                return code
    return None


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
    features = addr_resp.json().get("features", [])
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
    zone_features = s.get(ZONING_URL, params=zone_params).json().get("features", [])
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
    flum_features = s.get(FLUM_URL, params=flum_params).json().get("features", [])
    flum_designation = None
    flum_category = None
    if flum_features:
        flum_designation = flum_features[0]["attributes"].get("SUB_CATEGO")
        flum_category    = flum_features[0]["attributes"].get("CATEGORY")

    # Step 4: check Downtown Automotive Overlay
    in_dao = False
    if base_zone == "DT":
        dao_params = {
            "geometry": f"{lng},{lat}",
            "geometryType": "esriGeometryPoint",
            "inSR": "4326",
            "spatialRel": "esriSpatialRelIntersects",
            "outFields": "LABEL",
            "returnGeometry": "false",
            "f": "json"
        }
        in_dao = len(s.get(DAO_URL, params=dao_params).json().get("features", [])) > 0

    # Step 5: detect DT sub-district
    dt_subdistrict = detect_dt_subdistrict(lat, lng) if base_zone == "DT" else None

    gdc_zoning = z.get("GDC_ZONING") or ""
    pd_num = z.get("PD_NUM", "").strip() or None
    has_existing_sup = gdc_zoning.startswith("S ") and not is_pd

    return {
        "base_zone": base_zone,
        "gdc_zoning": gdc_zoning,
        "pd_num": pd_num,
        "has_existing_sup": has_existing_sup,
        "existing_sup_num": gdc_zoning if has_existing_sup else None,
        "lat": lat,
        "lng": lng,
        "is_planned_development": is_pd,
        "requires_manual_review": is_pd,
        "flum_designation": flum_designation,
        "flum_category": flum_category,
        "in_downtown_automotive_overlay": in_dao,
        "dt_subdistrict": dt_subdistrict,
    }