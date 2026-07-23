import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // FastAPI server
});

// Intercept requests to add the JWT token
api.interceptors.request.use((config) => {
  const token = import.meta.env.VITE_JWT_TOKEN;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const extractRules = async (file: File) => {
  const formData = new FormData();
  formData.append('document', file);
  
  const response = await api.post('/extract-rules', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};
