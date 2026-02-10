from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel
from .core.config import settings

# Use the database URL from settings
database_url = settings.DATABASE_URL

# For SQLite, we need to use a sync engine
if database_url.startswith("sqlite://"):
    # Use sync engine for SQLite
    engine = create_engine(database_url, echo=True)
else:
    # For PostgreSQL, we need to use the asyncpg driver for async operations
    if "postgresql" in database_url:
        # Replace postgresql with postgresql+asyncpg for async operations
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
    from sqlalchemy.ext.asyncio import create_async_engine
    engine = create_async_engine(
        database_url,
        echo=True,
        future=True,
        pool_pre_ping=True,
        pool_recycle=300,
    )

# Create sessionmaker for sync operations
sync_sessionmaker = sessionmaker(bind=engine, expire_on_commit=False)

def get_sync_session():
    with sync_sessionmaker() as session:
        yield session

async def create_db_and_tables():
    # Check if engine is an async engine by checking its type
    engine_type_str = str(type(engine))
    if 'Async' in engine_type_str or 'asyncpg' in database_url:
        # For async engine (PostgreSQL with asyncpg), use async context manager
        from sqlalchemy.ext.asyncio import AsyncEngine
        if isinstance(engine, AsyncEngine):
            async with engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
        else:
            # Fallback: For sync engine (SQLite)
            with engine.begin() as conn:
                SQLModel.metadata.create_all(conn)
    else:
        # For sync engine (SQLite)
        with engine.begin() as conn:
            SQLModel.metadata.create_all(conn)