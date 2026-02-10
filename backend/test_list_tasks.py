import requests
import json

# Test the chat endpoint to list tasks
BASE_URL = "http://localhost:8080/api"

# Using the user ID from the database: '58e4a416-6e09-4559-bb11-86a82f86d508'
user_id = "58e4a416-6e09-4559-bb11-86a82f86d508"

# Test listing tasks
test_message = "list my tasks"

payload = {
    "message": test_message,
    "user_id": user_id
}

headers = {
    "Content-Type": "application/json"
}

try:
    print(f"Sending message: {test_message}")
    response = requests.post(f"{BASE_URL}/{user_id}/chat", json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        response_data = response.json()
        print(f"Chat Response: {response_data['response']}")
        print(f"Tool Calls: {response_data['tool_calls']}")
    else:
        print("Error occurred during chat request")
        
except Exception as e:
    print(f"Exception occurred: {str(e)}")