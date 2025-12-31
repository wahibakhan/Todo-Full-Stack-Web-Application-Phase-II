# Security Guidelines

## Protected Files (NEVER Commit to GitHub)

The following files contain sensitive information and are protected by `.gitignore`:

### Environment Files (.env)
- `backend/.env` - Contains database password and JWT secret
- `frontend/.env.local` - Contains API keys and secrets
- **These files are NEVER pushed to GitHub**

### Database Files
- `backend/todo_app.db` - Contains all user data
- Any `.sqlite` or `.db` files

### Cookie Files
- `cookies.txt`
- `*-cookies.txt`

## Safe Files (Can be Committed)

### Template Files
- `backend/.env.example` - Empty template with no secrets
- `frontend/.env.example` - Empty template with no secrets
- **These are safe to commit and help other developers set up their environment**

## How to Verify Security

Before pushing to GitHub, run:

```bash
# Check what files will be committed
git status

# Verify no .env files are listed
git ls-files | grep .env
# Should only show .env.example files, NOT .env or .env.local

# Verify no database files are listed
git ls-files | grep -E "\.db$|\.sqlite"
# Should show nothing
```

## If You Accidentally Committed Secrets

If you accidentally committed `.env` files with real secrets:

1. **Immediately change all passwords and secrets**
2. **Remove the file from git history:**
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch backend/.env" \
     --prune-empty --tag-name-filter cat -- --all
   ```
3. **Force push (WARNING: This rewrites history):**
   ```bash
   git push origin --force --all
   ```

## Secret Values

Current secrets to protect:
- `BETTER_AUTH_SECRET` - JWT signing key
- `DATABASE_URL` - Database connection with password
- Session cookies
- User passwords (always hashed in database)

## Best Practices

1. ✅ Never hardcode secrets in code
2. ✅ Always use environment variables
3. ✅ Keep `.gitignore` updated
4. ✅ Use `.env.example` with empty values
5. ✅ Regularly check `git status` before committing
6. ✅ Review GitHub repository to ensure no secrets are visible

## Current Protection Status

✅ `.gitignore` created with comprehensive rules
✅ All `.env` files excluded from git
✅ All database files excluded from git
✅ `.env.example` files use placeholders only
✅ No secrets currently tracked by git
