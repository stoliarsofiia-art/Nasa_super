#!/usr/bin/env python3
"""
Quick demonstration of the exoplanet classification system.
Shows example predictions for different types of celestial objects.
"""

from exoplanet_classifier import ExoplanetClassificationSystem
import pandas as pd

print("="*70)
print("EXOPLANET CLASSIFICATION SYSTEM - QUICK DEMO")
print("="*70)

# Initialize and train system (or load if exists)
print("\nInitializing system...")
system = ExoplanetClassificationSystem()

if not system.load_models():
    print("Training models (this will take a few minutes)...")
    system.train()
else:
    print("Loaded pre-trained models")

print("\n" + "="*70)
print("EXAMPLE PREDICTIONS")
print("="*70)

# Example 1: Likely confirmed exoplanet (Earth-like)
print("\n" + "-"*70)
print("Example 1: Hot Jupiter-like Planet")
print("-"*70)
example1 = {
    'orbital_period': 3.5,           # Short period
    'transit_duration': 2.5,         # Typical transit
    'transit_depth': 0.01,           # Deep transit (large planet)
    'snr': 30.0,                     # High SNR
    'stellar_mass': 1.0,             # Sun-like star
    'stellar_temp': 5800.0,          # Sun-like temperature
    'stellar_magnitude': 11.5        # Bright star
}

result1 = system.predict(example1)
print(f"\nClassification: {result1['classification'].upper()}")
print(f"Confidence: {result1['confidence']:.2%}")
print(f"Uncertainty: {result1['uncertainty']:.4f}")

if 'properties' in result1:
    props = result1['properties']
    print(f"\nPredicted Properties:")
    print(f"  Radius: {props['planet_radius']:.2f} Earth radii")
    print(f"  Temperature: {props['planet_temp']:.0f} K")
    print(f"  Orbital Distance: {props['semi_major_axis']:.4f} AU")
    print(f"  Impact Parameter: {props['impact_parameter']:.3f}")

# Example 2: Planetary candidate (weaker signal)
print("\n" + "-"*70)
print("Example 2: Planetary Candidate (Lower SNR)")
print("-"*70)
example2 = {
    'orbital_period': 45.2,
    'transit_duration': 4.1,
    'transit_depth': 0.0005,
    'snr': 8.5,                      # Lower SNR
    'stellar_mass': 0.9,
    'stellar_temp': 5200.0,
    'stellar_magnitude': 14.2
}

result2 = system.predict(example2)
print(f"\nClassification: {result2['classification'].upper()}")
print(f"Confidence: {result2['confidence']:.2%}")
print(f"Uncertainty: {result2['uncertainty']:.4f}")

if 'properties' in result2:
    props = result2['properties']
    print(f"\nPredicted Properties:")
    print(f"  Radius: {props['planet_radius']:.2f} Earth radii")
    print(f"  Temperature: {props['planet_temp']:.0f} K")

# Example 3: False positive (eclipsing binary characteristics)
print("\n" + "-"*70)
print("Example 3: Likely False Positive (Eclipsing Binary)")
print("-"*70)
example3 = {
    'orbital_period': 2.1,
    'transit_duration': 5.5,         # Long duration
    'transit_depth': 0.15,           # Very deep (too large for planet)
    'snr': 12.0,
    'stellar_mass': 1.2,
    'stellar_temp': 6000.0,
    'stellar_magnitude': 13.8
}

result3 = system.predict(example3)
print(f"\nClassification: {result3['classification'].upper()}")
print(f"Confidence: {result3['confidence']:.2%}")
print(f"Uncertainty: {result3['uncertainty']:.4f}")

print("\n" + "="*70)
print("DEMO COMPLETE")
print("="*70)
print("\nKey Insights:")
print("  • High SNR and typical transit parameters → Confirmed Exoplanet")
print("  • Moderate SNR with uncertain parameters → Planetary Candidate")
print("  • Extreme transit depth or duration → False Positive")
print("\nFor interactive mode, run:")
print("  python3 exoplanet_classifier.py")
print("\n" + "="*70)
