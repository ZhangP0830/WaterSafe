const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  // Enable CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
  };

  // Handle preflight OPTIONS request
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  try {
    // Extract the API path from the request
    const apiPath = event.path.replace('/.netlify/functions/proxy', '');
    
    // Construct the backend URL
    const backendUrl = `http://13.239.237.65:8000${apiPath}`;
    
    // Forward the request to the backend
    const response = await fetch(backendUrl, {
      method: event.httpMethod,
      headers: {
        'Content-Type': 'application/json',
        ...(event.headers.authorization && { 'Authorization': event.headers.authorization })
      },
      body: event.httpMethod !== 'GET' ? event.body : undefined
    });

    // Get the response data
    const data = await response.text();
    
    // Return the response with proper headers
    return {
      statusCode: response.status,
      headers: {
        ...headers,
        'Content-Type': response.headers.get('content-type') || 'application/json'
      },
      body: data
    };
    
  } catch (error) {
    console.error('Proxy error:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Internal server error',
        message: error.message
      })
    };
  }
};
