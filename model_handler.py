import torch
import torchvision.transforms as T
from torchvision import models
from PIL import Image
import json
from logger_config import get_logger

logger = get_logger("ModelHandler")

class ModelHandler:
    def __init__(self, labels_path="labels.json"):
        self.model = None
        with open(labels_path, "r") as f:
            self.labels = json.load(f)

        self.transform = T.Compose([
            T.Resize(256),
            T.CenterCrop(224),
            T.ToTensor(),
            T.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        logger.info("ModelHandler initialized with label file loaded.")

    def load_model(self):
        if self.model is None:
            logger.info("Loading pre-trained ResNet-50 model...")
            self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
            self.model.eval()
            logger.info("ResNet-50 model loaded successfully.")
        return self.model

    @torch.no_grad()
    def predict(self, image_path, device):
        logger.info(f"Running inference on {image_path} using {device}.")
        model = self.load_model()
        img = Image.open(image_path).convert("RGB")
        img_t = self.transform(img).unsqueeze(0).to(device)

        model = model.to(device)
        preds = model(img_t)
        probs = torch.nn.functional.softmax(preds, dim=1)[0]
        top5_prob, top5_catid = torch.topk(probs, 5)

        results = []
        for i in range(top5_prob.size(0)):
            results.append({
                "label": self.labels[str(top5_catid[i].item())],
                "probability": round(top5_prob[i].item(), 4)
            })
        logger.info(f"Inference complete. Top result: {results[0]['label']}")
        return results
