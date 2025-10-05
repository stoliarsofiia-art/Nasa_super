#!/bin/bash

echo "=================================================="
echo "QUICK FIX FOR CORS ERROR"
echo "=================================================="
echo ""

echo "Step 1: Adding updated app.py..."
git add app.py
echo "✓ app.py added"
echo ""

echo "Step 2: Committing changes..."
git commit -m "Fix CORS and add /analyze endpoint"
echo "✓ Changes committed"
echo ""

echo "Step 3: Pushing to Heroku..."
echo "This will take 1-2 minutes..."
echo ""
git push heroku main || git push heroku HEAD:main

echo ""
echo "=================================================="
echo "✓ DEPLOYED!"
echo "=================================================="
echo ""
echo "Now test your website:"
echo "https://martyniukaleksei.github.io/iaso-som-v1/"
echo ""
echo "Monitor logs with:"
echo "  heroku logs --tail"
echo ""
