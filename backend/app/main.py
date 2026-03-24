from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.parcel import router as parcel_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parcel_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}