# HRMS Lite - Human Resource Management System

A lightweight, modern Human Resource Management System built with FastAPI (Python) and React (TypeScript).

## 🌟 Features

### Employee Management
- Add new employees with unique Employee ID
- View all employees in a clean table interface
- Delete employee records
- Automatic validation for duplicate IDs and emails

### Attendance Management
- Mark daily attendance (Present/Absent)
- View all attendance records
- Filter attendance by date
- Prevent duplicate attendance entries for same employee on same date

### Dashboard
- Real-time statistics overview
- Total employees count
- Today's attendance summary (Present/Absent)
- Total attendance records
- Quick action cards

### Bonus Features Implemented ✨
- **Filter attendance by date**: View attendance records for specific dates
- **Display total present days per employee**: Available via API endpoint
- **Dashboard summary**: Comprehensive overview with key metrics

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL (Production) / SQLite (Local Development)
- **ORM**: SQLAlchemy 2.0.25
- **Validation**: Pydantic 2.5.3
- **Server**: Uvicorn

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS 3.4
- **HTTP Client**: Axios
- **Routing**: React Router DOM 6

## 📦 Project Structure

```
hrms-lite/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── crud.py              # Database CRUD operations
│   ├── database.py          # Database configuration
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
└── frontend/
    ├── src/
    │   ├── components/      # Reusable React components
    │   ├── pages/           # Page components
    │   ├── services/        # API service layer
    │   ├── types/           # TypeScript type definitions
    │   ├── App.tsx          # Main app component
    │   └── main.tsx         # Application entry point
    ├── package.json         # Node.js dependencies
    └── vite.config.ts       # Vite configuration
```

## 🚀 Local Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file (optional for local development):
```bash
cp .env.example .env
```

5. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
cp .env.example .env
```

For local development, `.env` should contain:
```
VITE_API_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 🌐 Deployment

### Backend Deployment (Render)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the service:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**: Add `DATABASE_URL` (PostgreSQL connection string)

### Frontend Deployment (Vercel)

1. Create a new project on Vercel
2. Connect your GitHub repository
3. Configure build settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Add environment variable:
   - `VITE_API_URL`: Your deployed backend URL

## 📝 API Endpoints

### Employees
- `GET /api/employees` - Get all employees
- `GET /api/employees/{id}` - Get employee by ID with attendance records
- `POST /api/employees` - Create new employee
- `DELETE /api/employees/{id}` - Delete employee

### Attendance
- `GET /api/attendance` - Get all attendance records
- `GET /api/attendance/employee/{id}` - Get attendance for specific employee
- `GET /api/attendance/date/{date}` - Get attendance for specific date
- `POST /api/attendance` - Mark attendance
- `DELETE /api/attendance/{id}` - Delete attendance record

### Statistics
- `GET /api/statistics/dashboard` - Get dashboard summary
- `GET /api/statistics/employee/{id}` - Get attendance summary for employee

## 🔒 Data Validation

### Employee Validation
- Employee ID must be unique
- Email must be valid and unique
- All fields are required and cannot be empty
- Email is stored in lowercase

### Attendance Validation
- Employee must exist
- Date cannot have duplicate attendance for same employee
- Status must be either "Present" or "Absent"

## ⚠️ Error Handling

The application includes comprehensive error handling:
- **400 Bad Request**: Validation errors, duplicate entries
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server errors

All errors return meaningful messages to help users understand what went wrong.

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Loading States**: Spinners shown during data fetching
- **Empty States**: Helpful messages when no data exists
- **Error States**: Clear error messages with retry options
- **Confirmation Dialogs**: Prevent accidental deletions
- **Form Validation**: Client-side validation before submission
- **Professional Styling**: Clean, modern interface with consistent spacing

## 🧪 Testing the Application

### Sample Data
1. Add employees with different departments
2. Mark attendance for various dates
3. Use date filter to view specific day's attendance
4. View dashboard for statistics

### Test Cases
- Try adding duplicate Employee ID (should fail)
- Try adding duplicate email (should fail)
- Try marking attendance twice for same employee on same day (should fail)
- Delete an employee and verify attendance records are also deleted
- Filter attendance by date and verify results

## 📋 Assumptions & Limitations

### Assumptions
- Single admin user (no authentication required)
- All times are in server timezone
- Employee ID is alphanumeric string defined by organization

### Limitations
- No user authentication/authorization
- No employee update functionality (can delete and re-add)
- No attendance editing (can delete and re-mark)
- No leave management
- No payroll integration
- No file uploads (profile pictures, documents)
- No email notifications
- No audit logs

## 🔮 Future Enhancements

- User authentication and role-based access
- Employee profile editing
- Attendance editing capabilities
- Leave management system
- Bulk attendance marking
- Export reports (PDF, Excel)
- Email notifications
- Mobile app
- Advanced analytics and reporting
- Employee self-service portal

## 👨‍💻 Development Notes

- Backend uses SQLAlchemy ORM for database abstraction
- Frontend uses Axios interceptors for API calls
- Environment variables used for configuration
- CORS enabled for cross-origin requests
- Database migrations handled automatically on startup
- TypeScript for type safety in frontend
- Tailwind CSS for utility-first styling

## 📄 License

This project is created as an assignment and is free to use for educational purposes.

## 🤝 Support

For issues or questions, please check:
1. API documentation at `/docs` endpoint
2. Console logs for error details
3. Network tab in browser developer tools

---

**Built with ❤️ using FastAPI and React**
