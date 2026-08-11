import pandas as pd

_df = None
_dt_df = None

DT_SUBDISTRICTS = {"DH", "DS", "U", "IR", "SC"}

# ── Official GDC Chapter 6 definitions for split uses ────────────────────────
USE_DEFINITIONS = {
    "Automobile Repair, Major": (
        "General repair/reconditioning: engines, A/C overhaul, transmissions, "
        "collision/body/frame/fender work, painting, steam cleaning, undercoating, "
        "rustproofing. Also includes all Minor services."
    ),
    "Automobile Repair, Minor": (
        "Minor repair only: parts/tire/battery replacement, diagnostics, oil/lube, "
        "tune-ups, brake parts, washing/polishing, state inspections, normal A/C "
        "servicing, glass/upholstery repair. Excludes any Major operation."
    ),
    "Drive-Through Service": (
        "Accessory use: receipt of products/services through a building opening while "
        "patrons remain in vehicles. Requires separate SUP in NS, CR, LC, HC even when "
        "the primary use is permitted by right."
    ),
    "Reception Facility, Small Scale": "Occupancy of 49 or fewer persons.",
    "Reception Facility, Large Scale": "Occupancy of greater than 49 persons.",
    "Theater, Small Scale": "Seating capacity of 700 or fewer persons.",
    "Theater, Large Scale": "Seating capacity of over 700 persons.",
    "Hotel/Motel, Full Service": "Has meeting facilities and on-site food service.",
    "Hotel/Motel, Limited Service": "May have on-site food prep; no meeting facilities required.",
    "Hotel/Motel, Extended Stay": "Stays of 30+ days; includes kitchenette and sitting/work area.",
    "Bakery, Retail": "Small-scale retail production and sale of baked goods for off-site consumption.",
    "Bakery, Commercial": "Large-scale manufacturing of baked goods primarily for wholesale/off-site distribution.",
    "Distribution Center, Small (indoors only)": "10 or fewer shipping truck bays.",
    "Distribution Center, Large (indoors only)": "Over 10 shipping truck bays.",
    "Contractor's Office/Warehouse (indoors only)": "All storage indoors only.",
    "Contractor's Office/Storage Yard (outside storage)": "Includes outdoor storage of materials/equipment/vehicles.",
    "Industrial or Manufacturing, Light": "Indoor assembly/manufacturing from previously prepared materials.",
    "Industrial or Manufacturing, Heavy": "Processing/manufacture from raw materials; significant impacts possible.",
    "Veterinary Clinic, Small Animal (indoors only)": "All activities indoors; outdoor breaks max 60 min.",
    "Veterinary Clinic, Small Animal (outdoor kennels)": "Includes extended outdoor activities and overnight boarding.",
    "Pet Care/Play Facility (indoor)": "All activities indoors except periodic supervised outdoor breaks (max 1 hr).",
    "Pet Care/Play Facility (outdoor)": "Includes extended outdoor activities and overnight outdoor boarding.",
    "Antenna, Private": "Personal use; satellite dish 6 ft or under.",
    "Antenna, Commercial": "Commercial broadcasting or cellular/wireless; satellite dish over 6 ft.",
    "Pharmacy (without drive-through)": "Walk-in only.",
    "Pharmacy (with drive-through)": "Includes drive-through lane.",
    "Laundry, Self-Serve (Laundromat)": "Customer self-service machines on-site.",
    "Laundry, Drop-Off (without drive-through)": "Drop-off/pick-up service, max 3,000 sf, no drive-through.",
    "Laundry, Drop-Off (with drive-through)": "Drop-off/pick-up service with drive-through lane.",
    "Restaurant": "Food prepared and served on premises or carry-out. May include pick-up drive-through lane (no ordering at window).",
    "Restaurant, Drive-Through": "Food primarily served to persons in vehicles; includes menu/order board.",
    "Car Wash, Automated/Rollover": "Automated self-service drive-through/rollover wash bays.",
    "Car Wash, Self-Service/Wand": "Patron-operated wand-type wash bays, typically open-air.",
    "Flea Market, Indoor": "Periodic market fully within a building.",
    "Flea Market, Outdoor": "Periodic market in open area, not enclosed.",
    "Commercial Amusement, Indoor": "All entertainment activities fully enclosed within a building.",
    "Commercial Amusement, Outdoor": "Some or all activities occur outdoors.",
}

