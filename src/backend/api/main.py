from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.research import router as research_router

app = FastAPI(title="AI Research Hub API")

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
async def read_root():
    return {
        "message": "Welcome to AI Research Hub API",
        "version": "1.0.0",
        "docs_url": "/docs"
    } 