# Deploy Backend to Hugging Face Spaces

This guide walks you through deploying the FastAPI backend to Hugging Face Spaces.

## Prerequisites

1. **Hugging Face Account**: Sign up at [huggingface.co](https://huggingface.co)
2. **Neon PostgreSQL Database**: Set up at [neon.tech](https://neon.tech)
3. **Git installed** on your machine

## Step 1: Prepare Your Environment Variables

You'll need to configure these secrets in Hugging Face Spaces:

### Required Secrets

1. **BETTER_AUTH_SECRET**
   - Generate with: `openssl rand -base64 32`
   - Must be at least 32 characters
   - CRITICAL: Use the SAME secret in your frontend deployment

2. **DATABASE_URL**
   - Get from your Neon dashboard
   - Use the **pooler connection string** for better performance
   - Format: `postgresql://user:password@host-pooler.region.aws.neon.tech/dbname?sslmode=require`

3. **ENVIRONMENT**
   - Set to: `production`

4. **CORS_ORIGINS** (optional, already configured in code)
   - Frontend URLs that can access the API
   - Example: `["https://your-frontend.vercel.app"]`

## Step 2: Create a New Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Fill in the details:
   - **Space name**: `todo-backend-api` (or your preferred name)
   - **License**: Apache 2.0 (or your choice)
   - **Select the Space SDK**: **Docker**
   - **Space hardware**: CPU basic (free tier is sufficient)
   - **Visibility**: Public or Private

3. Click **Create Space**

## Step 3: Configure Environment Secrets

1. Go to your Space's **Settings** tab
2. Scroll to **Variables and secrets**
3. Add the following secrets (click **New secret** for each):

   ```
   BETTER_AUTH_SECRET=<your-generated-secret>
   DATABASE_URL=postgresql://user:password@host-pooler.region.aws.neon.tech/dbname?sslmode=require
   ENVIRONMENT=production
   ```

**Important**:
- Use the **"Secret"** option (not "Variable") to hide sensitive values
- Double-check your DATABASE_URL format
- Keep BETTER_AUTH_SECRET safe - you'll need it for your frontend

## Step 4: Deploy Your Code

### Option A: Deploy via Git (Recommended)

1. **Navigate to backend directory**:
   ```bash
   cd C:\projects\todo_app\backend
   ```

2. **Add Hugging Face remote** (if not already added):
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   ```
   Replace `YOUR_USERNAME` and `YOUR_SPACE_NAME` with your actual values.

3. **Create deployment branch** (optional but recommended):
   ```bash
   git checkout -b deploy-hf
   ```

4. **Commit and push to Hugging Face**:
   ```bash
   git add .
   git commit -m "Deploy backend to Hugging Face Spaces"
   git push hf deploy-hf:main
   ```

   Note: Hugging Face Spaces uses `main` as the default branch.

### Option B: Deploy via Web Interface

1. In your Space, click **Files**
2. Click **Add file** → **Upload files**
3. Upload all files from the `backend` directory
4. Make sure these files are included:
   - `Dockerfile`
   - `requirements.txt`
   - `README.md` (with Hugging Face frontmatter)
   - `runtime.txt` (optional)
   - `app/` directory with all Python files

## Step 5: Verify Deployment

1. **Wait for build**: Hugging Face will build your Docker container (this takes 3-5 minutes)
2. **Check logs**: Click on **Logs** tab to monitor build progress
3. **Test the API**:
   - Your Space URL will be: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`
   - Visit: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/docs`
   - You should see the FastAPI Swagger documentation

4. **Test health endpoint**:
   ```bash
   curl https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/
   ```
   Expected response:
   ```json
   {
     "message": "Todo App API - Phase 2",
     "status": "running",
     "docs": "/docs"
   }
   ```

## Step 6: Update Frontend Configuration

After your backend is deployed, update your frontend to point to the Hugging Face Spaces URL:

1. In your frontend `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space
   BETTER_AUTH_SECRET=<same-secret-as-backend>
   ```

2. Also update CORS_ORIGINS in your backend secrets if needed to include your frontend URL.

## Troubleshooting

### Build Fails

- **Check logs** in the Logs tab for specific errors
- **Verify requirements.txt**: Make sure all dependencies are listed
- **Check Dockerfile**: Ensure it's properly formatted

### API Returns 500 Errors

- **Check environment secrets**: Ensure BETTER_AUTH_SECRET and DATABASE_URL are set correctly
- **Database connection**: Verify your Neon database is active and the URL is correct
- **Check logs**: Look for Python errors in the application logs

### CORS Errors from Frontend

- **Update CORS_ORIGINS**: Add your frontend URL to the allowed origins
- In backend config.py or via environment variable
- Redeploy after changing

### Database Connection Issues

- **Use pooler URL**: Neon pooler URLs perform better (`-pooler.` in hostname)
- **Check SSL mode**: Ensure `?sslmode=require` is in DATABASE_URL
- **Verify credentials**: Double-check username/password in connection string

## Monitoring and Maintenance

- **View logs**: Use the Logs tab to monitor application activity
- **Restart Space**: Settings → Factory reboot to restart your container
- **Update code**: Push changes via Git and the Space will rebuild automatically
- **Database backups**: Configure in Neon dashboard

## API Endpoints

Once deployed, your API will have these endpoints:

- `GET /` - Health check
- `GET /docs` - Interactive API documentation
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `GET /api/tasks` - List user's tasks
- `POST /api/tasks` - Create new task
- `PATCH /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

## Security Notes

- All secrets are stored in Hugging Face Spaces secrets (not in code)
- Database uses SSL (sslmode=require)
- JWT tokens for authentication
- User data isolation (queries filtered by user_id)
- CORS configured to only allow your frontend

## Next Steps

1. Test all API endpoints using `/docs`
2. Deploy your frontend (Next.js) to Vercel or another Hugging Face Space
3. Update frontend to use the backend API URL
4. Test the complete flow: signup → login → create tasks

## Resources

- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Docker Spaces Guide](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [Neon PostgreSQL Docs](https://neon.tech/docs/introduction)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
