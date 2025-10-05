# Heroku Deployment Guide

## Step 1: Prepare Your Files

Make sure you have these files in your project:
- `app.py` - Flask API server
- `Procfile` - Tells Heroku how to run your app
- `runtime.txt` - Specifies Python version
- `requirements.txt` - Python dependencies (updated with Flask)
- `models/` folder - Your trained ML models
- All your ML code files

## Step 2: Install Heroku CLI

```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
# Or install via:
curl https://cli-assets.heroku.com/install.sh | sh
```

## Step 3: Login to Heroku

```bash
heroku login
```

## Step 4: Create Heroku App

```bash
# Create new app (replace 'your-app-name' with your desired name)
heroku create your-exoplanet-classifier

# Or connect to existing app
heroku git:remote -a your-existing-app-name
```

## Step 5: Deploy to Heroku

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Deploy exoplanet classifier API"

# Push to Heroku
git push heroku main
# Or if you're on master branch:
git push heroku master
```

## Step 6: Scale Dynos

```bash
heroku ps:scale web=1
```

## Step 7: Check Logs

```bash
heroku logs --tail
```

## Step 8: Test Your API

Your API will be available at: `https://your-app-name.herokuapp.com`

---

## API Endpoints

### 1. Health Check
```bash
curl https://your-app-name.herokuapp.com/health
```

### 2. Make Prediction

