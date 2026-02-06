# Deployment Readiness Checklist

Use this checklist to ensure your HRMS Lite application is ready for production deployment.

## Pre-Deployment Checklist

### Backend (FastAPI)

- [x] **Environment Variables Configured**
  - [x] `.env.example` file exists with all required variables
  - [x] `DATABASE_URL` configured for production (PostgreSQL)
  - [x] `ALLOWED_ORIGINS` configured for CORS (production URLs)

- [x] **Dependencies**
  - [x] `requirements.txt` includes all dependencies with versions
  - [x] `runtime.txt` specifies Python version (3.11.0)

- [x] **Configuration Files**
  - [x] `render.yaml` configured for Render deployment
  - [x] CORS middleware supports environment-based origins
  - [x] Health check endpoint includes database connectivity test

- [x] **Security**
  - [x] `.gitignore` excludes `.env` files
  - [x] CORS configured to restrict origins in production
  - [x] Database credentials stored as environment variables

- [ ] **Testing**
  - [ ] All API endpoints tested locally
  - [ ] Database migrations tested
  - [ ] Health check endpoint verified

### Frontend (React/Vite)

- [x] **Environment Variables**
  - [x] `.env.example` file exists
  - [x] `VITE_API_URL` configured for production

- [x] **Build Configuration**
  - [x] `package.json` includes build script
  - [x] `vercel.json` configured for Vercel deployment
  - [x] Vite config optimized for production

- [x] **Security**
  - [x] `.gitignore` excludes `.env` files
  - [x] API URL uses environment variables

- [ ] **Testing**
  - [ ] Build completes without errors (`npm run build`)
  - [ ] All pages load correctly
  - [ ] API calls work with production backend URL

### Repository

- [x] **Git Configuration**
  - [x] Root `.gitignore` file exists
  - [x] Sensitive files excluded (`.env`, `*.db`, `node_modules`, `venv`)
  - [x] Code pushed to GitHub repository

- [ ] **Documentation**
  - [x] `README.md` updated with deployment instructions
  - [x] `DEPLOYMENT.md` includes step-by-step guide
  - [ ] API documentation accessible at `/docs`

## Deployment Steps

### 1. Backend Deployment (Render)

1. **Create PostgreSQL Database**
   - Go to Render Dashboard → New → PostgreSQL
   - Name: `hrms-lite-db`
   - Save the Internal Database URL

2. **Deploy Web Service**
   - Go to Render Dashboard → New → Web Service
   - Connect GitHub repository
   - Configure:
     - Root Directory: `backend`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variables:
     - `DATABASE_URL`: [Your PostgreSQL Internal Database URL]
     - `ALLOWED_ORIGINS`: [Your frontend URL after deployment]
   - Deploy

3. **Verify Backend**
   - Visit `https://your-backend.onrender.com/docs`
   - Test `/health` endpoint
   - Verify database connection

### 2. Frontend Deployment (Vercel)

1. **Deploy to Vercel**
   - Go to Vercel Dashboard → Add New Project
   - Import GitHub repository
   - Configure:
     - Framework Preset: Vite
     - Root Directory: `frontend`
     - Build Command: `npm run build` (auto-detected)
     - Output Directory: `dist` (auto-detected)
   - Add Environment Variable:
     - `VITE_API_URL`: [Your Render backend URL]
   - Deploy

2. **Update Backend CORS**
   - After frontend deployment, update backend environment variable:
     - `ALLOWED_ORIGINS`: [Your Vercel frontend URL]
   - Redeploy backend (Render auto-deploys on env var change)

3. **Verify Frontend**
   - Visit your Vercel URL
   - Test all features
   - Check browser console for errors

## Post-Deployment Verification

- [ ] Backend accessible at `/docs` endpoint
- [ ] Frontend loads without errors
- [ ] Dashboard displays correctly
- [ ] Can add new employees
- [ ] Can mark attendance
- [ ] All API calls work (check browser console)
- [ ] CORS properly configured (no CORS errors)
- [ ] Database connected and working
- [ ] Health check returns healthy status

## Troubleshooting

### Common Issues

**Backend won't start**
- Check `requirements.txt` for all dependencies
- Verify Python version matches `runtime.txt`
- Check Render logs for errors

**Database connection failed**
- Verify `DATABASE_URL` format (should be `postgresql://`)
- Check database is running in Render dashboard
- Ensure URL uses internal database URL (not external)

**CORS errors**
- Update `ALLOWED_ORIGINS` in backend environment variables
- Include exact frontend URL (with https://)
- Redeploy backend after changes

**Frontend build fails**
- Check Node.js version compatibility
- Verify all dependencies installed
- Check Vercel build logs

**API calls failing**
- Verify `VITE_API_URL` is set correctly
- Check backend is running
- Verify CORS configuration

## Environment Variables Reference

### Backend (.env)
```bash
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### Frontend (.env)
```bash
VITE_API_URL=https://your-backend.onrender.com
```

## Next Steps After Deployment

1. Monitor application logs
2. Set up error tracking (optional)
3. Configure custom domain (optional)
4. Set up SSL certificates (usually automatic)
5. Regular backups of database
6. Monitor performance and usage

---

**Ready to deploy?** Follow the steps in `DEPLOYMENT.md` for detailed instructions.
