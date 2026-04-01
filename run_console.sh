# Exit immediately if a command exits with a non-zero status
set -e

# Define cleanup function to kill background processes on exit
cleanup() {
    echo "Stopping services..."

    kill $(jobs -p) 2>/dev/null

    pkill -9 -f "manage.py" 2>/dev/null

    if [ -d "docker" ]; then
        (cd docker && docker-compose down 2>/dev/null)
    fi

    lsof -ti:8000 | xargs kill -9 2>/dev/null
    
    echo "All background processes and ports have been successfully freed."
    exit
}
trap cleanup SIGINT EXIT

echo "Starting Django API..."
# Navigate to the api directory where the backend pyproject.toml is located
cd api || exit

if ! command -v poetry &> /dev/null; then
    echo "Error: poetry is not installed or not in PATH."
    echo "Please install it from: https://python-poetry.org/docs/"
    exit 1
fi

# Install Python dependencies automatically for the backend
echo "Checking and installing backend dependencies..."
poetry install

# Navigate to src where manage.py is located
cd src || exit

# Run database migrations to ensure the DB is up to date
echo "Running database migrations..."
poetry run python manage.py migrate

# Start backend in the background
echo "Starting backend server in the background..."
poetry run python manage.py runserver &
BACKEND_PID=$!

# Go back to the root directory
cd ../..

echo "====================================================="
echo "🚀 API is running! Starting Desktop App..."
echo "====================================================="

# Install root dependencies without installing the project itself as a Python package
poetry install --no-root

# Install the specific console dependencies from the requirements.txt file
# Using --trusted-host flags to bypass WSL2 SSL decryption issues
if [ -f "console/requirements.txt" ]; then
    poetry run pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r console/requirements.txt
fi

# Run the console CLI application in the foreground
# The script will pause here until the user exits the program (e.g., choosing option 6)
poetry run python console/ToDo.py
