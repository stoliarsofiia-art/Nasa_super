# URGENT FIX - App Not Running on Heroku

## 🔴 Current Errors

1. **404** - Endpoint doesn't exist (app not deployed or crashed)
2. **503** - Service unavailable (app not running)

## ✅ Step-by-Step Fix

### Step 1: Check if App Exists

```bash
heroku apps:info -a sophia-nasa-ml-app
```

If this fails, you need to connect to your app:
```bash
heroku git:remote -a sophia-nasa-ml-app
```

### Step 2: Deploy the Fixed Code

```bash
# Make sure you're in the project directory
cd /workspace

# Add all files
git add .

# Commit
git commit -m "Add ML model and API endpoints"

# Push to Heroku
git push heroku HEAD:main -f
```

The `-f` (force) flag ensures it pushes even if there are conflicts.

### Step 3: Check Deployment Logs

```bash
heroku logs --tail -a sophia-nasa-ml-app
```

Watch for:
- ✅ "Loading exoplanet classification model..."
- ✅ "Model loaded successfully!"
- ❌ Any errors about missing files

### Step 4: Ensure Models are Deployed

**Important:** Heroku might not include your `models/` folder if it's in `.gitignore`

```bash
# Check if models folder is tracked
git ls-files | grep models

# If nothing shows up, add models
git add -f models/
git commit -m "Add model files"
git push heroku HEAD:main
```

### Step 5: Scale the Dyno

```bash
heroku ps:scale web=1 -a sophia-nasa-ml-app
```

### Step 6: Check Status

```bash
heroku ps -a sophia-nasa-ml-app
```

Should show:
```
web.1: up 2023/10/05 12:00:00 (~ 1m ago)
```

If it shows "crashed", check logs:
```bash
heroku logs --tail -a sophia-nasa-ml-app
```

---

## 🚨 Common Issues

### Issue 1: Models Folder Not Deployed

**Symptoms:** Logs show `FileNotFoundError` or `models not found`

**Fix:**
```bash
# Force add models folder
git add -f models/
git commit -m "Add model files"
git push heroku HEAD:main
```

### Issue 2: App Slug Too Large (>500MB)

**Symptoms:** "Compiled slug size exceeds the maximum" error

**Fix:** Models are too large. Options:
1. Use Git LFS
2. Load models from cloud storage (S3, Google Cloud)
3. Use smaller models

### Issue 3: Buildpack Not Detected

**Symptoms:** "Failed to detect app"

**Fix:**
```bash
heroku buildpacks:set heroku/python -a sophia-nasa-ml-app
git commit --allow-empty -m "Trigger rebuild"
git push heroku HEAD:main
```

### Issue 4: Out of Memory

**Symptoms:** "Error R14 (Memory quota exceeded)"

**Fix:** Upgrade dyno or reduce model size
```bash
heroku ps:type hobby -a sophia-nasa-ml-app
```

---

## 🔍 Debug Commands

### Check what's deployed:
```bash
heroku run ls -la -a sophia-nasa-ml-app
heroku run ls -la models/ -a sophia-nasa-ml-app
```

### Check if Python packages are installed:
```bash
heroku run pip list -a sophia-nasa-ml-app
```

### Access bash:
```bash
heroku run bash -a sophia-nasa-ml-app
# Then inside bash:
ls -la
ls -la models/
python -c "from exoplanet_classifier import ExoplanetClassificationSystem"
```

### Test loading model:
```bash
heroku run python -c "from exoplanet_classifier import ExoplanetClassificationSystem; s = ExoplanetClassificationSystem(); s.load_models()" -a sophia-nasa-ml-app
```

---

## 📋 Complete Deployment Checklist

```bash
# 1. Connect to your Heroku app
heroku git:remote -a sophia-nasa-ml-app

# 2. Check what files will be deployed
git ls-files

# 3. Make sure models are included
git add -f models/

# 4. Add all Python files
git add *.py

# 5. Add config files
git add Procfile requirements.txt runtime.txt

# 6. Commit everything
git commit -m "Deploy complete ML API"

# 7. Push to Heroku (force if needed)
git push heroku HEAD:main -f

# 8. Scale dyno
heroku ps:scale web=1 -a sophia-nasa-ml-app

# 9. Watch logs
heroku logs --tail -a sophia-nasa-ml-app

# 10. Check status
heroku ps -a sophia-nasa-ml-app
```

---

## ✅ When It's Working

You should see in logs:
```
Loading exoplanet classification model...
Models loaded from models/
Model loaded successfully!
State changed from starting to up
```

And `heroku ps` should show:
```
web.1: up 2023/10/05 12:00:00
```

Then test:
```bash
curl https://sophia-nasa-ml-app-7bc530f3ab97.herokuapp.com/health
```

Should return:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

---

## 🎯 Quick Fix (All-in-One)

```bash
# Run all these commands:
cd /workspace
heroku git:remote -a sophia-nasa-ml-app
git add -f models/
git add *.py Procfile requirements.txt runtime.txt
git commit -m "Deploy ML API with models"
git push heroku HEAD:main -f
heroku ps:scale web=1 -a sophia-nasa-ml-app
heroku logs --tail -a sophia-nasa-ml-app
```

Watch the logs. When you see "Model loaded successfully!", press Ctrl+C and try your website!

---

## 📞 Still Not Working?

Share the output of:
```bash
heroku logs --tail -a sophia-nasa-ml-app
```

Look for error messages in red.