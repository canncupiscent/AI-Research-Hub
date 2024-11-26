from sqlalchemy import create_engine, text
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

DATABASE_URL = Config.DATABASE_URL
engine = create_engine(DATABASE_URL)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connected:", result.scalar())
            return True
    except Exception as e:
        print("Database connection failed:", str(e))
        return False 