# ── Split use triggers ────────────────────────────────────────────────────────
SPLIT_USES = {
    # Auto repair
    "auto repair":            ["Automobile Repair, Major", "Automobile Repair, Minor"],
    "automobile repair":      ["Automobile Repair, Major", "Automobile Repair, Minor"],
    "car repair":             ["Automobile Repair, Major", "Automobile Repair, Minor"],
    "vehicle repair":         ["Automobile Repair, Major", "Automobile Repair, Minor"],
    # Car wash
    "car wash":               ["Car Wash, Automated/Rollover", "Car Wash, Self-Service/Wand"],
    # Restaurant
    "restaurant":             ["Restaurant", "Restaurant, Drive-Through"],
    # Reception
    "reception facility":     ["Reception Facility, Small Scale", "Reception Facility, Large Scale"],
    "reception hall":         ["Reception Facility, Small Scale", "Reception Facility, Large Scale"],
    "event venue":            ["Reception Facility, Small Scale", "Reception Facility, Large Scale"],
    "banquet":                ["Reception Facility, Small Scale", "Reception Facility, Large Scale"],
    # Theater
    "theater":                ["Theater, Small Scale", "Theater, Large Scale"],
    "theatre":                ["Theater, Small Scale", "Theater, Large Scale"],
    "cinema":                 ["Theater, Small Scale", "Theater, Large Scale"],
    "movie":                  ["Theater, Small Scale", "Theater, Large Scale"],
    # Hotel/motel
    "hotel":                  ["Hotel/Motel, Limited Service", "Hotel/Motel, Full Service", "Hotel/Motel, Extended Stay"],
    "motel":                  ["Hotel/Motel, Limited Service", "Hotel/Motel, Full Service", "Hotel/Motel, Extended Stay"],
    "inn":                    ["Hotel/Motel, Limited Service", "Hotel/Motel, Full Service", "Hotel/Motel, Extended Stay"],
    # Laundry
    "laundry":                ["Laundry, Drop-Off (without drive-through)", "Laundry, Drop-Off (with drive-through)", "Laundry, Self-Serve (Laundromat)"],
    "laundromat":             ["Laundry, Self-Serve (Laundromat)", "Laundry, Drop-Off (without drive-through)"],
    "dry clean":              ["Laundry, Drop-Off (without drive-through)", "Laundry, Drop-Off (with drive-through)"],
    # Bakery
    "bakery":                 ["Bakery, Retail", "Bakery, Commercial"],
    # Pharmacy
    "pharmacy":               ["Pharmacy (without drive-through)", "Pharmacy (with drive-through)"],
    "drug store":             ["Pharmacy (without drive-through)", "Pharmacy (with drive-through)"],
    # Veterinary
    "veterinary":             ["Veterinary Clinic, Small Animal (indoors only)", "Veterinary Clinic, Small Animal (outdoor kennels)"],
    "vet clinic":             ["Veterinary Clinic, Small Animal (indoors only)", "Veterinary Clinic, Small Animal (outdoor kennels)"],
    "animal clinic":          ["Veterinary Clinic, Small Animal (indoors only)", "Veterinary Clinic, Small Animal (outdoor kennels)"],
    # Pet care
    "pet care":               ["Pet Care/Play Facility (indoor)", "Pet Care/Play Facility (outdoor)"],
    "dog boarding":           ["Pet Care/Play Facility (indoor)", "Pet Care/Play Facility (outdoor)"],
    "kennel":                 ["Pet Care/Play Facility (indoor)", "Pet Care/Play Facility (outdoor)"],
    "doggy day":              ["Pet Care/Play Facility (indoor)", "Pet Care/Play Facility (outdoor)"],
    # Antenna
    "antenna":                ["Antenna, Private", "Antenna, Commercial"],
    "cell tower":             ["Antenna, Commercial"],
    "cell antenna":           ["Antenna, Commercial"],
    # Distribution / warehouse
    "distribution center":    ["Distribution Center, Small (indoors only)", "Distribution Center, Large (indoors only)"],
    "distribution":           ["Distribution Center, Small (indoors only)", "Distribution Center, Large (indoors only)"],
    # Manufacturing / industrial
    "manufacturing":          ["Industrial or Manufacturing, Light", "Industrial or Manufacturing, Heavy"],
    "industrial":             ["Industrial or Manufacturing, Light", "Industrial or Manufacturing, Heavy"],
    "factory":                ["Industrial or Manufacturing, Light", "Industrial or Manufacturing, Heavy"],
    # Contractor
    "contractor":             ["Contractor's Office/Warehouse (indoors only)", "Contractor's Office/Storage Yard (outside storage)"],
    # Day care
    "day care":               ["Day Care, Youth - Licensed Child-Care Center", "Day Care, Youth - Registered Child-Care Home", "Day Care Center, Adult"],
    "daycare":                ["Day Care, Youth - Licensed Child-Care Center", "Day Care, Youth - Registered Child-Care Home", "Day Care Center, Adult"],
    "child care":             ["Day Care, Youth - Licensed Child-Care Center", "Day Care, Youth - Registered Child-Care Home"],
    # School
    "school":                 ["School, Public", "School, Private, Religious or Charter", "School, Business", "School, Trade", "School, Retail/Personal Services Training"],
    "trade school":           ["School, Trade"],
    "vocational":             ["School, Trade", "School, Business"],
    # Flea market
    "flea market":            ["Flea Market, Indoor", "Flea Market, Outdoor"],
    # Amusement
    "amusement":              ["Commercial Amusement, Indoor", "Commercial Amusement, Outdoor"],
    "entertainment":          ["Commercial Amusement, Indoor", "Commercial Amusement, Outdoor"],
    # Bank + drive-through
    "bank with drive":        ["Financial Institution", "Drive-Through Service"],
    "drive-through bank":     ["Financial Institution", "Drive-Through Service"],
    "drive through bank":     ["Financial Institution", "Drive-Through Service"],
    "bank drive":             ["Financial Institution", "Drive-Through Service"],
    "drive-through":          ["Restaurant, Drive-Through", "Laundry, Drop-Off (with drive-through)", "Pharmacy (with drive-through)", "Drive-Through Service"],
    "drive through":          ["Restaurant, Drive-Through", "Laundry, Drop-Off (with drive-through)", "Pharmacy (with drive-through)", "Drive-Through Service"],
    # Brewery/winery/distillery
    "brewery":                ["Breweries/Wineries/Distilleries"],
    "winery":                 ["Breweries/Wineries/Distilleries"],
    "distillery":             ["Breweries/Wineries/Distilleries"],
    "breweries":              ["Breweries/Wineries/Distilleries"],
    "taproom":                ["Breweries/Wineries/Distilleries"],
    "craft beer":             ["Breweries/Wineries/Distilleries"],
    "craft brewery":          ["Breweries/Wineries/Distilleries"],
    # Makerspace
    "makerspace":             ["Makerspace (Hackerspace)"],
    "hackerspace":            ["Makerspace (Hackerspace)"],
    # Drone delivery
    "drone delivery":         ["Commercial Drone Delivery Hub (large)", "Commercial Drone Delivery Hub (small)"],
    "drone hub":              ["Commercial Drone Delivery Hub (large)", "Commercial Drone Delivery Hub (small)"],
    # Smoke shop
    "smoke shop":             ["Smoke Shop"],
    "vape shop":              ["Smoke Shop"],
    "tobacco":                ["Smoke Shop"],
    # Blood/plasma
    "plasma":                 ["Commercial Blood, Plasma, Tissue and Cell Collection Center"],
    "blood center":           ["Commercial Blood, Plasma, Tissue and Cell Collection Center"],
    "donation center":        ["Commercial Blood, Plasma, Tissue and Cell Collection Center"],
    # Sexually oriented
    "sexually oriented":      ["Sexually Oriented Business"],
    "adult entertainment":    ["Sexually Oriented Business"],
    "strip club":             ["Sexually Oriented Business"],
    "adult bookstore":        ["Sexually Oriented Business"],
    # Tattoo
    "tattoo":                 ["Tattooing/Body Piercing Establishment"],
    "piercing":               ["Tattooing/Body Piercing Establishment"],
    "body piercing":          ["Tattooing/Body Piercing Establishment"],
    # Alternative financial
    "payday loan":            ["Alternative Financial Establishment"],
    "check cashing":          ["Alternative Financial Establishment"],
    "title loan":             ["Alternative Financial Establishment"],
    "pawn shop":              ["Pawn Shop"],
    "pawnshop":               ["Pawn Shop"],
    # Personal services
    "salon":                  ["Personal Services"],
    "hair salon":             ["Personal Services"],
    "barber":                 ["Personal Services"],
    "beauty shop":            ["Personal Services"],
    "nail salon":             ["Personal Services"],
    "manicure":               ["Personal Services"],
    "massage":                ["Personal Services"],
    "tanning":                ["Personal Services"],
    "spa":                    ["Personal Services"],
    "hair removal":           ["Personal Services"],
    "permanent cosmetics":    ["Personal Services"],
    "portrait studio":        ["Personal Services"],
    "photography studio":     ["Personal Services"],
    "tailoring":              ["Personal Services"],
    "alterations":            ["Personal Services"],
    "weight loss":            ["Personal Services"],
    # Single family / residential
    "single family house":    ["Dwelling, Single-Family Detached"],
    "single family home":     ["Dwelling, Single-Family Detached"],
    "single family":          ["Dwelling, Single-Family Detached"],
    "detached house":         ["Dwelling, Single-Family Detached"],
    "detached home":          ["Dwelling, Single-Family Detached"],
    "new house":              ["Dwelling, Single-Family Detached"],
    "new home":               ["Dwelling, Single-Family Detached"],
    "house":                  ["Dwelling, Single-Family Detached"],
    "home":                   ["Dwelling, Single-Family Detached"],
    "townhouse":              ["Dwelling, Single-Family Attached (Townhouse)"],
    "townhome":               ["Dwelling, Single-Family Attached (Townhouse)"],
    "town house":             ["Dwelling, Single-Family Attached (Townhouse)"],
    "town home":              ["Dwelling, Single-Family Attached (Townhouse)"],
    "rowhouse":               ["Dwelling, Single-Family Attached (Townhouse)"],
    "row house":              ["Dwelling, Single-Family Attached (Townhouse)"],
    "attached home":          ["Dwelling, Single-Family Attached (Townhouse)"],
    "attached house":         ["Dwelling, Single-Family Attached (Townhouse)"],
    "duplex":                 ["Dwelling, Two-Family (duplex)"],
    "multifamily":            ["Dwelling, Multifamily"],
    "apartment":              ["Dwelling, Apartment"],
    "apartment complex":      ["Dwelling, Apartment"],
    "condo":                  ["Dwelling, Apartment"],
    "condominium":            ["Dwelling, Apartment"],
    "accessory dwelling":     ["Accessory Dwelling - Guest House", "Accessory Dwelling - Rental Unit"],
    "adu":                    ["Accessory Dwelling - Guest House", "Accessory Dwelling - Rental Unit"],
    "in-law suite":           ["Accessory Dwelling - Guest House"],
    "granny flat":            ["Accessory Dwelling - Guest House"],
    "mobile home":            ["Dwelling, Mobile Home"],
    "manufactured home":      ["Dwelling, Manufactured/HUD-Code Home"],
    "modular home":           ["Dwelling, Industrialized Housing Unit"],
}

