# backend/scripts/gdc_watcher.py
# Monitors the Garland GDC Ordinance Disposition Table for amendments
# and uses Claude to analyze what changed and whether your CSVs need updating.
#
# Run: python backend/scripts/gdc_watcher.py
# Schedule weekly via Task Scheduler

import asyncio
import json
import os
import re
import tempfile
import urllib.request
from datetime import datetime

import fitz  # PyMuPDF
import requests
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

DISPOSITION_TABLE_URL = "https://ecode360.com/40080759"
ECODE_PDF_BASE = "https://ecode360.com/GA6318/laws/"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_FILE = os.path.normpath(
    os.path.join(SCRIPT_DIR, "..", "data", "gdc_watch.json")
)

# Chapters that affect your app
WATCH_CHAPTERS = {"Ch. 2", "Ch. 6", "Ch. 7"}

CHAPTER_NOTES = {
    "Ch. 2": "LAND USE MATRIX — may need CSV updates",
    "Ch. 6": "DEFINITIONS — may need USE_DEFINITIONS updates in landuse.py",
    "Ch. 7": "DOWNTOWN DISTRICT — may need DT CSV updates",
    "Ch. 4": "SITE DEVELOPMENT — check for parking/landscaping changes",
}

CLAUDE_PROMPT = """You are analyzing a Garland TX municipal ordinance amendment to determine 
what changes need to be made to a zoning pre-application tool.

The tool maintains two CSV files:
1. garland_land_use_matrix.csv — columns: category, use_name, AG, SF-E, SF-10, SF-7, SF-5, SFA, 2F, MF, NO, CO, NS, CR, LC, HC, IN, UR, UB, DT
   Values: P=permitted by right, S=requires SUP, *=special standards, blank=not permitted
2. garland_dt_land_use_matrix.csv — columns: category, use_name, DH, DS, U, IR, SC
   Same value scheme, for Downtown sub-districts only.

Analyze the ordinance text and return ONLY a JSON object with this exact structure:
{
  "summary": "plain English 2-3 sentence summary of what changed",
  "affects_app": true or false,
  "csv_changes": [
    {
      "file": "garland_land_use_matrix.csv or garland_dt_land_use_matrix.csv",
      "use_name": "exact use name as it appears in the matrix",
      "district": "district code e.g. NS or DS",
      "old_value": "P or S or * or blank",
      "new_value": "P or S or * or blank",
      "notes": "any context"
    }
  ],
  "other_changes": ["any non-matrix changes worth knowing about"],
  "action_required": "specific instruction or No action required"
}

Return ONLY the JSON. No preamble, no markdown, no explanation.

ORDINANCE TEXT:
"""


def load_store():
    if os.path.exists(STORE_FILE):
        with open(STORE_FILE) as f:
            return json.load(f)
    return {"last_ordinance": None, "history": [], "analyses": {}}


def save_store(store):
    os.makedirs(os.path.dirname(STORE_FILE), exist_ok=True)
    with open(STORE_FILE, "w") as f:
        json.dump(store, f, indent=2)


def extract_pdf_text(pdf_url: str) -> str:
    """Download and extract text from an ordinance PDF."""
    req = urllib.request.Request(
        pdf_url, headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(data)
        tmp = f.name

    try:
        doc = fitz.open(tmp)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
    finally:
        try:
            os.unlink(tmp)
        except Exception:
            pass

    return text


def analyze_with_claude(ordinance_text: str, ordinance_num: str) -> dict:
    """Send ordinance text to Claude and get structured analysis back."""
    print(f"  Sending to Claude for analysis...")

    # Truncate if very long — keep first 15k chars which covers most ordinances
    text_to_send = ordinance_text[:15000]

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": CLAUDE_PROMPT + text_to_send,
                }
            ],
        },
        timeout=30,
    )

    raw = response.json()["content"][0]["text"].strip()

    # Strip markdown fences if present
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    return json.loads(raw)


def find_pdf_url(ordinance_num: str) -> str | None:
    """
    Attempt to construct the eCode PDF URL for a given ordinance number.
    eCode URLs follow the pattern LF + numeric ID — we can't know the ID
    without fetching the page, so we try the disposition table link pattern.
    Returns None if we can't determine the URL.
    """
    # We'd need to scrape the actual ordinance link from eCode.
    # For now return None and fall back to manual — this can be improved
    # by parsing the disposition table page for href links.
    return None


