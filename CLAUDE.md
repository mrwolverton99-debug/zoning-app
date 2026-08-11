# CLAUDE.md

Context for Claude Code sessions on this repo. Read this first.

## What this project is

A zoning pre-application analysis tool for Garland, TX. A user enters a property
address and a proposed use, and gets back:

- The zoning district for that parcel
- Land use matrix result (permitted by right / requires SUP / prohibited)
- Parking requirement for the proposed use
- An AI-generated pre-application analysis written in the voice of a city planner

Built by a City of Garland Planner II. The domain knowledge encoded here (verified
GDC matrix values, real staff report patterns, Garland GIS quirks) is the core value
of the project — treat it as authoritative and do not "correct" it from general
zoning knowledge.

Architecture is multi-city by design. Garland is city #1. Addison, TX is next,
followed by Mesquite, Richardson, and Rowlett.

## Stack

| Layer | Tech |
|---|---|
| Frontend | React + Vite (port 5173) |
| Backend | Python FastAPI + uvicorn (port 8000) |
| Database / logging | Supabase |
| AI | Claude API |
| Data | DCAD bulk parcel data, Garland ArcGIS REST services, GeoJSON for DT sub-districts |

UI theme is navy/gold municipal.

## Running locally

Backend (from `backend/`):

```
venv\Scripts\activate
uvicorn app.main:app --reload
```

Frontend (from `frontend/`):

```
npm run dev
```

Backend API docs at http://127.0.0.1:8000/docs

Secrets live in `backend/.env` (Supabase URL + key, Anthropic API key).
**Never commit `.env`.** Confirm it stays in `.gitignore`.

## Key files

```
frontend/src/App.jsx                        entire React frontend
frontend/src/App.css                        mobile-responsive CSS
backend/app/routes/parcel.py                /lookup and /suggest endpoints
backend/app/services/landuse.py             matrix lookup, split uses, fuzzy matcher
backend/app/services/ai_analysis.py         Claude AI analysis
backend/app/services/zoning.py              GIS / geocoder
backend/app/services/dcad.py                DCAD parcel lookup
backend/app/db.py                           Supabase logging
backend/scripts/generate_matrix.py          main matrix generator (17 districts)
backend/scripts/generate_dt_matrix.py       downtown matrix generator (5 sub-districts)
backend/data/garland_land_use_matrix.csv    generated main matrix w/ parking column
backend/data/garland_dt_land_use_matrix.csv generated DT matrix
```

## Data pipeline

`ACCOUNT_INFO.CSV` is the full Dallas County DCAD dump (351MB, ~800k rows,
every column DCAD publishes) — gitignored, kept locally only, never deployed.

`backend/scripts/generate_parcels.py` filters it down to `garland_parcels.csv`
(76,769 rows, 6.17MB, committed) — Garland rows only, and only the six columns
`dcad.py` actually reads (`ACCOUNT_NUM`, `GIS_PARCEL_ID`, `STREET_NUM`,
`FULL_STREET_NAME`, `PROPERTY_CITY`, `PROPERTY_ZIPCODE`).

The running app reads only the filtered file (`cities.py`'s `dcad_file`
points at `data/garland_parcels.csv`, not the raw dump). New cities follow
the same pattern: drop the city's raw DCAD export locally, add a filter step
for it, commit only the small filtered output.

## CRITICAL: matrix integrity

This has caused significant rework before. Get it right.

- The **main matrix has exactly 17 district columns**: AG, SF-E, SF-10, SF-7, SF-5,
  SFA, 2F, MF, NO, CO, NS, CR, LC, HC, IN, UR, UB
- **There is no DT column in the main matrix.** Do not add one.
- Every row must have **exactly 17 values**. `[:17]` truncation handles padding.
- DT lookups route to a **separate 5-column matrix**: DH, DS, U, IR, SC
- When changing matrix data, do a **full rewrite of the affected file**, not
  piecemeal row edits. Partial edits here have repeatedly introduced misalignment.

## Domain corrections that must be preserved

These were discovered the hard way. Do not regress them.

- DCAD's `PROPERTY_CITY` field for Garland is stored as `"GARLAND (DALLAS CO)"` —
  not `"GARLAND"`.
- Garland's ArcGIS server requires **HTTPS with a legacy SSL adapter**.
- The GIS zoning layer returns `"DT"` for all downtown parcels with **no
  sub-district detail**. Sub-district (DH/DS/U/IR/SC) is resolved separately via
  GeoJSON polygon detection.
- Garland staff no longer uses a "decline to recommend" pattern in staff reports.
  Do not generate that language.
- Fuzzy matching must use **whole-word matching**. Without it, "house" matches
  "Townhouse" and returns wrong results.

## Verified matrix values (spot-check references)

- **Personal Services**: S in NO/CO, P in CR/NS/LC/HC, S in IN, P in UR/UB
- **Automobile Repair, Minor**: S in CR
- **Smoke Shop**: S in IN only
- Footnote system handles conditional SUP requirements — e.g. Light Manufacturing
  requires an SUP when contiguous to or within 100' of residential zoning or use.

## Liability language

Output must say **"appears permitted subject to staff review"** — never "approved,"
"allowed," or anything that reads as a determination. This tool does not make
zoning determinations. Keep the disclaimer prominent.

## Known issues

- AI occasionally hallucinates site-specific conditions (alley access, yard depth)
  that it cannot actually know from available data. Partially mitigated via system
  prompt. Not fully eliminated.
- FLUM red-flag hallucination partially fixed via system prompt.

## Current punch list

- [ ] Rate limiting on the API (**required before public deploy** — protects the
      Anthropic key from unbounded cost)
- [ ] Inline feedback form (mailto link is broken for most users)
- [ ] Favicon + page title update
- [ ] Disclaimer color: green → gray
- [ ] Loading skeleton UI
- [ ] Replace `print()` statements with the Python `logging` module
- [ ] Verify the dimensional standards the AI cites for CR and other districts
- [ ] Deploy (frontend → Vercel, backend → Render/Railway; update CORS, move env
      vars to host dashboard)

## Working style

- Prefer **complete file rewrites over piecemeal fixes**, especially for the land
  use matrix.
- Matrix values are verified directly against the GDC PDF. If a correction is
  given, apply it immediately — do not re-litigate it.
- Communication is direct and fast-paced. Skip preamble.
