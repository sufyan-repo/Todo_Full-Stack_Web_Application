import requests
import json

# Test script to verify the frontend can communicate with the backend
BASE_URL = "http://localhost:8080/api"

# Using the user ID from the database: '58e4a416-6e09-4559-bb11-86a82f86d508'
user_id = "58e4a416-6e09-4559-bb11-86a82f86d508"

# Test adding a task
test_message = "Add a task to buy groceries"

payload = {
    "message": test_message,
    "user_id": user_id
}

headers = {
    "Content-Type": "application/json",
    "Origin": "http://localhost:3000"  # Simulate frontend origin
}

try:
    print(f"Sending message: {test_message}")
    print(f"URL: {BASE_URL}/{user_id}/chat")
    print(f"Headers: {headers}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/{user_id}/chat", json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 200:
        response_data = response.json()
        print(f"\n✅ SUCCESS: Chat Response: {response_data['response']}")
        print(f"Tool Calls: {response_data['tool_calls']}")
        
        # Verify that the response structure is correct
        assert 'response' in response_data, "Response missing 'response' field"
        assert 'tool_calls' in response_data, "Response missing 'tool_calls' field"
        print("✅ Response structure is valid")
    else:
        print("❌ ERROR: Request failed")
        
except requests.exceptions.ConnectionError:
    print("❌ ERROR: Could not connect to backend server")
except requests.exceptions.RequestException as e:
    print(f"❌ ERROR: Request failed with exception: {str(e)}")
except json.JSONDecodeError:
    print(f"❌ ERROR: Response is not valid JSON: {response.text}")
except AssertionError as e:
    print(f"❌ ERROR: Response validation failed: {str(e)}")
except Exception as e:
    print(f"❌ ERROR: Unexpected error occurred: {str(e)}")