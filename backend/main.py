from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import date
import os

import models
import schemas
import crud
from database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HRMS Lite API",
    description="A lightweight Human Resource Management System",
    version="1.0.0"
)

# CORS configuration - supports environment variable for production
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
# Parse comma-separated origins if provided, otherwise use wildcard
if ALLOWED_ORIGINS != "*":
    origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]
else:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "message": "HRMS Lite API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint for deployment monitoring"""
    try:
        # Test database connection
        from sqlalchemy import text
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()
        return {
            "status": "healthy",
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


# Employee Endpoints
@app.post("/api/employees", response_model=schemas.Employee, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    # Check if employee_id already exists
    db_employee = crud.get_employee_by_employee_id(db, employee_id=employee.employee_id)
    if db_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee ID '{employee.employee_id}' already exists"
        )
    
    # Check if email already exists
    db_employee = crud.get_employee_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{employee.email}' is already registered"
        )
    
    return crud.create_employee(db=db, employee=employee)


@app.get("/api/employees", response_model=List[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees


@app.get("/api/employees/{employee_id}", response_model=schemas.EmployeeWithAttendance)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )
    return db_employee


@app.delete("/api/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    success = crud.delete_employee(db, employee_id=employee_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )
    return None


# Attendance Endpoints
@app.post("/api/attendance", response_model=schemas.Attendance, status_code=status.HTTP_201_CREATED)
def create_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    # Check if employee exists
    db_employee = crud.get_employee(db, employee_id=attendance.employee_id)
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {attendance.employee_id} not found"
        )
    
    # Check if attendance already exists for this employee on this date
    existing = crud.get_attendance_by_employee_and_date(
        db, 
        employee_id=attendance.employee_id, 
        target_date=attendance.date
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Attendance already marked for employee {attendance.employee_id} on {attendance.date}"
        )
    
    return crud.create_attendance(db=db, attendance=attendance)


@app.get("/api/attendance", response_model=List[schemas.Attendance])
def read_all_attendance(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    attendance = crud.get_all_attendance(db, skip=skip, limit=limit)
    return attendance


@app.get("/api/attendance/employee/{employee_id}", response_model=List[schemas.Attendance])
def read_employee_attendance(employee_id: int, db: Session = Depends(get_db)):
    # Check if employee exists
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )
    
    attendance = crud.get_attendance_by_employee(db, employee_id=employee_id)
    return attendance


@app.get("/api/attendance/date/{target_date}", response_model=List[schemas.Attendance])
def read_attendance_by_date(target_date: date, db: Session = Depends(get_db)):
    attendance = crud.get_attendance_by_date(db, target_date=target_date)
    return attendance


@app.put("/api/attendance/{attendance_id}", response_model=schemas.Attendance)
def update_attendance(
    attendance_id: int, 
    status: schemas.AttendanceStatusEnum, 
    db: Session = Depends(get_db)
):
    db_attendance = crud.update_attendance(db, attendance_id=attendance_id, status=status)
    if not db_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance record with ID {attendance_id} not found"
        )
    return db_attendance


@app.delete("/api/attendance/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    success = crud.delete_attendance(db, attendance_id=attendance_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance record with ID {attendance_id} not found"
        )
    return None


# Statistics Endpoints
@app.get("/api/statistics/employee/{employee_id}", response_model=schemas.AttendanceSummary)
def get_employee_statistics(employee_id: int, db: Session = Depends(get_db)):
    summary = crud.get_attendance_summary(db, employee_id=employee_id)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )
    return summary


@app.get("/api/statistics/dashboard", response_model=schemas.DashboardSummary)
def get_dashboard_statistics(db: Session = Depends(get_db)):
    return crud.get_dashboard_summary(db)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
