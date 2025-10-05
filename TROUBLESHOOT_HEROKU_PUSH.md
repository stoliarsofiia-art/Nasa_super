# Troubleshooting Heroku Push Issues

## 🔍 Step 1: Diagnose the Problem

Run these commands and share the output:

```bash
# Check git status
git status

# Check git remotes
git remote -v

# Check Heroku apps
heroku apps

# Check if you're logged in
heroku auth:whoami
```

---

## 🔧 Common Issues & Solutions

### Issue 1: "fatal: 'heroku' does not appear to be a git repository"

**Cause:** Heroku remote not configured

**Solution:**
```bash
# Connect to your existing app
heroku git:remote -a sophia-nasa-ml-app

# Verify it worked
git remote -v
# Should show:
# heroku  https://git.heroku.com/sophia-nasa-ml-app.git (fetch)
# heroku  https://git.heroku.com/sophia-nasa-ml-app.git (push)
```

---

### Issue 2: "Everything up-to-date" but app not working

**Cause:** No changes to push OR wrong branch

**Solution:**
```bash
# Check your current branch
git branch

# If you're on a different branch, push that branch to Heroku's main:
git push heroku your-branch:main

# Or if on main:
git push heroku main

# Force a rebuild even without changes:
git commit --allow-empty -m "Trigger Heroku rebuild"
git push heroku main
```

---

### Issue 3: "Updates were rejected" or "non-fast-forward"

**Cause:** Heroku has commits you don't have locally

**Solution:**
```bash
# Force push (this will overwrite Heroku's version)
git push heroku main --force

# Or if on different branch:
git push heroku HEAD:main --force
```

---

### Issue 4: "Permission denied" or "Authentication failed"

**Cause:** Not logged in or wrong credentials

**Solution:**
```bash
# Login to Heroku
heroku login

# If that doesn't work, try browser login
heroku login -i

# Check authentication
heroku auth:whoami
```

---

### Issue 5: Git not initialized

**Cause:** No git repository

**Solution:**
```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add Heroku remote
heroku git:remote -a sophia-nasa-ml-app

# Push
git push heroku main
```

---

### Issue 6: "You do not have access to this app"

**Cause:** Wrong app name or no permission

**Solution:**
```bash
# Check your apps
heroku apps

# If sophia-nasa-ml-app is yours, add it:
heroku git:remote -a sophia-nasa-ml-app

# If it's not in the list, you need to be added as collaborator
# Or create a new app:
heroku create your-new-app-name
```

---

### Issue 7: "Could not find an app to deploy to"

**Cause:** No app specified

**Solution:**
```bash
# Specify app explicitly
git push https://git.heroku.com/sophia-nasa-ml-app.git HEAD:main --force

# Or add remote first
heroku git:remote -a sophia-nasa-ml-app
git push heroku main
```

---

### Issue 8: Large files preventing push

**Cause:** Files larger than 100MB

**Solution:**
```bash
# Check for large files
find . -type f -size +50M

# If you find large model files, use Git LFS
git lfs install
git lfs track "models/*.pkl"
git add .gitattributes
git commit -m "Track large files with LFS"
git push heroku main
```

---

### Issue 9: Wrong branch name

**Cause:** Trying to push wrong branch

**Solution:**
```bash
# Check current branch
git branch

# If you're on 'master', push to Heroku's main:
git push heroku master:main

# If you're on another branch:
git push heroku your-branch-name:main

# Or checkout main first:
git checkout -b main
git push heroku main
```

---

## ✅ Complete Fresh Start (Nuclear Option)

If nothing works, start completely fresh:

```bash
# 1. Remove existing git and start over
rm -rf .git
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Fresh start"

# 4. Connect to Heroku
heroku git:remote -a sophia-nasa-ml-app

# 5. Force push
git push heroku main --force
```

---

## 🎯 Step-by-Step Debug Process

Run these commands one by one and share where it fails:

```bash
# 1. Check git status
echo "=== GIT STATUS ==="
git status

# 2. Check remotes
echo "=== GIT REMOTES ==="
git remote -v

# 3. Check current branch
echo "=== CURRENT BRANCH ==="
git branch

# 4. Check Heroku authentication
echo "=== HEROKU AUTH ==="
heroku auth:whoami

# 5. Check Heroku apps
echo "=== HEROKU APPS ==="
heroku apps

# 6. Try connecting to app
echo "=== CONNECTING TO APP ==="
heroku git:remote -a sophia-nasa-ml-app

# 7. Try pushing
echo "=== PUSHING TO HEROKU ==="
git push heroku HEAD:main --force
```

---

## 📋 What I Need to Help You

Please run this and share the output:

```bash
# Save diagnostics to file
{
  echo "=== GIT STATUS ==="
  git status
  echo ""
  echo "=== GIT REMOTES ==="
  git remote -v
  echo ""
  echo "=== GIT BRANCH ==="
  git branch
  echo ""
  echo "=== HEROKU WHOAMI ==="
  heroku auth:whoami
  echo ""
  echo "=== HEROKU APPS ==="
  heroku apps
  echo ""
  echo "=== LAST GIT LOG ==="
  git log --oneline -5
} > heroku_debug.txt

cat heroku_debug.txt
```

Share the contents of `heroku_debug.txt` so I can see exactly what's wrong.

---

## 🚀 Most Common Working Solution

This works 90% of the time:

```bash
# 1. Make sure you have changes committed
git add .
git commit -m "Deploy to Heroku"

# 2. Connect to app (even if already connected)
heroku git:remote -a sophia-nasa-ml-app

# 3. Force push current branch to Heroku's main
git push heroku HEAD:main --force

# 4. Watch logs
heroku logs --tail -a sophia-nasa-ml-app
```

---

## 📞 Alternative: Deploy from GitHub

If git push keeps failing, you can deploy from GitHub instead:

1. Push your code to GitHub
2. In Heroku Dashboard, go to your app
3. Click "Deploy" tab
4. Connect to GitHub
5. Select your repository
6. Click "Deploy Branch"

This bypasses git push entirely!

---

## ⚡ Quick Copy-Paste Fix

Just run this entire block:

```bash
cd /workspace && \
heroku git:remote -a sophia-nasa-ml-app && \
git add . && \
git commit -m "Deploy ML API" || true && \
git push heroku HEAD:main --force
```

If this doesn't work, please share the **exact error message** you're seeing!