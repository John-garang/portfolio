// Admin API Configuration
const ADMIN_API_BASE_URL = 'https://portfolio-backend-1-53hz.onrender.com';

// Override fetch globally to replace localhost URLs
const originalFetch = window.fetch;
window.fetch = function(url, options) {
    if (typeof url === 'string' && (url.includes('localhost:3000') || url.startsWith('http://localhost:3000'))) {
        url = url.replace('http://localhost:3000', ADMIN_API_BASE_URL);
        console.log('Redirected API call to:', url);
    }
    return originalFetch(url, options);
};

// Also set global API config
window.API_BASE_URL = ADMIN_API_BASE_URL;