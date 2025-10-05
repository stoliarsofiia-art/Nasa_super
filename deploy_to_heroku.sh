#!/bin/bash

echo "=========================================="
echo "DEPLOYING TO HEROKU"
echo "=========================================="
echo ""

# Step 1: Check if git is initialized
if [ ! -d .git ]; then
    echo "Step 1: Initializing git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git already initialized"
fi
echo ""

# Step 2: Add .gitignore
echo "Step 2: Creating .gitignore..."
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
*.log
.DS_Store
*.swp
*.swo
.env
venv/
env/
.vscode/
.idea/
EOF
echo "✓ .gitignore created"
echo ""

# Step 3: Add all files
echo "Step 3: Adding files to git..."
git add .
echo "✓ Files added"
echo ""

# Step 4: Commit
echo "Step 4: Committing files..."
git commit -m "Deploy exoplanet classifier API with CORS" || echo "Files already committed or no changes"
echo "✓ Commit complete"
echo ""

# Step 5: Check Heroku login
echo "Step 5: Checking Heroku login..."
echo "Please make sure you're logged in to Heroku CLI"
echo "If not logged in, run: heroku login"
echo ""
read -p "Are you logged in to Heroku? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please login first:"
    echo "  heroku login"
    exit 1
fi
echo ""

# Step 6: Check if Heroku remote exists
echo "Step 6: Checking Heroku app..."
if git remote | grep -q heroku; then
    echo "✓ Heroku remote already exists"
    heroku apps:info
else
    echo "No Heroku app found."
    read -p "Enter your Heroku app name (or press Enter to create new): " APP_NAME
    echo ""
    
    if [ -z "$APP_NAME" ]; then
        echo "Creating new Heroku app..."
        heroku create
    else
        echo "Connecting to existing app: $APP_NAME"
        heroku git:remote -a "$APP_NAME"
    fi
fi
echo ""

# Step 7: Push to Heroku
echo "Step 7: Pushing to Heroku..."
echo "This may take a few minutes..."
echo ""
git push heroku main || git push heroku master

echo ""
echo "=========================================="
echo "✓ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Scale your dyno: heroku ps:scale web=1"
echo "2. Check logs: heroku logs --tail"
echo "3. Open app: heroku open"
echo ""
echo "Your API URL will be:"
heroku apps:info -s | grep web_url | cut -d= -f2
echo ""