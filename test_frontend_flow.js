// Test script to simulate the frontend task creation flow
// This mimics how the API client would work with the proxy

const BASE_URL = "http://localhost:3000"; // Frontend URL

async function testTaskCreation() {
  console.log("Testing task creation flow...");
  
  // Step 1: Sign up a test user
  console.log("Step 1: Signing up test user...");
  try {
    const signupResponse = await fetch(`${BASE_URL}/api/proxy/api/auth/sign-up`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: "test_frontend@example.com",
        name: "Test User",
        password: "password123"
      })
    });
    
    const signupData = await signupResponse.json();
    if (signupResponse.ok) {
      console.log("✓ Signup successful");
      var token = signupData.token;
    } else {
      console.log("Signup failed or user exists, trying sign in...");
      // Try sign in instead
      const signinResponse = await fetch(`${BASE_URL}/api/proxy/api/auth/sign-in`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: "test_frontend@example.com",
          password: "password123"
        })
      });
      
      if (signinResponse.ok) {
        const signinData = await signinResponse.json();
        console.log("✓ Signin successful");
        token = signinData.token;
      } else {
        console.error("✗ Both signup and signin failed:", await signinResponse.text());
        return;
      }
    }
  } catch (error) {
    console.error("✗ Error during auth:", error);
    return;
  }
  
  console.log("Received token:", token.substring(0, 20) + "...");
  
  // Step 2: Create a task using the token
  console.log("Step 2: Creating a task...");
  try {
    const taskResponse = await fetch(`${BASE_URL}/api/proxy/api/tasks/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        title: "Test Task from Frontend",
        description: "This is a test task created through the frontend proxy",
        completed: false
      })
    });
    
    if (taskResponse.ok) {
      const taskData = await taskResponse.json();
      console.log("✓ Task created successfully:", taskData);
    } else {
      console.error("✗ Task creation failed:", await taskResponse.text());
    }
  } catch (error) {
    console.error("✗ Error during task creation:", error);
  }
  
  console.log("Test completed.");
}

// Run the test
testTaskCreation().catch(console.error);