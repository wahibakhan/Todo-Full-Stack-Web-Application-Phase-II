# Deployment Guide - Todo Full Stack App Phase 2

## 🎯 Recommended Deployment Setup

### Frontend (Next.js) → Vercel
### Backend (FastAPI) → Render or Railway

---

## 🔐 CRITICAL: How to Handle Secrets Securely

### ❌ NEVER DO THIS:
```bash
# DON'T commit .env files
git add backend/.env  # ❌ WRONG
git add frontend/.env.local  # ❌ WRONG
```

### ✅ CORRECT WAY:

**Secrets stay on deployment platform only, NOT in GitHub!**

---

## 📦 Option 1: Deploy to Vercel (Frontend) + Render (Backend)

### Step 1: Deploy Backend to Render

1. **Create Render Account**
   - Go to: https://render.com/
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select: `Todo-Full-Stack-Web-Application---Phase-II`
   - Branch: `002-fullstack-web`

3. **Configure Backend Settings**
   ```
   Name: todo-backend
   Root Directory: backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free
   ```

4. **Add Environment Variables on Render** (CRITICAL 🔒)

   **In Render Dashboard → Environment:**

   ```
   BETTER_AUTH_SECRET=your-secret-key-min-32-chars-change-this
   DATABASE_URL=your-neon-postgres-url-from-dashboard
   ENVIRONMENT=production
   CORS_ORIGINS=["https://your-frontend-url.vercel.app"]
   ```

   **⚠️ IMPORTANT:**
   - These values are ONLY entered on Render dashboard
   - Never commit these to GitHub
   - Copy from your local `.env` file but paste ONLY on Render

5. **Deploy**
   - Click "Create Web Service"
   - Render will deploy automatically
   - Note your backend URL: `https://todo-backend-xyz.onrender.com`

---

### Step 2: Deploy Frontend to Vercel

1. **Create Vercel Account**
   - Go to: https://vercel.com/
   - Sign up with GitHub

2. **Import Project**
   - Click "Add New" → "Project"
   - Import: `Todo-Full-Stack-Web-Application---Phase-II`
   - Branch: `002-fullstack-web`

3. **Configure Frontend Settings**
   ```
   Framework Preset: Next.js
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```

4. **Add Environment Variables on Vercel** (CRITICAL 🔒)

   **In Vercel Dashboard → Settings → Environment Variables:**

   ```
   BETTER_AUTH_SECRET=your-secret-key-min-32-chars-change-this
   NEXT_PUBLIC_API_URL=https://todo-backend-xyz.onrender.com
   DATABASE_URL=your-neon-postgres-url-from-dashboard
   ```

   **⚠️ IMPORTANT:**
   - Use the SAME `BETTER_AUTH_SECRET` as backend (must match exactly!)
   - Use the backend URL from Render (Step 1)
   - These are entered ONLY on Vercel dashboard
   - Never commit to GitHub

5. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy
   - Your frontend URL: `https://your-app-name.vercel.app`

---

### Step 3: Update CORS in Backend

After frontend is deployed, update backend environment variables on Render:

```
CORS_ORIGINS=["https://your-app-name.vercel.app"]
```

---

## 📦 Option 2: Deploy to Vercel (Frontend) + Railway (Backend)

### Step 1: Deploy Backend to Railway

1. **Create Railway Account**
   - Go to: https://railway.app/
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose: `Todo-Full-Stack-Web-Application---Phase-II`

3. **Configure Backend**
   - Root Directory: `backend`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables on Railway** (CRITICAL 🔒)

   **In Railway Dashboard → Variables:**

   ```
   BETTER_AUTH_SECRET=your-secret-key-min-32-chars-change-this
   DATABASE_URL=your-neon-postgres-url
   ENVIRONMENT=production
   CORS_ORIGINS=["https://your-frontend.vercel.app"]
   PORT=8000
   ```

5. **Generate Domain**
   - Railway → Settings → Generate Domain
   - Note URL: `https://todo-backend.railway.app`

### Step 2: Deploy Frontend (Same as Option 1)

Follow Vercel steps above, but use Railway backend URL in `NEXT_PUBLIC_API_URL`

---

## 🔒 Security Checklist Before Deployment

### ✅ Verify These Files Are NOT in GitHub:

```bash
# Run this command to check:
cd C:\projects\todo_app
git ls-files | grep -E "\.env$|\.db$"

# Should return NOTHING (empty result means safe)
```

### ✅ Verify .gitignore Is Working:

```bash
git check-ignore backend/.env frontend/.env.local backend/todo_app.db

# Should show all three files (means they're ignored)
```

### ✅ Only These Template Files Should Be in GitHub:

- ✅ `backend/.env.example` (with EMPTY values)
- ✅ `frontend/.env.example` (with EMPTY values)

---

## 🗄️ Database Setup (Neon PostgreSQL)

### Get Your Database URL:

1. Go to: https://neon.tech/
2. Sign up / Login
3. Create New Project: "todo-app-phase2"
4. Copy **Pooler Connection String**:
   ```
   postgresql://user:password@ep-xxx-pooler.us-east-1.aws.neon.tech/dbname?sslmode=require
   ```

### Use This URL in:
- ✅ Render/Railway Backend Environment Variables: `DATABASE_URL`
- ✅ Vercel Frontend Environment Variables: `DATABASE_URL`
- ❌ NEVER commit to GitHub

---

## 🔑 Generate Secure BETTER_AUTH_SECRET

### Method 1: Python
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Method 2: Node.js
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### Method 3: Online (use once, don't save)
- https://generate-secret.vercel.app/32

**⚠️ IMPORTANT:**
- Generate ONE secret
- Use SAME secret in both frontend and backend
- Never commit to GitHub
- Enter only on Vercel and Render/Railway dashboards

---

## 📊 Environment Variables Summary

### Backend (Render/Railway):
```env
BETTER_AUTH_SECRET=<random-32-char-secret>
DATABASE_URL=<neon-postgres-pooler-url>
ENVIRONMENT=production
CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

### Frontend (Vercel):
```env
BETTER_AUTH_SECRET=<same-secret-as-backend>
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
DATABASE_URL=<same-neon-url-as-backend>
```

---

## ✅ Deployment Verification

After deployment, test:

1. **Visit Frontend URL**
   - Should show login page with animations

2. **Sign Up New User**
   - Create account
   - Should redirect to dashboard

3. **Create Task**
   - Add a todo item
   - Should save to database

4. **Logout and Login Again**
   - Tasks should persist
   - User-specific data should load

---

## 🚨 Common Issues & Fixes

### Issue 1: CORS Error
**Error:** "Access blocked by CORS policy"

**Fix:** Update backend `CORS_ORIGINS` with correct frontend URL:
```env
CORS_ORIGINS=["https://your-exact-frontend.vercel.app"]
```

### Issue 2: 401 Unauthorized
**Error:** "Authentication failed"

**Fix:** Ensure `BETTER_AUTH_SECRET` is EXACTLY the same in frontend and backend

### Issue 3: Database Connection Failed
**Error:** "Could not connect to database"

**Fix:**
- Use Neon **Pooler** URL (not direct URL)
- Check DATABASE_URL includes `?sslmode=require`

### Issue 4: "Failed to fetch"
**Error:** Frontend can't reach backend

**Fix:** Update `NEXT_PUBLIC_API_URL` in Vercel with correct backend URL

---

## 💰 Cost Breakdown

### Free Tier:
- ✅ Vercel Frontend: Free (100GB bandwidth)
- ✅ Render Backend: Free (750 hours/month, sleeps after 15 min inactivity)
- ✅ Neon Database: Free (0.5GB storage, 1 branch)

**Total Monthly Cost: $0** (with free tiers)

### Paid Options (for production):
- Vercel Pro: $20/month (better performance, no sleep)
- Render Starter: $7/month (no sleep, always on)
- Railway: ~$5/month (usage-based)
- Neon Pro: $19/month (3GB storage, autoscaling)

---

## 🎯 Recommended Workflow

1. **Deploy Backend First** (Render/Railway)
   - Get backend URL

2. **Deploy Frontend Second** (Vercel)
   - Use backend URL in environment variables

3. **Update Backend CORS**
   - Add frontend URL to allowed origins

4. **Test Everything**
   - Signup, login, create tasks, logout

---

## 📝 Important Notes

### 🔒 Security:
- ✅ Secrets are ONLY on deployment platforms
- ✅ GitHub only has code and `.env.example` templates
- ✅ `.gitignore` protects sensitive files
- ✅ Environment variables are encrypted by Vercel/Render

### 🔄 Auto-Deploy:
- Push to `002-fullstack-web` branch
- Vercel and Render auto-deploy new changes
- No manual steps needed after initial setup

### 🌐 Custom Domain (Optional):
- Vercel: Add custom domain in settings
- Render: Add custom domain in settings
- Free SSL certificates included

---

## ✅ Final Security Verification

Before going live, run this checklist:

```bash
# 1. Check no secrets in GitHub
git ls-files | grep -E "\.env$|\.db$"
# Should return: NOTHING

# 2. Check .gitignore is working
git check-ignore backend/.env frontend/.env.local
# Should return: backend/.env, frontend/.env.local

# 3. Check only templates are tracked
git ls-files | grep "\.env"
# Should return: backend/.env.example, frontend/.env.example ONLY

# 4. Verify no database files tracked
git ls-files | grep "\.db"
# Should return: NOTHING
```

**If all checks pass → ✅ SAFE TO DEPLOY**

---

## 🆘 Need Help?

### Deployment Issues:
- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app/

### Security Questions:
- Read: `SECURITY.md` in project root
- Read: `GITHUB_SECURITY_REPORT.md`

---

**Your secrets will NEVER be public if you follow this guide!** 🔒
