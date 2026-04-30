import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as T
from PIL import Image
import numpy as np

class ReidExtractor:
    def __init__(self):
        # Load pre-trained MobileNetV2
        self.model = models.mobilenet_v2(weights="DEFAULT")
        # Remove classifier to get 1280-dim embeddings
        self.model.classifier = nn.Identity()
        self.model.eval()
        
        # Standard ImageNet transforms
        self.transform = T.Compose([
            T.Resize((224, 224)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def get_embedding(self, cv2_img):
        """
        Takes a CV2 (BGR) image crop, converts to tensor and returns normalized embedding.
        """
        try:
            # Convert BGR (OpenCV) to RGB (PIL)
            img = Image.fromarray(cv2_img[:, :, ::-1])
            img_t = self.transform(img).unsqueeze(0)
            
            with torch.no_grad():
                embedding = self.model(img_t)
            
            # Normalize for cosine similarity
            embedding = embedding.squeeze().numpy()
            norm = np.linalg.norm(embedding)
            if norm > 1e-6:
                embedding = embedding / norm
                
            return embedding
        except Exception as e:
            print(f"ReID Error: {e}")
            return None

def cosine_similarity(a, b):
    return np.dot(a, b)
