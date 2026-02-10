// Simple test to check API connectivity
async function testApiConnection() {
  console.log('Testing API connection...');
  
  try {
    // Test the health endpoint first
    console.log('Testing health endpoint...');
    const healthResponse = await fetch('/api/proxy/health');
    const healthData = await healthResponse.json();
    console.log('Health check result:', healthData, 'Status:', healthResponse.status);
    
    // Test the tasks endpoint (should fail without auth)
    console.log('\nTesting tasks endpoint (should fail without auth)...');
    const tasksResponse = await fetch('/api/proxy/api/tasks/');
    console.log('Tasks response status:', tasksResponse.status);
    
    if (tasksResponse.status === 401) {
      console.log('Correctly received 401 - authentication required');
    } else {
      const tasksData = await tasksResponse.json();
      console.log('Tasks response:', tasksData);
    }
  } catch (error) {
    console.error('Error during API test:', error);
  }
}

// Run the test
testApiConnection();