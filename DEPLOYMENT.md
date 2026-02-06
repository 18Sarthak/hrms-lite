# Deployment Guide for HRMS Lite

This guide will walk you through deploying the HRMS Lite application to production.

## Backend Deployment (Render.com)

### Step 1: Prepare Your Repository
1. Push your code to GitHub
2. Ensure `backend/` directory contains all necessary files

### Step 2: Create PostgreSQL Database
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: hrms-lite-db
   - **Database**: hrms_lite
   - **User**: hrms_user
   - **Region**: Choose closest to your users
   - **Plan**: Free
4. Click "Create Database"
5. **Save the Internal Database URL** (you'll need this)

### Step 3: Deploy Backend API
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: hrms-lite-backend
   - **Region**: Same as database
   - **Branch**: main
   - **Root Directory**: backend
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variable:
   - **Key**: `DATABASE_URL`
   - **Value**: [Your PostgreSQL Internal Database URL]
5. Click "Create Web Service"
6. Wait for deployment to complete
7. **Save your backend URL** (e.g., `https://hrms-lite-backend.onrender.com`)

### Testing Backend
Visit `https://your-backend-url.onrender.com/docs` to see the API documentation.

## Frontend Deployment (Vercel)

### Step 1: Prepare Frontend
1. Ensure your code is pushed to GitHub
2. Make sure `frontend/` directory is ready

### Step 2: Deploy to Vercel
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: frontend
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: dist (auto-detected)
5. Add Environment Variable:
   - **Key**: `VITE_API_URL`
   - **Value**: [Your Render backend URL] (e.g., `https://hrms-lite-backend.onrender.com`)
6. Click "Deploy"
7. Wait for deployment to complete
8. **Save your frontend URL** (e.g., `https://hrms-lite.vercel.app`)

### Step 3: Update CORS (Important!)
After deploying frontend, update your backend's CORS settings:

1. In `backend/main.py`, find the CORS configuration
2. Update `allow_origins` from `["*"]` to your specific frontend URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hrms-lite.vercel.app"],  # Your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. Commit and push the change
4. Render will automatically redeploy

## Alternative: Deploy Backend to Railway

### Step 1: Create Account
1. Go to [Railway.app](https://railway.app/)
2. Sign up with GitHub

### Step 2: Deploy
1. Click "New Project" → "Deploy from GitHub repo"
2. Select your repository
3. Click "Add variables"
4. Add PostgreSQL plugin (Railway will auto-configure DATABASE_URL)
5. Configure:
   - **Root Directory**: backend
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy

## Alternative: Deploy Frontend to Netlify

### Step 1: Deploy
1. Go to [Netlify](https://www.netlify.com/)
2. Click "Add new site" → "Import an existing project"
3. Connect to GitHub and select repository
4. Configure:
   - **Base directory**: frontend
   - **Build command**: `npm run build`
   - **Publish directory**: frontend/dist
5. Add Environment Variable:
   - **Key**: `VITE_API_URL`
   - **Value**: [Your backend URL]
6. Click "Deploy site"

## Post-Deployment Checklist

- [ ] Backend is accessible at `/docs` endpoint
- [ ] Frontend loads without errors
- [ ] Dashboard displays correctly
- [ ] Can add new employees
- [ ] Can mark attendance
- [ ] All API calls work (check browser console for errors)
- [ ] CORS is properly configured
- [ ] Database is connected and working

## Troubleshooting

### Backend Issues

**Database Connection Failed**
- Verify DATABASE_URL is correctly set
- Check if database is running
- Ensure URL format is `postgresql://` not `postgres://`

**Import Errors**
- Make sure all dependencies are in `requirements.txt`
- Check Python version compatibility

**CORS Errors**
- Update `allow_origins` in `main.py`
- Redeploy backend after changes

### Frontend Issues

**API Calls Failing**
- Check VITE_API_URL is set correctly
- Verify backend is running
- Check browser console for CORS errors

**Build Failures**
- Ensure all TypeScript types are correct
- Check for missing dependencies
- Verify Node.js version

**Environment Variables Not Working**
- Ensure variables start with `VITE_`
- Rebuild after adding variables
- Check deployment logs

## Free Tier Limitations

### Render (Backend)
- 750 hours/month (always on)
- 512 MB RAM
- May spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds

### Vercel (Frontend)
- 100 GB bandwidth/month
- Unlimited static sites
- Fast CDN

### Railway (Alternative)
- $5 free credit/month
- Auto-sleeps after 15 minutes

## Monitoring

1. **Backend Health**: Visit `/health` endpoint
2. **Backend Logs**: Check Render/Railway dashboard
3. **Frontend Logs**: Check Vercel dashboard
4. **Database**: Monitor in Render dashboard

## Updating Deployment

### Backend Updates
1. Push code to GitHub
2. Render auto-deploys from main branch
3. Check deployment logs

### Frontend Updates
1. Push code to GitHub
2. Vercel auto-deploys from main branch
3. Check deployment logs

## Security Notes

- Never commit `.env` files
- Use environment variables for secrets
- Keep DATABASE_URL private
- Update CORS to specific origins in production
- Regularly update dependencies

---

**Your application is now live! 🎉**

Backend: `https://your-backend.onrender.com`  
Frontend: `https://your-frontend.vercel.app`

Share these URLs in your assignment submission.
