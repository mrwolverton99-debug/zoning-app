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

def log_feedback(address: str, base_zone: str, proposed_use: str, issue: str):
    try:
        db = get_db()
        db.table("feedback").insert({
            "address": address,
            "base_zone": base_zone,
            "proposed_use": proposed_use,
            "issue_description": issue,
        }).execute()
    except Exception as e:
        print(f"Supabase feedback error: {e}")