import asyncio
import uvicorn
import sys
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

# Define settings class
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    PROJECT_NAME: str = "Todo API"
    BETTER_AUTH_SECRET: str = "dev-secret"
    BETTER_AUTH_URL: str = "http://localhost:3000"
    DATABASE_URL: str = "sqlite+aiosqlite:///./todo_local_test.db"

settings = Settings()

# Override the DATABASE_URL to use SQLite for local testing
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./todo_local_test.db'

# Add current directory to path to ensure modules can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Use SQLite for local testing
database_url = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///./todo_local_test.db')

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log full traceback to server stdout for debugging
    traceback.print_exception(type(exc), exc, exc.__traceback__)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )

# Import routers after app is defined to avoid circular imports
from app.api import tasks, auth
app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api/tasks")

@app.get("/health")
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

def main():
    print("Starting FastAPI server with SQLite database...")
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