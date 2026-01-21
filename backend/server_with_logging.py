import asyncio
import logging
from app.main import app
from app.db import create_db_and_tables
import uvicorn

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def startup_event():
    """Initialize database on startup"""
    try:
        logger.info("Creating database tables...")
        await create_db_and_tables()
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

if __name__ == "__main__":
    # Run startup tasks
    asyncio.run(startup_event())
    
    # Configure uvicorn logging
    uvicorn_config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8080,
        log_level="info",
        reload=False
    )
    
    server = uvicorn.Server(uvicorn_config)
    
    logger.info("Starting server on http://127.0.0.1:8080")
    try:
        server.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise