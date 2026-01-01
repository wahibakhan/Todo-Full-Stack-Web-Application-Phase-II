# 🔒 Secure Vercel Deployment Guide - Full Stack Todo App

## ✅ SECURITY STATUS: Your Keys Are SAFE!

**Confirmed:** Your `.env` files are **NOT in Git** and **NOT deployed publicly**.

---

## 🚀 Deploy to Vercel - Single Project (Frontend + Backend)

### Step 1: Push to GitHub (Secrets Stay Safe!)

```bash
# 1. Check that secrets are NOT in git
git ls-files | grep "\.env$"
# Should only show: backend/.env.example, frontend/.env.example

# 2. Add all changes
git add .

# 3. Commit
git commit -m "Phase 2: Vercel deployment configuration

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# 4. Push to GitHub
git push origin 002-fullstack-web
```

**✅ GUARANTEED SAFE:**
- Only code files are pushed
- `.gitignore` protects all `.env` files
- `.gitignore` protects database files
- Secrets NEVER leave your local machine

---

### Step 2: Deploy to Vercel

#### 2.1 Create Vercel Account
1. Go to: https://vercel.com/
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel to access your GitHub

#### 2.2 Import Project
1. Click "Add New" → "Project"
2. Find your repository: `todo_app` (or your repo name)
3. Click "Import"

#### 2.3 Configure Project Settings
**Vercel will auto-detect the configuration from `vercel.json`**

Leave these settings as-is:
- ✅ Framework Preset: `Next.js`
- ✅ Root Directory: `./` (leave empty or root)
- ✅ Build Command: (auto-detected from vercel.json)
- ✅ Output Directory: (auto-detected from vercel.json)

**DO NOT DEPLOY YET!** Click "Configure Project" to add environment variables first.

---

### Step 3: Add Environment Variables (CRITICAL 🔒)

**IMPORTANT:** These values are entered ONLY in Vercel Dashboard. They will NEVER be in Git or publicly accessible.

#### 3.1 In Vercel Dashboard → Environment Variables

Click "Add Environment Variable" for each one:

---

#### Variable 1: `BETTER_AUTH_SECRET`
```
Name: BETTER_AUTH_SECRET
Value: [Generate a new secret - see below]
Environment: Production, Preview, Development (select all 3)
```

**Generate Secret (choose one method):**

**Option A: Python**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Option B: Node.js**
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

**Option C: Online (use once)**
```bash
# Visit: https://generate-secret.vercel.app/32
# Copy the generated secret
# Close the page (don't save it anywhere else)
```

**Copy the output and paste it in Vercel as the value for `BETTER_AUTH_SECRET`**

---

#### Variable 2: `DATABASE_URL`
```
Name: DATABASE_URL
Value: [Your Neon PostgreSQL URL - see below]
Environment: Production, Preview, Development (select all 3)
```

**Get Neon Database URL:**

1. Go to: https://neon.tech/
2. Sign up / Login with GitHub
3. Click "Create Project"
   - Name: `todo-app-phase2`
   - Region: Choose closest to you
   - Postgres Version: 16 (latest)
4. Click "Create Project"
5. **Copy the "Pooler Connection String"** (NOT the regular connection string)
   ```
   Example:
   postgresql://user:password@ep-xxx-pooler.us-east-1.aws.neon.tech/dbname?sslmode=require
   ```
6. Paste this in Vercel as the value for `DATABASE_URL`

**⚠️ IMPORTANT:** Use the **Pooler URL**, not the direct URL!

---

#### Variable 3: `NEXT_PUBLIC_API_URL`
```
Name: NEXT_PUBLIC_API_URL
Value: https://your-app-name.vercel.app
Environment: Production, Preview, Development (select all 3)
```

**Note:** You'll get this URL after deployment. For now, use a placeholder:
```
https://todo-app.vercel.app
```

You'll update this after deployment in Step 5.

---

#### Variable 4: `ENVIRONMENT`
```
Name: ENVIRONMENT
Value: production
Environment: Production only
```

---

#### Variable 5: `CORS_ORIGINS`
```
Name: CORS_ORIGINS
Value: ["https://your-app-name.vercel.app"]
Environment: Production, Preview, Development (select all 3)
```

**Note:** Use the same URL as `NEXT_PUBLIC_API_URL`. Update this after deployment.

---

### Step 4: Deploy!

1. After adding ALL environment variables, click "Deploy"
2. Wait 2-3 minutes for deployment to complete
3. You'll see: ✅ Deployment successful!
4. **Copy your deployment URL**: `https://your-app-name.vercel.app`

---

### Step 5: Update Environment Variables with Real URL

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Edit `NEXT_PUBLIC_API_URL`:
   - Change to: `https://your-actual-url.vercel.app`
3. Edit `CORS_ORIGINS`:
   - Change to: `["https://your-actual-url.vercel.app"]`
4. Click "Save"
5. Go to "Deployments" tab
6. Click "Redeploy" on the latest deployment
7. Select "Use existing Build Cache"
8. Click "Redeploy"

---

## ✅ Verify Your Deployment is Secure

### Security Checklist:

