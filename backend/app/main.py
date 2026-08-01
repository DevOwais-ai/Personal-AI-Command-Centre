from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.core.config import settings
from app.core.logging import setup_logging

from app.api.auth import router as auth_router

from app.api.users import router as users_router

from app.api.tasks import router as tasks_router

from app.api.appointments import router as appointments_router

from app.api.reminders import router as reminders_router

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

app.include_router(
    auth_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    users_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    tasks_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    appointments_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    reminders_router,
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

