import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // FastAPI server
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