ACCESSORY_TRIGGERS = {
    "carport":            "accessory_structure",
    "canopy":             "accessory_structure",
    "porte cochere":      "accessory_structure",
    "shed":               "accessory_structure",
    "detached garage":    "accessory_structure",
    "workshop":           "accessory_structure",
    "accessory building": "accessory_structure",
    "guest house":        "accessory_dwelling",
    "accessory dwelling": "accessory_dwelling",
    "adu":                "accessory_dwelling",
    "pool":               "accessory_structure",
    "swimming pool":      "accessory_structure",
    "fence":              "fence",
    "home occupation":    "home_occupation",
    "home based business":"home_occupation",
    "home business":      "home_occupation",
    "work from home":     "home_occupation",
}

STATUS_ORDER = ["prohibited", "requires_rezoning", "requires_sup", "special_standards", "permitted_by_right"]

from app.config.cities import get_city


def _match_trigger(text: str, triggers) -> str | None:
    """
    Find the best matching trigger contained in `text`.

    Triggers are checked longest-first so that specific terms beat generic
    substrings — "townhome" must win over "home", "trade school" over
    "school", "auto repair" over "repair".

    Triggers of 3 characters or fewer require a whole-word match so they do
    not fire inside longer words: "adu" must not match "adult", "spa" must
    not match "space", "inn" must not match "winner".
    """
    import re
    for trigger in sorted(triggers, key=len, reverse=True):
        if len(trigger) <= 3:
            if re.search(r'\b' + re.escape(trigger) + r'\b', text):
                return trigger
        elif trigger in text:
            return trigger
    return None


