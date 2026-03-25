import pandas as pd

_df = None

def get_df():
    global _df
    if _df is None:
        _df = pd.read_csv("data/garland_land_use_matrix.csv", dtype=str).fillna("")
    return _df

def get_uses_for_district(district: str):
    df = get_df()
    district = district.upper().strip()
    if district not in df.columns:
        return None
    
    subset = df[["category", "use_name", district]].copy()
    subset = subset[subset[district] != ""]
    
    permitted = subset[subset[district] == "P"]["use_name"].tolist()
    sup = subset[subset[district] == "S"]["use_name"].tolist()
    conditional = subset[subset[district] == "*"]["use_name"].tolist()
    
    return {
        "district": district,
        "permitted_by_right": permitted,
        "requires_sup": sup,
        "special_standards": conditional,
    }

def check_use(district: str, proposed_use: str):
    df = get_df()
    district = district.upper().strip()
    proposed = proposed_use.lower().strip()
    
    if district not in df.columns:
        return None
    
    # Build search terms from proposed use
    search_terms = proposed.lower().split()

    # Score each row by how many terms match
    def score_row(use_name):
        name_lower = use_name.lower()
        return sum(1 for term in search_terms if term in name_lower)

    df['_score'] = df['use_name'].apply(score_row)
    matches = df[df['_score'] > 0].sort_values('_score', ascending=False)
    df.drop('_score', axis=1, inplace=True)
    
    if matches.empty:
        return {"match": None, "status": "not_found", "message": f"No matching use type found for '{proposed_use}'"}
    
    best = matches.iloc[0]
    status = best[district]
    
    if status == "P":
        label = "permitted_by_right"
        message = f"'{best['use_name']}' appears permitted by right in {district}."
    elif status == "S":
        label = "requires_sup"
        message = f"'{best['use_name']}' requires a Specific Use Provision (SUP) in {district}."
    elif status == "*":
        label = "special_standards"
        message = f"'{best['use_name']}' is allowed in {district} subject to special standards. See GDC for details."
    else:
        label = "prohibited"
        message = f"'{best['use_name']}' appears prohibited in {district}."
    
    return {
        "match": best["use_name"],
        "category": best["category"],
        "status": label,
        "message": message,
    }