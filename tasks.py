from celery import Celery
from model_handler import ModelHandler
from gpu_manager import GPUManager
import torch
from logger_config import get_logger

logger = get_logger("Worker")

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

gpu_manager = GPUManager()
model_handler = ModelHandler()

@app.task
def classify_image(image_path):
    logger.info(f"Received task for image: {image_path}")
    device_id = gpu_manager.acquire_device()
    device = torch.device(f"cuda:{device_id}" if device_id is not None else "cpu")

    try:
        result = model_handler.predict(image_path, device)
        logger.info(f"Task completed successfully for {image_path}")
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error during inference: {str(e)}")
        return {"status": "error", "message": str(e)}
