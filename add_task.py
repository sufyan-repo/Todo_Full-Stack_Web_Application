import requests
import json

# Base URL for the backend
BASE_URL = "http://127.0.0.1:8000"

def signin_user():
    """Sign in an existing user and return the token"""
    signin_data = {
        "email": "test2@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/sign-in", json=signin_data)
    
    if response.status_code == 200:
        result = response.json()
        print("User signed in successfully!")
        return result["token"]
    else:
        print(f"Signin failed: {response.status_code} - {response.text}")
        return None

def signup_user():
    """Sign up a new user and return the token"""
    signup_data = {
        "email": "newuser@example.com",
        "name": "New User",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/sign-up", json=signup_data)
    
    if response.status_code == 200:
        result = response.json()
        print("User signed up successfully!")
        return result["token"]
    else:
        print(f"Signup failed: {response.status_code} - {response.text}")
        return None

def create_task(token, title, description=None):
    """Create a new task using the provided token"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    task_data = {
        "title": title
    }
    
    if description:
        task_data["description"] = description
    
    response = requests.post(f"{BASE_URL}/api/tasks/", json=task_data, headers=headers)
    
    if response.status_code == 201:
        result = response.json()
        print(f"Task created successfully! ID: {result['id']}")
        print(f"Title: {result['title']}")
        print(f"Description: {result.get('description', 'N/A')}")
        return result
    else:
        print(f"Task creation failed: {response.status_code} - {response.text}")
        return None

def main():
    print("Trying to sign in user...")
    token = signin_user()
    
    # If sign in fails, try to sign up
    if not token:
        print("Trying to sign up user instead...")
        token = signup_user()
        
        if not token:
            print("Failed to sign up user. Exiting.")
            return
    
    if not token:
        print("Failed to get token. Exiting.")
        return
    
    print(f"Received token: {token[:10]}...")
    
    print("\nCreating a task...")
    task = create_task(token, "Test Task from Script", "This is a test task created via script")
    
    if task:
        print("\nTask added successfully!")
    else:
        print("\nFailed to add task.")

if __name__ == "__main__":
    main()