const axios = require('axios');

async function testProxy() {
  try {
    console.log('Testing proxy route...');
    const response = await axios.get('http://localhost:3000/api/proxy/health');
    console.log('Response:', response.data);
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

testProxy();