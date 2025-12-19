// API Client for Backend Communication
const API_BASE = 'https://portfolio-backend-1-53hz.onrender.com/api';

const API = {
    // Messages
    async getMessages() {
        const res = await fetch(`${API_BASE}/messages`);
        return res.json();
    },

    async addMessage(message) {
        const res = await fetch(`${API_BASE}/messages`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(message)
        });
        return res.json();
    },

    async deleteMessage(id) {
        const res = await fetch(`${API_BASE}/messages/${id}`, {
            method: 'DELETE'
        });
        return res.json();
    },

    async updateMessage(id, data) {
        const res = await fetch(`${API_BASE}/messages/${id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },

    // Analytics
    async getAnalytics() {
        const res = await fetch(`${API_BASE}/analytics`);
        return res.json();
    },

    async updateAnalytics(data) {
        const res = await fetch(`${API_BASE}/analytics`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },

    // Blog Posts
    async getBlogPosts() {
        const res = await fetch(`${API_BASE}/blog-posts`);
        return res.json();
    },

    async addBlogPost(post) {
        const res = await fetch(`${API_BASE}/blog-posts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(post)
        });
        return res.json();
    },

    async deleteBlogPost(id) {
        const res = await fetch(`${API_BASE}/blog-posts/${id}`, {
            method: 'DELETE'
        });
        return res.json();
    },

    // Projects
    async getProjects() {
        const res = await fetch(`${API_BASE}/projects`);
        return res.json();
    },

    async addProject(project) {
        const res = await fetch(`${API_BASE}/projects`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(project)
        });
        return res.json();
    },

    async deleteProject(id) {
        const res = await fetch(`${API_BASE}/projects/${id}`, {
            method: 'DELETE'
        });
        return res.json();
    }
};
