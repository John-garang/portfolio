// API Client for Backend Communication
const API_BASE = 'https://portfolio-backend-1-53hz.onrender.com/api';

function validateURL(url) {
    try {
        const parsedURL = new URL(url);
        const allowedHosts = ['portfolio-backend-1-53hz.onrender.com'];
        if (!allowedHosts.includes(parsedURL.hostname)) {
            throw new Error('Invalid host');
        }
        return url;
    } catch (e) {
        throw new Error('Invalid URL');
    }
}

const API = {
    // Messages
    async getMessages() {
        const url = validateURL(`${API_BASE}/messages`);
        const res = await fetch(url);
        return res.json();
    },

    async addMessage(message) {
        const url = validateURL(`${API_BASE}/messages`);
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(message)
        });
        return res.json();
    },

    async deleteMessage(id) {
        const url = validateURL(`${API_BASE}/messages/${id}`);
        const res = await fetch(url, {
            method: 'DELETE'
        });
        return res.json();
    },

    async updateMessage(id, data) {
        const url = validateURL(`${API_BASE}/messages/${id}`);
        const res = await fetch(url, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },

    // Analytics
    async getAnalytics() {
        const url = validateURL(`${API_BASE}/analytics`);
        const res = await fetch(url);
        return res.json();
    },

    async updateAnalytics(data) {
        const url = validateURL(`${API_BASE}/analytics`);
        const res = await fetch(url, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },

    // Blog Posts
    async getBlogPosts() {
        const url = validateURL(`${API_BASE}/blog-posts`);
        const res = await fetch(url);
        return res.json();
    },

    async addBlogPost(post) {
        const url = validateURL(`${API_BASE}/blog-posts`);
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(post)
        });
        return res.json();
    },

    async deleteBlogPost(id) {
        const url = validateURL(`${API_BASE}/blog-posts/${id}`);
        const res = await fetch(url, {
            method: 'DELETE'
        });
        return res.json();
    },

    // Projects
    async getProjects() {
        const url = validateURL(`${API_BASE}/projects`);
        const res = await fetch(url);
        return res.json();
    },

    async addProject(project) {
        const url = validateURL(`${API_BASE}/projects`);
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(project)
        });
        return res.json();
    },

    async deleteProject(id) {
        const url = validateURL(`${API_BASE}/projects/${id}`);
        const res = await fetch(url, {
            method: 'DELETE'
        });
        return res.json();
    }
};

