#!/bin/bash
# ==========================================================
# InferX Local Runner
# Author: Nikhil Tomar
# Description: Run Redis, Celery, and FastAPI locally
# ==========================================================

# --- CONFIGURATION ---
APP_NAME="InferX"
REDIS_PORT=6379
API_PORT=8000

# --- FUNCTIONS ---

check_command() {
  if ! command -v "$1" &> /dev/null; then
    echo -e "$1 not found. Please install it before running this script."
    exit 1
  fi
}

start_redis() {
  echo -e "Starting Redis server..."
  if pgrep redis-server > /dev/null; then
    echo -e " Redis is already running."
  else
    redis-server --port $REDIS_PORT &
    sleep 2
    echo -e " Redis server started on port $REDIS_PORT."
  fi
}

start_celery() {
  echo -e " Starting Celery worker..."
  celery -A tasks worker --loglevel=info > logs/celery.log 2>&1 &
  sleep 3
  echo -e " Celery worker running (logs in logs/celery.log)."
}

start_fastapi() {
  echo -e "Starting FastAPI server..."
  uvicorn main:app --host 0.0.0.0 --port $API_PORT --reload > logs/fastapi.log 2>&1 &
  sleep 3
  echo -e " FastAPI running on http://127.0.0.1:${API_PORT}"
}

# --- MAIN EXECUTION ---
echo -e "==============================================="
echo -e " Starting ${APP_NAME} Local Environment"
echo -e "==============================================="

# 1. Check dependencies
check_command redis-server
check_command celery
check_command uvicorn

# 2. Create directories if not exist
mkdir -p logs uploads

# 3. Start components
start_redis
start_celery
start_fastapi

# --- SUMMARY ---
echo -e "\n${APP_NAME} is up and running!"
echo -e "Upload images via POST: http://127.0.0.1:${API_PORT}/predict/"
echo -e "Check results at: http://127.0.0.1:${API_PORT}/result/<task_id>"
echo -e "Logs: stored in ./logs"
echo -e "\nPress Ctrl+C to stop all services."

# Keep script alive to prevent background kill
wait