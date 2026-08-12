import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_client: Client = None

def get_db() -> Client:
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client

def log_lookup(result: dict, proposed_use: str = None):
    try:
        db = get_db()
        db.table("lookups").insert({
            "address": f"{result.get('street_num','')} {result.get('street_name','')}".strip(),
            "street_num": result.get("street_num"),
            "street_name": result.get("street_name"),
            "base_zone": result.get("base_zone"),
            "dt_subdistrict": result.get("dt_subdistrict"),
            "flum": result.get("flum_designation"),
            "proposed_use": proposed_use,
            "use_status": result.get("proposed_use_check", {}).get("status") if result.get("proposed_use_check") else None,
            "is_pd": result.get("requires_manual_review", False),
            "geocoded_fallback": result.get("geocoded_fallback", False),
        }).execute()
    except Exception as e:
        print(f"Supabase log error: {e}")

def log_feedback(
    issue: str,
    address: str = None,
    city: str = None,
    proposed_use: str = None,
    base_zone: str = None,
    matched_use: str = None,
    reply_email: str = None,
):
    db = get_db()
    db.table("feedback").insert({
        "address": address,
        "city": city,
        "proposed_use": proposed_use,
        "base_zone": base_zone,
        "matched_use": matched_use,
        "issue_description": issue,
        "reply_email": reply_email,
    }).execute()