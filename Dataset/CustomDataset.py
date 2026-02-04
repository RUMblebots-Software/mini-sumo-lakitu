import torch
from torch.utils.data import Dataset
from torchvision.datasets import ImageFolder
from torchvision.datasets.folder import default_loader
from PIL import Image
import json
import os

class BoundingBoxImageFolder(ImageFolder):
    def __init__(
            self, 
            img_dir, 
            json_dir, 
            transform=None, 
            target_transform=None, 
            loader=default_loader, 
            is_valid_file = None
        ):
            # super().__init__(
            #     root=img_dir,
            #     transform=transform,
            #     target_transform=target_transform,
            #     loader=loader,
            #     is_valid_file=is_valid_file
            # )
            self.img_dir = img_dir
            self.json_dir = json_dir

            # Get list of all image filenames
            self.img_files = [f for f in os.listdir(img_dir) if f.endswith('.png') or f.endswith('.jpg')]
            # Assuming JSON filenames match image filenames (e.g., image.jpg -> image.json)
        
    
    def find_bounding_boxes(self, json_dir):

        # Open the json
        # Read the json 
        # for each element in json:
            # find the "BoundingBoxes" tag
            # extract information TODO: what is the relevant info and what do we achieve with it?
            # call function to process the data and fetch results
            # contain processed data in tensor/matrix whatever
            # return output to feed into make_dataset             
        with open(json_dir, "r") as file:
                data = json.load(file)        
        
        for image in data['files']:
            # NOTE: if there are multiple bounding boxes in the same image we can access them by image['boundingBoxes'][index]
            boundingBoxesPerImage = len(image['boundingBoxes'])

            if(boundingBoxesPerImage > 1):
                print(f"This has {boundingBoxesPerImage} boxes\n")
                for boxes in image['boundingBoxes']:
                    
                    print(boxes)

            else:                 
                print(image['boundingBoxes'])  
        
        return

    def make_dataset(self, ):
        return

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



        return image, target



# class BondingBoxDataset(Dataset):
#     def __init__(self):
#         self.dataset = BoundingBoxImageFolder(img_dir, json_dir, transform)

#         if self.transform:
#         # Note: The transforms for object detection usually require applying
#         # the same transformation to both the image and the bounding boxes.
#         # Torchvision's new transforms API handles this with tv_tensors.
#         image, target = self.transform(image, target)

obj = BoundingBoxImageFolder(None,None,None,None,None,None)
obj.find_bounding_boxes("Dataset\\DatasetSample.json")