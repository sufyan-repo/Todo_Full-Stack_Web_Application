import requests
import json

# Test the frontend proxy
PROXY_BASE_URL = "http://localhost:3000/api/proxy"

# First, let's try to sign up a test user through the proxy
print("Creating test user through proxy...")
signup_response = requests.post(f"{PROXY_BASE_URL}/api/auth/sign-up", json={
    "email": "test3@example.com",
    "name": "Test User",
    "password": "password123"
})

if signup_response.status_code == 200:
    print("Signup successful through proxy:", signup_response.json())
    token = signup_response.json()["token"]
else:
    print("Signup through proxy failed:", signup_response.text)
    # Try to sign in if user already exists
    signin_response = requests.post(f"{PROXY_BASE_URL}/api/auth/sign-in", json={
        "email": "test3@example.com",
        "password": "password123"
    })
    if signin_response.status_code == 200:
        print("Signin successful through proxy:", signin_response.json())
        token = signin_response.json()["token"]
    else:
        print("Both signup and signin through proxy failed:", signin_response.text)
        exit(1)

# Now try to create a task with the token through the proxy
print("\nTrying to create a task through proxy...")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

task_response = requests.post(f"{PROXY_BASE_URL}/api/tasks/", json={
    "title": "Test Task Through Proxy",
    "description": "This is a test task created through proxy",
    "completed": False
}, headers=headers)

print("Task creation through proxy response:", task_response.status_code, task_response.text)