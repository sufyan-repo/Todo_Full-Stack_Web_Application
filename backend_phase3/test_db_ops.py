#!/usr/bin/env python3
"""
Simple test to check if the database operations work correctly
"""
import asyncio
from app.mcp_server import handler

async def test_database_operations():
    print("Testing database operations...")
    
    try:
        # Test adding a task
        result = await handler.add_task("Test task", "Test description", "test_user")
        print(f"Add task result: {result}")

        # Test listing tasks
        result = await handler.list_tasks("test_user")
        print(f"List tasks result: {result}")

        print("[SUCCESS] Database operations working correctly")
    except Exception as e:
        print(f"✗ Database operation error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_database_operations())