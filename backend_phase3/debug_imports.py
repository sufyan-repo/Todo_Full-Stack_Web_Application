#!/usr/bin/env python3
"""
Debug script to identify where the server is crashing
"""
import traceback
import sys

print("Starting import test...")

try:
    print("1. Importing main app...")
    from main import app
    print("   [OK] Main app imported successfully")
except Exception as e:
    print(f"   [ERROR] Error importing main app: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("2. Testing app routes...")
    from app.routes import chat
    print("   [OK] Chat routes imported successfully")
except Exception as e:
    print(f"   [ERROR] Error importing chat routes: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("3. Testing agents...")
    from app.agents.qwen_agent import QwenAgent
    print("   [OK] Qwen agent imported successfully")
except Exception as e:
    print(f"   [ERROR] Error importing Qwen agent: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("4. Testing MCP server...")
    from app.mcp_server import handler
    print("   [OK] MCP server imported successfully")
except Exception as e:
    print(f"   [ERROR] Error importing MCP server: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("5. Testing models...")
    from models import Conversation, Message, Task
    print("   [OK] Models imported successfully")
except Exception as e:
    print(f"   [ERROR] Error importing models: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("6. Testing database...")
    from app.db import engine
    print("   [OK] Database engine imported successfully")
except Exception as e:
    print(f"   [ERROR] Error importing database: {e}")
    traceback.print_exc()
    sys.exit(1)

print("All imports successful!")