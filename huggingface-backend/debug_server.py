import asyncio
import uvicorn
from app.main import app
from app.db import create_db_and_tables

async def startup_event():
    """Run startup tasks"""
    print("Creating database tables...")
    try:
        await create_db_and_tables()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise

def run_server():
    # Run startup event first
    asyncio.run(startup_event())
    
    # Then run the server
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    run_server()