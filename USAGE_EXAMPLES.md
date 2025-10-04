# Usage Examples for Exoplanet Classification System

## Quick Start

### 1. Run the Quick Demo

```bash
python3 quick_demo.py
```

This will train models (if needed) and show example predictions for different types of celestial objects.

### 2. Interactive Terminal Interface

```bash
python3 exoplanet_classifier.py
```

Follow the prompts to input observation parameters and get real-time classifications.

### 3. Command-Line Single Prediction

```bash
python3 exoplanet_classifier.py predict 10.5 2.8 0.001 25 1.1 5800 12.5
```

**Parameters (in order):**
1. Orbital period (days)
2. Transit duration (hours)
3. Transit depth (0-1, relative)
4. SNR
5. Stellar mass (solar masses)
6. Stellar temperature (K)
7. Stellar magnitude

## Example Scenarios

### Hot Jupiter Detection

**Characteristics:** Short period, deep transit, high SNR

```bash
python3 exoplanet_classifier.py predict 3.5 2.5 0.01 30 1.0 5800 11.5
```

**Expected Output:**
- Classification: CONFIRMED_EXOPLANET
- High confidence (>90%)
- Large radius (>10 Earth radii)
- High temperature (>1000K)

### Earth-like Planet (Habitable Zone)

**Characteristics:** Medium period, shallow transit, moderate SNR

```bash
python3 exoplanet_classifier.py predict 365 3.0 0.0001 15 1.0 5778 12.0
```

**Expected Output:**
- Classification: CONFIRMED_EXOPLANET or PLANETARY_CANDIDATE
- Moderate confidence (70-85%)
- Earth-sized radius (~1 Earth radius)
- Moderate temperature (~200-300K)

### False Positive (Eclipsing Binary)

**Characteristics:** Very deep transit, long duration

```bash
python3 exoplanet_classifier.py predict 2.1 5.5 0.15 12 1.2 6000 13.8
```

**Expected Output:**
- Classification: FALSE_POSITIVE
- High confidence
- No planet properties predicted

### Planetary Candidate (Uncertain)

**Characteristics:** Low SNR, distant from Earth

```bash
python3 exoplanet_classifier.py predict 45.2 4.1 0.0005 8.5 0.9 5200 14.2
```

**Expected Output:**
- Classification: PLANETARY_CANDIDATE
- Lower confidence (60-80%)
- Higher uncertainty metric
- Tentative planet properties

## Python API Examples

### Basic Prediction

```python
from exoplanet_classifier import ExoplanetClassificationSystem

# Initialize system
system = ExoplanetClassificationSystem()
system.load_models()  # or system.train() if models don't exist

# Make prediction
observation = {
    'orbital_period': 10.5,
    'transit_duration': 2.8,
    'transit_depth': 0.001,
    'snr': 25.0,
    'stellar_mass': 1.1,
    'stellar_temp': 5800.0,
    'stellar_magnitude': 12.5
}

result = system.predict(observation)

print(f"Classification: {result['classification']}")
print(f"Confidence: {result['confidence']:.2%}")

if 'properties' in result:
    print(f"Planet Radius: {result['properties']['planet_radius']:.2f} Earth radii")
```

### Batch Processing

```python
import pandas as pd
from exoplanet_classifier import ExoplanetClassificationSystem

# Load system
system = ExoplanetClassificationSystem()
system.load_models()

# Batch of observations
observations = pd.DataFrame([
    {
        'orbital_period': 3.5,
        'transit_duration': 2.5,
        'transit_depth': 0.01,
        'snr': 30.0,
        'stellar_mass': 1.0,
        'stellar_temp': 5800.0,
        'stellar_magnitude': 11.5
    },
    {
        'orbital_period': 45.2,
        'transit_duration': 4.1,
        'transit_depth': 0.0005,
        'snr': 8.5,
        'stellar_mass': 0.9,
        'stellar_temp': 5200.0,
        'stellar_magnitude': 14.2
    }
])

# Process all observations
results = []
for idx, obs in observations.iterrows():
    result = system.predict(obs.to_dict())
    results.append({
        'id': idx,
        'classification': result['classification'],
        'confidence': result['confidence']
    })

results_df = pd.DataFrame(results)
print(results_df)
```

### With Uncertainty Analysis

```python
from exoplanet_classifier import ExoplanetClassificationSystem

system = ExoplanetClassificationSystem()
system.load_models()

observation = {...}  # Your observation parameters

result = system.predict(observation, return_uncertainty=True)

print(f"Classification: {result['classification']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Uncertainty: {result['uncertainty']:.4f}")
print(f"Model Agreement: {result['model_agreement']:.2%}")

print("\nClass Probabilities:")
for cls, prob in result['class_probabilities'].items():
    print(f"  {cls}: {prob:.2%}")

if 'properties' in result:
    props = result['properties']
    uncerts = result['property_uncertainties']
    
    print(f"\nPlanet Properties (with uncertainties):")
    print(f"  Radius: {props['planet_radius']:.2f} ± {uncerts['planet_radius']:.2f} R⊕")
    print(f"  Temperature: {props['planet_temp']:.0f} ± {uncerts['planet_temp']:.0f} K")
    print(f"  Semi-major axis: {props['semi_major_axis']:.4f} ± {uncerts['semi_major_axis']:.4f} AU")
```

