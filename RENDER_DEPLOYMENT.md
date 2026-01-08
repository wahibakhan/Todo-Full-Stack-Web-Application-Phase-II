# Render Deployment Guide - Backend API

This guide covers deploying the FastAPI backend to Render.

## Prerequisites

- Render account (https://render.com)
- Neon PostgreSQL database already set up
- GitHub repository connected to Render

## Quick Deploy

### Method 1: One-Click Deploy (Recommended)

1. Go to https://render.com/
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Select repository: `Todo-Full-Stack-Web-Application-Phase-II`
5. Branch: `002-fullstack-web`
6. Render will detect `render.yaml` automatically
7. Click **"Apply"**

### Method 2: Manual Setup

#### Step 1: Create New Web Service

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select: `Todo-Full-Stack-Web-Application-Phase-II`
5. Configure the service:

**Basic Settings:**
- **Name:** `todo-backend` (or your choice)
- **Region:** Oregon (or closest to you)
- **Branch:** `002-fullstack-web`
- **Root Directory:** `backend` ⚠️ **IMPORTANT!**
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Plan:**
- Select **"Free"** (or paid plan for better performance)

#### Step 2: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"** and add:

**Variable 1: BETTER_AUTH_SECRET**
```
Key: BETTER_AUTH_SECRET
Value: <generate with: openssl rand -base64 32>
```

**Variable 2: DATABASE_URL**
```
Key: DATABASE_URL
Value: <your-neon-pooler-connection-string>
```

**Variable 3: ENVIRONMENT**
```
Key: ENVIRONMENT
Value: production
```

**Variable 4: CORS_ORIGINS**
```
Key: CORS_ORIGINS
Value: ["http://localhost:3001"]
```

**Important Notes:**
- `BETTER_AUTH_SECRET`: Generate a secure random string (min 32 chars)
- `DATABASE_URL`: Get from Neon dashboard (use **pooler** connection string)
- `CORS_ORIGINS`: Update with your frontend URL after deploying frontend

#### Step 3: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `backend/requirements.txt`
   - Start FastAPI with uvicorn
3. Wait for deployment to complete (2-3 minutes)

### Step 4: Get Your API URL

After deployment completes:
1. Your service URL will be shown at the top
2. Format: `https://todo-backend.onrender.com`
3. Copy this URL

### Step 5: Test Your API

Visit in browser or use curl:
```bash
curl https://todo-backend.onrender.com/
```

Expected response:
```json
{
  "message": "Todo App API - Phase 2",
  "status": "running",
  "docs": "/docs"
}
```

## API Documentation

Access auto-generated docs at:
- **Swagger UI:** `https://todo-backend.onrender.com/docs`
- **ReDoc:** `https://todo-backend.onrender.com/redoc`

## Database Setup

Render can provision PostgreSQL, but we're using Neon:

1. Get connection string from Neon dashboard
2. Use the **pooler** URL for better performance:
   ```
   postgresql://user:password@ep-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require
   ```
3. Add to Render environment variables as `DATABASE_URL`

## Configuration Files

- **`render.yaml`** (root): Blueprint configuration for one-click deploy
- **`backend/requirements.txt`**: Python dependencies

## Important: Monorepo Setup

⚠️ **CRITICAL:** Set **Root Directory** to `backend`

This project uses a monorepo structure. Render needs to know to build only the backend folder.

In Render Dashboard:
- Go to **Settings** → **Build & Deploy**
- Set **Root Directory** to: `backend`

## Monitoring

Render provides:
- **Logs:** Real-time application logs (Logs tab)
- **Metrics:** CPU, memory, bandwidth (Metrics tab)
- **Events:** Deployment history (Events tab)

## Health Checks

Render automatically monitors your service:
- **Health Check Path:** `/` (configured in render.yaml)
- **Auto-restart:** If service crashes, Render auto-restarts

## Troubleshooting

### Build Fails: "Could not find requirements.txt"

**Cause:** Root Directory not set to `backend`

**Fix:**
1. Go to Settings → Build & Deploy
2. Set **Root Directory** to: `backend`
3. Trigger manual deploy

### Database Connection Issues

**Verify:**
- `DATABASE_URL` includes `?sslmode=require`
- Using pooler URL (not direct connection)
- Neon database is active (free tier sleeps after inactivity)

### CORS Errors

**Update `CORS_ORIGINS`:**
1. Go to Environment tab
2. Edit `CORS_ORIGINS` variable
3. Add your frontend URL: `["https://your-frontend.vercel.app"]`
4. Save (auto-redeploys)

### Port Binding Issues

Render automatically sets `$PORT` environment variable.

Our start command uses `--port $PORT` which binds correctly.

### Free Tier Limitations

Render Free tier:
- ✅ 750 hours/month (enough for 1 service 24/7)
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ Cold starts take ~30 seconds

**Upgrade to paid plan** ($7/month) for:
- No spin down
- Faster builds
- More memory/CPU

## Automatic Deploys

By default, Render auto-deploys on every push to `002-fullstack-web` branch.

**To disable:**
1. Go to Settings
2. Toggle **"Auto-Deploy"** off
3. Use manual deploys instead

## Custom Domain (Optional)

1. Go to Settings → Custom Domains
2. Add your domain (e.g., `api.yourdomain.com`)
3. Configure DNS (Render provides instructions)
4. SSL/TLS is automatic and free

## Environment Variable Security

✅ **Secure practices:**
- Variables are encrypted at rest
- Not visible in build logs
- Accessible only to your service

⚠️ **Never commit secrets to git** - use environment variables only!

## Cost Estimates

**Free Tier:**
- $0/month
- Good for development/testing
- Spins down after inactivity

**Starter Plan:**
- $7/month per service
- Always on (no spin down)
- 512 MB RAM
- Recommended for production

## Next Steps

1. ✅ Deploy backend to Render
2. Deploy frontend to Vercel/Netlify
3. Update `CORS_ORIGINS` with frontend URL
4. Set `NEXT_PUBLIC_API_URL` to Render backend URL
5. Test end-to-end authentication flow

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Render Status: https://status.render.com

## Comparison: Render vs Railway

| Feature | Render | Railway |
|---------|--------|---------|
| Free Tier | 750 hrs/month | $5 credit/month |
| Spin Down | After 15 min | Configurable |
| Build Time | Fast | Fast |
| Setup | Easier | More config needed |
| Postgres | Built-in option | Built-in option |
| Pricing | $7/month starter | $5-10/month |

**Recommendation:** Use Render for simpler setup and better free tier!
