// pages/api/proxy/[...path].js
export default async function handler(req, res) {
  // Get the backend URL from environment variables
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  // Get the path from the URL - using the catch-all route
  const { path } = req.query;
  const backendPath = Array.isArray(path) ? path.join('/') : path || '';
  
  // Extract query parameters from the original request URL
  const urlParts = req.url.split('?');
  const queryString = urlParts.length > 1 ? '?' + urlParts[1] : '';
  const backendEndpoint = `${backendUrl}/${backendPath}${queryString}`;
  
  console.log('Backend endpoint:', backendEndpoint); // Debug log
  
  try {
    // Create headers object without the problematic ones
    const headers = {};
    for (const [key, value] of Object.entries(req.headers)) {
      // Skip problematic headers
      if (
        ![
          'connection',
          'host',
          'accept-encoding',
          'content-length',
          'x-forwarded-host',
          'x-forwarded-proto',
          'x-forwarded-for',
          'x-real-ip',
          'x-vercel-forwarded-for',
          'x-vercel-id',
          'x-amzn-trace-id',
          'cf-ray',
          'cf-connecting-ip',
          'x-forwarded-server',
          'x-original-host',
          'content-encoding',
          'transfer-encoding'
        ].includes(key.toLowerCase())
      ) {
        headers[key] = value;
      }
    }
    
    // Add content type if not present
    if (!headers['content-type']) {
      headers['content-type'] = 'application/json';
    }

    // Extract the body if present
    let body = null;
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      // Use the raw body if available, otherwise use req.body
      body = req.body ? JSON.stringify(req.body) : null;
    }

    // Forward the request to the backend
    const response = await fetch(backendEndpoint, {
      method: req.method,
      headers,
      body,
    });

    console.log('Backend response status:', response.status); // Debug log

    // Get response body
    const responseBody = await response.text();

    // Set response status and headers
    res.status(response.status);

    // Forward safe headers
    for (const [key, value] of response.headers.entries()) {
      if (!['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'set-cookie'].includes(key.toLowerCase())) {
        res.setHeader(key, value);
      }
    }

    // Send the response body
    res.send(responseBody);
  } catch (error) {
    console.error('Proxy error:', error);
    res.status(500).json({ error: 'Proxy request failed', details: error.message });
  }
}

// Allow all HTTP methods
export const config = {
  api: {
    bodyParser: true, // Enable body parsing for this route
  },
};