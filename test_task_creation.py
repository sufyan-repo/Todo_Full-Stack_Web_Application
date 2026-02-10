import requests
import json

# Test the backend directly
BASE_URL = "http://127.0.0.1:8000"

# First, let's try to sign up a test user
print("Creating test user...")
signup_response = requests.post(f"{BASE_URL}/api/auth/sign-up", json={
    "email": "test2@example.com",
    "name": "Test User",
    "password": "password123"
})

if signup_response.status_code == 200:
    print("Signup successful:", signup_response.json())
    token = signup_response.json()["token"]
else:
    print("Signup failed:", signup_response.text)
    # Try to sign in if user already exists
    signin_response = requests.post(f"{BASE_URL}/api/auth/sign-in", json={
        "email": "test2@example.com",
        "password": "password123"
    })
    if signin_response.status_code == 200:
        print("Signin successful:", signin_response.json())
        token = signin_response.json()["token"]
    else:
        print("Both signup and signin failed:", signin_response.text)
        exit(1)

# Now try to create a task with the token
print("\nTrying to create a task...")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

task_response = requests.post(f"{BASE_URL}/api/tasks/", json={
    "title": "Test Task",
    "description": "This is a test task",
    "completed": False
}, headers=headers)

print("Task creation response:", task_response.status_code, task_response.text)