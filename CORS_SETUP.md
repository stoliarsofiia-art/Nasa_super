# CORS Setup for GitHub Pages

## ✅ CORS Configuration Complete

Your Flask API is now configured to accept requests from:
- `https://martyniukaleksei.github.io` (your GitHub Pages site)
- `http://localhost:*` (for local testing)
- `http://127.0.0.1:*` (for local testing)

## 📝 What Changed

### In `app.py`:
```python
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://martyniukaleksei.github.io",
            "http://localhost:*",
            "http://127.0.0.1:*"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": False
    }
})
```

## 🚀 Deploy Updated API

```bash
# Commit changes
git add app.py
git commit -m "Update CORS for GitHub Pages"

# Push to Heroku
git push heroku main

# Check logs
heroku logs --tail
```

## 📱 Use in Your GitHub Pages Site

### Option 1: Fetch API (Recommended)

```javascript
// In your https://martyniukaleksei.github.io/iaso-som-v1/ site

async function classifyExoplanet(formData) {
    try {
        const response = await fetch('https://your-app-name.herokuapp.com/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                orbital_period: parseFloat(formData.orbitalPeriod),
                transit_duration: parseFloat(formData.transitDuration),
                transit_depth: parseFloat(formData.transitDepth),
                snr: parseFloat(formData.snr),
                stellar_mass: parseFloat(formData.stellarMass),
                stellar_temp: parseFloat(formData.stellarTemp),
                stellar_magnitude: parseFloat(formData.stellarMagnitude)
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        // Use the result
        console.log('Classification:', result.classification);
        console.log('Confidence:', result.confidence);
        console.log('Properties:', result.properties);
        
        return result;
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error connecting to API: ' + error.message);
    }
}

// Example usage
const data = {
    orbitalPeriod: 289.9,
    transitDuration: 7.4,
    transitDepth: 0.00492,
    snr: 12,
    stellarMass: 0.97,
    stellarTemp: 5627,
    stellarMagnitude: 11.7
};

classifyExoplanet(data).then(result => {
    if (result) {
        // Display results in your UI
        document.getElementById('classification').textContent = result.classification;
        document.getElementById('confidence').textContent = (result.confidence * 100).toFixed(2) + '%';
        
        if (result.properties) {
            document.getElementById('planet_radius').textContent = result.properties.planet_radius.toFixed(4);
            document.getElementById('planet_temp').textContent = result.properties.planet_temp.toFixed(4);
            document.getElementById('semi_major_axis').textContent = result.properties.semi_major_axis.toFixed(4);
            document.getElementById('impact_parameter').textContent = result.properties.impact_parameter.toFixed(4);
        }
    }
});
```

### Option 2: Axios (If you use Axios)

```javascript
import axios from 'axios';

const API_URL = 'https://your-app-name.herokuapp.com/predict';

async function classifyExoplanet(data) {
    try {
        const response = await axios.post(API_URL, {
            orbital_period: parseFloat(data.orbitalPeriod),
            transit_duration: parseFloat(data.transitDuration),
            transit_depth: parseFloat(data.transitDepth),
            snr: parseFloat(data.snr),
            stellar_mass: parseFloat(data.stellarMass),
            stellar_temp: parseFloat(data.stellarTemp),
            stellar_magnitude: parseFloat(data.stellarMagnitude)
        });
        
        return response.data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}
```

### Option 3: jQuery (If you use jQuery)

```javascript
$.ajax({
    url: 'https://your-app-name.herokuapp.com/predict',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({
        orbital_period: 289.9,
        transit_duration: 7.4,
        transit_depth: 0.00492,
        snr: 12,
        stellar_mass: 0.97,
        stellar_temp: 5627,
        stellar_magnitude: 11.7
    }),
    success: function(result) {
        console.log('Success:', result);
        // Handle the result
    },
    error: function(xhr, status, error) {
        console.error('Error:', error);
    }
});
```

## 🧪 Test CORS Configuration

### Method 1: Use the Test HTML File

1. Open `test_cors.html` in your browser
2. Update the API URL to your Heroku app
3. Click "Classify Exoplanet"
4. Check browser console for any CORS errors

### Method 2: Browser Console Test

Open your GitHub Pages site and run this in the browser console:

```javascript
fetch('https://your-app-name.herokuapp.com/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        orbital_period: 289.9,
        transit_duration: 7.4,
        transit_depth: 0.00492,
        snr: 12,
        stellar_mass: 0.97,
        stellar_temp: 5627,
        stellar_magnitude: 11.7
    })
})
.then(response => response.json())
.then(data => console.log('Success:', data))
.catch(error => console.error('Error:', error));
```

