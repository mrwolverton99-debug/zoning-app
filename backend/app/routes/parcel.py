from fastapi import APIRouter, HTTPException
from app.services.dcad import lookup_parcel
from app.services.zoning import get_parcel_zoning

router = APIRouter()

@router.get("/lookup")
def lookup(address: str):
    parcel = lookup_parcel(address)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found in DCAD data")

    zoning = get_parcel_zoning(address)
    if zoning is None:
        raise HTTPException(status_code=404, detail="Zoning not found in Garland GIS")

    return {**parcel, **zoning}