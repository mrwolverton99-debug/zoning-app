from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from app.services.dcad import lookup_parcel
from app.services.zoning import get_parcel_zoning, geocode_address
from app.services.landuse import get_uses_for_district, check_use
from app.services.ai_analysis import get_ai_analysis

router = APIRouter()

@router.get("/lookup")
async def lookup(address: str, proposed_use: str = None, city: str = "garland"):
    parcel = await run_in_threadpool(lookup_parcel, address, city)
    # ... pass city through to all service calls
    geocoded = False
    lat, lng = None, None

    if parcel is None:
        coords = await run_in_threadpool(geocode_address, address)
        if coords is None:
            raise HTTPException(
                status_code=404,
                detail="Address not found. Check the address and try again."
            )
        lat, lng = coords
        geocoded = True
        parcel = {
            "account_num":        None,
            "gis_parcel_id":      None,
            "street_num":         "",
            "street_name":        address.upper(),
            "city":               "Garland TX",
            "zipcode":            "",
            "normalized_address": address.upper(),
        }

    normalized = parcel.get("normalized_address", address)
    zoning = await run_in_threadpool(get_parcel_zoning, normalized, lat, lng)

    if zoning is None:
        raise HTTPException(
            status_code=404,
            detail="Zoning not found in Garland GIS for this address."
        )

    district = zoning.get("base_zone", "")
    dt_sub = zoning.get("dt_subdistrict")
    lookup_district = dt_sub if dt_sub else district

    result = {**parcel, **zoning}

    if geocoded:
        result["geocoded_fallback"] = True
        result["geocoded_note"] = (
            "Address not found in DCAD — parcel details unavailable. "
            "Zoning retrieved via coordinates only."
        )

    if not zoning["is_planned_development"] and district:
        result["land_uses"] = get_uses_for_district(lookup_district)
        if proposed_use:
            use_check = check_use(lookup_district, proposed_use)
            result["proposed_use_check"] = use_check
            if use_check and use_check.get("status") != "not_found":
                try:
                    result["ai_analysis"] = get_ai_analysis(
                        address, zoning, use_check, proposed_use
                    )
                except Exception as e:
                    result["ai_analysis_error"] = str(e)

    return result