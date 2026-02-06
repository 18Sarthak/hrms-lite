from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import List, Optional
from enum import Enum


class AttendanceStatusEnum(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"


# Employee Schemas
class EmployeeBase(BaseModel):
    employee_id: str = Field(..., min_length=1, description="Unique employee identifier")
    full_name: str = Field(..., min_length=1, description="Employee full name")
    email: EmailStr = Field(..., description="Employee email address")
    department: str = Field(..., min_length=1, description="Employee department")

    @field_validator('employee_id', 'full_name', 'department')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or whitespace')
        return v.strip()

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        return v.lower().strip()


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True


# Attendance Schemas
class AttendanceBase(BaseModel):
    date: date
    status: AttendanceStatusEnum


class AttendanceCreate(AttendanceBase):
    employee_id: int = Field(..., description="Employee ID")


class Attendance(AttendanceBase):
    id: int
    employee_id: int

    class Config:
        from_attributes = True


class AttendanceWithEmployee(Attendance):
    employee: 'Employee'


# Response Schemas
class EmployeeWithAttendance(Employee):
    attendance_records: List['Attendance'] = []


class AttendanceSummary(BaseModel):
    employee_id: int
    employee_name: str
    total_present: int
    total_absent: int
    total_days: int


class DashboardSummary(BaseModel):
    total_employees: int
    total_attendance_records: int
    today_present: int
    today_absent: int
