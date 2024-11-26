from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.research import router as research_router
from services.research_service import ResearchService

app = FastAPI(
    title="AI Research Hub",
    description="API for AI Research Hub",
    version="1.0.0"
)

# Initialize services
research_service = ResearchService()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(research_router, prefix="/api/v1", tags=["research"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Research Hub API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    await research_service.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    await research_service.close() 