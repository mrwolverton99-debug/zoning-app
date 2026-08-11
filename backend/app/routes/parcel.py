from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from app.services.dcad import lookup_parcel
from app.services.zoning import get_parcel_zoning, geocode_address
from app.services.landuse import get_uses_for_district, check_use
from app.services.ai_analysis import get_ai_analysis
from app.limiter import limiter
from fastapi import Request

router = APIRouter()

@router.get("/suggest")
async def suggest(q: str, city: str = "garland"):
    if len(q.strip()) < 3:
        return {"suggestions": []}
    from app.services.dcad import get_df, normalize_address
    df = await run_in_threadpool(get_df, city)
    q_upper = q.upper().strip()
    normalized = normalize_address(q).upper()
    matches = df[
        df["full_address"].str.startswith(q_upper) |
        df["full_address"].str.startswith(normalized)
    ].head(8)
    return {"suggestions": matches["full_address"].drop_duplicates().tolist()}


@router.get("/lookup")
@limiter.limit("15/hour")
async def lookup(request: Request, address: str, proposed_use: str = None, city: str = "garland"):
    parcel = await run_in_threadpool(lookup_parcel, address, city)
    geocoded = False
    lat, lng = None, None

    if parcel is None:
        coords = await run_in_threadpool(geocode_address, address, city)
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
    zoning = await run_in_threadpool(get_parcel_zoning, normalized, lat, lng, city)

    # If GIS address lookup failed but we have DCAD parcel, try geocoder as fallback
    if zoning is None and not geocoded:
        coords = await run_in_threadpool(geocode_address, address, city)
        if coords:
            lat, lng = coords
            zoning = await run_in_threadpool(get_parcel_zoning, normalized, lat, lng, city)
            if zoning:
                geocoded = True

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
            "Zoning retrieved via coordinates — address format may differ from GIS records."
            if result.get("account_num") else
            "Address not in DCAD — account number unavailable. Zoning and FLUM retrieved via coordinates."
        )

    if not zoning["is_planned_development"] and district:
        result["land_uses"] = get_uses_for_district(lookup_district)
        if proposed_use:
            use_check = check_use(lookup_district, proposed_use)
            result["proposed_use_check"] = use_check
            if use_check and use_check.get("status") not in ("not_found",):
                try:
                    result["ai_analysis"] = await run_in_threadpool(
                        get_ai_analysis, address, zoning, use_check, proposed_use
                    )
                except Exception as e:
                    result["ai_analysis_error"] = str(e)

# Save to history (non-blocking)
    try:
        from app.services.history import save_lookup
        await run_in_threadpool(save_lookup, address, result)
    except Exception:
        pass

    # Log to Supabase
    try:
        from app.db import log_lookup
        await run_in_threadpool(log_lookup, result, proposed_use)
    except Exception as e:
        print(f"Supabase log error: {e}")

    return result