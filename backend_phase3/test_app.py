import asyncio
import json
from httpx import AsyncClient
from main import app


async def test_chat_endpoint():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        # Test the root endpoint
        response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Phase 3 AI Chatbot API"}
        print("✓ Root endpoint test passed")

        # Test the chat endpoint
        user_id = "test_user_123"
        payload = {
            "message": "Add a task to buy groceries",
            "user_id": user_id
        }
        response = await ac.post(f"/api/{user_id}/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        print(f"✓ Chat endpoint test passed: {data['response']}")


if __name__ == "__main__":
    asyncio.run(test_chat_endpoint())