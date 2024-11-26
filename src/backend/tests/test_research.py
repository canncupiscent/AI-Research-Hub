import asyncio
from services.research_service import ResearchService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_research_service():
    """Test the complete research pipeline."""
    try:
        service = ResearchService()
        topic = "transformer models in natural language processing"
        
        logger.info(f"Testing research pipeline for topic: {topic}")
        
        # Test query generation
        query = await service.generate_search_query(topic)
        logger.info(f"Generated query: {query}")
        
        # Test paper search
        papers = await service.search_papers(query, limit=5)
        logger.info(f"Found {len(papers)} papers")
        for paper in papers:
            logger.info(f"Paper: {paper['title']}")
        
        # Test paper analysis
        if papers:
            analysis = await service.analyze_papers(papers)
            logger.info("Analysis results:")
            logger.info(analysis)
        
        logger.info("Test completed successfully")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_research_service()) 