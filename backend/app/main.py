import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.limiter import limiter
from app.routes.parcel import router as parcel_router
from app.db import log_lookup

load_dotenv()

# Comma-separated list, e.g. "https://zoning-app.vercel.app,https://staging.example.com"
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]


def _rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    slowapi's default handler responds outside CORSMiddleware's wrapping, so
    the browser reports a CORS error instead of surfacing the 429 — the
    frontend's rate-limit message never displays. Build the same CORS
    headers CORSMiddleware would have added, by hand.
    """
    response = JSONResponse(
        {"detail": f"Rate limit exceeded: {exc.detail}"}, status_code=429
    )
    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )
    origin = request.headers.get("origin")
    if origin in CORS_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
    return response


app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parcel_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}