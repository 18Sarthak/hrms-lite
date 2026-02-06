export interface Employee {
  id: number;
  employee_id: string;
  full_name: string;
  email: string;
  department: string;
}

export interface EmployeeCreate {
  employee_id: string;
  full_name: string;
  email: string;
  department: string;
}

export enum AttendanceStatus {
  PRESENT = "Present",
  ABSENT = "Absent"
}

export interface Attendance {
  id: number;
  employee_id: number;
  date: string;
  status: AttendanceStatus;
}

export interface AttendanceCreate {
  employee_id: number;
  date: string;
  status: AttendanceStatus;
}

export interface AttendanceSummary {
  employee_id: number;
  employee_name: string;
  total_present: number;
  total_absent: number;
  total_days: number;
}

export interface DashboardSummary {
  total_employees: number;
  total_attendance_records: number;
  today_present: number;
  today_absent: number;
}

export interface EmployeeWithAttendance extends Employee {
  attendance_records: Attendance[];
}
