# Hugging Face Deployment Quick Start

## Pre-Deployment Checklist

- [ ] Hugging Face account created
- [ ] Neon PostgreSQL database set up
- [ ] BETTER_AUTH_SECRET generated (`openssl rand -base64 32`)
- [ ] DATABASE_URL from Neon (pooler connection string)

## Quick Deploy Steps

### 1. Create Hugging Face Space
Visit: https://huggingface.co/new-space
- Name: `todo-backend-api` (or your choice)
- SDK: **Docker**
- Hardware: CPU basic (free)

### 2. Add Environment Secrets
In Space Settings → Variables and secrets:

```
BETTER_AUTH_SECRET=<your-32-char-secret>
DATABASE_URL=postgresql://user:password@host-pooler.region.aws.neon.tech/dbname?sslmode=require
ENVIRONMENT=production
```

### 3. Deploy Code

**Method 1: Git Push (Fastest)**
```bash
cd C:\projects\todo_app\backend

# Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# Push to deploy (from current branch)
git subtree push --prefix=backend hf main
```

**Method 2: Direct Upload**
- In your Space, click Files → Upload files
- Upload entire `backend` folder contents

### 4. Verify Deployment

Once build completes (3-5 minutes):
- Visit: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/docs`
- Test health: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/`

### 5. Update Frontend
In frontend `.env.local`:
```
NEXT_PUBLIC_API_URL=https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space
```

## Key Files (Already Configured)

- `Dockerfile` - Uses port 7860 (HF default)
- `README.md` - Has HF frontmatter
- `requirements.txt` - All dependencies
- `app/main.py` - CORS configured
- `app/core/config.py` - Environment variables

## Common Issues

**Build fails**: Check Logs tab for errors
**500 errors**: Verify DATABASE_URL and BETTER_AUTH_SECRET in Secrets
**CORS errors**: Update CORS_ORIGINS in backend config to include your frontend URL

## Need Help?
See full guide: `DEPLOYMENT_HUGGINGFACE.md`
