import torch
from torchvision import transforms
from PIL import Image
from torch.utils.data import Dataset, dataloader
from torchvision.datasets import ImageFolder
from torchvision.datasets.folder import default_loader
from PIL import Image
import json
import cv2
import numpy as np

class BoundingBoxImageFolder(ImageFolder):
    def __init__(
            self, 
            instance,
            img_dir, 
            json_dir, 
            transform=None, 
            target_transform=None, 
            loader=default_loader, 
            is_valid_file = None,
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
            self.instance = instance
            
        
    
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
        """
        Description
        
        :param instances: 
        :returns instance list: a list containtaining all images in RGB with their target
        """

        instancesList = []

        for instance in instances:
            instancesList.append(self.load_instance(instance))
        
        return instancesList


    def xywh_to_xyxy(self,box):
        x, y, w, h = box
        return [x, y, x+w, y+h]
        

    def load_instance(self,instance):
        """
        Descripion
        
        
        :param instance: a single image instance (tuple) with elements (path,label index, coordinates)
        :returns: a cropped image in RGB and the label of the cropped image
        """
        path,label, (x,y,w,h) = instance
        
        img = Image.open(path).convert("RGB")
        img = np.array(img)

        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        box_xyxy = self.xywh_to_xyxy((x,y,w,h))


        y_start = int(box_xyxy[1])
        y_end = int(box_xyxy[3])
        x_start = int(box_xyxy[0])
        x_end = int(box_xyxy[2])
        croppedIMG = img[y_start:y_end,x_start:x_end]
        img = croppedIMG
        # debug images
        # cv2.imshow("Before RGB", np.array(Image.open(path)))
        # cv2.imshow("Original Image", img)
        # cv2.imshow("Cropped Image", croppedIMG)
        
        # # Wait for a key press and then close windows
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        imgTensor = transforms.ToTensor()(img)



        labels = torch.tensor([label],dtype=torch.int64)


        self.dataset = [imgTensor, labels]

        return self.dataset


    def __len__(self):
        return len(self.img_files)

    def __getitem__(self, idx):

        imgTensor, target = self.dataset[idx]

        
        return imgTensor, target



# class BondingBoxDataset(Dataset):
#     def __init__(self):
#         self.dataset = BoundingBoxImageFolder(img_dir, json_dir, transform)

#         if self.transform:
#         # Note: The transforms for object detection usually require applying
#         # the same transformation to both the image and the bounding boxes.
#         # Torchvision's new transforms API handles this with tv_tensors.
#         image, target = self.transform(image, target)

obj = BoundingBoxImageFolder(None,None,None,None,None,None,None)
json_dir = "G:\\Shared drives\\RB\\2025-2026\\Spring 2026\\Software\\MiniSumoDataset\\info.json"
imageInstancesArray = obj.make_dataset(json_dir, obj.find_bounding_boxes(json_dir))

# print(imageInstancesArray)

print(obj.create_tensors(imageInstancesArray))




# ('data/minisumo.09(1).jpg.4o4v5mqp.ingestion-6d4b7975-8kjp4.jpg', 0, (33, 0, 525, 404)), 

# "G:\\Shared drives\\RB\\2025-2026\\Spring 2026\\Software\\MiniSumoDataset\\data\\