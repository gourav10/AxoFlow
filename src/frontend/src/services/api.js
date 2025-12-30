// API Service for AxoFlow Backend
// Base URL for the FastAPI backend
const API_BASE_URL = 'http://localhost:8001';

/**
 * Generic API request handler with error handling
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;

    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        });

        // Parse JSON response
        const data = await response.json();

        // Handle HTTP errors
        if (!response.ok) {
            throw new Error(data.detail || `HTTP error! status: ${response.status}`);
        }

        return data;
    } catch (error) {
        // Network errors or parsing errors
        if (error.message.includes('fetch')) {
            throw new Error('Unable to connect to server. Please check if the backend is running.');
        }
        throw error;
    }
}

/**
 * Authentication API
 */
export const authAPI = {
    /**
     * Register a new user
     * @param {string} fullName - User's full name
     * @param {string} email - User's email
     * @param {string} password - User's password
     * @returns {Promise<Object>} User object
     */
    async register(fullName, email, password) {
        const data = await apiRequest('/api/auth/register', {
            method: 'POST',
            body: JSON.stringify({
                full_name: fullName,
                email: email,
                password: password,
            }),
        });

        return data;
    },

    /**
     * Login user
     * @param {string} email - User's email
     * @param {string} password - User's password
     * @returns {Promise<Object>} Login response with token and user
     */
    async login(email, password) {
        const data = await apiRequest('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({
                email: email,
                password: password,
            }),
        });

        // Store token in localStorage
        if (data.access_token) {
            localStorage.setItem('auth_token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
        }

        return data;
    },

    /**
     * Logout user
     */
    async logout() {
        await apiRequest('/api/auth/logout', {
            method: 'POST',
        });

        // Clear local storage
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
    },

    /**
     * Get current authenticated user
     * @returns {Promise<Object>} Current user object
     */
    async getCurrentUser() {
        return await apiRequest('/api/auth/me', {
            method: 'GET',
        });
    },

    /**
     * Check if user is authenticated
     * @returns {boolean}
     */
    isAuthenticated() {
        return !!localStorage.getItem('auth_token');
    },

    /**
     * Get stored user data
     * @returns {Object|null}
     */
    getUser() {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },
};

/**
 * Jobs API
 */
export const jobsAPI = {
    /**
     * Get list of jobs
     * @param {number} skip - Number of jobs to skip
     * @param {number} limit - Number of jobs to return
     * @returns {Promise<Array>} Array of job objects
     */
    async getJobs(skip = 0, limit = 10) {
        return await apiRequest(`/api/jobs?skip=${skip}&limit=${limit}`, {
            method: 'GET',
        });
    },

    /**
     * Get job by ID
     * @param {number} jobId - Job ID
     * @returns {Promise<Object>} Job object
     */
    async getJob(jobId) {
        return await apiRequest(`/api/jobs/${jobId}`, {
            method: 'GET',
        });
    },

    /**
     * Search jobs
     * @param {Object} searchParams - Search parameters
     * @returns {Promise<Array>} Array of matching jobs
     */
    async searchJobs(searchParams) {
        return await apiRequest('/api/jobs/search', {
            method: 'POST',
            body: JSON.stringify(searchParams),
        });
    },
};

/**
 * Applications API
 */
export const applicationsAPI = {
    /**
     * Get user's applications
     * @returns {Promise<Array>} Array of application objects
     */
    async getApplications() {
        return await apiRequest('/api/applications', {
            method: 'GET',
        });
    },

    /**
     * Submit a new application
     * @param {Object} applicationData - Application data
     * @returns {Promise<Object>} Created application
     */
    async submitApplication(applicationData) {
        return await apiRequest('/api/applications', {
            method: 'POST',
            body: JSON.stringify(applicationData),
        });
    },

    /**
     * Get application by ID
     * @param {number} appId - Application ID
     * @returns {Promise<Object>} Application object
     */
    async getApplication(appId) {
        return await apiRequest(`/api/applications/${appId}`, {
            method: 'GET',
        });
    },

    /**
     * Update application
     * @param {number} appId - Application ID
     * @param {Object} updateData - Update data
     * @returns {Promise<Object>} Updated application
     */
    async updateApplication(appId, updateData) {
        return await apiRequest(`/api/applications/${appId}`, {
            method: 'PUT',
            body: JSON.stringify(updateData),
        });
    },
};

/**
 * Users API
 */
export const usersAPI = {
    /**
     * Get user profile
     * @returns {Promise<Object>} User profile
     */
    async getProfile() {
        return await apiRequest('/api/users/profile', {
            method: 'GET',
        });
    },

    /**
     * Update user profile
     * @param {Object} profileData - Profile update data
     * @returns {Promise<Object>} Updated profile
     */
    async updateProfile(profileData) {
        return await apiRequest('/api/users/profile', {
            method: 'PUT',
            body: JSON.stringify(profileData),
        });
    },

    /**
     * Upload resume
     * @param {File} file - Resume file
     * @returns {Promise<Object>} Upload response
     */
    async uploadResume(file) {
        const formData = new FormData();
        formData.append('file', file);

        const url = `${API_BASE_URL}/api/users/resume`;
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Resume upload failed');
        }

        return await response.json();
    },
};

export default {
    auth: authAPI,
    jobs: jobsAPI,
    applications: applicationsAPI,
    users: usersAPI,
};
