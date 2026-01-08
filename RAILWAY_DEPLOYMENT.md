# Railway Deployment Guide - Backend API

This guide covers deploying the FastAPI backend to Railway.

## Prerequisites

- Railway account (https://railway.app)
- Neon PostgreSQL database already set up
- GitHub repository connected to Railway

## Quick Deploy

### 1. Create New Project on Railway

1. Go to https://railway.app/new
2. Select "Deploy from GitHub repo"
3. Choose your todo_app repository
4. Railway will auto-detect the configuration from `railway.json`

### 2. Configure Environment Variables

Add these variables in Railway Dashboard → Variables:

```env
BETTER_AUTH_SECRET=<generate-with-openssl-rand-base64-32>
DATABASE_URL=<your-neon-pooler-connection-string>
ENVIRONMENT=production
CORS_ORIGINS=["https://your-frontend-url.vercel.app"]
```

**Important Notes:**
- `BETTER_AUTH_SECRET`: Must match your frontend's secret
- `DATABASE_URL`: Get from Neon dashboard (use **pooler** connection string)
- `CORS_ORIGINS`: Add your frontend URL (Vercel, Netlify, etc.)

### 3. Deploy

Railway will automatically:
1. Detect Python project
2. Install dependencies from `backend/requirements.txt`
3. Start FastAPI with `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 4. Get Your API URL

After deployment completes:
1. Go to Settings → Networking
2. Click "Generate Domain"
3. Copy the URL (e.g., `https://your-app.up.railway.app`)

### 5. Update Frontend Configuration

Update your frontend's `.env.local`:

```env
NEXT_PUBLIC_API_URL=https://your-app.up.railway.app
```

## Database Setup

Railway can provision PostgreSQL, but we're using Neon:

1. Get connection string from Neon dashboard
2. Use the **pooler** URL for better performance:
   ```
   postgresql://user:password@ep-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require
   ```
3. Add to Railway environment variables as `DATABASE_URL`

## Configuration Files

- **`railway.json`** (root): Main Railway configuration
- **`backend/railway.json`**: Backend-specific settings
- **`backend/Procfile`**: Alternative start command definition

## Health Check

After deployment, test your API:

```bash
curl https://your-app.up.railway.app/api/health
```

## API Documentation

Access auto-generated docs at:
- Swagger UI: `https://your-app.up.railway.app/docs`
- ReDoc: `https://your-app.up.railway.app/redoc`

## Monitoring

Railway provides:
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, network usage
- **Deployments**: History and rollback options

Access via Railway Dashboard → your project → Observability tab

## Troubleshooting

### Build Fails

Check that `backend/requirements.txt` is valid:
```bash
cd backend
pip install -r requirements.txt
```

### Database Connection Issues

Verify:
- `DATABASE_URL` includes `?sslmode=require`
- Using pooler URL (not direct connection)
- Neon database is active (free tier sleeps after inactivity)

### CORS Errors

Update `CORS_ORIGINS` in Railway variables:
```json
["https://your-frontend.vercel.app", "https://your-custom-domain.com"]
```

### Port Binding

Railway automatically sets `$PORT` - don't hardcode port 8000!

The start command uses `--port $PORT` to bind correctly.

## Cost Estimates

Railway free tier includes:
- $5 free credit per month
- ~500 hours of runtime
- Sufficient for development/testing

For production, expect ~$5-10/month for a basic API.

## Next Steps

1. Deploy frontend to Vercel/Netlify
2. Update `CORS_ORIGINS` with frontend URL
3. Set `NEXT_PUBLIC_API_URL` to Railway backend URL
4. Test end-to-end authentication flow

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Railway Status: https://status.railway.app
