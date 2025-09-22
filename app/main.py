from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import api_router
from app.core.database import get_db_provider


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    yield
    db_provider = get_db_provider()
    await db_provider.close()


app = FastAPI(
    title="FastAPI Template Backend",
    version="0.1.0",
    lifespan=lifespan
)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


# ✅ Only include the real app routers
app.include_router(api_router)
