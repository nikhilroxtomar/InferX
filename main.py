from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path
from tasks import classify_image
from logger_config import get_logger

logger = get_logger("API")

app = FastAPI(title="ImageNet Classification API")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def home():
    logger.info("Root endpoint accessed.")
    return {"message": "ImageNet Classification API is running"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    logger.info(f"Received file: {file.filename}, saved to {file_path}")
    task = classify_image.delay(str(file_path))
    logger.info(f"Task {task.id} created for {file.filename}")
    return {"task_id": task.id, "status": "queued"}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task = classify_image.AsyncResult(task_id)
    if task.ready():
        logger.info(f"Returning result for task {task_id}")
        return task.result
    logger.info(f"Task {task_id} still pending")
    return {"status": "pending"}
