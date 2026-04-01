# Define cleanup function to kill background processes on exit
cleanup() {
    echo "Stopping services..."

    kill $(jobs -p) 2>/dev/null

    pkill -9 -f "vite" 2>/dev/null
    pkill -9 -f "node" 2>/dev/null
    pkill -9 -f "manage.py" 2>/dev/null

    taskkill.exe /F /IM node.exe 2>/dev/null

    if [ -d "docker" ]; then
        (cd docker && docker-compose down 2>/dev/null)
    fi

    for port in 8000 5173 5174 5175 5176 5177 5178 5179 5180; do
        lsof -ti:$port | xargs kill -9 2>/dev/null
    done
    
    echo "All processes and ports have been successfully freed."
    exit
}

trap cleanup SIGINT

echo "Starting Django API..."
cd api || exit

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

npm run dev &
FRONTEND_PID=$!
cd ..

echo "====================================================="
echo "🚀 Both services are running! Press Ctrl+C to stop."
echo "====================================================="

wait