async def fetch_ordinance_table(page) -> list[dict]:
    """Fetch and parse the ordinance disposition table."""
    await page.goto(
        DISPOSITION_TABLE_URL, wait_until="domcontentloaded", timeout=60000
    )
    await page.wait_for_timeout(4000)

    body = await page.inner_text("body")
    if "security verification" in body.lower() or "cloudflare" in body.lower():
        print("  Cloudflare check — please click verify in the browser window...")
        await page.wait_for_timeout(30000)

    # Also grab href links so we can find PDF URLs
    links = await page.query_selector_all("a[href*='.pdf'], a[href*='laws/']")
    pdf_links = {}
    for link in links:
        href = await link.get_attribute("href")
        text = await link.inner_text()
        if href:
            # Try to match ordinance numbers in the link text or nearby
            nums = re.findall(r"\b7\d{3}\b", text)
            for n in nums:
                pdf_links[n] = href if href.startswith("http") else f"https://ecode360.com{href}"

    rows = await page.query_selector_all("table tr")
    ordinances = []

    for row in rows:
        cells = await row.query_selector_all("td")
        if len(cells) < 3:
            continue
        texts = [await c.inner_text() for c in cells]
        texts = [t.strip() for t in texts]

        if not texts[0].isdigit():
            continue

        # Try to find PDF link in this row
        row_links = await row.query_selector_all("a")
        pdf_url = None
        for rl in row_links:
            href = await rl.get_attribute("href")
            if href and (".pdf" in href or "laws/" in href):
                pdf_url = href if href.startswith("http") else f"https://ecode360.com{href}"
                break

        ordinances.append({
            "ordinance":   texts[0],
            "date":        texts[1] if len(texts) > 1 else "",
            "description": texts[2] if len(texts) > 2 else "",
            "chapters":    texts[3] if len(texts) > 3 else "",
            "pages":       texts[4] if len(texts) > 4 else "",
            "pdf_url":     pdf_url or pdf_links.get(texts[0]),
        })

    return ordinances


async def main():
    store = load_store()
    if "analyses" not in store:
        store["analyses"] = {}

    last_ord = store.get("last_ordinance")

    print(f"GDC Ordinance Watcher — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Last known ordinance: {last_ord or 'None (first run)'}")
    print(f"Fetching disposition table...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            ordinances = await fetch_ordinance_table(page)
        except Exception as e:
            print(f"✗ Failed to fetch table: {e}")
            await browser.close()
            return

        await browser.close()

    if not ordinances:
        print("✗ No ordinances parsed — table may not have loaded")
        return

    print(f"✓ Parsed {len(ordinances)} ordinances")
    latest = ordinances[-1]["ordinance"]

    # First run
    if last_ord is None:
        store["last_ordinance"] = latest
        store["history"] = ordinances
        save_store(store)
        print(f"\n✓ First run — baseline stored at ordinance {latest}")
        return

    # Find new ordinances
    new_ordinances = [
        o for o in ordinances
        if int(o["ordinance"]) > int(last_ord)
    ]

    if not new_ordinances:
        print(f"\n✓ No new ordinances since {last_ord} — GDC unchanged")
        store["last_ordinance"] = latest
        save_store(store)
        return

    print(f"\n{'='*60}")
    print(f"  {len(new_ordinances)} NEW ORDINANCE(S) FOUND")
    print(f"{'='*60}")

    action_needed = False

    for o in new_ordinances:
        chapters_hit = [ch for ch in WATCH_CHAPTERS if ch in o["chapters"]]
        print(f"\n  Ordinance {o['ordinance']} — {o['date']}")
        print(f"  {o['description']}")
        print(f"  Chapters: {o['chapters']}")

        if not chapters_hit:
            print(f"  ✓ No action needed for zoning app")
            continue

        action_needed = True
        print(f"  🚨 Relevant chapters: {', '.join(chapters_hit)}")

        # Try to get and analyze the PDF
        pdf_url = o.get("pdf_url")
        if pdf_url and ANTHROPIC_API_KEY:
            print(f"  Downloading ordinance PDF...")
            try:
                pdf_text = extract_pdf_text(pdf_url)
                print(f"  ✓ Extracted {len(pdf_text)} chars from PDF")

                analysis = analyze_with_claude(pdf_text, o["ordinance"])
                store["analyses"][o["ordinance"]] = analysis

                print(f"\n  📋 CLAUDE ANALYSIS:")
                print(f"  {analysis.get('summary', 'No summary')}")

                if analysis.get("csv_changes"):
                    print(f"\n  CSV CHANGES NEEDED:")
                    for change in analysis["csv_changes"]:
                        print(f"    • {change['file']}")
                        print(f"      {change['use_name']} — {change['district']}: "
                              f"{change['old_value'] or 'blank'} → {change['new_value']}")
                        if change.get("notes"):
                            print(f"      Note: {change['notes']}")
                else:
                    print(f"  ✓ No CSV changes needed")

                if analysis.get("other_changes"):
                    print(f"\n  Other changes:")
                    for c in analysis["other_changes"]:
                        print(f"    • {c}")

                print(f"\n  Action: {analysis.get('action_required', 'Review manually')}")

            except Exception as e:
                print(f"  ✗ Could not analyze PDF: {e}")
                print(f"  Manual review required: {pdf_url or 'find PDF on ecode360.com/GA6318'}")
        else:
            if not pdf_url:
                print(f"  ⚠ No PDF link found — review manually at ecode360.com/GA6318")
            if not ANTHROPIC_API_KEY:
                print(f"  ⚠ No ANTHROPIC_API_KEY — set in .env to enable auto-analysis")

        # Chapter-specific notes
        for ch in [c.strip() for c in o["chapters"].replace(";", ",").split(",")]:
            note = CHAPTER_NOTES.get(ch)
            if note:
                print(f"  [{ch}] {note}")

    print(f"\n{'='*60}")
    if action_needed:
        print("  Review changes above and update CSVs as needed")
        print(f"  Full GDC: https://ecode360.com/GA6318")
    else:
        print("  ✓ No updates needed for zoning app")

    store["last_ordinance"] = latest
    store["history"] = ordinances
    save_store(store)


if __name__ == "__main__":
    asyncio.run(main())