### Model Training with Custom Data

```python
import pandas as pd
from exoplanet_classifier import ExoplanetClassificationSystem

# Load your custom dataset
# Must have columns: orbital_period, transit_duration, transit_depth,
# snr, stellar_mass, stellar_temp, stellar_magnitude, classification
custom_data = pd.read_csv('my_exoplanet_data.csv')

# Initialize and train
system = ExoplanetClassificationSystem()
system.train(df=custom_data, save_models=True)

# Models are now trained and saved to 'models/' directory
```

### Model Validation

```python
from model_validation import ModelValidator, validate_system

# Run comprehensive validation
results = validate_system()

# Access validation metrics
print(f"Cross-validation accuracy: {results['cv_mean']:.4f}")
print(f"Expected calibration error: {results['ece']:.4f}")
print(f"Error rate: {results['error_rate']:.2%}")
```

## Understanding the Output

### Classification Types

1. **confirmed_exoplanet**: High-confidence planet detection
   - Strong signal
   - Consistent with planetary physics
   - Low false positive probability

2. **planetary_candidate**: Likely planet, needs confirmation
   - Moderate signal strength
   - Some uncertainty in parameters
   - Requires follow-up observations

3. **false_positive**: Not a planet
   - Likely eclipsing binary star system
   - Instrumental artifact
   - Background contamination

### Confidence Metrics

- **Confidence (0-1)**: Probability assigned to predicted class
  - >0.90: Very confident
  - 0.70-0.90: Confident
  - <0.70: Uncertain

- **Uncertainty (0-1)**: Entropy of probability distribution
  - <0.2: Low uncertainty
  - 0.2-0.5: Moderate uncertainty
  - >0.5: High uncertainty

- **Model Agreement (0-1)**: Fraction of models agreeing
  - >0.80: Strong agreement
  - 0.60-0.80: Moderate agreement
  - <0.60: Disagreement (be cautious)

### Planet Properties

When classification is "confirmed_exoplanet" or "planetary_candidate":

- **Planet Radius** (Earth radii = R⊕)
  - <0.5 R⊕: Sub-Earth
  - 0.5-2 R⊕: Earth to Super-Earth
  - 2-6 R⊕: Neptune-like
  - >6 R⊕: Jupiter-like

- **Planet Temperature** (Kelvin)
  - <200K: Very cold
  - 200-400K: Temperate (potentially habitable)
  - 400-1000K: Hot
  - >1000K: Very hot (Hot Jupiter)

- **Semi-major Axis** (AU)
  - <0.1 AU: Very close orbit
  - 0.1-1 AU: Inner system
  - 1-5 AU: Outer system
  - >5 AU: Far orbit

- **Impact Parameter** (0-1)
  - 0: Central transit (planet crosses center of star)
  - 0-0.7: Normal transit
  - 0.7-1: Grazing transit (planet barely crosses star)

## Tips for Best Results

1. **Data Quality**: Higher SNR (>10) gives more reliable results
2. **Stellar Parameters**: Accurate stellar mass and temperature are crucial
3. **Transit Depth**: Very deep transits (>0.05) are often false positives
4. **Multiple Observations**: If possible, average results from multiple transits
5. **Uncertainty**: Pay attention to uncertainty metrics; high uncertainty suggests need for more data

## Troubleshooting

### Low Confidence Predictions

**Problem**: System returns low confidence (<70%)

**Solutions:**
- Check if SNR is sufficient (>7 recommended)
- Verify stellar parameters are reasonable
- Consider classifying as "planetary_candidate" and collect more data

### Unrealistic Planet Properties

**Problem**: Predicted radius or temperature seems wrong

**Possible Causes:**
- Incorrect stellar parameters
- Very low SNR
- False positive misclassified as planet

**Solution:** Review input parameters, especially stellar mass and temperature

### Models Not Found Error

**Problem**: "Models not found in models/"

**Solution:**
```bash
python3 exoplanet_classifier.py train
```

This will train and save models (takes 5-10 minutes).

## Performance Optimization

### For Faster Predictions

If XGBoost and LightGBM are not installed, the system falls back to basic models (faster but slightly less accurate).

### For Better Accuracy

Install all dependencies including XGBoost and LightGBM:
```bash
pip install xgboost lightgbm
```

Then retrain models:
```bash
python3 exoplanet_classifier.py train
```

## Next Steps

1. Try the quick demo: `python3 quick_demo.py`
2. Run interactive mode: `python3 exoplanet_classifier.py`
3. Experiment with different parameters
4. Check `README.md` for detailed documentation
5. Run validation: `python3 model_validation.py`

## Support

For issues or questions:
1. Check the README.md
2. Review this usage guide
3. Examine example predictions in quick_demo.py
4. Contact the maintainers

---

**Happy Exoplanet Hunting! 🔭🪐**
