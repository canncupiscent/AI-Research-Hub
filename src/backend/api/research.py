"""Research API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from services.research_service import ResearchService

router = APIRouter()

@router.get("/health/ollama")
async def check_ollama_health(
    service: ResearchService = Depends(ResearchService)
):
    """Check if Ollama service is healthy."""
    try:
        result = await service.check_ollama_health()
        if result["status"] != "healthy":
            raise HTTPException(status_code=503, detail=result)
        return result
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/search")
async def search_papers(
    query: str,
    page: Optional[int] = 1,
    limit: Optional[int] = 20,
    sources: Optional[str] = "semantic_scholar,arxiv",
    service: ResearchService = Depends(ResearchService)
):
    """Search for research papers."""
    try:
        # Convert sources string to list
        source_list = sources.split(',') if sources else ["semantic_scholar", "arxiv"]
        results = await service.search_papers(query, page, limit, source_list)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/paper/{paper_id}")
async def get_paper_details(
    paper_id: str,
    service: ResearchService = Depends(ResearchService)
):
    """Get detailed information about a specific paper."""
    try:
        paper = await service.get_paper_details(paper_id)
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")
        return paper
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/{paper_id}")
async def analyze_paper(
    paper_id: str,
    service: ResearchService = Depends(ResearchService)
):
    """Analyze a paper using Ollama."""
    try:
        analysis = await service.analyze_paper(paper_id)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 