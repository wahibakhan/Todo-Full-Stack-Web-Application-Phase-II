# Todo App - Quick Start Guide

## Port Configuration

This project uses custom ports to avoid conflicts with other projects:

- **Frontend (Next.js)**: http://localhost:3001
- **Backend (FastAPI)**: http://localhost:8001

## Prerequisites

- Node.js 20+ installed
- Python 3.11+ installed
- PostgreSQL database (Neon recommended)

## Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env and add your credentials:
# - BETTER_AUTH_SECRET (generate with: openssl rand -base64 32)
# - DATABASE_URL (get from Neon dashboard)

# Start backend server on port 8001
python start_dev.py
```

Backend will be available at: **http://localhost:8001**

API Documentation: **http://localhost:8001/docs**

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local file from example
cp .env.example .env.local

# Edit .env.local and add:
# - BETTER_AUTH_SECRET (same as backend!)
# - NEXT_PUBLIC_API_URL=http://localhost:8001
# - DATABASE_URL (same as backend)

# Start frontend server on port 3001
npm run dev
```

Frontend will be available at: **http://localhost:3001**

## Running Both Services

### Terminal 1 - Backend:
```bash
cd backend
python start_dev.py
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

## Testing the Application

1. Open browser: http://localhost:3001
2. Click "Sign Up" to create an account
3. Login with your credentials
4. Start managing your todos!

## API Endpoints

Once backend is running on port 8001:

- `GET /` - Health check
- `GET /docs` - Interactive API documentation
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `GET /api/tasks` - List user's tasks
- `POST /api/tasks` - Create new task
- `PATCH /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

## Troubleshooting

### Port Already in Use

If you see "port already in use" errors:

**Frontend:**
```bash
# Edit frontend/package.json and change -p 3001 to another port
# Then update backend CORS_ORIGINS to match
```

**Backend:**
```bash
# Edit backend/start_dev.py and change port=8001 to another port
# Then update frontend .env.local NEXT_PUBLIC_API_URL to match
```

### CORS Errors

Make sure:
- Backend CORS_ORIGINS includes `http://localhost:3001`
- Frontend API URL is `http://localhost:8001`
- Both services are running

### Database Connection Failed

- Verify DATABASE_URL in both frontend and backend .env files
- Check Neon dashboard - database should be active
- Ensure connection string uses pooler URL (has `-pooler.` in hostname)

## Production Deployment

### Backend (Hugging Face Spaces)
- See: `backend/DEPLOYMENT_HUGGINGFACE.md`

### Frontend (Vercel)
- Connect your GitHub repository to Vercel
- Add environment variables in Vercel dashboard
- Deploy automatically on git push

## Environment Variables

### Backend (.env)
```
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
DATABASE_URL=postgresql://user:pass@host-pooler.region.aws.neon.tech/db?sslmode=require
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:3001"]
```

### Frontend (.env.local)
```
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
NEXT_PUBLIC_API_URL=http://localhost:8001
DATABASE_URL=postgresql://user:pass@host-pooler.region.aws.neon.tech/db?sslmode=require
```

**IMPORTANT**: BETTER_AUTH_SECRET must be identical in both frontend and backend!

## Project Structure

```
todo_app/
├── backend/              # FastAPI backend (port 8001)
│   ├── app/
│   │   ├── main.py      # FastAPI app initialization
│   │   ├── routes/      # API endpoints
│   │   ├── models/      # Database models
│   │   └── core/        # Configuration & security
│   ├── start_dev.py     # Development server script
│   └── requirements.txt # Python dependencies
│
├── frontend/            # Next.js frontend (port 3001)
│   ├── app/            # Next.js App Router
│   ├── components/     # React components
│   ├── lib/           # Utilities & API client
│   └── package.json   # Node dependencies
│
└── QUICKSTART.md      # This file
```

## Next Steps

1. Set up your database on Neon: https://neon.tech
2. Generate a secure BETTER_AUTH_SECRET: `openssl rand -base64 32`
3. Configure both .env files with matching secrets
4. Start backend on port 8001
5. Start frontend on port 3001
6. Build your todo app!

## Support

- Frontend docs: https://nextjs.org/docs
- Backend docs: https://fastapi.tiangolo.com/
- Database docs: https://neon.tech/docs

Happy coding! 🚀
