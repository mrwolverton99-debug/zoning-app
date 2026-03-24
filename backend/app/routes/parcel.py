from fastapi import APIRouter, HTTPException
from app.services.dcad import lookup_parcel
from app.services.zoning import get_parcel_zoning
from app.services.landuse import get_uses_for_district, check_use

router = APIRouter()

@router.get("/lookup")
def lookup(address: str, proposed_use: str = None):
    parcel = lookup_parcel(address)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found in DCAD data")

    zoning = get_parcel_zoning(address)
    if zoning is None:
        raise HTTPException(status_code=404, detail="Zoning not found in Garland GIS")

    district = zoning.get("base_zone", "")
    result = {**parcel, **zoning}

    if not zoning["is_planned_development"] and district:
        result["land_uses"] = get_uses_for_district(district)
        if proposed_use:
            result["proposed_use_check"] = check_use(district, proposed_use)

    return result