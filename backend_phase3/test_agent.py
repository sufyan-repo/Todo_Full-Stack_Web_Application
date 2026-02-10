#!/usr/bin/env python3
"""
Test script to isolate the issue with the chat endpoint
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

# Test the agent directly
from app.agents.qwen_agent import QwenAgent

async def test_agent():
    print("Testing QwenAgent directly...")
    agent = QwenAgent()
    
    try:
        # Test with a simple request
        result = await agent.process_request("Say hello", "test_user", [])
        print(f"Agent response: {result}")
        print("✓ Agent working correctly")
    except Exception as e:
        print(f"✗ Agent error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent())