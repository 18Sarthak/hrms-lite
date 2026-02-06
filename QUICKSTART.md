# Quick Start Guide

Get HRMS Lite running locally in 5 minutes!

## Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Git installed

## Quick Setup

### 1. Clone or Download the Project
```bash
cd hrms-lite
```

### 2. Start Backend (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

✅ Backend running at http://localhost:8000

### 3. Start Frontend (Terminal 2)

```bash
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# Start development server
npm run dev
```

✅ Frontend running at http://localhost:3000

## 🎉 You're Ready!

Open your browser and go to: **http://localhost:3000**

## First Steps

1. **Add an Employee**
   - Click "Employees" in navigation
   - Click "+ Add Employee"
   - Fill in the form
   - Click "Add Employee"

2. **Mark Attendance**
   - Click "Attendance" in navigation
   - Click "+ Mark Attendance"
   - Select employee, date, and status
   - Click "Mark Attendance"

3. **View Dashboard**
   - Click "Dashboard" in navigation
   - See your statistics

## API Documentation

While backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Stopping the Application

- Press `Ctrl + C` in both terminal windows
- Deactivate virtual environment: `deactivate`

## Common Issues

### Port Already in Use
**Backend (8000)**:
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows
```

**Frontend (3000)**:
```bash
# Find and kill process
lsof -ti:3000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :3000   # Windows
```

### Module Not Found
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Database Locked (SQLite)
```bash
cd backend
rm hrms_lite.db  # Delete and restart
```

## Development Tips

### Backend Auto-Reload
The FastAPI server automatically reloads on code changes.

### Frontend Hot Module Replacement
Vite provides instant hot module replacement - save and see changes immediately.

### Testing API with curl

```bash
# Get all employees
curl http://localhost:8000/api/employees

# Create employee
curl -X POST http://localhost:8000/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP001",
    "full_name": "John Doe",
    "email": "john@example.com",
    "department": "Engineering"
  }'

# Mark attendance
curl -X POST http://localhost:8000/api/attendance \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "date": "2024-01-15",
    "status": "Present"
  }'
```

## Project Structure Overview

```
hrms-lite/
├── backend/
│   ├── main.py          # 🚀 Start here - FastAPI app
│   ├── models.py        # 📊 Database models
│   ├── schemas.py       # ✅ Data validation
│   ├── crud.py          # 💾 Database operations
│   └── database.py      # 🔌 DB connection
└── frontend/
    └── src/
        ├── pages/       # 📄 Dashboard, Employees, Attendance
        ├── components/  # 🧩 Reusable UI components
        └── services/    # 🌐 API calls
```

## Next Steps

1. Read the full [README.md](README.md) for detailed information
2. Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions
3. Explore the API documentation at http://localhost:8000/docs
4. Start building your features!

---

**Happy Coding! 🚀**

For questions, check the API docs or console logs for debugging.
