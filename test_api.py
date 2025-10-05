"""
Test the Flask API locally before deploying to Heroku
"""

import requests
import json

# Test locally (run 'python app.py' first)
LOCAL_URL = 'http://localhost:5000'

# Or test on Heroku (replace with your app name)
# HEROKU_URL = 'https://your-app-name.herokuapp.com'

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f'{LOCAL_URL}/health')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_predict():
    """Test prediction endpoint"""
    print("Testing /predict endpoint...")
    
    data = {
        'orbital_period': 289.9,
        'transit_duration': 7.4,
        'transit_depth': 0.00492,
        'snr': 12,
        'stellar_mass': 0.97,
        'stellar_temp': 5627,
        'stellar_magnitude': 11.7
    }
    
    response = requests.post(
        f'{LOCAL_URL}/predict',
        headers={'Content-Type': 'application/json'},
        json=data
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}\n")
    
    if result['status'] == 'success':
        print(f"✅ Classification: {result['classification']}")
        print(f"✅ Confidence: {result['confidence']:.2%}")
        
        if 'properties' in result:
            print(f"\n✅ Planet Properties:")
            for key, value in result['properties'].items():
                print(f"   {key}: {value:.4f}")

def test_batch():
    """Test batch prediction endpoint"""
    print("\nTesting /predict/batch endpoint...")
    
    data = {
        'observations': [
            {
                'orbital_period': 289.9,
                'transit_duration': 7.4,
                'transit_depth': 0.00492,
                'snr': 12,
                'stellar_mass': 0.97,
                'stellar_temp': 5627,
                'stellar_magnitude': 11.7
            },
            {
                'orbital_period': 3.5,
                'transit_duration': 2.5,
                'transit_depth': 0.015,
                'snr': 30,
                'stellar_mass': 1.11,
                'stellar_temp': 6091,
                'stellar_magnitude': 7.7
            }
        ]
    }
    
    response = requests.post(
        f'{LOCAL_URL}/predict/batch',
        headers={'Content-Type': 'application/json'},
        json=data
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}\n")

def test_missing_field():
    """Test error handling for missing fields"""
    print("Testing error handling...")
    
    data = {
        'orbital_period': 289.9,
        # Missing other required fields
    }
    
    response = requests.post(
        f'{LOCAL_URL}/predict',
        headers={'Content-Type': 'application/json'},
        json=data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

if __name__ == '__main__':
    print("="*70)
    print("API TESTING")
    print("="*70)
    print("\nMake sure Flask app is running: python app.py\n")
    
    try:
        test_health()
        test_predict()
        test_batch()
        test_missing_field()
        
        print("="*70)
        print("✅ ALL TESTS COMPLETED")
        print("="*70)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API")
        print("Make sure Flask app is running: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")