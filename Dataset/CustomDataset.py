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
         
        with open(json_dir, "r") as file:
                data = json.load(file)        
        classList = []
        classToIndex = dict()
        for image in data['files']:
           
            boundingBoxesPerImage = len(image['boundingBoxes'])

            if(boundingBoxesPerImage > 1):
               
                for boxes in image['boundingBoxes']:
                    
                    if(boxes["label"] not in classList):
                        classList.append(boxes["label"])
                        classToIndex[boxes["label"]] = len(classToIndex)

            else:                 

                if(image['boundingBoxes'][0]["label"] not in classList):
                    classList.append(image['boundingBoxes'][0]["label"]) 
                    classToIndex[image['boundingBoxes'][0]["label"]] = len(classToIndex)
        
        return (classList, classToIndex)

    def make_dataset(self, json_dir,classToIndex):

        # Iterate in the different paths in the json 
        with open(json_dir,"r") as file:
             data = json.load(file)

        pathArray = []

        for image in data["files"]:
            path = image["path"]

            for boxes in image["boundingBoxes"]:

                idx = classToIndex[1][boxes["label"]]
                coords = tuple([boxes["x"],boxes["y"],boxes["width"],boxes["height"]])
                pathArray.append(tuple([path,idx,coords]))

        # path -> boundingbox ---> paths can be repeated but bounding boxes not
        # return an array of tuple(path,idx,coords(x,y,w,h))

        return pathArray






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
json_dir = "Dataset\\DatasetSample.json"
print(obj.make_dataset(json_dir, obj.find_bounding_boxes(json_dir)))