from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time

from app.core.config import settings
from app.core.logger import setup_logger
from app.db.database import engine, Base
from app.api.routers import address

logger = setup_logger("app.main")

# Initialize database tables
logger.info("Ensuring database tables exist...")
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="REST API for managing an address book with geodesic coordinate validation and search.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Request duration logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} completed in {process_time:.4f}s with status {response.status_code}")
    return response

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error. Please contact support if the issue persists."},
    )

# Include the address router
app.include_router(address.router, prefix="/addresses", tags=["Addresses"])

@app.get("/health", tags=["System"])
def health_check():
    """Endpoint for basic infrastructure health check."""
    return {"status": "ok", "app_name": settings.app_name}
