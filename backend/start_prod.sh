#!/bin/bash
# Start the ARQ worker in the background
echo "Starting ARQ worker..."
.venv/bin/arq src.workers.tasks.WorkerSettings &

# Start the FastAPI server
# Hugging Face Spaces expect the app to run on port 7860
echo "Starting FastAPI server on port 7860..."
.venv/bin/uvicorn src.main_refactored:app --host 0.0.0.0 --port 7860
