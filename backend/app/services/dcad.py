import pandas as pd

_df = None

STREET_TYPE_MAP = {
    "DRIVE": "DR", "STREET": "ST", "AVENUE": "AVE", "BOULEVARD": "BLVD",
    "LANE": "LN", "COURT": "CT", "PLACE": "PL", "ROAD": "RD",
    "FREEWAY": "FWY", "PARKWAY": "PKWY", "HIGHWAY": "HWY", "CIRCLE": "CIR",
    "TRAIL": "TRL", "CROSSING": "XING", "EXPRESSWAY": "EXPY",
    "SQUARE": "SQ", "PATH": "PATH", "LOOP": "LOOP",
    "DR": "DR", "ST": "ST", "AVE": "AVE", "BLVD": "BLVD",
    "LN": "LN", "CT": "CT", "PL": "PL", "RD": "RD",
    "FWY": "FWY", "PKWY": "PKWY", "HWY": "HWY", "CIR": "CIR",
    "TRL": "TRL", "XING": "XING", "EXPY": "EXPY", "WAY": "WAY",
}

DIRECTION_MAP = {
    "NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W",
    "N": "N", "S": "S", "E": "E", "W": "W",
}

DIRECTIONS = ["N", "S", "E", "W"]

import re

def normalize_address(address: str) -> str:
    # Strip suite/unit numbers before normalization
    address = re.sub(r'\s+(suite|ste|apt|unit|#)\s*[\w-]+', '', address, flags=re.IGNORECASE).strip()
    
    parts = address.upper().strip().split()
    if len(parts) < 2:
        return address.upper().strip()

    street_num = parts[0]
    remaining = parts[1:]

    direction = ""
    if remaining and remaining[0] in DIRECTION_MAP:
        direction = DIRECTION_MAP[remaining[0]]
        remaining = remaining[1:]

    if remaining:
        last = remaining[-1]
        if last in STREET_TYPE_MAP:
            street_type = STREET_TYPE_MAP[last]
            street_name = " ".join(remaining[:-1])
        else:
            street_type = ""
            street_name = " ".join(remaining)
    else:
        street_type = ""
        street_name = ""

    parts_out = [street_num]
    if direction:
        parts_out.append(direction)
    if street_name:
        parts_out.append(street_name)
    if street_type:
        parts_out.append(street_type)

    return " ".join(parts_out)

from app.config.cities import get_city

def get_df(city_key: str = None):
    global _df
    if _df is None:
        from app.config.cities import get_city
        city = get_city(city_key)
        df = pd.read_csv(city["dcad_file"], dtype=str)
        df = df[df["PROPERTY_CITY"].str.upper() == city["dcad_city_filter"]]
        df["full_address"] = (
            df["STREET_NUM"].str.strip() + " " +
            df["FULL_STREET_NAME"].str.strip()
        ).str.upper()
        _df = df
    return _df

def _build_result(row, normalized: str) -> dict:
    return {
        "account_num":        row["ACCOUNT_NUM"],
        "gis_parcel_id":      row["GIS_PARCEL_ID"],
        "street_num":         row["STREET_NUM"],
        "street_name":        row["FULL_STREET_NAME"],
        "city":               row["PROPERTY_CITY"],
        "zipcode":            row["PROPERTY_ZIPCODE"],
        "normalized_address": normalized,
    }


def lookup_parcel(address: str, city_key: str = None) -> dict | None:
    df = get_df(city_key)
    normalized = normalize_address(address)

    # 1. Exact match on normalized address
    match = df[df["full_address"] == normalized]
    if not match.empty:
        return _build_result(match.iloc[0], normalized)

    # 2. Exact match on raw input (user already typed correct format)
    match = df[df["full_address"] == address.upper().strip()]
    if not match.empty:
        return _build_result(match.iloc[0], normalized)

    # 3. Missing direction — try inserting N/S/E/W after street number
    #    e.g. "532 MAIN ST" → try "532 N MAIN ST", "532 S MAIN ST", etc.
    parts = normalized.split()
    if len(parts) >= 2 and parts[1] not in DIRECTIONS:
        for d in DIRECTIONS:
            candidate = parts[0] + " " + d + " " + " ".join(parts[1:])
            match = df[df["full_address"] == candidate]
            if not match.empty:
                return _build_result(match.iloc[0], normalized)

    # 4. Tight partial match — requires street number AND full street name fragment
    #    Fragment must be > 3 chars to avoid matching on tiny ambiguous strings
    num = parts[0]
    street_fragment = " ".join(p for p in parts[1:] if p not in DIRECTIONS)

    if street_fragment and len(street_fragment) > 3:
        match = df[
            (df["full_address"].str.startswith(num + " ")) &
            (df["full_address"].str.contains(street_fragment, na=False))
        ]
        if len(match) == 1:
            return _build_result(match.iloc[0], normalized)
        elif len(match) > 1:
            # Multiple hits — pick shortest (least extra tokens = closest match)
            match = match.copy()
            match["_len"] = match["full_address"].str.len()
            return _build_result(match.sort_values("_len").iloc[0], normalized)

    # No confident match found
    return None