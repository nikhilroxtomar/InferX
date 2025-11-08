import pynvml
from logger_config import get_logger

logger = get_logger("GPUManager")

class GPUManager:
    def __init__(self, min_free_mem_mb=2000):
        self.device = None
        self.min_free_mem_mb = min_free_mem_mb
        self._initialize_nvml()

    def _initialize_nvml(self):
        """Initialize NVML safely inside each Celery worker process."""
        try:
            pynvml.nvmlInit()
            self.device = pynvml.nvmlDeviceGetHandleByIndex(0)
            logger.info("NVML initialized successfully.")
        except pynvml.NVMLError as e:
            logger.error(f"NVML initialization failed: {e}")
            self.device = None

    def _check_and_reinit_nvml(self):
        """Reinitialize NVML if it was uninitialized (e.g., in child process)."""
        try:
            pynvml.nvmlDeviceGetCount()
        except pynvml.NVMLError_Uninitialized:
            logger.warning("NVML was uninitialized in this process. Reinitializing...")
            self._initialize_nvml()

    def get_free_memory_mb(self):
        """Return free GPU memory in MB, or 0 if unavailable."""
        self._check_and_reinit_nvml()
        if self.device is None:
            return 0
        try:
            info = pynvml.nvmlDeviceGetMemoryInfo(self.device)
            return info.free / (1024 ** 2)
        except pynvml.NVMLError_Uninitialized:
            logger.error("NVML Uninitialized even after reinit. Returning 0.")
            return 0

    def acquire_device(self):
        """Return GPU index (0) if free memory > threshold, else None."""
        self._check_and_reinit_nvml()
        if self.device is None:
            logger.warning("No GPU detected. Using CPU instead.")
            return None

        try:
            free_mem = self.get_free_memory_mb()
            if free_mem > self.min_free_mem_mb:
                logger.info(f"GPU available with {free_mem:.2f} MB free.")
                return 0
            else:
                logger.warning(f"GPU busy ({free_mem:.2f} MB free). Using CPU.")
                return None
        except pynvml.NVMLError as e:
            logger.error(f"NVML error: {e}. Using CPU instead.")
            return None
