"""Script to run all tests."""
import pytest
import logging
from models.database import check_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run all tests."""
    try:
        # First check if database is accessible
        logger.info("Checking database connection before running tests...")
        if not check_db_connection():
            logger.error("Database connection failed. Please check your database configuration.")
            return False

        # Run the tests
        logger.info("Running tests...")
        result = pytest.main([
            "tests",
            "-v",
            "--capture=no",  # Show print statements
            "--log-cli-level=INFO",  # Show logs
            "--tb=short"  # Shorter traceback format
        ])

        if result == 0:
            logger.info("All tests passed successfully!")
            return True
        else:
            logger.error("Some tests failed. Please check the test output above.")
            return False

    except Exception as e:
        logger.error(f"Error running tests: {str(e)}")
        return False

if __name__ == "__main__":
    main() 