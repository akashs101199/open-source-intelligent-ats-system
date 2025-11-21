#!/bin/bash

echo "Installing frontend dependencies..."

npm install

echo "Creating .env file..."
cat > .env << EOF
VITE_API_URL=http://localhost:8000
EOF

echo "Frontend setup complete!"
echo "Run 'npm run dev' to start the development server"