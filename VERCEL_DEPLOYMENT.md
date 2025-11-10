# Vercel Deployment Guide for Exoplanet Classification API

## 🚀 Quick Start

This guide will help you deploy your Exoplanet Classification API to Vercel for free.

## 📋 Prerequisites

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Vercel Account** - Sign up at [vercel.com](https://vercel.com) (free tier available)
3. **Pre-trained Models** - Ensure your `models/` directory contains:
   - `preprocessor.pkl`
   - `feature_engineer.pkl`
   - `classifier.pkl`
   - `regressors.pkl`

## 🔧 Configuration Files

The following files have been created for Vercel deployment:

### 1. `vercel.json`
Configures the Vercel build and routing:
- Uses Python 3.12 runtime
- Routes all requests to `api/index.py`
- Sets maximum Lambda size to 250MB

### 2. `.vercelignore`
Excludes unnecessary files from deployment:
- Training data (CSV files)
- Documentation (MD files except README)
- Test files
- Scripts and tools
- Python cache

### 3. `api/index.py`
Serverless function entry point:
- Flask app configured for Vercel
- Lazy loading of ML models
- CORS enabled for GitHub Pages

### 4. `requirements.txt` (Optimized)
Minimal dependencies to stay under 250MB:
- Removed: matplotlib, seaborn, gunicorn
- Kept: flask, flask-cors, numpy, pandas, scikit-learn, joblib

## 📦 Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Configure for Vercel deployment"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Click "Import Project"
   - Select your GitHub repository
   - Click "Import"

3. **Configure Project**
   - Framework Preset: **Other**
   - Root Directory: `./` (leave as default)
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements.txt`

4. **Deploy**
   - Click "Deploy"
   - Wait 2-5 minutes for deployment
   - Your API will be available at: `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```
   
   Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N**
   - What's your project's name? Enter a name
   - In which directory is your code located? **./**
   - Want to override the settings? **N**

4. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## 🧪 Testing Your Deployment

### 1. Health Check
```bash
curl https://your-project.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 2. Make a Prediction
```bash
curl -X POST https://your-project.vercel.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "orbital_period": 289.9,
    "transit_duration": 7.4,
    "transit_depth": 0.00492,
    "snr": 12,
    "stellar_mass": 0.97,
    "stellar_temp": 5627,
    "stellar_magnitude": 11.7
  }'
```

## 🔍 Troubleshooting

### Issue: "Serverless Function has exceeded 250 MB"

**Solutions:**

1. **Reduce Model Size**
   - Compress your model files
   - Use model quantization
   - Consider using lighter ML libraries

2. **Use External Storage**
   Store models externally and download at runtime:
   
   ```python
   import requests
   import joblib
   import os
   
   def load_model_from_url(url, filename):
       if not os.path.exists(filename):
           response = requests.get(url)
           with open(filename, 'wb') as f:
               f.write(response.content)
       return joblib.load(filename)
   
   # In your api/index.py
   MODEL_URL = "https://your-storage.com/models/classifier.pkl"
   model = load_model_from_url(MODEL_URL, '/tmp/classifier.pkl')
   ```

3. **Split into Multiple Functions**
   Create separate endpoints for different models

4. **Upgrade to Vercel Pro**
   - Pro plan allows up to 50MB per function
   - Supports larger deployments

### Issue: "Module not found"

**Solution:** Ensure all Python files are in the root directory or properly imported:

```python
# In api/index.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### Issue: "Models not loading"

**Solution:** Check that `models/` directory is committed to Git:

```bash
git add models/*.pkl
git commit -m "Add trained models"
git push
```

### Issue: CORS errors

**Solution:** Update CORS origins in `api/index.py`:

```python
CORS(app, 
     origins=[
         "https://your-github-pages-site.github.io",
         "http://localhost:*"
     ])
```

## 📊 API Endpoints

Once deployed, your API will have these endpoints:

- `GET /` - Home page with API info
- `GET /api/health` - Health check
- `POST /api/predict` - Single prediction
- `POST /api/analyze` - Analyze exoplanet data (alias for predict)
- `POST /api/predict/batch` - Batch predictions

## 🌐 Updating Your Frontend

Update your GitHub Pages frontend to use the new Vercel URL:

```javascript
// In your frontend JavaScript
const API_URL = 'https://your-project.vercel.app/api/predict';

async function classifyExoplanet(data) {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  });
  return await response.json();
}
```

## 💰 Cost Considerations

**Vercel Free Tier Includes:**
- 100 GB bandwidth per month
- 100 hours of serverless function execution
- Automatic HTTPS
- Global CDN
- Perfect for hobby projects and demos

**When to Upgrade:**
- High traffic (>100GB/month)
- Need larger function sizes
- Require team collaboration features

## 🔐 Environment Variables

If you need to add environment variables:

1. **Via Dashboard:**
   - Go to your project settings
   - Navigate to "Environment Variables"
   - Add variables

2. **Via CLI:**
   ```bash
   vercel env add VARIABLE_NAME
   ```

## 📝 Best Practices

1. **Keep Dependencies Minimal** - Only include what you need
2. **Use .vercelignore** - Exclude unnecessary files
3. **Lazy Load Models** - Load models only when needed
4. **Cache Models** - Use global variables to cache loaded models
5. **Monitor Usage** - Check Vercel dashboard for usage stats
6. **Set Up Monitoring** - Use Vercel Analytics for insights

## 🆘 Getting Help

- **Vercel Documentation:** [vercel.com/docs](https://vercel.com/docs)
- **Vercel Community:** [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
- **Python on Vercel:** [vercel.com/docs/functions/serverless-functions/runtimes/python](https://vercel.com/docs/functions/serverless-functions/runtimes/python)

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `models/` directory contains all .pkl files
- [ ] `vercel.json` configured
- [ ] `.vercelignore` created
- [ ] `api/index.py` created
- [ ] `requirements.txt` optimized
- [ ] Vercel account created
- [ ] Project imported to Vercel
- [ ] Deployment successful
- [ ] Health check passes
- [ ] Test prediction works
- [ ] Frontend updated with new API URL
- [ ] CORS configured correctly

## 🎉 Success!

Your Exoplanet Classification API is now live on Vercel!

Share your API: `https://your-project.vercel.app`