def get_df(city_key: str = None):
    global _df
    if _df is None:
        city = get_city(city_key)
        _df = pd.read_csv(city["matrix_file"], dtype=str).fillna("")
    return _df


def get_dt_df(city_key: str = None):
    global _dt_df
    if _dt_df is None:
        city = get_city(city_key)
        _dt_df = pd.read_csv(city["dt_matrix_file"], dtype=str).fillna("")
    return _dt_df


def get_uses_for_district(district: str):
    if district is None:
        return None
    district = district.upper().strip()

    if district in DT_SUBDISTRICTS:
        return _get_dt_subdistrict_uses(district)
    if district == "DT":
        return _get_dt_aggregate_uses()

    df = get_df()
    if district not in df.columns:
        return None

    subset = df[["category", "use_name", district]].copy()
    subset = subset[subset[district] != ""]

    return {
        "district": district,
        "permitted_by_right": subset[subset[district] == "P"]["use_name"].tolist(),
        "requires_sup":       subset[subset[district] == "S"]["use_name"].tolist(),
        "special_standards":  subset[subset[district] == "*"]["use_name"].tolist(),
    }


def _get_dt_subdistrict_uses(subdistrict: str):
    df = get_dt_df()
    if subdistrict not in df.columns:
        return None

    subset = df[["category", "use_name", subdistrict]].copy()
    subset = subset[subset[subdistrict] != ""]

    return {
        "district":           f"DT ({subdistrict})",
        "subdistrict":        subdistrict,
        "permitted_by_right": subset[subset[subdistrict] == "P"]["use_name"].tolist(),
        "requires_sup":       subset[subset[subdistrict] == "S"]["use_name"].tolist(),
        "special_standards":  subset[subset[subdistrict] == "*"]["use_name"].tolist(),
    }


