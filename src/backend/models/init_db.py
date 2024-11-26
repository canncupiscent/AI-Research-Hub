"""Script to initialize the database."""
import logging
from database import init_db, check_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Initialize the database."""
    try:
        # Check database connection
        logger.info("Checking database connection...")
        if not check_db_connection():
            logger.error("Failed to connect to database")
            return

        # Initialize database tables
        logger.info("Initializing database tables...")
        init_db()
        logger.info("Database initialization completed successfully")

    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 