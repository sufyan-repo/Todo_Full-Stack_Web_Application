from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings

from urllib.parse import urlparse

# Ensure PostgreSQL URL format for asyncpg
database_url = settings.DATABASE_URL

# Convert standard PostgreSQL URL to asyncpg format if needed
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Parse URL to determine SSL settings
parsed = urlparse(database_url)
hostname = parsed.hostname or ""

# Set connect args for PostgreSQL
connect_args = {}

# Enable SSL for non-local hosts (e.g., cloud databases like Supabase/Neon)
if hostname not in ("localhost", "127.0.0.1", "0.0.0.0", ""):
    connect_args = {"ssl": "require"}

engine = create_async_engine(
    database_url,
    echo=True,
    future=True,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=300,
)

from sqlmodel import SQLModel

async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)