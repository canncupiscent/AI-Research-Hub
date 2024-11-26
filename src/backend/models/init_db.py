import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine
from models import Base

def init_database():
    try:
        print("Creating database tables...")
        Base.metadata.create_all(engine)
        print("Database tables created successfully!")
        return True
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")
        print(f"Error type: {type(e)}")
        return False

if __name__ == "__main__":
    print("Initializing database tables...")
    init_database() 