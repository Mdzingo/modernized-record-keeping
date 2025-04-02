#!/bin/bash
# Script to start the FastAPI application

echo "Starting Modernized Record Keeping API..."

# Activate the Poetry environment
cd "$(dirname "$0")/.."

# Test database connection first
echo "Testing database connection..."
poetry run python scripts/test_db_connection.py

if [ $? -ne 0 ]; then
    echo "❌ Database connection failed. Please check your PostgreSQL configuration."
    echo "Make sure PostgreSQL is running and the database exists."
    exit 1
fi

echo "✅ Database connection successful!"
echo "Starting FastAPI application..."

# Start the application
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
