# backend/scripts/generate_parcels.py
# One-time filter: the full Dallas County DCAD dump (ACCOUNT_INFO.CSV) is ~800k
# rows across every column DCAD publishes. dcad.py only ever reads Garland rows
# and six columns. This script pre-filters that down to a small file that can
# be committed to git and loaded into memory on a small deploy instance.
#
# Run: python backend/scripts/generate_parcels.py

import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(SCRIPT_DIR, "..", "data", "ACCOUNT_INFO.CSV")
OUTPUT = os.path.join(SCRIPT_DIR, "..", "data", "garland_parcels.csv")

CITY_FILTER = "GARLAND (DALLAS CO)"

COLUMNS = [
    "ACCOUNT_NUM",
    "GIS_PARCEL_ID",
    "STREET_NUM",
    "FULL_STREET_NAME",
    "PROPERTY_CITY",
    "PROPERTY_ZIPCODE",
]


def main():
    df = pd.read_csv(SOURCE, dtype=str, usecols=COLUMNS)
    df = df[df["PROPERTY_CITY"].str.upper() == CITY_FILTER]
    df.to_csv(OUTPUT, index=False)

    size_mb = os.path.getsize(OUTPUT) / (1024 * 1024)
    print(f"Rows: {len(df)}")
    print(f"Output: {OUTPUT} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
