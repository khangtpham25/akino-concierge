from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import Base, engine
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Runs on startup and shutdown."""
    # Create tables if they don't exist (in production, use Alembic migrations instead)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
    # Auto-generated API docs available at /docs (Swagger) and /redoc
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


# ─── Register routers here as you build them ──────────────────────────────────
# from app.api.v1 import properties, rooms, bookings, guests
# app.include_router(properties.router, prefix="/api/v1/properties", tags=["Properties"])
# app.include_router(rooms.router,      prefix="/api/v1/rooms",      tags=["Rooms"])
# app.include_router(bookings.router,   prefix="/api/v1/bookings",   tags=["Bookings"])
# app.include_router(guests.router,     prefix="/api/v1/guests",     tags=["Guests"])