### Method 3: curl Test

```bash
curl -X POST https://your-app-name.herokuapp.com/predict \
  -H "Content-Type: application/json" \
  -H "Origin: https://martyniukaleksei.github.io" \
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

## 🔍 Troubleshooting CORS Issues

### Issue 1: "No 'Access-Control-Allow-Origin' header"

**Solution:** Make sure you've deployed the updated `app.py` to Heroku:
```bash
git push heroku main
heroku restart
```

### Issue 2: "Preflight request failed"

**Check that:**
1. Your Heroku app is running: `heroku ps`
2. CORS is configured for OPTIONS method (already done)
3. Check Heroku logs: `heroku logs --tail`

### Issue 3: "Network error" or "Failed to fetch"

**Possible causes:**
1. Heroku app is sleeping (free tier) - first request takes longer
2. Wrong API URL - check your Heroku app name
3. Heroku app crashed - check `heroku logs`

### Issue 4: CORS working locally but not on GitHub Pages

**Check:**
1. API URL uses `https://` (not `http://`)
2. GitHub Pages site uses `https://` (not `http://`)
3. Origin is exactly: `https://martyniukaleksei.github.io`

## 📋 Complete Integration Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>Exoplanet Classifier</title>
</head>
<body>
    <h1>Exoplanet Classification</h1>
    
    <form id="exoplanetForm">
        <input type="number" name="orbital_period" placeholder="Orbital Period (days)" required>
        <input type="number" name="transit_duration" placeholder="Transit Duration (hours)" required>
        <input type="number" name="transit_depth" placeholder="Transit Depth" required>
        <input type="number" name="snr" placeholder="SNR" required>
        <input type="number" name="stellar_mass" placeholder="Stellar Mass" required>
        <input type="number" name="stellar_temp" placeholder="Stellar Temp (K)" required>
        <input type="number" name="stellar_magnitude" placeholder="Stellar Magnitude" required>
        <button type="submit">Classify</button>
    </form>
    
    <div id="results" style="display:none;">
        <h2>Results</h2>
        <p><strong>Classification:</strong> <span id="classification"></span></p>
        <p><strong>Confidence:</strong> <span id="confidence"></span></p>
        <div id="properties" style="display:none;">
            <h3>Planet Properties</h3>
            <p>Radius: <span id="planet_radius"></span> Earth radii</p>
            <p>Temperature: <span id="planet_temp"></span> K</p>
            <p>Semi-major Axis: <span id="semi_major_axis"></span> AU</p>
            <p>Impact Parameter: <span id="impact_parameter"></span></p>
        </div>
    </div>
    
    <script>
        const API_URL = 'https://your-app-name.herokuapp.com/predict';
        
        document.getElementById('exoplanetForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = parseFloat(value);
            });
            
            try {
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const result = await response.json();
                
                // Display results
                document.getElementById('results').style.display = 'block';
                document.getElementById('classification').textContent = result.classification;
                document.getElementById('confidence').textContent = (result.confidence * 100).toFixed(2) + '%';
                
                if (result.properties) {
                    document.getElementById('properties').style.display = 'block';
                    document.getElementById('planet_radius').textContent = result.properties.planet_radius.toFixed(4);
                    document.getElementById('planet_temp').textContent = result.properties.planet_temp.toFixed(2);
                    document.getElementById('semi_major_axis').textContent = result.properties.semi_major_axis.toFixed(4);
                    document.getElementById('impact_parameter').textContent = result.properties.impact_parameter.toFixed(4);
                }
                
            } catch (error) {
                console.error('Error:', error);
                alert('Error: ' + error.message);
            }
        });
    </script>
</body>
</html>
```

## 🎯 Quick Checklist

- [ ] Updated `app.py` with CORS configuration
- [ ] Committed and pushed to Heroku: `git push heroku main`
- [ ] App is running: `heroku ps`
- [ ] Tested with curl or Postman
- [ ] Tested from GitHub Pages site
- [ ] No CORS errors in browser console
- [ ] API returns expected results

## 📞 Need Help?

Check Heroku logs:
```bash
heroku logs --tail
```

Restart app:
```bash
heroku restart
```

Check app status:
```bash
heroku ps
```

---

**Your API URL:** `https://your-app-name.herokuapp.com/predict`

**Allowed Origin:** `https://martyniukaleksei.github.io`

Now anyone visiting your GitHub Pages site can make fetch/POST requests to your API! 🚀