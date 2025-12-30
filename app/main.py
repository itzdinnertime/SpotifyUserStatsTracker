"""
FastAPI application for serving Spotify stats.
Run with: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import stats, user
from .models import init_db

# Initialize database on startup
init_db()

# Create FastAPI app
app = FastAPI(title="Spotify Stats API")

# Allow React frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route files
app.include_router(stats.router, prefix="/api/stats", tags=["Stats"])
app.include_router(user.router, prefix="/api/user", tags=["User"])


@app.get("/")
def root():
    return {"message": "Spotify Stats API", "docs": "/docs"}
