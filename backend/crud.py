from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import date
from typing import List, Optional
import models
import schemas


# Employee CRUD
def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def get_employee_by_employee_id(db: Session, employee_id: str):
    return db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()


def get_employee_by_email(db: Session, email: str):
    return db.query(models.Employee).filter(models.Employee.email == email.lower()).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(
        employee_id=employee.employee_id,
        full_name=employee.full_name,
        email=employee.email.lower(),
        department=employee.department
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee(db, employee_id)
    if db_employee:
        db.delete(db_employee)
        db.commit()
        return True
    return False


# Attendance CRUD
def get_attendance(db: Session, attendance_id: int):
    return db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()


def get_attendance_by_employee(db: Session, employee_id: int):
    return db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id
    ).order_by(models.Attendance.date.desc()).all()


def get_attendance_by_date(db: Session, target_date: date):
    return db.query(models.Attendance).filter(
        models.Attendance.date == target_date
    ).all()


def get_attendance_by_employee_and_date(db: Session, employee_id: int, target_date: date):
    return db.query(models.Attendance).filter(
        and_(
            models.Attendance.employee_id == employee_id,
            models.Attendance.date == target_date
        )
    ).first()


def get_all_attendance(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Attendance).order_by(
        models.Attendance.date.desc()
    ).offset(skip).limit(limit).all()


def create_attendance(db: Session, attendance: schemas.AttendanceCreate):
    db_attendance = models.Attendance(
        employee_id=attendance.employee_id,
        date=attendance.date,
        status=attendance.status
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance


def update_attendance(db: Session, attendance_id: int, status: schemas.AttendanceStatusEnum):
    db_attendance = get_attendance(db, attendance_id)
    if db_attendance:
        db_attendance.status = status
        db.commit()
        db.refresh(db_attendance)
        return db_attendance
    return None


def delete_attendance(db: Session, attendance_id: int):
    db_attendance = get_attendance(db, attendance_id)
    if db_attendance:
        db.delete(db_attendance)
        db.commit()
        return True
    return False


# Statistics
def get_attendance_summary(db: Session, employee_id: int):
    employee = get_employee(db, employee_id)
    if not employee:
        return None
    
    total_present = db.query(models.Attendance).filter(
        and_(
            models.Attendance.employee_id == employee_id,
            models.Attendance.status == models.AttendanceStatus.PRESENT
        )
    ).count()
    
    total_absent = db.query(models.Attendance).filter(
        and_(
            models.Attendance.employee_id == employee_id,
            models.Attendance.status == models.AttendanceStatus.ABSENT
        )
    ).count()
    
    return {
        "employee_id": employee_id,
        "employee_name": employee.full_name,
        "total_present": total_present,
        "total_absent": total_absent,
        "total_days": total_present + total_absent
    }


def get_dashboard_summary(db: Session):
    total_employees = db.query(models.Employee).count()
    total_attendance = db.query(models.Attendance).count()
    
    today = date.today()
    today_present = db.query(models.Attendance).filter(
        and_(
            models.Attendance.date == today,
            models.Attendance.status == models.AttendanceStatus.PRESENT
        )
    ).count()
    
    today_absent = db.query(models.Attendance).filter(
        and_(
            models.Attendance.date == today,
            models.Attendance.status == models.AttendanceStatus.ABSENT
        )
    ).count()
    
    return {
        "total_employees": total_employees,
        "total_attendance_records": total_attendance,
        "today_present": today_present,
        "today_absent": today_absent
    }
