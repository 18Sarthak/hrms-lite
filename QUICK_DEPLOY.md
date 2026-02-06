# Quick Deployment Guide

## 🚀 Fast Track Deployment

### Prerequisites
- GitHub repository with code pushed
- Render.com account (free tier available)
- Vercel account (free tier available)

### Step 1: Deploy Backend (5 minutes)

1. **Go to [Render Dashboard](https://dashboard.render.com/)**

2. **Create PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - Name: `hrms-lite-db`
   - Plan: Free
   - Click "Create Database"
   - **Copy the Internal Database URL** (starts with `postgresql://`)

3. **Deploy Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - **Name**: `hrms-lite-backend`
     - **Root Directory**: `backend`
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     - `DATABASE_URL`: [Paste Internal Database URL]
   - Click "Create Web Service"
   - Wait for deployment (~2-3 minutes)
   - **Copy your backend URL** (e.g., `https://hrms-lite-backend.onrender.com`)

4. **Verify Backend**
   - Visit: `https://your-backend.onrender.com/docs`
   - Should see FastAPI documentation

### Step 2: Deploy Frontend (3 minutes)

1. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**

2. **Import Project**
   - Click "Add New..." → "Project"
   - Import your GitHub repository

3. **Configure**
   - **Framework Preset**: Vite (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)

4. **Environment Variables**
   - Click "Environment Variables"
   - Add:
     - **Key**: `VITE_API_URL`
     - **Value**: `https://your-backend.onrender.com` (from Step 1)
   - Click "Save"

5. **Deploy**
   - Click "Deploy"
   - Wait for build (~1-2 minutes)
   - **Copy your frontend URL** (e.g., `https://hrms-lite.vercel.app`)

### Step 3: Update CORS (2 minutes)

1. **Go back to Render Dashboard**
   - Open your backend service
   - Go to "Environment" tab
   - Add new environment variable:
     - **Key**: `ALLOWED_ORIGINS`
     - **Value**: `https://your-frontend.vercel.app` (from Step 2)
   - Click "Save Changes"
   - Render will auto-redeploy (~1 minute)

### Step 4: Test Everything

1. Visit your frontend URL
2. Test features:
   - ✅ Dashboard loads
   - ✅ Add employee
   - ✅ Mark attendance
   - ✅ View employees
3. Check browser console (F12) for errors

## ✅ Done!

Your application is now live:
- **Backend**: `https://your-backend.onrender.com`
- **Frontend**: `https://your-frontend.vercel.app`

## 🐛 Troubleshooting

**Backend won't start?**
- Check Render logs
- Verify `DATABASE_URL` is correct
- Ensure Python version is 3.11

**CORS errors?**
- Verify `ALLOWED_ORIGINS` includes exact frontend URL
- Check it starts with `https://`
- Redeploy backend after changes

**Frontend can't connect?**
- Verify `VITE_API_URL` is set correctly
- Check backend is running
- Test backend URL directly in browser

**Database errors?**
- Use Internal Database URL (not External)
- URL should start with `postgresql://`
- Check database is running in Render dashboard

## 📚 More Details

For detailed instructions, see:
- `DEPLOYMENT.md` - Full deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Pre-deployment checklist