def _get_dt_aggregate_uses():
    df = get_dt_df()
    results_p, results_s = set(), set()

    for sub in DT_SUBDISTRICTS:
        if sub not in df.columns:
            continue
        results_p.update(df[df[sub] == "P"]["use_name"].tolist())
        results_s.update(df[df[sub] == "S"]["use_name"].tolist())

    results_s -= results_p

    return {
        "district":           "DT",
        "subdistrict":        None,
        "note":               "Sub-district not determined. Showing uses permitted in any DT sub-district. Verify with Garland Planning staff.",
        "permitted_by_right": sorted(results_p),
        "requires_sup":       sorted(results_s),
        "special_standards":  [],
    }


def _lookup_use_status(use_name: str, lookup_col: str) -> tuple[str, str, str, str]:
    """Returns (status_val, category, source, parking)"""
    dt = get_dt_df()
    rows = dt[dt["use_name"] == use_name]
    if not rows.empty and lookup_col in rows.columns:
        row = rows.iloc[0]
        parking = str(row.get("parking", "")) if "parking" in row.index else ""
        return row.get(lookup_col, ""), row["category"], "dt", parking

    main = get_df()
    main_col = "DT" if lookup_col in DT_SUBDISTRICTS else lookup_col
    rows = main[main["use_name"] == use_name]
    if not rows.empty and main_col in rows.columns:
        row = rows.iloc[0]
        parking = str(row.get("parking", "")) if "parking" in row.index else ""
        return row.get(main_col, ""), row["category"], "main", parking

    return "", "Unknown", "none", ""


