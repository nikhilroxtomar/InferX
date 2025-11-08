# 🚀 InferX: Deep Learning Model Inference API

**InferX** is a lightweight, production-ready deep learning inference server built with **FastAPI**, **Celery**, and **PyTorch**.  
It enables asynchronous and GPU-aware model inference for computer vision tasks — starting here with **ImageNet image classification** using a pre-trained **ResNet-50** model.

---

## 🧩 Features

- ⚡ **FastAPI** — modern async REST API  
- 🔄 **Celery + Redis** — background task queue for non-blocking inference  
- 🧠 **PyTorch (ResNet-50)** — pre-trained ImageNet classifier  
- 💡 **Dynamic GPU VRAM management** (via `pynvml`)  
- 🪵 **Detailed logging system** for each module  
- 📂 **Extensible architecture** — easy to plug in other models or tasks later

---

## 🧱 Project Structure
```
InferX/
│
├── gpu_manager.py        # Handles GPU VRAM checks and device allocation
├── labels.json           # ImageNet class labels (1,000 categories)
├── logger_config.py      # Unified logger setup for all modules
├── logs/                 # Auto-generated logs for API, workers, GPU, etc.
│
├── main.py               # FastAPI server (API entry point)
├── model_handler.py      # Loads the pre-trained model and runs inference
├── requirements.txt      # Python dependencies
├── start_local.sh        # Launch Redis, Celery, and FastAPI together
├── stop_local.sh         # Gracefully stops all running services
├── tasks.py              # Celery worker for asynchronous inference
│
├── test_images/          # Sample images for testing
│   ├── cat.jpeg
│   └── dog.jpg
├── test.py               # Automated test client script
└── uploads/              # Temporary directory for uploaded images
```
---

## ⚙️ Setup Instructions

### 1. Clone the repository
```
git clone https://github.com/nikhilroxtomar/InferX.git
cd InferX
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Start the System
Run everything (Redis, Celery, FastAPI) automatically:
```
redis-server
```

### 4. Test the API
Use the included script:
```
python3 test.py
```
---

## 🧠 How It Works

- User uploads an image via /predict/.
- FastAPI saves it and queues a Celery task in Redis.
- Celery worker picks up the task:
--Checks GPU memory availability
-- Runs ResNet-50 inference
-- Returns top-5 predictions
- User retrieves the result using /result/{task_id}.

---

## 🧪 Example Usage

### Upload Image
```
curl -X POST "http://127.0.0.1:8000/predict/" -F "file=@cat.jpg"
```

### Response
```
{"task_id": "a1b2c3...", "status": "queued"}
```

### Get Result
```
curl "http://127.0.0.1:8000/result/a1b2c3..."
```

### Response
```
{
  "status": "success",
  "result": [
    {"label": "tabby cat", "probability": 0.97},
    {"label": "tiger cat", "probability": 0.02},
    {"label": "Egyptian cat", "probability": 0.01}
  ]
}
```
---

## 🪵 Logging

All logs are automatically saved in the logs/ directory:
```
logs/
├── API.log
├── Worker.log
├── GPUManager.log
└── ModelHandler.log
```

---

## 💻 GPU Management

InferX intelligently checks available GPU VRAM using NVIDIA’s pynvml:
 - If GPU has >2 GB free memory → inference runs on GPU.
 - Otherwise → falls back to CPU.

You can change the threshold in:
```
GPUManager(min_free_mem_mb=2000)
```
If NVML is uninitialized after forking, InferX auto-reinitializes it safely in each Celery worker process.

---

## 🧪 Testing & Validation

- InferX includes an automated test client (test.py) that:
-- Uploads an image
-- Waits for async inference completion
-- Displays top-5 predictions neatly formatted

Example:
```
Starting InferX Test...
Uploading image for classification...
Task ID: 841452bf-95e1-4f55-b513-5bbe3f7f0350
Waiting for inference result...
....
Inference completed!

🔍 Top-5 Predictions:
----------------------------------------
golden retriever                          53.24%
Labrador retriever                         2.61%
tennis ball                                0.70%
flat-coated retriever                      0.46%
kuvasz                                     0.37%
----------------------------------------
```

---

## 🧹 Managing Services

Start all services:
```
./start_local.sh
```

Stop all services cleanly:
```
./stop_local.sh
```
Optional cleanup (uploads + logs) is built in.

---

## Future Extensions
 - Add segmentation/detection model support
 - Integrate batching for higher GPU utilization
 - Dockerize for cloud deployment
 - Add result caching (Redis)
 - Add user authentication & dashboard

---

## 🧑‍💻 Author

Nikhil Tomar
Deep Learning Engineer | Medical Image Analysis Researcher
📍 India

---

## 🏁 License

This project is released under the MIT License.
