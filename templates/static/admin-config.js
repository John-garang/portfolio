// Admin API Configuration
const ADMIN_API_BASE_URL = 'https://portfolio-backend-1-53hz.onrender.com';

// Override fetch globally to replace portfolio-backend-1-53hz.onrender.com URLs
const originalFetch = window.fetch;
window.fetch = function(url, options) {
    if (typeof url === 'string' && (url.includes('portfolio-backend-1-53hz.onrender.com') || url.startsWith('https://portfolio-backend-1-53hz.onrender.com'))) {
        url = url.replace('https://portfolio-backend-1-53hz.onrender.com', ADMIN_API_BASE_URL);
        console.log('Redirected API call to:', url);
    }
    return originalFetch(url, options);
};

// Also set global API config
window.API_BASE_URL = ADMIN_API_BASE_URL;
