"""
FastAPI Application Entrypoint
Serves REST API endpoints, agentic chat router, and luxury single-page application.
"""

import logging
import os
import uuid
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.config import settings
from app.services.property_service import property_service
from app.services.lead_service import lead_service
from app.agent.agent import agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("darglobal-app")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production Agentic Real Estate Assistant connecting DarGlobal Luxury Developments & Wasalt Saudi Proptech Marketplace."
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatRequest(BaseModel):
    message: str = Field(..., description="User query or message")
    session_id: Optional[str] = Field(None, description="Client session ID for conversation memory")
    model: Optional[str] = Field(None, description="OpenRouter model name")
    api_key: Optional[str] = Field(None, description="Optional OpenRouter API key override")

class ConsultationRequest(BaseModel):
    client_name: str
    email: str
    phone: Optional[str] = None
    property_id: Optional[str] = None
    property_name: Optional[str] = None
    preferred_datetime: Optional[str] = None
    notes: Optional[str] = None

# Static Files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": settings.APP_NAME, "version": settings.APP_VERSION}

@app.get("/health")
async def health_check():
    stats = property_service.get_summary_stats()
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "properties_indexed": stats["total_properties"],
        "darglobal_developments": stats["darglobal_developments"],
        "wasalt_listings": stats["wasalt_listings"],
        "default_model": settings.OPENROUTER_MODEL
    }

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    session_id = req.session_id or str(uuid.uuid4())
    
    try:
        result = await agent.chat(
            session_id=session_id,
            message=req.message,
            model=req.model,
            api_key=req.api_key
        )
        return result
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal agent execution error.")

@app.get("/api/properties")
async def list_properties(
    query: Optional[str] = None,
    city: Optional[str] = None,
    country: Optional[str] = None,
    source: Optional[str] = None,
    min_price_usd: Optional[float] = None,
    max_price_usd: Optional[float] = None,
    bedrooms: Optional[int] = None,
    brand_partner: Optional[str] = None,
    property_type: Optional[str] = None,
    limit: int = Query(20, ge=1, le=50)
):
    results = property_service.filter(
        query=query,
        city=city,
        country=country,
        source=source if source != "All" else None,
        min_price_usd=min_price_usd,
        max_price_usd=max_price_usd,
        bedrooms=bedrooms,
        brand_partner=brand_partner,
        property_type=property_type,
        limit=limit
    )
    return {"count": len(results), "properties": results}

@app.get("/api/properties/{property_id}")
async def get_property(property_id: str):
    prop = property_service.get_by_id(property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found.")
    return prop

@app.post("/api/consultation")
async def book_consultation(req: ConsultationRequest):
    booking = lead_service.create_booking(
        client_name=req.client_name,
        email=req.email,
        phone=req.phone,
        property_id=req.property_id,
        property_name=req.property_name,
        preferred_datetime=req.preferred_datetime,
        notes=req.notes
    )
    return {"success": True, "booking": booking}

@app.get("/api/models")
async def get_models():
    return {
        "default_model": settings.OPENROUTER_MODEL,
        "available_free_models": settings.FREE_MODELS,
        "active_has_env_key": bool(settings.OPENROUTER_API_KEY)
    }

@app.get("/api/stats")
async def get_stats():
    return property_service.get_summary_stats()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
