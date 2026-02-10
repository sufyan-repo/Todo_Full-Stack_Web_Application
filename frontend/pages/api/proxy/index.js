// pages/api/proxy/index.js
export default async function handler(req, res) {
  // Get the backend URL from environment variables
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  // Get the path from the URL - req.url will be something like '/api/proxy/api/tasks/'
  // We need to extract everything after '/api/proxy'
  const proxyPrefix = '/api/proxy';
  const originalPath = req.url.replace(proxyPrefix, '');
  const backendEndpoint = `${backendUrl}${originalPath}`;

  // Extract the body if present
  let body;
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    body = req.body;
  }

  try {
    // Forward the request to the backend
    const response = await fetch(backendEndpoint, {
      method: req.method,
      headers: {
        ...req.headers,
        'Content-Type': 'application/json',
        // Remove problematic headers
        connection: undefined,
        host: undefined,
        'accept-encoding': undefined,
        'content-length': undefined,
        'x-forwarded-host': undefined,
        'x-forwarded-proto': undefined,
        'x-forwarded-for': undefined,
        'x-real-ip': undefined,
        'x-vercel-forwarded-for': undefined,
        'x-vercel-id': undefined,
        'x-amzn-trace-id': undefined,
        'cf-ray': undefined,
        'cf-connecting-ip': undefined,
        'x-forwarded-server': undefined,
        'x-original-host': undefined,
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    // Get response body
    const responseBody = await response.text();

    // Set all original headers except problematic ones
    const headers = {};
    for (const [key, value] of Object.entries(response.headers)) {
      // Only forward safe headers to avoid conflicts
      if (!['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'set-cookie'].includes(key.toLowerCase())) {
        headers[key] = value;
      }
    }

    // Send the response back to the client
    res.status(response.status).set(headers).send(responseBody);
  } catch (error) {
    console.error('Proxy error:', error);
    res.status(500).json({ error: 'Proxy request failed' });
  }
}

// Allow all HTTP methods
export const config = {
  api: {
    bodyParser: false,
  },
};