def _status_label(status_val: str) -> str:
    if status_val == "P": return "permitted_by_right"
    if status_val == "S": return "requires_sup"
    if status_val == "*": return "special_standards"
    return "prohibited"


def _status_message(use_name: str, label: str, district: str) -> str:
    if label == "permitted_by_right":
        return f"'{use_name}' appears permitted by right in {district}."
    if label == "requires_sup":
        return f"'{use_name}' requires a Specific Use Provision (SUP) in {district}."
    if label == "special_standards":
        return f"'{use_name}' is allowed in {district} subject to special standards. See GDC for details."
    return f"'{use_name}' appears prohibited in {district}."


def _status_text(label: str) -> str:
    return {
        "permitted_by_right": "permitted by right",
        "requires_sup":       "requires a Specific Use Provision (SUP)",
        "special_standards":  "subject to special standards",
        "prohibited":         "prohibited",
    }.get(label, label.replace("_", " "))


def _worst_status(statuses: list[str]) -> str:
    for s in STATUS_ORDER:
        if s in statuses:
            return s
    return "prohibited"


def _check_split_use(proposed_use: str, district: str, lookup_col: str) -> dict | None:
    proposed_lower = proposed_use.lower().strip()

    trigger = _match_trigger(proposed_lower, SPLIT_USES)
    matched_variants = SPLIT_USES[trigger] if trigger else None

    if not matched_variants:
        return None

    results = []
    for use_name in matched_variants:
        status_val, category, _, parking = _lookup_use_status(use_name, lookup_col)
        label = _status_label(status_val)
        results.append({
            "use_name": use_name,
            "category": category,
            "status":   label,
            "status_code": status_val,
            "definition": USE_DEFINITIONS.get(use_name, ""),
            "parking": parking,
        })

    if not results:
        return None

    statuses = [r["status"] for r in results]
    worst = _worst_status(statuses)
    all_same = len(set(statuses)) == 1

    variant_summary = " | ".join(
        f"{r['use_name']}: {r['status'].replace('_', ' ')}"
        for r in results
    )

    if all_same:
        names = " and ".join(r["use_name"] for r in results)
        if len(results) == 1:
            message = _status_message(results[0]["use_name"], worst, district)
        else:
            message = (
                f"All variants of '{proposed_use}' are {_status_text(worst)} "
                f"in {district}."
            )
        match_str = names
    else:
        base = results[0]["use_name"].split(",")[0].split("(")[0].strip()
        message = (
            f"'{proposed_use}' could match multiple GDC use types with different "
            f"statuses in {district}. Clarify your operation: {variant_summary}."
        )
        match_str = f"{base} — clarification needed"

    best_order = ["permitted_by_right", "special_standards", "requires_sup", "requires_rezoning", "prohibited"]
    best = min(statuses, key=lambda s: best_order.index(s) if s in best_order else 99)

    result = {
        "match":    match_str,
        "category": results[0]["category"],
        "status":   best if not all_same else worst,
        "message":  message,
        "variants": results,
    }

    # Add parking from the best/first variant that has it
    for r in results:
        if r.get("parking"):
            result["parking"] = r["parking"]
            break

    if any(r["use_name"] == "Drive-Through Service" for r in results):
        result["drive_through_note"] = (
            "Drive-Through Service is an accessory use requiring a separate SUP in "
            "NS, CR, LC, and HC — even when the primary use is permitted by right."
        )

    if not all_same:
        result["clarification_needed"] = True

    return result


