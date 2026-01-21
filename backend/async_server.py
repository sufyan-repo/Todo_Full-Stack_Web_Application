import asyncio
import sys
import traceback
from app.main import app
from app.db import create_db_and_tables
import uvicorn
import logging

# Set up logging to see what's happening
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def main():
    print("Starting backend server setup...")
    
    try:
        print("Initializing database...")
        await create_db_and_tables()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Database initialization failed: {e}")
        traceback.print_exc()
        sys.exit(1)
    
    print("Database setup complete. Starting server...")
    
    try:
        # Configure uvicorn with explicit settings for Hugging Face
        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=7860,
            log_level="debug",
            reload=False,
            workers=1
        )
        server = uvicorn.Server(config)

        print("Server configured. Starting...")
        await server.serve()
        
    except Exception as e:
        print(f"Server startup failed: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()