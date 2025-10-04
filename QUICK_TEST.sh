#!/bin/bash
echo "======================================================================"
echo "QUICK TEST - User's Example"
echo "======================================================================"
echo ""
echo "Testing: P=289.9d, depth=0.00492, SNR=12 (Neptune-sized, Venus-like orbit)"
echo ""
python3 exoplanet_classifier.py predict 289.9 7.4 0.00492 12 0.97 5627 11.7
echo ""
echo "======================================================================"
