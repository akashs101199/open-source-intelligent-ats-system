#!/bin/bash

echo "================================================"
echo "  Intelligent ATS - Complete Setup"
echo "================================================"
echo

# Backend setup
echo "Setting up backend..."
cd backend
chmod +x ../setup.sh
../setup.sh
cd ..

# Frontend setup
echo ""
echo "Setting up frontend..."
cd frontend
chmod +x install.sh
./install.sh
cd ..

echo ""
echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "Backend running at: http://localhost:8000"
echo "Frontend starting... Run: cd frontend && npm run dev"
echo ""
echo "Open http://localhost:5173 in your browser"
echo "================================================"