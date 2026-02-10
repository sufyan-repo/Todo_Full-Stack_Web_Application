# Simple test to check if there are import errors
try:
    from main import app
    print("[OK] Main app imported successfully")
except Exception as e:
    print(f"[ERROR] Error importing main app: {e}")

try:
    from app.routes import chat
    print("[OK] Chat route imported successfully")
except Exception as e:
    print(f"[ERROR] Error importing chat route: {e}")

try:
    from app.agents.qwen_agent import QwenAgent
    print("[OK] Qwen agent imported successfully")
except Exception as e:
    print(f"[ERROR] Error importing Qwen agent: {e}")

try:
    from app.mcp_server import handler
    print("[OK] MCP server imported successfully")
except Exception as e:
    print(f"[ERROR] Error importing MCP server: {e}")

try:
    from app.db import engine
    print("[OK] Database engine imported successfully")
except Exception as e:
    print(f"[ERROR] Error importing database engine: {e}")

try:
    from models import Conversation, Message
    print("[OK] Models imported successfully")
except Exception as e:
    print(f"[ERROR] Error importing models: {e}")

print("Import tests completed.")