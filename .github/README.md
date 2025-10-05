# GitHub Actions Keep-Alive Setup

This directory contains GitHub Actions workflows to keep your Render backend alive automatically.

## Files Created:

1. **`keep-alive.yml`** - Full-featured workflow with detailed logging
2. **`simple-keep-alive.yml`** - Simple workflow (recommended)

## How to Use:

### Step 1: Commit and Push
```bash
git add .github/
git commit -m "Add GitHub Actions keep-alive workflows"
git push
```

### Step 2: Enable GitHub Actions
1. Go to your GitHub repository
2. Click on "Actions" tab
3. You should see the workflows listed
4. GitHub Actions will automatically start running

### Step 3: Monitor
- Go to Actions tab to see workflow runs
- Each run will ping your backend every 10 minutes
- Green checkmark = success, Red X = failure

## Workflow Details:

### Simple Version (`simple-keep-alive.yml`):
- Runs every 10 minutes
- Pings `https://saco-ai-assistant.onrender.com/ping`
- Minimal logging
- Easy to understand

### Full Version (`keep-alive.yml`):
- Runs every 10 minutes
- Detailed logging with timestamps
- Manual trigger option
- Better error handling
- Status reporting

## Manual Testing:

You can manually trigger a workflow:
1. Go to Actions tab
2. Click on "Keep Backend Alive"
3. Click "Run workflow" button
4. Click "Run workflow" to start

## Troubleshooting:

- **Workflow not running**: Check if GitHub Actions is enabled for your repo
- **Backend still sleeping**: Try reducing the interval (change `*/10` to `*/5` for 5 minutes)
- **Permission issues**: Make sure the repository allows GitHub Actions

## Benefits:

✅ **Free** - GitHub Actions has generous free tier
✅ **24/7** - Runs automatically without your computer
✅ **Reliable** - GitHub's infrastructure
✅ **No setup** - Just push the files and it works
