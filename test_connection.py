import requests

# Test if the backend is accessible
try:
    response = requests.get("http://127.0.0.1:8080/health")
    print(f"Backend health check response: {response.status_code}")
    print(f"Response content: {response.json()}")
except requests.exceptions.ConnectionError:
    print("Connection error: Could not connect to backend at http://127.0.0.1:8080")
except Exception as e:
    print(f"Error connecting to backend: {e}")

# Also try with localhost
try:
    response = requests.get("http://localhost:8080/health")
    print(f"Backend health check response (localhost): {response.status_code}")
    print(f"Response content: {response.json()}")
except requests.exceptions.ConnectionError:
    print("Connection error: Could not connect to backend at http://localhost:8080")
except Exception as e:
    print(f"Error connecting to backend (localhost): {e}")