#!/bin/bash

# Quick Deployment Script for Vercel
# Run this script to prepare and deploy your project

echo "=========================================="
echo "Vercel Deployment Script"
echo "=========================================="
echo ""

# Check if models exist
echo "✓ Checking models directory..."
if [ ! -d "models" ]; then
    echo "❌ ERROR: models/ directory not found!"
    echo "   Please ensure your trained models are in the models/ directory"
    exit 1
fi

if [ ! -f "models/classifier.pkl" ]; then
    echo "❌ ERROR: models/classifier.pkl not found!"
    exit 1
fi

echo "✓ Models found ($(du -sh models/ | cut -f1))"
echo ""

# Check if git is initialized
echo "✓ Checking git repository..."
if [ ! -d ".git" ]; then
    echo "❌ ERROR: Not a git repository!"
    echo "   Initialize with: git init"
    exit 1
fi

echo "✓ Git repository found"
echo ""

# Show current status
echo "✓ Current git status:"
git status --short
echo ""

# Ask to commit
read -p "Do you want to commit changes? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "✓ Adding files to git..."
    git add .
    
    echo "✓ Committing changes..."
    git commit -m "Configure for Vercel deployment"
    
    echo "✓ Pushing to GitHub..."
    git push origin main || git push origin master
    
    echo ""
    echo "✓ Code pushed to GitHub!"
fi

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Go to: https://vercel.com/new"
echo "2. Click 'Import Project'"
echo "3. Select your GitHub repository"
echo "4. Click 'Deploy'"
echo ""
echo "OR use Vercel CLI:"
echo ""
echo "  npm install -g vercel"
echo "  vercel login"
echo "  vercel"
echo "  vercel --prod"
echo ""
echo "=========================================="
echo "Your API will be available at:"
echo "https://your-project.vercel.app"
echo "=========================================="
echo ""
echo "Test with:"
echo "curl https://your-project.vercel.app/api/health"
echo ""
