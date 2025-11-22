import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 0, // No timeout - allow requests to run as long as needed
});

// Request interceptor for logging
api.interceptors.request.use(
  config => {
    console.log(`📤 ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  error => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  response => {
    console.log(`✅ ${response.config.method.toUpperCase()} ${response.config.url}`);
    return response;
  },
  error => {
    console.error('Response error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Jobs API
export const jobsApi = {
  create: jobData => api.post('/api/jobs', jobData),
  list: () => api.get('/api/jobs'),
  get: jobId => api.get(`/api/jobs/${jobId}`),
  delete: jobId => api.delete(`/api/jobs/${jobId}`),
};

// Candidates API
export const candidatesApi = {
  upload: (file, candidateName) => {
    const formData = new FormData();
    formData.append('file', file);
    if (candidateName) {
      formData.append('candidate_name', candidateName);
    }
    return api.post('/api/candidates/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  list: () => api.get('/api/candidates'),
  get: candidateId => api.get(`/api/candidates/${candidateId}`),
  delete: candidateId => api.delete(`/api/candidates/${candidateId}`),
};

// Matching API
export const matchingApi = {
  matchCandidates: (jobId, topK = 10, minScore = 0.0) =>
    api.post('/api/match', { job_id: jobId, top_k: topK, min_score: minScore }),
  getScore: (jobId, candidateId) => api.get(`/api/match/${jobId}/${candidateId}`),
  getJobScores: jobId => api.get(`/api/match/${jobId}/scores`),
};

// Health API
export const healthApi = {
  check: () => api.get('/api/health'),
};

export default api;
