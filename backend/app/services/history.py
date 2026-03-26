# backend/app/services/history.py
# Supabase integration for saving lookup history
# Requires SUPABASE_URL and SUPABASE_KEY in .env

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")


def save_lookup(address: str, result: dict) -> None:
    """
    Save a lookup result to Supabase.
    Fails silently — never block the main response.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        return

    try:
        payload = {
            "address":        address,
            "base_zone":      result.get("base_zone"),
            "dt_subdistrict": result.get("dt_subdistrict"),
            "flum":           result.get("flum_designation"),
            "proposed_use":   result.get("proposed_use_check", {}).get("match"),
            "use_status":     result.get("proposed_use_check", {}).get("status"),
            "geocoded":       result.get("geocoded_fallback", False),
            "looked_up_at":   datetime.utcnow().isoformat(),
        }

        requests.post(
            f"{SUPABASE_URL}/rest/v1/lookups",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            },
            json=payload,
            timeout=3,
        )
    except Exception:
        pass  # Never let history saving break the main response