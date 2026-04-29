#!/bin/bash
# Start the ARQ worker in the background
echo "Starting ARQ worker..."
.venv/bin/arq src.workers.tasks.WorkerSettings &

# Start the FastAPI server
# Fly.io and other platforms use the PORT env var
TARGET_PORT=${PORT:-8080}
echo "Starting FastAPI server on port $TARGET_PORT..."
.venv/bin/uvicorn src.main_refactored:app --host 0.0.0.0 --port $TARGET_PORT
