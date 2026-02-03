import torch
from torch.utils.data import Dataset
from PIL import Image
import json
import os

class CustomImageBoundingBoxDataset(Dataset):
    def __init__(self, img_dir, json_dir, transform=None):
        self.img_dir = img_dir
        self.json_dir = json_dir
        self.transform = transform
        # Get list of all image filenames
        self.img_files = [f for f in os.listdir(img_dir) if f.endswith('.png') or f.endswith('.jpg')]
        # Assuming JSON filenames match image filenames (e.g., image.jpg -> image.json)

    def __len__(self):
        return len(self.img_files)

    def __getitem__(self, idx):
        img_name = self.img_files[idx]
        img_path = os.path.join(self.img_dir, img_name)
        
        # Construct the JSON filename (adjust extension as needed)
        json_name = os.path.splitext(img_name)[0] + '.json'
        json_path = os.path.join(self.json_dir, json_name)

        # Load image
        image = Image.open(img_path).convert("RGB")

        # Load and parse JSON bounding box data
        with open(json_path, 'r') as f:
            annotation = json.load(f)
        
        # Extract bounding boxes (assuming a specific JSON structure)
        # You will need to adapt this part to your specific JSON format
        boxes = [obj['bbox'] for obj in annotation['objects']] # Example structure
        # Convert to a PyTorch tensor, ensuring correct format (e.g., XYXY)
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        
        # Create a dictionary for the target (annotations)
        target = {}
        target["boxes"] = boxes
        # Add other relevant information like labels, image_id, etc.
        # target["labels"] = torch.as_tensor([obj['label'] for obj in annotation['objects']], dtype=torch.int64)

        if self.transform:
            # Note: The transforms for object detection usually require applying
            # the same transformation to both the image and the bounding boxes.
            # Torchvision's new transforms API handles this with tv_tensors.
            image, target = self.transform(image, target)

        return image, target