def check_use(district: str, proposed_use: str) -> dict | None:
    if district is None:
        return None
    district = district.upper().strip()

    if district in DT_SUBDISTRICTS:
        lookup_col = district
    elif district == "DT":
        lookup_col = "DH"
    else:
        lookup_col = district

    # ── 0. Accessory structure triggers ───────────────────────────────────
    proposed_lower = proposed_use.lower().strip()
    acc_trigger = _match_trigger(proposed_lower, ACCESSORY_TRIGGERS)
    if acc_trigger:
        acc_type = ACCESSORY_TRIGGERS[acc_trigger]
        return {
            "match":          proposed_use,
            "status":         "development_standard",
            "category":       "Accessory Structures & Development Standards",
            "message":        f"'{proposed_use}' is governed by GDC development standards, not the land use matrix. See analysis below.",
            "accessory_type": acc_type,
        }

    # ── 1. Split use check ────────────────────────────────────────────────
    split_result = _check_split_use(proposed_use, district, lookup_col)
    if split_result:
        if district == "DT" and lookup_col == "DH":
            split_result["dt_note"] = (
                "Sub-district unknown — result shown against DH baseline. "
                "Verify with Garland Planning staff."
            )
        return split_result

    # ── 2. Fuzzy match ────────────────────────────────────────────────────
    import re
    search_terms = proposed_use.lower().strip().split()

    def score(use_name: str) -> int:
        n = use_name.lower()
        count = 0
        for t in search_terms:
            if re.search(r'\b' + re.escape(t) + r'\b', n):
                count += 2
            elif t in n:
                count += 1
        return count

    best_row = None
    best_score = 0
    best_lookup_col = lookup_col
    best_df = None

    if district in DT_SUBDISTRICTS or district == "DT":
        dt = get_dt_df().copy()
        dt["_score"] = dt["use_name"].apply(score)
        matches = dt[dt["_score"] > 0]
        if not matches.empty:
            top = matches.sort_values("_score", ascending=False).iloc[0]
            if top["_score"] > best_score:
                best_score = top["_score"]
                best_row = top
                best_df = get_dt_df()
                best_lookup_col = district if district in DT_SUBDISTRICTS else "DH"

    main = get_df().copy()
    main["_score"] = main["use_name"].apply(score)
    matches = main[main["_score"] > 0]
    if not matches.empty:
        top = matches.sort_values("_score", ascending=False).iloc[0]
        if top["_score"] > best_score:
            best_score = top["_score"]
            best_row = top
            best_df = get_df()
            best_lookup_col = "DT" if (district in DT_SUBDISTRICTS or district == "DT") else district

    if best_row is None:
        return {
            "match":   None,
            "status":  "not_found",
            "message": f"No matching use type found for '{proposed_use}'",
        }

    status_val = ""
    if best_lookup_col in best_row.index:
        status_val = best_row.get(best_lookup_col, "")

    label = _status_label(status_val)

    if label == "permitted_by_right":
        message = f"'{best_row['use_name']}' appears permitted by right in {district}."
    elif label == "requires_sup":
        message = f"'{best_row['use_name']}' requires a Specific Use Provision (SUP) in {district}."
    elif label == "special_standards":
        message = f"'{best_row['use_name']}' is allowed in {district} subject to special standards. See GDC for details."
    else:
        message = f"'{best_row['use_name']}' appears prohibited in {district}."

    result = {
        "match":    best_row["use_name"],
        "category": best_row["category"],
        "status":   label,
        "message":  message,
    }

    if "parking" in best_row.index and best_row.get("parking"):
        result["parking"] = str(best_row["parking"])

    definition = USE_DEFINITIONS.get(best_row["use_name"])
    if definition:
        result["definition"] = definition

    if district == "DT" and best_lookup_col == "DT":
        result["dt_note"] = (
            "Sub-district unknown — result shown for DT baseline. "
            "Verify with Garland Planning staff."
        )

    return result