#!/bin/bash
# ==========================================================
# InferX Stop Script
# Author: Nikhil Tomar
# Description: Gracefully stop Redis, Celery, and FastAPI
# ==========================================================

APP_NAME="InferX"


echo -e "==============================================="
echo -e " Stopping ${APP_NAME} Local Environment"
echo -e "===============================================${NC}"

stop_process() {
  local name=$1
  local pattern=$2
  local pid=$(pgrep -f "$pattern")

  if [ -n "$pid" ]; then
    echo -e "Stopping $name (PID: $pid)..."
    pkill -f "$pattern"
    sleep 1
    echo -e "$name stopped successfully.$"
  else
    echo -e "$name not running."
  fi
}

# --- Stop Services ---
stop_process "FastAPI (Uvicorn)" "uvicorn main:app"
stop_process "Celery Worker" "celery -A tasks worker"
stop_process "Redis Server" "redis-server"

# --- Optional Cleanup ---
read -p "Do you want to clean temporary files (uploads/, logs/)? [y/N]: " cleanup_choice
cleanup_choice=${cleanup_choice,,} # lowercase
if [[ "$cleanup_choice" == "y" || "$cleanup_choice" == "yes" ]]; then
  echo -e "Cleaning temporary folders..."
  rm -rf uploads/*
  rm -rf logs/*
  echo -e "$uploads/ and logs/ cleaned."
else
  echo -e "$Skipping cleanup."
fi

echo -e "\nAll ${APP_NAME} processes have been stopped."
