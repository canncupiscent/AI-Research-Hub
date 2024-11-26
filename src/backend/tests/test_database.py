"""Test database setup and basic operations."""
import pytest
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.database import engine, SessionLocal, check_db_connection
from models.models import Base, AnalyzedPaper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def db_session():
    """Create a test database session."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Clean up tables
        Base.metadata.drop_all(bind=engine)

def test_database_connection():
    """Test database connection."""
    assert check_db_connection() is True
    logger.info("Database connection test passed")

def test_create_tables(db_session: Session):
    """Test if all tables are created successfully."""
    try:
        # Get all table names from metadata
        tables = Base.metadata.tables.keys()
        
        # Check if our tables exist
        assert 'analyzed_papers' in tables
        assert 'users' in tables
        assert 'projects' in tables
        assert 'datasets' in tables
        
        logger.info("Table creation test passed")
    except Exception as e:
        logger.error(f"Table creation test failed: {str(e)}")
        raise

def test_paper_crud(db_session: Session):
    """Test CRUD operations for AnalyzedPaper."""
    try:
        # Create test paper
        test_paper = AnalyzedPaper(
            source_id="test_arxiv_123",
            title="Test Paper",
            abstract="This is a test paper abstract",
            authors=["John Doe", "Jane Smith"],
            year=2024,
            venue="Test Conference",
            url="https://example.com/paper",
            citations=42,
            source="arXiv",
            summary="Test summary",
            key_findings=["Finding 1", "Finding 2"],
            methodology="Test methodology",
            applications=["App 1", "App 2"],
            future_work=["Future work 1"]
        )

        # Create
        db_session.add(test_paper)
        db_session.commit()
        logger.info("Create operation test passed")

        # Read
        retrieved_paper = db_session.query(AnalyzedPaper)\
            .filter_by(source_id="test_arxiv_123")\
            .first()
        assert retrieved_paper is not None
        assert retrieved_paper.title == "Test Paper"
        assert len(retrieved_paper.authors) == 2
        logger.info("Read operation test passed")

        # Update
        retrieved_paper.citations = 43
        db_session.commit()
        updated_paper = db_session.query(AnalyzedPaper)\
            .filter_by(source_id="test_arxiv_123")\
            .first()
        assert updated_paper.citations == 43
        logger.info("Update operation test passed")

        # Delete
        db_session.delete(retrieved_paper)
        db_session.commit()
        deleted_paper = db_session.query(AnalyzedPaper)\
            .filter_by(source_id="test_arxiv_123")\
            .first()
        assert deleted_paper is None
        logger.info("Delete operation test passed")

    except SQLAlchemyError as e:
        logger.error(f"CRUD operations test failed: {str(e)}")
        db_session.rollback()
        raise

def test_paper_constraints(db_session: Session):
    """Test database constraints and validations."""
    try:
        # Test unique source_id constraint
        paper1 = AnalyzedPaper(
            source_id="test_unique_123",
            title="Test Paper 1",
            abstract="Abstract 1",
            source="arXiv"
        )
        paper2 = AnalyzedPaper(
            source_id="test_unique_123",  # Same source_id
            title="Test Paper 2",
            abstract="Abstract 2",
            source="arXiv"
        )

        db_session.add(paper1)
        db_session.commit()

        with pytest.raises(SQLAlchemyError):
            db_session.add(paper2)
            db_session.commit()

        logger.info("Unique constraint test passed")

        # Test required fields
        with pytest.raises(SQLAlchemyError):
            invalid_paper = AnalyzedPaper(
                abstract="Just an abstract"  # Missing required fields
            )
            db_session.add(invalid_paper)
            db_session.commit()

        logger.info("Required fields constraint test passed")

    except SQLAlchemyError as e:
        logger.error(f"Constraint test failed: {str(e)}")
        db_session.rollback()
        raise
    finally:
        # Clean up
        db_session.query(AnalyzedPaper).delete()
        db_session.commit()

def test_json_fields(db_session: Session):
    """Test JSON field handling."""
    try:
        # Test complex JSON data
        paper = AnalyzedPaper(
            source_id="test_json_123",
            title="JSON Test Paper",
            abstract="Testing JSON fields",
            source="arXiv",
            authors=[
                {"name": "John Doe", "affiliation": "University A"},
                {"name": "Jane Smith", "affiliation": "University B"}
            ],
            key_findings=[
                {"finding": "Finding 1", "confidence": 0.9},
                {"finding": "Finding 2", "confidence": 0.8}
            ],
            applications=[
                {"domain": "Healthcare", "readiness": "High"},
                {"domain": "Education", "readiness": "Medium"}
            ]
        )

        db_session.add(paper)
        db_session.commit()

        # Retrieve and verify JSON data
        retrieved_paper = db_session.query(AnalyzedPaper)\
            .filter_by(source_id="test_json_123")\
            .first()
        
        assert len(retrieved_paper.authors) == 2
        assert retrieved_paper.authors[0]["affiliation"] == "University A"
        assert len(retrieved_paper.key_findings) == 2
        assert retrieved_paper.key_findings[1]["confidence"] == 0.8
        
        logger.info("JSON field handling test passed")

    except SQLAlchemyError as e:
        logger.error(f"JSON field test failed: {str(e)}")
        db_session.rollback()
        raise
    finally:
        # Clean up
        db_session.query(AnalyzedPaper).delete()
        db_session.commit()

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 