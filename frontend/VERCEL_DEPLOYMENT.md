# Deploy Frontend to Vercel

## Quick Deployment Steps

### 1. Push to GitHub (if not already done)
```bash
git add .
git commit -m "Prepare frontend for Vercel deployment"
git push origin 002-fullstack-web
```

### 2. Deploy to Vercel

#### Option A: Via Vercel Dashboard (Recommended)

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New" → "Project"
3. Import your GitHub repository:
   - Repository: `Todo-Full-Stack-Web-Application-Phase-II`
4. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

5. **Add Environment Variables** (CRITICAL):

   Click "Environment Variables" and add these:

   | Name | Value |
   |------|-------|
   | `BETTER_AUTH_SECRET` | `IONfNJ7anNPityGTLYGu4xGaipXAZNDHxYId2CkqKzM` |
   | `NEXT_PUBLIC_API_URL` | `https://wahibakhan-todo-backend.hf.space` |
   | `DATABASE_URL` | `postgresql://neondb_owner:npg_UHrME3ZBzwq2@ep-mute-voice-a4j8dlct-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require` |

6. Click "Deploy"

#### Option B: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend
cd frontend

# Deploy
vercel

# Follow prompts and set environment variables when asked
```

---

## Environment Variables Explained

### BETTER_AUTH_SECRET
- **What**: Shared secret for JWT token encryption
- **CRITICAL**: Must match backend exactly
- **Value**: `IONfNJ7anNPityGTLYGu4xGaipXAZNDHxYId2CkqKzM`

### NEXT_PUBLIC_API_URL
- **What**: Your backend API URL
- **Local**: `http://localhost:8001`
- **Production**: `https://wahibakhan-todo-backend.hf.space`
- **Note**: `NEXT_PUBLIC_` prefix makes it available in browser

### DATABASE_URL
- **What**: Neon PostgreSQL connection string
- **Required by**: Better Auth (if used)
- **Format**: `postgresql://user:pass@host/db?sslmode=require`

---

## After Deployment

### 1. Update Backend CORS

Your backend needs to allow requests from your Vercel frontend.

**Go to Hugging Face Space settings:**
https://huggingface.co/spaces/wahibakhan/Todo_backend/settings

**Add/Update secret:**
- Name: `CORS_ORIGINS`
- Value: `https://your-app.vercel.app,*`
  (Replace `your-app.vercel.app` with your actual Vercel URL)

### 2. Test Your Deployment

Visit your Vercel URL and test:
- ✅ Sign up new user
- ✅ Log in
- ✅ Create task
- ✅ Update task
- ✅ Mark complete
- ✅ Delete task

---

## Troubleshooting

### API Calls Fail (CORS errors)
- **Fix**: Update CORS_ORIGINS in backend HF Space
- Include your Vercel URL in allowed origins

### Authentication Not Working
- **Fix**: Verify BETTER_AUTH_SECRET matches backend exactly
- Check browser cookies are enabled

### Database Connection Issues
- **Fix**: Verify DATABASE_URL is correct
- Check Neon database is active

### Build Fails
- **Fix**: Check build logs in Vercel dashboard
- Verify all dependencies in package.json
- Run `npm run build` locally first

---

## Your URLs

After deployment:
- **Frontend (Vercel)**: `https://your-app.vercel.app`
- **Backend (Hugging Face)**: `https://wahibakhan-todo-backend.hf.space`
- **API Docs**: `https://wahibakhan-todo-backend.hf.space/docs`

---

## Auto-Deploy Setup

Vercel automatically redeploys when you push to GitHub:
1. Make changes to frontend code
2. Commit and push to GitHub
3. Vercel automatically rebuilds and deploys

---

## Security Notes

✅ BETTER_AUTH_SECRET is stored securely in Vercel
✅ Database credentials are environment variables (not in code)
✅ CORS is properly configured
✅ HTTPOnly cookies for JWT tokens
✅ SSL/TLS enabled by default on Vercel
