from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.proof import router as proof_router
from app.db.database import init_db
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="PROVE — Proof Builder & Evidence Intelligence API",
    description="Automated evidence extraction, skill verification, L0-L5 proficiency, 7-dimension scoring, and proof gap resolution API.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware for React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "PROVE Engine API",
        "llm_provider": settings.LLM_PROVIDER,
        "database": "SQLite initialized",
    }

app.include_router(proof_router)
