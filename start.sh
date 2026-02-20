#!/bin/bash

# Define cleanup function to kill background processes on exit
cleanup() {
    echo "Stopping services..."
    
    # Gracefully kill all background jobs spawned by this script
    kill $(jobs -p) 2>/dev/null
    
    # Forcefully kill any lingering Node (Vite) or Python (Django) processes in WSL
    pkill -9 -f "vite" 2>/dev/null
    pkill -9 -f "node" 2>/dev/null
    pkill -9 -f "manage.py" 2>/dev/null
    
    # Kill Windows host Node processes (crucial for WSL interoperability)
    taskkill.exe /F /IM node.exe 2>/dev/null
    
    # Shut down any running Docker containers for this project to free up ports
    if [ -d "docker" ]; then
        (cd docker && docker-compose down 2>/dev/null)
    fi
    
    # Aggressively clear the exact ports just to be absolutely sure
    for port in 8000 5173 5174 5175 5176 5177 5178 5179 5180; do
        lsof -ti:$port | xargs kill -9 2>/dev/null
    done
    
    echo "All processes and ports have been successfully freed."
    exit
}

# Catch Ctrl+C (SIGINT) and execute the cleanup function
trap cleanup SIGINT

echo "Starting Django API..."
# Navigate to the api directory where the backend pyproject.toml is located
cd api || exit

# Check if poetry command is available in the system
if ! command -v poetry &> /dev/null; then
    echo "Error: poetry is not installed or not in PATH."
    echo "Please install it from: https://python-poetry.org/docs/"
    exit 1
fi

# Install Python dependencies automatically
echo "Checking and installing backend dependencies..."
poetry install

# Navigate to src where manage.py is located
cd src || exit

# Run database migrations to ensure the DB is up to date
echo "Running database migrations..."
poetry run python manage.py migrate

# Start backend in the background and save its Process ID
poetry run python manage.py runserver &
BACKEND_PID=$!

# Go back to the root directory
cd ../..

echo "Starting Vite Web App..."
cd web || exit

# Install npm dependencies automatically if node_modules folder is missing
if [ ! -d "node_modules" ]; then
    echo "Missing node_modules. Installing frontend dependencies..."
    npm install
fi

# Start frontend in the background and save its Process ID
npm run dev &
FRONTEND_PID=$!
cd ..

echo "====================================================="
echo "🚀 Both services are running! Press Ctrl+C to stop."
echo "====================================================="

# Wait for background processes to finish (keeps the script running)
wait