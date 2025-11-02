import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (lscNumber: string, password: string) =>
    api.post('/auth/login/', { lscNumber, password }),

  refreshToken: (refresh: string) =>
    api.post('/auth/token/refresh/', { refresh }),

  logout: () => api.post('/auth/logout/'),

  changePassword: (oldPassword: string, newPassword: string) =>
    api.post('/auth/change-password/', { oldPassword, newPassword }),
};

export const studentAPI = {
  getStudents: () => api.get('/students/'),
  getStudent: (id: number) => api.get(`/students/${id}/`),
  createStudent: (data: any) => api.post('/students/', data),
  updateStudent: (id: number, data: any) => api.put(`/students/${id}/`, data),
  deleteStudent: (id: number) => api.delete(`/students/${id}/`),
};

export const attendanceAPI = {
  getAttendance: () => api.get('/attendance/'),
  createAttendance: (data: any) => api.post('/attendance/', data),
  updateAttendance: (id: number, data: any) => api.put(`/attendance/${id}/`, data),
};

export const assignmentMarksAPI = {
  getMarks: () => api.get('/assignment-marks/'),
  createMark: (data: any) => api.post('/assignment-marks/', data),
  updateMark: (id: number, data: any) => api.put(`/assignment-marks/${id}/`, data),
};

export const counsellorAPI = {
  getCounsellors: () => api.get('/counsellors/'),
  createCounsellor: (data: any) => api.post('/counsellors/', data),
  updateCounsellor: (id: number, data: any) => api.put(`/counsellors/${id}/`, data),
};

export const reportsAPI = {
  getSummary: () => api.get('/reports/summary/'),
  getApplicationReport: () => api.get('/reports/application_report/'),
  getUnpaidReport: () => api.get('/reports/unpaid_report/'),
  getConfirmedReport: () => api.get('/reports/confirmed_report/'),
};

export default api;