```bash
# 1. Check no secrets in GitHub
git ls-files | grep -E "\.env$|\.db$"
# Should return ONLY: backend/.env.example, frontend/.env.example

# 2. Try accessing .env file publicly (should fail)
# Open in browser: https://your-app.vercel.app/.env
# Should show: 404 Not Found ✅

# 3. Try accessing backend .env (should fail)
# Open in browser: https://your-app.vercel.app/backend/.env
# Should show: 404 Not Found ✅

# 4. Check API is working
# Open in browser: https://your-app.vercel.app/api
# Should show: API root endpoint response ✅
```

---

## 🔐 Where Are Your Secrets Stored?

### ✅ SAFE LOCATIONS (Encrypted by Vercel):
1. **Vercel Dashboard** → Environment Variables (encrypted at rest)
2. **Your local machine** → `.env` files (protected by .gitignore)
3. **Neon Dashboard** → Database connection strings (encrypted)

### ❌ NEVER STORED HERE:
1. ❌ GitHub repository
2. ❌ Git history
3. ❌ Publicly accessible URLs
4. ❌ Deployment logs (Vercel redacts secrets automatically)

---

## 🎯 Test Your Deployed Application

### 1. Visit Your App
```
https://your-app-name.vercel.app
```

### 2. Sign Up
- Click "Sign Up"
- Enter email and password
- Should redirect to dashboard ✅

### 3. Create Task
- Add a new todo item
- Should save to Neon database ✅

### 4. Logout and Login
- Logout
- Login with same credentials
- Tasks should still be there ✅

---

## 🚨 Common Issues & Fixes

### Issue 1: "Failed to fetch" or "Network Error"

**Cause:** `NEXT_PUBLIC_API_URL` not set correctly

**Fix:**
1. Go to Vercel → Settings → Environment Variables
2. Check `NEXT_PUBLIC_API_URL` is set to: `https://your-exact-url.vercel.app`
3. Redeploy

---

### Issue 2: CORS Error

**Cause:** `CORS_ORIGINS` not set correctly

**Fix:**
1. Go to Vercel → Settings → Environment Variables
2. Check `CORS_ORIGINS` is set to: `["https://your-exact-url.vercel.app"]`
3. Include the square brackets and quotes exactly as shown
4. Redeploy

---

### Issue 3: Database Connection Failed

**Cause:** `DATABASE_URL` is incorrect or not set

**Fix:**
1. Go to Neon Dashboard
2. Copy the **Pooler Connection String** (not direct URL)
3. Should end with `?sslmode=require`
4. Update `DATABASE_URL` in Vercel
5. Redeploy

---

### Issue 4: "BETTER_AUTH_SECRET is not set"

**Cause:** Environment variable not added

**Fix:**
1. Generate a new secret (see Step 3.1)
2. Add to Vercel environment variables
3. Make sure it's set for all environments (Production, Preview, Development)
4. Redeploy

---

## 💰 Cost (100% Free for Personal Projects)

- ✅ Vercel Hobby Plan: **FREE**
  - Unlimited deployments
  - 100GB bandwidth/month
  - Automatic HTTPS

- ✅ Neon Free Tier: **FREE**
  - 0.5GB storage
  - 1 branch
  - Pooler connection included

**Total Monthly Cost: $0** 🎉

---

## 🔄 Auto-Deploy on Git Push

After initial setup, Vercel automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin 002-fullstack-web
```

Vercel will:
1. Detect the push
2. Build frontend and backend
3. Deploy automatically
4. Send you a deployment URL

---

## 📊 Monitor Your Deployments

### Vercel Dashboard Shows:
- ✅ Deployment status (success/failed)
- ✅ Build logs (secrets are automatically redacted)
- ✅ Function logs (API calls)
- ✅ Analytics (pageviews, etc.)

**Secrets are NEVER shown in logs!** Vercel automatically redacts them.

---

## ✅ Final Security Verification

**Run this checklist before going live:**

```bash
# 1. Confirm .env files are ignored
git check-ignore backend/.env frontend/.env.local
# Should output both file paths ✅

# 2. Confirm only templates are tracked
git ls-files | grep "env"
# Should ONLY show .env.example files ✅

# 3. Try to access secrets via URL
# Browser: https://your-app.vercel.app/.env
# Should return: 404 ✅

# 4. Check Vercel environment variables
# Dashboard → Settings → Environment Variables
# All 5 variables should be set ✅
```

**If all checks pass → YOU ARE SECURE! 🔒**

---

## 🆘 Need Help?

### Vercel Support:
- Docs: https://vercel.com/docs
- Community: https://github.com/vercel/vercel/discussions

### Neon Support:
- Docs: https://neon.tech/docs
- Community: https://neon.tech/discord

---

## 🎉 You're All Set!

Your application is now:
- ✅ Deployed on Vercel
- ✅ Secrets are encrypted and secure
- ✅ Auto-deploys on git push
- ✅ 100% free hosting
- ✅ Professional production setup

**Your keys will NEVER be public! 🔒**

---

**Generated with security-first practices for Panaversity Hackathon Phase 2**
