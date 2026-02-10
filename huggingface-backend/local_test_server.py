import asyncio
from app.main import app
from app.core.config import settings
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
import uvicorn
import sys
import os

# Override the DATABASE_URL to use SQLite for local testing
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./todo_local_test.db'

# Add current directory to path to ensure modules can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Reconfigure the database engine to use SQLite
database_url = os.environ['DATABASE_URL']

# Create a new engine with SQLite
engine = create_async_engine(
    database_url,
    echo=True,
    future=True,
    pool_pre_ping=True,
    pool_recycle=300,
)

async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def initialize_database():
    """Initialize the database on startup"""
    print("Initializing database with SQLite...")
    try:
        await create_db_and_tables()
        print("Database initialized successfully with SQLite!")
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
    # Run the server with the requested configuration
    uvicorn.run(
        app,
        host="0.0.0.0",  # Changed to match requirement
        port=7860,       # Changed to match requirement
        log_level="info",
        timeout_keep_alive=30,
        workers=1
    )

if __name__ == "__main__":
    main()