**From Command Line:**
```bash
curl -X POST https://your-app-name.herokuapp.com/predict \
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

**From JavaScript (Your Website):**
```javascript
// Make prediction request
async function predictExoplanet(data) {
    const response = await fetch('https://your-app-name.herokuapp.com/predict', {
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
        console.log('Classification:', result.classification);
        console.log('Confidence:', result.confidence);
        
        if (result.properties) {
            console.log('Planet Properties:', result.properties);
            // Display: planet_radius, planet_temp, semi_major_axis, impact_parameter
        }
    }
    
    return result;
}

// Example usage
const inputData = {
    orbitalPeriod: 289.9,
    transitDuration: 7.4,
    transitDepth: 0.00492,
    snr: 12,
    stellarMass: 0.97,
    stellarTemp: 5627,
    stellarMagnitude: 11.7
};

predictExoplanet(inputData).then(result => {
    console.log('Result:', result);
});
```

**From Python:**
```python
import requests

url = 'https://your-app-name.herokuapp.com/predict'

data = {
    'orbital_period': 289.9,
    'transit_duration': 7.4,
    'transit_depth': 0.00492,
    'snr': 12,
    'stellar_mass': 0.97,
    'stellar_temp': 5627,
    'stellar_magnitude': 11.7
}

response = requests.post(url, json=data)
result = response.json()

print('Classification:', result['classification'])
print('Confidence:', result['confidence'])

if 'properties' in result:
    print('Planet Properties:')
    print('  Radius:', result['properties']['planet_radius'])
    print('  Temperature:', result['properties']['planet_temp'])
    print('  Semi-major axis:', result['properties']['semi_major_axis'])
    print('  Impact parameter:', result['properties']['impact_parameter'])
```

---

## Response Format

**Successful Prediction:**
```json
{
    "status": "success",
    "classification": "confirmed_exoplanet",
    "confidence": 0.857,
    "class_probabilities": {
        "confirmed_exoplanet": 0.857,
        "false_positive": 0.0009,
        "planetary_candidate": 0.1421
    },
    "properties": {
        "planet_radius": 7.8106,
        "planet_temp": 43.5868,
        "semi_major_axis": 0.8522,
        "impact_parameter": 0.4699
    },
    "uncertainty": 0.4123
}
```

**Error Response:**
```json
{
    "status": "error",
    "error": "Missing required fields: snr, stellar_mass"
}
```

---

## Important Notes

### 1. Model Files Size
Heroku has a 500MB slug size limit. Your models should be included in the deployment.

If models are too large:
```bash
# Use Git LFS for large files
git lfs install
git lfs track "models/*.pkl"
git add .gitattributes
git commit -m "Track models with LFS"
```

### 2. Environment Variables
```bash
# Set environment variables if needed
heroku config:set MODEL_PATH=models/
```

### 3. Free Dyno Limitations
- Sleeps after 30 minutes of inactivity
- 550 free dyno hours per month
- First request after sleep takes longer

### 4. Upgrade to Paid Dyno (if needed)
```bash
heroku ps:type hobby
# Or
heroku ps:type standard-1x
```

---

## Troubleshooting

### Check Logs
```bash
heroku logs --tail
```

### Restart Dyno
```bash
heroku restart
```

### Check Dyno Status
```bash
heroku ps
```

### Run One-off Commands
```bash
heroku run python
heroku run bash
```

### Check Build Log
```bash
heroku builds:info
```

---

## Testing Locally Before Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask app locally
python app.py

# Test in another terminal
curl -X POST http://localhost:5000/predict \
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

---

## HTML Form Example (For Your Website)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Exoplanet Classifier</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; }
        input { width: 100%; padding: 8px; margin: 5px 0; }
        button { background: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🔭 Exoplanet Classifier</h1>
    
    <form id="predictForm">
        <label>Orbital Period (days):</label>
        <input type="number" step="any" name="orbital_period" required>
        
        <label>Transit Duration (hours):</label>
        <input type="number" step="any" name="transit_duration" required>
        
        <label>Transit Depth (relative):</label>
        <input type="number" step="any" name="transit_depth" required>
        
        <label>SNR:</label>
        <input type="number" step="any" name="snr" required>
        
        <label>Stellar Mass (solar masses):</label>
        <input type="number" step="any" name="stellar_mass" required>
        
        <label>Stellar Temperature (K):</label>
        <input type="number" step="any" name="stellar_temp" required>
        
        <label>Stellar Magnitude:</label>
        <input type="number" step="any" name="stellar_magnitude" required>
        
        <button type="submit">Classify</button>
    </form>
    
    <div id="result" class="result" style="display:none;"></div>
    
    <script>
        document.getElementById('predictForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = parseFloat(value);
            });
            
            document.getElementById('result').innerHTML = 'Analyzing...';
            document.getElementById('result').style.display = 'block';
            
            try {
                const response = await fetch('https://your-app-name.herokuapp.com/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    let html = `
                        <h2>Classification: ${result.classification.toUpperCase()}</h2>
                        <p><strong>Confidence:</strong> ${(result.confidence * 100).toFixed(2)}%</p>
                    `;
                    
                    if (result.properties) {
                        html += `
                            <h3>Planet Properties:</h3>
                            <p><strong>Planet Radius:</strong> ${result.properties.planet_radius.toFixed(4)} Earth radii</p>
                            <p><strong>Planet Temperature:</strong> ${result.properties.planet_temp.toFixed(4)} K</p>
                            <p><strong>Semi-major Axis:</strong> ${result.properties.semi_major_axis.toFixed(4)} AU</p>
                            <p><strong>Impact Parameter:</strong> ${result.properties.impact_parameter.toFixed(4)}</p>
                        `;
                    }
                    
                    document.getElementById('result').innerHTML = html;
                } else {
                    document.getElementById('result').innerHTML = `<p style="color:red;">Error: ${result.error}</p>`;
                }
            } catch (error) {
                document.getElementById('result').innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
            }
        });
    </script>
</body>
</html>
```

---

## Summary

1. ✅ Create `app.py` - Flask API server
2. ✅ Create `Procfile` - Heroku process file
3. ✅ Update `requirements.txt` - Add Flask, gunicorn
4. ✅ Deploy to Heroku: `git push heroku main`
5. ✅ Test API endpoint
6. ✅ Integrate with your website using JavaScript fetch

Your API URL: `https://your-app-name.herokuapp.com/predict`

The ML model stays unchanged - just wrapped in a web API! 🚀