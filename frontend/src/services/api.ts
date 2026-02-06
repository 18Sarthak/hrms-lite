import axios from 'axios';
import type { 
  Employee, 
  EmployeeCreate, 
  Attendance, 
  AttendanceCreate,
  DashboardSummary,
  AttendanceSummary,
  EmployeeWithAttendance
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Employee API
export const employeeAPI = {
  getAll: async (): Promise<Employee[]> => {
    const response = await api.get('/api/employees');
    return response.data;
  },

  getById: async (id: number): Promise<EmployeeWithAttendance> => {
    const response = await api.get(`/api/employees/${id}`);
    return response.data;
  },

  create: async (employee: EmployeeCreate): Promise<Employee> => {
    const response = await api.post('/api/employees', employee);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/employees/${id}`);
  },
};

// Attendance API
export const attendanceAPI = {
  getAll: async (): Promise<Attendance[]> => {
    const response = await api.get('/api/attendance');
    return response.data;
  },

  getByEmployee: async (employeeId: number): Promise<Attendance[]> => {
    const response = await api.get(`/api/attendance/employee/${employeeId}`);
    return response.data;
  },

  getByDate: async (date: string): Promise<Attendance[]> => {
    const response = await api.get(`/api/attendance/date/${date}`);
    return response.data;
  },

  create: async (attendance: AttendanceCreate): Promise<Attendance> => {
    const response = await api.post('/api/attendance', attendance);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/attendance/${id}`);
  },
};

// Statistics API
export const statisticsAPI = {
  getDashboard: async (): Promise<DashboardSummary> => {
    const response = await api.get('/api/statistics/dashboard');
    return response.data;
  },

  getEmployeeSummary: async (employeeId: number): Promise<AttendanceSummary> => {
    const response = await api.get(`/api/statistics/employee/${employeeId}`);
    return response.data;
  },
};

export default api;
