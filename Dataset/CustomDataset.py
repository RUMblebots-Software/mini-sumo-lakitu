import torch
from torchvision import transforms
from PIL import Image
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
        # The differnt classes found in bounding boxes are stored in this array
        classList = []
        # Here class index pairs will be stored. Key = Class/label; value = enumeration of the class
        classToIndex = dict()

        # Goes through all image dictionaries in the json
        for image in data['files']:
           
            boundingBoxesPerImage = len(image['boundingBoxes'])

            # for images with multiple bounding boxes
            if(boundingBoxesPerImage > 1):
               
                for boxes in image['boundingBoxes']:
                    
                    if(boxes["label"] not in classList):
                        classList.append(boxes["label"])
                        classToIndex[boxes["label"]] = len(classToIndex)

            # for images with a single bounding box
            else:                 
                # image[boundingBoxes][0] accesses the only dictionary available 
                if(image['boundingBoxes'][0]["label"] not in classList):

                    classList.append(image['boundingBoxes'][0]["label"]) 
                    classToIndex[image['boundingBoxes'][0]["label"]] = len(classToIndex)
        
        return (classList, classToIndex)

    def make_dataset(self, json_dir,classToIndex):
        """
        returns a list -> [img, indx, (x,y,w,h)]
        classToIndex is ([label types],{label with enumeration}) and is a result of calling Find_bouding_Boxes
        """

        # Iterate in the different paths in the json 
        with open(json_dir,"r") as file:
             data = json.load(file)

        instaces = []

         # Goes through all image dictionaries in the json
        for image in data["files"]:

            # path = image["path"]
            
            path = "G:\\Shared drives\\RB\\2025-2026\\Spring 2026\\Software\\MiniSumoDataset\\" + image["path"].replace("/", "\\")
            
            for boxes in image["boundingBoxes"]:

                # classToIndex is a tupple (class Array, {class : enumeration} )
                idx = classToIndex[1][boxes["label"]]

                coords = tuple([boxes["x"],boxes["y"],boxes["width"],boxes["height"]])
                instaces.append(tuple([path,idx,coords]))

        self.samples = instaces

        return instaces
    
    def create_tensors(self,instances):

        instancesList = []

        for instance in instances:
            instancesList.append(self.load_instance(instance))
        
        return instancesList


    def xywh_to_xyxy(self,box):
        x, y, w, h = box
        return [x, y, x+w, y+h]
        

    def load_instance(self,instance):
        # instance values  were hardcoded temporarly to prove the func works, current error: permission error
        path,label, (x,y,w,h) = instance
        img = Image.open(path).convert("RGB")
        imgTensor = transforms.ToTensor()(img)


        box_xyxy = self.xywh_to_xyxy((x,y,w,h))
        
        boxes = torch.tensor([box_xyxy],dtype=torch.float32)

        labels = torch.tensor([label],dtype=torch.int64)

        target = {
            "boundingBoxes" : boxes,
            "label" : labels
        }

        return imgTensor, target

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
json_dir = "G:\\Shared drives\\RB\\2025-2026\\Spring 2026\\Software\\MiniSumoDataset\\info.json"
imageInstancesArray = obj.make_dataset(json_dir, obj.find_bounding_boxes(json_dir))

# print(imageInstancesArray)

print(obj.create_tensors(imageInstancesArray))




# ('data/minisumo.09(1).jpg.4o4v5mqp.ingestion-6d4b7975-8kjp4.jpg', 0, (33, 0, 525, 404)), 

# "G:\\Shared drives\\RB\\2025-2026\\Spring 2026\\Software\\MiniSumoDataset\\data\\