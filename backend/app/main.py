"""
Main FastAPI application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time

from .config import settings
from .api.routes import api_router
from .models.database import db
from .services.llm_service import llm_service
from .services.vector_db_service import vector_db_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    logger.info("Starting Intelligent ATS System...")
    
    # Check services
    services_status = {
        "ollama": llm_service.check_health(),
        "qdrant": vector_db_service.check_health()
    }
    
    for service, status in services_status.items():
        if status:
            logger.info(f"✓ {service.capitalize()} service is healthy")
        else:
            logger.warning(f"✗ {service.capitalize()} service is not available")
    
    # Load persisted data if exists
    try:
        db.load_from_file("data/ats_data.json")
        logger.info("Loaded persisted data")
    except:
        logger.info("No persisted data found, starting fresh")
    
    yield
    
    # Cleanup
    logger.info("Shutting down...")
    try:
        db.save_to_file("data/ats_data.json")
        logger.info("Saved data to disk")
    except:
        pass

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multi-Agent ATS System for Agentic AI Roles",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"completed in {process_time:.3f}s "
        f"with status {response.status_code}"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include routers
app.include_router(api_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    services = {
        "ollama": llm_service.check_health(),
        "qdrant": vector_db_service.check_health()
    }
    
    stats = db.get_statistics()
    
    all_healthy = all(services.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "version": settings.APP_VERSION,
        "services": services,
        "statistics": stats,
        "configuration": {
            "ollama_model": settings.OLLAMA_MODEL,
            "embedding_model": settings.EMBEDDING_MODEL,
            "weights": {
                "agentic": settings.WEIGHT_AGENTIC,
                "technical": settings.WEIGHT_TECHNICAL,
                "semantic": settings.WEIGHT_SEMANTIC,
                "experience": settings.WEIGHT_EXPERIENCE
            }
        }
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )