// Test script to verify the proxy is working
async function testProxy() {
  console.log('Testing proxy functionality...');

  // First, let's try to sign in
  const signInResult = await fetch('http://localhost:3000/api/proxy/api/auth/sign-in', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: 'test2@example.com',
      password: 'password123'
    })
  });

  console.log('Sign in response:', signInResult.status);
  const signInData = await signInResult.json();
  console.log('Sign in data:', signInData);

  if (signInResult.ok) {
    const token = signInData.token;
    console.log('Got token, trying to create task...');

    // Now try to create a task with the token
    const taskResponse = await fetch('http://localhost:3000/api/proxy/api/tasks/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        title: 'Test from Proxy',
        description: 'Task created via proxy route'
      })
    });

    console.log('Task creation response:', taskResponse.status);
    const taskData = await taskResponse.json();
    console.log('Task data:', taskData);
  } else {
    console.log('Sign in failed, trying sign up...');

    // Try to sign up
    const signUpResponse = await fetch('http://localhost:3000/api/proxy/api/auth/sign-up', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'proxytest@example.com',
        name: 'Proxy Test User',
        password: 'password123'
      })
    });

    console.log('Sign up response:', signUpResponse.status);
    const signUpData = await signUpResponse.json();
    console.log('Sign up data:', signUpData);
  }
}

testProxy();