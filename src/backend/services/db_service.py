"""Database service for paper analysis storage."""
import logging
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.models import AnalyzedPaper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self, session: Session):
        """Initialize database service with session."""
        self.session = session
        logger.info("DatabaseService initialized")

    async def store_paper_analysis(self, paper_data: Dict, analysis_data: Dict) -> Optional[Dict]:
        """Store paper analysis in database."""
        try:
            # Create paper object
            paper = AnalyzedPaper(
                source_id=paper_data.get("source_id"),
                title=paper_data.get("title"),
                abstract=paper_data.get("abstract"),
                authors=paper_data.get("authors"),
                year=paper_data.get("year"),
                venue=paper_data.get("venue"),
                url=paper_data.get("url"),
                citations=paper_data.get("citations"),
                source=paper_data.get("source"),
                summary=analysis_data.get("summary"),
                key_findings=analysis_data.get("key_findings"),
                methodology=analysis_data.get("methodology"),
                applications=analysis_data.get("applications"),
                future_work=analysis_data.get("future_work")
            )

            # Add to database
            self.session.add(paper)
            self.session.commit()
            logger.info(f"Stored analysis for paper: {paper.title}")
            
            return paper.to_dict()
            
        except IntegrityError:
            logger.info(f"Paper already analyzed: {paper_data.get('source_id')}")
            self.session.rollback()
            # Return existing analysis
            existing = self.get_paper_analysis(paper_data.get("source_id"))
            return existing.to_dict() if existing else None
            
        except Exception as e:
            logger.error(f"Error storing paper analysis: {str(e)}")
            self.session.rollback()
            return None

    def get_paper_analysis(self, source_id: str) -> Optional[AnalyzedPaper]:
        """Get paper analysis from database."""
        try:
            paper = self.session.query(AnalyzedPaper).filter_by(source_id=source_id).first()
            return paper
        except Exception as e:
            logger.error(f"Error retrieving paper analysis: {str(e)}")
            return None

    def get_recent_analyses(self, limit: int = 10) -> List[Dict]:
        """Get recent paper analyses."""
        try:
            papers = self.session.query(AnalyzedPaper)\
                .order_by(AnalyzedPaper.created_at.desc())\
                .limit(limit)\
                .all()
            return [paper.to_dict() for paper in papers]
        except Exception as e:
            logger.error(f"Error retrieving recent analyses: {str(e)}")
            return []

    def get_paper_stats(self) -> Dict:
        """Get statistics about analyzed papers."""
        try:
            total = self.session.query(AnalyzedPaper).count()
            arxiv_count = self.session.query(AnalyzedPaper)\
                .filter_by(source="arXiv")\
                .count()
            semantic_count = self.session.query(AnalyzedPaper)\
                .filter_by(source="Semantic Scholar")\
                .count()
            
            return {
                "total_papers": total,
                "arxiv_papers": arxiv_count,
                "semantic_scholar_papers": semantic_count
            }
        except Exception as e:
            logger.error(f"Error retrieving paper stats: {str(e)}")
            return {
                "total_papers": 0,
                "arxiv_papers": 0,
                "semantic_scholar_papers": 0
            } 