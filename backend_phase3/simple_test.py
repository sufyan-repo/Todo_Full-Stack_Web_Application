import asyncio
import httpx
from main import app

async def test_chat():
    # Test the root endpoint first
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testserver") as ac:
        response = await ac.get("/")
        print(f"Root Status: {response.status_code}")
        print(f"Root Content: {response.json()}")

    # Test the chat endpoint
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testserver") as ac:
        response = await ac.post("/api/test_user/chat", json={
            "message": "Say hello",
            "user_id": "test_user"
        })
        print(f"Chat Status: {response.status_code}")
        print(f"Chat Content: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_chat())