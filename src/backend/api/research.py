"""Research API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from services.research_service import ResearchService

router = APIRouter()

@router.get("/search")
async def search_papers(
    query: str,
    page: Optional[int] = 1,
    limit: Optional[int] = 10,
    service: ResearchService = Depends(ResearchService)
):
    """Search for research papers."""
    try:
        results = await service.search_papers(query, page, limit)
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

@router.post("/analyze")
async def analyze_paper(
    paper_id: str,
    service: ResearchService = Depends(ResearchService)
):
    """Analyze a paper using LLM."""
    try:
        analysis = await service.analyze_paper(paper_id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 