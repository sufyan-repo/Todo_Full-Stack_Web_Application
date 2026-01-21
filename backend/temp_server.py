
import uvicorn
from app.main import app

print("Starting uvicorn server...")
uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")
