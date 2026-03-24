import pandas as pd

# Load and filter once at startup
_df = None

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
    query = address.upper().strip()
    match = df[df["full_address"] == query]
    
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
    }