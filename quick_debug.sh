#!/bin/bash

echo "================================================================"
echo "HEROKU PUSH DIAGNOSTICS"
echo "================================================================"
echo ""

echo "1. Checking Git Status..."
echo "-----------------------------------"
git status
echo ""

echo "2. Checking Git Remotes..."
echo "-----------------------------------"
git remote -v
echo ""

echo "3. Checking Current Branch..."
echo "-----------------------------------"
git branch
echo ""

echo "4. Checking Heroku Login..."
echo "-----------------------------------"
heroku auth:whoami 2>&1
echo ""

echo "5. Checking Heroku Apps..."
echo "-----------------------------------"
heroku apps 2>&1
echo ""

echo "6. Checking if app exists..."
echo "-----------------------------------"
heroku apps:info -a sophia-nasa-ml-app 2>&1
echo ""

echo "================================================================"
echo "ATTEMPTING FIX..."
echo "================================================================"
echo ""

echo "Step 1: Connecting to Heroku app..."
heroku git:remote -a sophia-nasa-ml-app
echo ""

echo "Step 2: Checking remote was added..."
git remote -v
echo ""

echo "Step 3: Committing any uncommitted changes..."
git add .
git commit -m "Deploy to Heroku" || echo "Nothing to commit"
echo ""

echo "Step 4: Attempting push..."
echo "Running: git push heroku HEAD:main --force"
echo ""
git push heroku HEAD:main --force

echo ""
echo "================================================================"
if [ $? -eq 0 ]; then
    echo "✅ PUSH SUCCESSFUL!"
    echo "================================================================"
    echo ""
    echo "Now monitoring logs..."
    heroku logs --tail -a sophia-nasa-ml-app
else
    echo "❌ PUSH FAILED"
    echo "================================================================"
    echo ""
    echo "Please share the error message above so I can help fix it."
fi
