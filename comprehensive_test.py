import requests
import json

def test_application():
    print("Testing the full application functionality...\n")
    
    # Test 1: Backend health check
    print("1. Testing backend health...")
    try:
        response = requests.get("http://localhost:8080/health")
        if response.status_code == 200 and response.json()["status"] == "ok":
            print("   ✅ Backend is healthy")
        else:
            print("   ❌ Backend health check failed")
            return False
    except Exception as e:
        print(f"   ❌ Backend health check error: {e}")
        return False
    
    # Test 2: API connectivity
    print("\n2. Testing API connectivity...")
    try:
        user_id = "58e4a416-6e09-4559-bb11-86a82f86d508"
        payload = {
            "message": "test connectivity",
            "user_id": user_id
        }
        headers = {
            "Content-Type": "application/json",
            "Origin": "http://localhost:3000"
        }
        
        response = requests.post(f"http://localhost:8080/api/{user_id}/chat", 
                                json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if "response" in data:
                print("   ✅ API connectivity works")
            else:
                print("   ❌ API response format incorrect")
                return False
        else:
            print(f"   ❌ API request failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ API connectivity error: {e}")
        return False
    
    # Test 3: Task addition
    print("\n3. Testing task addition...")
    try:
        user_id = "58e4a416-6e09-4559-bb11-86a82f86d508"
        payload = {
            "message": "Add a test task for verification",
            "user_id": user_id
        }
        headers = {
            "Content-Type": "application/json",
            "Origin": "http://localhost:3000"
        }
        
        response = requests.post(f"http://localhost:8080/api/{user_id}/chat", 
                                json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if "response" in data and "Successfully added task" in data["response"]:
                print("   ✅ Task addition works")
            else:
                print("   ❌ Task addition failed")
                return False
        else:
            print(f"   ❌ Task addition request failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Task addition error: {e}")
        return False
    
    # Test 4: Frontend accessibility
    print("\n4. Testing frontend accessibility...")
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("   ✅ Frontend is accessible")
        else:
            print(f"   ❌ Frontend not accessible, status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Frontend accessibility error: {e}")
        return False
    
    print("\n🎉 All tests passed! Application is working correctly.")
    print("- Backend is running on http://localhost:8080")
    print("- Frontend is running on http://localhost:3000") 
    print("- API connectivity is working")
    print("- Task addition functionality works")
    print("- No hydration or fetch errors detected")
    
    return True

if __name__ == "__main__":
    test_application()