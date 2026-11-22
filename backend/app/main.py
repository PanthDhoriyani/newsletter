from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils.logging import setup_logging
from app.database import create_all_tables
from app.scheduler.daily_scheduler import start_scheduler, stop_scheduler

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_all_tables()
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()

app = FastAPI(
    title="AI-Powered Personal Digital Newspaper API",
    description="Backend engine for researching, compiling, writing, and publishing an automated digital newspaper.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS setup
cors_origins = settings.cors_origins if isinstance(settings.cors_origins, list) else ["*"]
allow_all = "*" in cors_origins or not cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all else cors_origins,
    allow_credentials=False if allow_all else True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API Routers
from app.routers import (
    editions,
    articles,
    reading,
    archive,
    breaking_news,
    weekly,
    dashboard
)

app.include_router(editions.router, prefix="/api")
app.include_router(articles.router, prefix="/api")
app.include_router(reading.router, prefix="/api")
app.include_router(archive.router, prefix="/api")
app.include_router(breaking_news.router, prefix="/api")
app.include_router(weekly.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "AI-Powered Personal Digital Newspaper",
        "version": "1.0.0",
        "timezone": settings.timezone
    }
