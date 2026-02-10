from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
import os

# Use SQLite for local development to avoid needing a PostgreSQL server
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot.db")
ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")

# Async engine for FastAPI
engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)