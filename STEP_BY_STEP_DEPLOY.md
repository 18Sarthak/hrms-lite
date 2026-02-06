# Step-by-Step Deployment Guide

Follow these steps **one by one** to deploy your HRMS Lite application.

---

## 📋 Prerequisites Checklist

Before starting, make sure:
- [ ] Your code is working locally (backend runs on port 8000, frontend on port 3000)
- [ ] You have a GitHub account
- [ ] Your code is pushed to a GitHub repository (if not, see Step 0 below)

---

## Step 0: Push Code to GitHub (If Not Already Done)

### 0.1 Create GitHub Repository
1. Go to [github.com](https://github.com)
2. Click the **"+"** icon → **"New repository"**
3. Name it: `hrms-lite` (or any name you like)
4. Choose **Public** or **Private**
5. **DO NOT** check "Initialize with README"
6. Click **"Create repository"**

### 0.2 Push Your Code
Open terminal/command prompt in your project folder and run:

```bash
# Navigate to your project folder
cd c:\Users\sarth\Downloads\hrms-lite

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - HRMS Lite"

# Add your GitHub repository (replace YOUR_USERNAME and YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Replace:**
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO_NAME` with your repository name

---

## Step 1: Deploy Backend to Render

### 1.1 Sign Up / Sign In to Render
1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Sign up (use GitHub account for easier setup) or sign in

### 1.2 Create PostgreSQL Database
1. Click the **"New +"** button (top right)
2. Select **"PostgreSQL"**
3. Fill in:
   - **Name:** `hrms-lite-db`
   - **Database:** `hrms_lite` (auto-filled)
   - **User:** `hrms_user` (auto-filled)
   - **Region:** Choose closest to you (e.g., "Oregon (US West)")
   - **PostgreSQL Version:** Latest (default)
   - **Plan:** Free
4. Click **"Create Database"**
5. **Wait 2-3 minutes** for database to be created
6. Once created, click on the database name
7. In the **"Connections"** section, find **"Internal Database URL"**
8. **Copy this URL** - it looks like: `postgresql://hrms_user:password@dpg-xxxxx/hrms_lite`
   - ⚠️ **IMPORTANT:** Copy the **Internal** URL, not External!

### 1.3 Create Web Service (Backend API)
1. Click **"New +"** button again
2. Select **"Web Service"**
3. Click **"Connect account"** → Connect your GitHub account
4. Select your repository (`hrms-lite` or whatever you named it)
5. Click **"Connect"**

6. **Configure the service:**
   - **Name:** `hrms-lite-backend`
   - **Region:** Same as database (e.g., "Oregon (US West)")
   - **Branch:** `main` (or `master` if that's your branch)
   - **Root Directory:** `backend` ⚠️ **IMPORTANT - Type exactly: backend**
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

7. **Add Environment Variable:**
   - Click **"Advanced"** → **"Add Environment Variable"**
   - **Key:** `DATABASE_URL`
   - **Value:** Paste the Internal Database URL you copied in step 1.2
   - Click **"Add"**

8. Click **"Create Web Service"**
9. **Wait 5-10 minutes** for deployment to complete
   - You'll see build logs scrolling
   - When it says "Your service is live", it's done!

10. **Copy your backend URL:**
    - It will be something like: `https://hrms-lite-backend.onrender.com`
    - Copy this URL - you'll need it for frontend!

11. **Test your backend:**
    - Visit: `https://your-backend-url.onrender.com/docs`
    - You should see FastAPI documentation page
    - If you see the docs, backend is working! ✅

---

## Step 2: Deploy Frontend to Vercel

### 2.1 Sign Up / Sign In to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click **"Sign Up"** or **"Log In"**
3. Choose **"Continue with GitHub"** (easiest option)

### 2.2 Import Your Project
1. After logging in, you'll see the dashboard
2. Click **"Add New..."** → **"Project"**
3. You'll see your GitHub repositories
4. Find and click **"Import"** next to your `hrms-lite` repository

### 2.3 Configure Frontend Build
1. **Framework Preset:** Should auto-detect as "Vite" - leave it
2. **Root Directory:** Click **"Edit"** and change to: `frontend` ⚠️ **IMPORTANT!**
3. **Build Command:** Should be `npm run build` (auto-detected) - leave it
4. **Output Directory:** Should be `dist` (auto-detected) - leave it
5. **Install Command:** Leave as `npm install` (default)

### 2.4 Add Environment Variable
1. Scroll down to **"Environment Variables"** section
2. Click **"Add"** or **"Add New"**
3. **Key:** `VITE_API_URL`
4. **Value:** Your backend URL from Step 1.3 (e.g., `https://hrms-lite-backend.onrender.com`)
   - ⚠️ **IMPORTANT:** Make sure it starts with `https://` and has no trailing slash!
5. Click **"Add"**

### 2.5 Deploy
1. Scroll to bottom
2. Click **"Deploy"** button
3. **Wait 2-3 minutes** for build to complete
4. When done, you'll see **"Congratulations!"** message
5. **Copy your frontend URL:**
   - It will be something like: `https://hrms-lite.vercel.app`
   - Copy this URL - you'll need it for CORS!

---

## Step 3: Fix CORS (Connect Frontend to Backend)

### 3.1 Update Backend CORS Settings
1. Go back to [Render Dashboard](https://dashboard.render.com)
2. Click on your backend service (`hrms-lite-backend`)
3. Go to **"Environment"** tab (left sidebar)
4. Click **"Add Environment Variable"**
5. **Key:** `ALLOWED_ORIGINS`
6. **Value:** Your Vercel frontend URL from Step 2.5 (e.g., `https://hrms-lite.vercel.app`)
   - ⚠️ **IMPORTANT:** Exact URL, no trailing slash, must start with `https://`
7. Click **"Save Changes"**
8. Render will **automatically redeploy** your backend (takes 2-3 minutes)

---

## Step 4: Test Your Deployed Application

### 4.1 Wait for Redeploy
- Wait for Render to finish redeploying (check the "Events" tab)
- Status should show "Live" when done

### 4.2 Test Frontend
1. Open your Vercel frontend URL in browser
2. You should see your HRMS Lite application
3. Try these:
   - ✅ Dashboard loads
   - ✅ Add an employee
   - ✅ Mark attendance
   - ✅ View employees list

### 4.3 Check for Errors
1. Open browser **Developer Tools** (F12)
2. Go to **"Console"** tab
3. Look for any red errors
4. If you see CORS errors, double-check Step 3.1

---

## ✅ Deployment Complete!

Your application is now live:
- **Backend:** `https://your-backend.onrender.com`
- **Frontend:** `https://your-frontend.vercel.app`

---

## 🐛 Troubleshooting

### Backend won't start?
- Check Render logs: Click on your service → "Logs" tab
- Common issues:
  - Wrong root directory (should be `backend`)
  - Missing `DATABASE_URL` environment variable
  - Database URL is wrong format

### Frontend can't connect to backend?
- Check browser console (F12) for errors
- Verify `VITE_API_URL` is set correctly in Vercel
- Make sure backend URL starts with `https://`

### CORS errors?
- Verify `ALLOWED_ORIGINS` is set in Render backend
- Make sure it matches your Vercel URL exactly
- Wait for backend to redeploy after adding the variable

### Database connection errors?
- Make sure you used **Internal Database URL** (not External)
- Check `DATABASE_URL` is set in Render backend environment variables
- Verify database is running (should show "Available" in Render)

---

## 📝 Quick Reference

**Backend Environment Variables (Render):**
```
DATABASE_URL=postgresql://... (Internal Database URL)
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

**Frontend Environment Variables (Vercel):**
```
VITE_API_URL=https://your-backend.onrender.com
```

---

**Need help?** Check the logs in Render (backend) or Vercel (frontend) for specific error messages.
