Zoning Pre-Application Analysis Tool

Live demo → zonepath.app

Enter a Garland, TX property address and a proposed use. Get back the zoning district, whether the use is permitted by right / requires a Specific Use Provision / is prohibited, the parking requirement, and an AI-generated pre-application analysis written the way a city planner would write it.

Free tier hosting — the first request may take up to a minute while the backend wakes up.

The problem

Before signing a lease, buying a lot, or starting a build, you need to know one thing: is my use allowed here, and what will it take to get approved?

Today that answer requires calling Planning staff, scheduling a pre-application meeting, or hiring a consultant. Each of those takes days to weeks. Meanwhile the person asking is often a small business owner deciding whether to sign a lease this week.

This tool answers it in about ten seconds.

Who it's for: small business owners scouting locations, commercial brokers and site selectors, small-to-mid developers, engineering and planning firms doing multi-site due diligence, and residents trying to understand what they can do with their own property.

Why this one is accurate

I'm an experienced Urban Planner. I've processed rezonings, Specific Use Provisions, and Planned Developments, and I've presented cases to the Plan Commission, City Council, and Board of Adjustment.

That matters here in concrete ways:

The 115-use land use matrix is transcribed and verified directly against the Garland Development Code, not scraped or inferred.
The AI's system prompt encodes real staff reasoning — how staff actually evaluates the seven SUP criteria, when Future Land Use Map consistency matters and when it's irrelevant, which rezoning paths staff will and won't support.
Split uses are handled the way the code handles them. "Restaurant" is permitted by right in Community Retail; "Restaurant, Drive-Through" requires an SUP. The tool surfaces both and asks the user to clarify rather than guessing.
Legally significant details are preserved: state preemption under Tex. Loc. Gov't Code Ch. 218 for multifamily and mixed-use residential, existing SUPs recorded on a parcel, the Downtown Automotive Overlay's land use credit system.

Output language is deliberately conservative throughout — "appears permitted subject to staff review," never "approved."

What it does

Address resolution — DCAD parcel data (76,000+ Garland parcels) with a geocoder fallback, plus type-ahead address suggestions.

Zoning — base district, Planned Development detection, existing SUP flags, and Future Land Use Map designation, pulled live from Garland's ArcGIS REST services.

Downtown sub-districts — the GIS layer returns a flat DT for every downtown parcel. The tool resolves the actual sub-district (Downtown Historic, Downtown Square, Uptown, InTown Residential, Suburban Corridor) through GeoJSON polygon detection, and each has its own land use matrix.

Land use matrix — 115 uses across 17 districts plus 5 downtown sub-districts, with parking requirements on every use and 50+ split-use triggers.

Accessory structures — carports, sheds, fences, detached garages, and home occupations are governed by development standards rather than the land use matrix, and are routed accordingly.

AI pre-application analysis — approval path, likely staff position, dimensional flags, red flags, and next steps. GDC section citations and the Planning phone number are computed in code rather than generated, because those were the two things a language model would not reliably get right.

Stack
Layer	Tech
Frontend	React + Vite, deployed on Vercel
Backend	Python + FastAPI, deployed on Render
AI	Claude API
Database	Supabase (lookup logging, feedback)
Data	DCAD bulk parcel data, Garland ArcGIS REST services, GeoJSON sub-district boundaries

Rate limited per IP to keep API costs bounded on a public endpoint.

Architecture
frontend/
  src/App.jsx                     single-page React UI
  src/App.css                     mobile-responsive styles

backend/
  app/routes/parcel.py            /lookup and /suggest endpoints
  app/services/zoning.py          ArcGIS + geocoder integration
  app/services/dcad.py            parcel lookup
  app/services/landuse.py         matrix lookup, split uses, fuzzy matching
  app/services/ai_analysis.py     Claude API integration and system prompt
  app/db.py                       Supabase logging
  scripts/generate_matrix.py      main matrix generator (17 districts)
  scripts/generate_dt_matrix.py   downtown matrix generator (5 sub-districts)
  scripts/generate_parcels.py     filters the county DCAD dump to Garland
  data/                           generated matrix and parcel CSVs

The city configuration layer is separated out so additional jurisdictions can be added without touching the lookup logic. Addison, Mesquite, Richardson, and Rowlett are the intended next cities.

Running locally

Requires Python 3.13 and Node 18+.

Backend

bash
cd backend
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Create backend/.env:

ANTHROPIC_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_KEY=your_key

Frontend

bash
cd frontend
npm install
npm run dev

The app runs at http://localhost:5173, the API at http://localhost:8000 (interactive docs at /docs).

Limitations

This is not a zoning determination. It's a pre-application research tool. Every result should be verified with Garland Planning & Development before a permit application is filed.

No site-specific knowledge. The tool knows the parcel's zoning, not its physical conditions. It cannot see whether an alley exists, what the lot dimensions are, or what's already built there. Site-specific items are framed as things to verify, never as findings.

Planned Developments are flagged, not parsed. A PD parcel returns links to the ordinance search and zoning map rather than a use determination, because each PD carries its own bespoke standards.

AI output requires judgment. The analysis is directionally reliable on approval paths and process, but a language model can still overstate confidence. The highest-risk values — section citations, phone numbers, parking requirements — are computed deterministically from verified data instead of generated, and that's the pattern any future high-stakes value should follow.

Garland only, for now.

Status

Garland v1 is complete and deployed. Next: additional DFW cities, an inline feedback form, and capturing the GDC's special-standards cross-reference column so every use carries its own authoritative citation.

Built by Matthew Wolverton.
