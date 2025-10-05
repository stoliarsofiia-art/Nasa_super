# Fix CORS Error

## ❌ Current Error
```
Access to fetch at 'https://sophia-nasa-ml-app-7bc530f3ab97.herokuapp.com/analyze' 
from origin 'https://martyniukaleksei.github.io' has been blocked by CORS policy: 
Response to preflight request doesn't pass access control check: 
It does not have HTTP ok status.
```

## ✅ Solution

### Step 1: Update app.py (ALREADY DONE)

I've updated `app.py` to:
1. Add `/analyze` endpoint (your site is calling this, not `/predict`)
2. Fix CORS configuration
3. Handle OPTIONS preflight requests properly

### Step 2: Deploy Updated Code to Heroku

```bash
# Add the updated app.py
git add app.py

# Commit
git commit -m "Fix CORS and add /analyze endpoint"

# Push to Heroku
git push heroku main
```

### Step 3: Wait for Deployment (1-2 minutes)

```bash
# Watch deployment logs
heroku logs --tail
```

Look for:
```
Loading exoplanet classification model...
Model loaded successfully!
```

### Step 4: Test the Endpoint

```bash
# Test with curl
curl -X POST https://sophia-nasa-ml-app-7bc530f3ab97.herokuapp.com/analyze \
  -H "Content-Type: application/json" \
  -H "Origin: https://martyniukaleksei.github.io" \
  -d '{
    "orbital_period": 365.25,
    "transit_duration": 6.5,
    "transit_depth": 1.234,
    "snr": 12.8,
    "stellar_mass": 0.97,
    "stellar_temp": 5627,
    "stellar_magnitude": 11.7
  }'
```

Expected response:
```json
{
  "status": "success",
  "classification": "confirmed_exoplanet",
  "confidence": 0.857,
  "properties": {
    "planet_radius": 7.8106,
    "planet_temp": 43.5868,
    "semi_major_axis": 0.8522,
    "impact_parameter": 0.4699
  }
}
```

### Step 5: Update Your JavaScript (if needed)

Make sure your JavaScript sends the correct field names:

```javascript
// Your current code in form-submission.js
const response = await fetch('https://sophia-nasa-ml-app-7bc530f3ab97.herokuapp.com/analyze', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        orbital_period: parseFloat(data.orbitalPeriod),
        transit_duration: parseFloat(data.transitDuration),
        transit_depth: parseFloat(data.transitDepth),
        snr: parseFloat(data.snr),
        stellar_mass: parseFloat(data.stellarMass),
        stellar_temp: parseFloat(data.stellarTemp),
        stellar_magnitude: parseFloat(data.stellarMagnitude)
    })
});

const result = await response.json();

if (result.status === 'success') {
    // Use result.classification
    // Use result.confidence
    // Use result.properties.planet_radius
    // Use result.properties.planet_temp
    // Use result.properties.semi_major_axis
    // Use result.properties.impact_parameter
}
```

## 🔍 Troubleshooting

### Issue 1: Still Getting CORS Error After Deployment

**Check Heroku logs:**
```bash
heroku logs --tail
```

Look for errors during model loading.

**Verify app is running:**
```bash
heroku ps
```

Should show:
```
web.1: up 2023/10/05 12:00:00
```

**Restart if needed:**
```bash
heroku restart
```

### Issue 2: "It does not have HTTP ok status"

This means the server is returning an error (not 200). Common causes:

1. **Model files missing**: Make sure `models/` folder is in git
   ```bash
   git add models/
   git commit -m "Add model files"
   git push heroku main
   ```

2. **Dependencies missing**: Check if all packages installed
   ```bash
   heroku run pip list
   ```

3. **App crashed**: Check logs
   ```bash
   heroku logs --tail
   ```

### Issue 3: Heroku App Not Responding

**Check if dyno is running:**
```bash
heroku ps
```

**Scale dyno if needed:**
```bash
heroku ps:scale web=1
```

**Check app info:**
```bash
heroku apps:info
```

### Issue 4: Model Files Too Large

Heroku has a 500MB slug size limit. If your models are large:

```bash
# Check slug size
heroku apps:info

# If too large, use Git LFS
git lfs install
git lfs track "models/*.pkl"
git add .gitattributes
git commit -m "Track large files with LFS"
git push heroku main
```

## ✅ Quick Fix Checklist

- [ ] Updated `app.py` with `/analyze` endpoint
- [ ] Committed changes: `git commit -m "Fix CORS"`
- [ ] Pushed to Heroku: `git push heroku main`
- [ ] Waited for deployment (1-2 min)
- [ ] Checked logs: `heroku logs --tail`
- [ ] Verified app is running: `heroku ps`
- [ ] Tested with curl
- [ ] Tested from website

## 🎯 Expected Working Flow

1. User fills form on `https://martyniukaleksei.github.io/iaso-som-v1/`
2. JavaScript sends POST to `https://sophia-nasa-ml-app-7bc530f3ab97.herokuapp.com/analyze`
3. Browser sends OPTIONS preflight request
4. Server responds with CORS headers (200 OK)
5. Browser sends actual POST request
6. Server processes and returns results
7. JavaScript displays results

## 📝 What Changed in app.py

### Before:
```python
@app.route('/predict', methods=['POST'])
def predict():
    # ... code
```

### After:
```python
@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return '', 204  # Handle preflight
    return predict_exoplanet()

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        return '', 204  # Handle preflight
    return predict_exoplanet()

def predict_exoplanet():
    # ... actual prediction code
```

Also updated CORS configuration to be more explicit.

## 🚀 Deploy Now

```bash
git add app.py
git commit -m "Fix CORS for GitHub Pages"
git push heroku main
heroku logs --tail
```

After deployment completes, try your website again!

---

**Need more help?** Check Heroku logs: `heroku logs --tail`