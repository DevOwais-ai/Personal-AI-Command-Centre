from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.core.config import settings
from app.core.logging import setup_logging


setup_logging()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "AI-powered personal operating system for "
        "communication, tasks, appointments, and automation."
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in settings.CORS_ORIGINS.split(",")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    health_router,
    prefix=settings.API_PREFIX,
)


@app.get("/")
def root():
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "status": "running",
    }