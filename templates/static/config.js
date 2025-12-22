// API Configuration
const API_BASE_URL = 'https://portfolio-backend-1-53hz.onrender.com';

// Export for use in other files
window.API_CONFIG = {
    BASE_URL: API_BASE_URL,
    ENDPOINTS: {
        ARTICLES: '/api/articles',
        POEMS: '/api/poems',
        COMMENTS: '/api/comments',
        MESSAGES: '/api/messages',
        SUBSCRIBERS: '/api/subscribers',
        LOGIN: '/api/login'
    }
};
