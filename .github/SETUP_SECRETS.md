# GitHub Actions Secrets Setup

This guide explains how to add required secrets for automatic Hugging Face deployment.

## Required GitHub Secrets

Go to your GitHub repository:
**Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add the following secrets:

### 1. HF_TOKEN
**Description:** Your Hugging Face access token

**How to get it:**
1. Go to https://huggingface.co/settings/tokens
2. Click **New token**
3. Name: `GitHub Actions Deploy`
4. Type: **Write** (required for pushing to Spaces)
5. Copy the token

**Add to GitHub:**
- Name: `HF_TOKEN`
- Value: `hf_xxxxxxxxxxxxxxxxxxxxx` (your token)

---

### 2. HF_USERNAME
**Description:** Your Hugging Face username

**How to get it:**
- Your username is visible at https://huggingface.co/settings/account
- Example: If your profile is `https://huggingface.co/wahibakhan`, then username is `wahibakhan`

**Add to GitHub:**
- Name: `HF_USERNAME`
- Value: `wahibakhan` (your username)

---

### 3. HF_SPACE_NAME
**Description:** The name of your Hugging Face Space

**How to get it:**
- If you created a Space called `todo-backend-api`, use that name
- The Space URL format: `https://huggingface.co/spaces/USERNAME/SPACE_NAME`

**Add to GitHub:**
- Name: `HF_SPACE_NAME`
- Value: `todo-backend-api` (your Space name)

---

## Environment Secrets for Hugging Face Space

These are configured in Hugging Face Spaces (NOT in GitHub):

Go to your Space: **Settings** → **Variables and secrets** → **New secret**

### 1. BETTER_AUTH_SECRET
Generate with:
```bash
openssl rand -base64 32
```

### 2. DATABASE_URL
Your Neon PostgreSQL pooler connection string:
```
postgresql://user:password@ep-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require
```

### 3. ENVIRONMENT
```
production
```

---

## Verify Setup

After adding all secrets:

1. **Check GitHub Secrets:**
   - Go to your repo → Settings → Secrets and variables → Actions
   - You should see: `HF_TOKEN`, `HF_USERNAME`, `HF_SPACE_NAME`

2. **Check Hugging Face Space Secrets:**
   - Go to your Space → Settings → Variables and secrets
   - You should see: `BETTER_AUTH_SECRET`, `DATABASE_URL`, `ENVIRONMENT`

3. **Test Deployment:**
   - Push a change to `002-fullstack-web` branch
   - Go to your repo → Actions tab
   - Watch the deployment workflow run

---

## Workflow Triggers

The deployment will automatically run when:
- ✅ You push changes to `002-fullstack-web` or `main` branch
- ✅ Changes are made to files in `backend/` folder
- ✅ You manually trigger from Actions tab (workflow_dispatch)

---

## Troubleshooting

**Workflow fails with "authentication failed":**
- Check that `HF_TOKEN` has **Write** permissions
- Verify `HF_USERNAME` matches your actual username

**Workflow succeeds but Space doesn't update:**
- Check Hugging Face Space logs
- Verify `HF_SPACE_NAME` matches your actual Space name
- Ensure Space is using Docker SDK

**Build fails on Hugging Face:**
- Check Space environment secrets are set correctly
- Verify `DATABASE_URL` is correct
- Check Space logs for error details
