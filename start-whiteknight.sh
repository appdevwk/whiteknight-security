#!/bin/bash
# Detect if src.main:app exists and start FastAPI
if [ -f "src/main.py" ]; then
    echo "Starting FastAPI server..."
    uvicorn src.main:app --host=0.0.0.0 --port=8000
elif [ -f "app.py" ]; then
    echo "Starting Flask app..."
    flask --app=app run --host=0.0.0.0 --port=5000
else
    echo "No application entry point found!"
fi
