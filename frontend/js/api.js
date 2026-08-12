const PROD_API_URL = 'https://projektor.onrender.com/api';
const LOCAL_API_URL = 'http://localhost:5000/api';

const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_BASE = isLocalhost ? LOCAL_API_URL : PROD_API_URL;

// Helper to handle API requests
async function fetchAPI(endpoint, options = {}) {
    // Ensure credentials (cookies) are sent with every request for session auth
    options.credentials = 'include';
    
    if (!options.headers) {
        options.headers = {};
    }
    
    if (options.body && !(options.body instanceof FormData)) {
        options.headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(options.body);
    }

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Something went wrong');
        }
        
        return { success: true, data };
    } catch (error) {
        console.error('API Error:', error);
        return { success: false, error: error.message };
    }
}

// Global Auth state checking
async function checkAuth() {
    const res = await fetchAPI('/auth/me');
    return res;
}

async function logout() {
    const res = await fetchAPI('/auth/logout', { method: 'POST' });
    if (res.success) {
        window.location.href = 'index.html';
    }
}

// Global Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

// Helper to handle image URLs (local vs cloud)
function getImageUrl(path) {
    if (!path) return '';
    if (path.startsWith('http://') || path.startsWith('https://')) {
        return path;
    }
    const backendBase = isLocalhost ? 'http://localhost:5000' : 'https://projektor.onrender.com';
    return `${backendBase}${path}`;
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update icons if they exist
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        themeIcon.innerHTML = newTheme === 'light' 
            ? '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>' // Sun icon
            : '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>'; // Moon icon
    }
}

// Run immediately to prevent flash
initTheme();

// Likes and Comments
async function toggleLike(projectId) {
    return await fetchAPI(`/projects/${projectId}/like`, { method: 'POST' });
}

async function getComments(projectId) {
    return await fetchAPI(`/projects/${projectId}/comments`);
}

async function postComment(projectId, content) {
    return await fetchAPI(`/projects/${projectId}/comments`, {
        method: 'POST',
        body: { content }
    });
}

async function deleteComment(commentId) {
    return await fetchAPI(`/projects/comments/${commentId}`, { method: 'DELETE' });
}
