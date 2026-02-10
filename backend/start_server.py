import asyncio
from app.main import app
from app.db import create_db_and_tables
import uvicorn
import sys
import os

# Add current directory to path to ensure modules can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def initialize_database():
    """Initialize the database on startup"""
    print("Initializing database...")
    try:
        await create_db_and_tables()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    # Initialize database first
    try:
        asyncio.run(initialize_database())
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        sys.exit(1)
    
    print("Starting FastAPI server...")
    # Run the server
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        timeout_keep_alive=30,
        workers=1
    )

if __name__ == "__main__":
    main()