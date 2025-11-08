"""
test.py — Automated Test Script for InferX
Author: Nikhil Tomar
Description:
    Sends a test image to the InferX API for classification,
    waits for the result, and prints top-5 predictions neatly.
"""

import requests
import time
import json
from pathlib import Path

API_URL = "http://127.0.0.1:8000"
IMAGE_PATH = Path("test_images/dog.jpg")

def upload_image():
    """Send image to InferX FastAPI /predict endpoint."""
    if not IMAGE_PATH.exists():
        raise FileNotFoundError(f"Test image not found at {IMAGE_PATH}. Please add one!")

    print("Uploading image for classification...")
    with open(IMAGE_PATH, "rb") as f:
        response = requests.post(f"{API_URL}/predict/", files={"file": f})
    
    if response.status_code != 200:
        raise RuntimeError(f"API request failed: {response.text}")

    result = response.json()
    print(f"Task ID: {result['task_id']}")
    return result["task_id"]

def poll_result(task_id, interval=2, timeout=60):
    """Poll the /result/{task_id} endpoint until result is ready."""
    print("Waiting for inference result...")
    start_time = time.time()

    while True:
        response = requests.get(f"{API_URL}/result/{task_id}")
        data = response.json()

        if data.get("status") == "success":
            print("\nInference completed!")
            return data["result"]
        elif "error" in data.get("status", ""):
            print(f"Error: {data}")
            return None
        elif time.time() - start_time > timeout:
            print("Timeout waiting for inference result.")
            return None
        
        time.sleep(interval)
        print(".", end="", flush=True)

def display_results(results):
    """Print top-5 predictions."""
    print("\n🔍 Top-5 Predictions:")
    print("-" * 40)
    for r in results:
        label = r["label"]
        prob = r["probability"]
        print(f"{label:<40} {prob*100:>6.2f}%")
    print("-" * 40)

if __name__ == "__main__":
    print("Starting InferX Test...")
    try:
        task_id = upload_image()
        results = poll_result(task_id)
        if results:
            display_results(results)
        else:
            print("No results received.")
    except Exception as e:
        print(f"Test failed: {e}")
