import pandas as pd
import re

_df = None

STREET_TYPE_MAP = {
    # Full words to abbreviations (what DCAD uses)
    "DRIVE": "DR", "STREET": "ST", "AVENUE": "AVE", "BOULEVARD": "BLVD",
    "LANE": "LN", "COURT": "CT", "PLACE": "PL", "ROAD": "RD",
    "FREEWAY": "FWY", "PARKWAY": "PKWY", "HIGHWAY": "HWY", "CIRCLE": "CIR",
    "TRAIL": "TRL", "CROSSING": "XING", "EXPRESSWAY": "EXPY",
    "SQUARE": "SQ", "PATH": "PATH", "LOOP": "LOOP",
    # Abbreviations stay as-is
    "DR": "DR", "ST": "ST", "AVE": "AVE", "BLVD": "BLVD",
    "LN": "LN", "CT": "CT", "PL": "PL", "RD": "RD",
    "FWY": "FWY", "PKWY": "PKWY", "HWY": "HWY", "CIR": "CIR",
    "TRL": "TRL", "XING": "XING", "EXPY": "EXPY", "WAY": "WAY",
}

DIRECTION_MAP = {
    "NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W",
    "N": "N", "S": "S", "E": "E", "W": "W",
}

def normalize_address(address: str) -> str:
    """Normalize address to match DCAD format: NUMBER DIRECTION STREET_NAME TYPE"""
    parts = address.upper().strip().split()
    if len(parts) < 2:
        return address.upper().strip()

    # Extract street number
    street_num = parts[0]
    remaining = parts[1:]

    # Check for direction prefix
    direction = ""
    if remaining and remaining[0] in DIRECTION_MAP:
        direction = DIRECTION_MAP[remaining[0]]
        remaining = remaining[1:]

    # Last word might be street type
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

    # Rebuild in DCAD format
    parts_out = [street_num]
    if direction:
        parts_out.append(direction)
    if street_name:
        parts_out.append(street_name)
    if street_type:
        parts_out.append(street_type)

    return " ".join(parts_out)

def get_df():
    global _df
    if _df is None:
        df = pd.read_csv("data/ACCOUNT_INFO.CSV", dtype=str)
        df = df[df["PROPERTY_CITY"].str.upper() == "GARLAND (DALLAS CO)"]
        df["full_address"] = (
            df["STREET_NUM"].str.strip() + " " +
            df["FULL_STREET_NAME"].str.strip()
        ).str.upper()
        _df = df
    return _df

def lookup_parcel(address: str):
    df = get_df()
    
    # Try normalized address first
    normalized = normalize_address(address)
    match = df[df["full_address"] == normalized]
    
    # Fall back to original if no match
    if match.empty:
        query = address.upper().strip()
        match = df[df["full_address"] == query]

    # Fall back to partial match
    if match.empty:
        match = df[df["full_address"].str.startswith(normalized.split()[0] + " ")]
        if not match.empty:
            # Try fuzzy on street name
            match = df[df["full_address"].str.contains(
                " ".join(normalized.split()[1:]), na=False
            )]

    if match.empty:
        return None

    row = match.iloc[0]
    return {
        "account_num": row["ACCOUNT_NUM"],
        "gis_parcel_id": row["GIS_PARCEL_ID"],
        "street_num": row["STREET_NUM"],
        "street_name": row["FULL_STREET_NAME"],
        "city": row["PROPERTY_CITY"],
        "zipcode": row["PROPERTY_ZIPCODE"],
        "normalized_address": normalized,
    }