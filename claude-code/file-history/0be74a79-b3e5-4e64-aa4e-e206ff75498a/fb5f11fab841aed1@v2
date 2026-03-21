from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from app.config import get_settings
from app.routers import reflection, synthesis, notifications, counselor
from app.models.requests import EmbedRequest, EmbedResponse
from app.services.embedding_service import embedding_service

app = FastAPI(
    title="COMPASS AI Service",
    description="Signal mining, reflection prompts, and synthesis for COMPASS",
    version="1.0.0",
)

# CORS — only allow our web app
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.app_url],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


# Auth middleware — verify AI_SERVICE_SECRET_KEY on all non-health routes
@app.middleware("http")
async def verify_service_key(request: Request, call_next):
    if request.url.path in ["/health", "/", "/docs", "/openapi.json"]:
        return await call_next(request)

    service_key = request.headers.get("X-Service-Key")
    expected_key = settings.ai_service_secret_key

    if not service_key or service_key != expected_key:
        return __import__("fastapi").responses.JSONResponse(
            status_code=401,
            content={"error": "Unauthorized"},
        )

    return await call_next(request)


# Include routers
app.include_router(reflection.router)
app.include_router(synthesis.router)
app.include_router(notifications.router)
app.include_router(counselor.router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "compass-ai"}


@app.get("/")
async def root():
    return {"service": "COMPASS AI Service", "version": "1.0.0"}


@app.post("/embed", response_model=EmbedResponse)
async def embed_text(request: EmbedRequest) -> EmbedResponse:
    """Generate embedding for a text using Voyage AI."""
    try:
        embedding = embedding_service.embed_text(request.text)
        return EmbedResponse(embedding=embedding)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
