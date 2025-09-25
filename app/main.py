from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 👈 add this import

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

# 👇 CORS middleware goes here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


# ✅ Only include the real app routers
app.include_router(api_router)
