#!/bin/bash

echo "================================================================"
echo "DEPLOYING TO HEROKU WITH ML MODELS"
echo "================================================================"
echo ""

APP_NAME="sophia-nasa-ml-app"

echo "Step 1: Connecting to Heroku app..."
heroku git:remote -a $APP_NAME
echo "✓ Connected"
echo ""

echo "Step 2: Adding all files including models..."
git add -f models/
git add *.py
git add Procfile requirements.txt runtime.txt
git add *.csv 2>/dev/null || true
echo "✓ Files staged"
echo ""

echo "Step 3: Committing..."
git commit -m "Deploy complete ML API with models and CORS fix" || echo "No changes to commit"
echo "✓ Committed"
echo ""

echo "Step 4: Checking current app status..."
heroku ps -a $APP_NAME
echo ""

echo "Step 5: Pushing to Heroku..."
echo "This will take 2-3 minutes. Please wait..."
echo ""
git push heroku HEAD:main -f

echo ""
echo "Step 6: Scaling dyno..."
heroku ps:scale web=1 -a $APP_NAME
echo "✓ Dyno scaled"
echo ""

echo "Step 7: Checking app status..."
heroku ps -a $APP_NAME
echo ""

echo "================================================================"
echo "DEPLOYMENT COMPLETE!"
echo "================================================================"
echo ""
echo "Your API URL:"
echo "https://sophia-nasa-ml-app-7bc530f3ab97.herokuapp.com"
echo ""
echo "Test health:"
echo "curl https://sophia-nasa-ml-app-7bc530f3ab97.herokuapp.com/health"
echo ""
echo "Monitor logs:"
echo "heroku logs --tail -a $APP_NAME"
echo ""
echo "If you see 'Model loaded successfully!' in logs, it's working!"
echo "================================================================"