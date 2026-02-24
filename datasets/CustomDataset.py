import os
import json
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from torchvision.datasets import VisionDataset
from torch.utils.data import Dataset
from torchvision.datasets.folder import default_loader


class BoundingBoxImageFolder(VisionDataset):
    """
    Dataset that reads image paths + bounding boxes from a JSON file
    and behaves similarly to torchvision.datasets.ImageFolder.

    Expected JSON format:
    {
        "files": [
            {
                "path": "relative/path/to/image.jpg",
                "boundingBoxes": [
                    {
                        "label": "class_name",
                        "x": int,
                        "y": int,
                        "width": int,
                        "height": int
                    }
                ]
            }
        ]
    }
    """

    def __init__(
        self,
        root,
        json_file,
        transform=None,
        target_transform=None,
        loader=default_loader
    ):
        super().__init__(root, transform=transform, target_transform=target_transform)

        self.root = root
        self.json_file = json_file
        self.loader = loader

        self.classes, self.class_to_idx = self.find_bounding_boxes()
        self.samples = self.make_dataset()
        self.targets = [s[1] for s in self.samples]
            
            
    def find_bounding_boxes(self):
        """
        Builds the (image_path, class_index, bbox) dataset.
        
        Returns:
            classes (`list[str]`): A list of unique class labels found in the dataset
            class_to_idx (`dict{str:int}`): A dictionary mapping class labels to their corresponding indices
        """
        
        with open(self.json_file, "r") as f:
            data = json.load(f)

        # Create a set to store unique class labels
        class_set = set()

        # Iterate through the files and bounding boxes to populate the class set
        for image in data["files"]:
            for box in image["boundingBoxes"]:
                class_set.add(box["label"])

        classes = sorted(list(class_set))
        class_to_idx = {cls_name: idx for idx, cls_name in enumerate(classes)}

        return classes, class_to_idx
    

    def make_dataset(self):
        """
        Builds the `(image_path, class_index, bbox)` dataset.
        
        Returns:
            instances (`list[tuple(str, int, tuple(int, int, int, int))]`): A list of tuples, where each tuple contains (image_path, class_index, bbox)
        """

        # Iterate in the different paths in the json 
        with open(self.json_file, "r") as f:
            data = json.load(f)

        instances = []

        for image in data["files"]:
            
            # Construct the full image path by joining the root directory with the relative path from the JSON
            image_path = os.path.join(self.root, image["path"])

            # Iterate through the bounding boxes for the current image and create instances
            for box in image["boundingBoxes"]:
                label = box["label"]
                class_idx = self.class_to_idx[label]

                bbox = (
                    box["x"],
                    box["y"],
                    box["width"],
                    box["height"]
                )

                instances.append((image_path, class_idx, bbox))

        return instances
    
    @staticmethod
    def xywh_to_xyxy(box):
        x, y, w, h = box
        return x, y, x + w, y + h

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        path, label, bbox = self.samples[index]

        img = self.loader(path)  # PIL image

        x1, y1, x2, y2 = self.xywh_to_xyxy(bbox)

        # Crop
        img = img.crop((x1, y1, x2, y2))

        if self.transform:
            img = self.transform(img)

        if self.target_transform:
            label = self.target_transform(label)

        return img, label

class BoundingBoxDataset(Dataset):

    def __init__(
        self,
        root_dir,
        json_file,
        transform=None
    ):
        self.dataset = BoundingBoxImageFolder(
            root=root_dir,
            json_file=json_file,
            transform=transform
        )

        self.classes = self.dataset.classes
        self.class_to_idx = self.dataset.class_to_idx
        self.targets = self.dataset.targets

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        img, label = self.dataset[idx]
        return img, label

    def getName(self):
        return self.name

    # def load_instance(self,instance):

    #     path,label, (x,y,w,h) = instance
        
    #     img = Image.open(path).convert("RGB")
    #     img = np.array(img)

    #     img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #     box_xyxy = self.xywh_to_xyxy((x,y,w,h))
    #     y_start = int(box_xyxy[1])
    #     y_end = int(box_xyxy[3])
    #     x_start = int(box_xyxy[0])
    #     x_end = int(box_xyxy[2])
    #     croppedIMG = img[y_start:y_end,x_start:x_end]
    #     img = croppedIMG
    #     # debug images
    #     # cv2.imshow("Before RGB", np.array(Image.open(path)))
    #     # cv2.imshow("Original Image", img)
    #     # cv2.imshow("Cropped Image", croppedIMG)
        
    #     # # Wait for a key press and then close windows
    #     # cv2.waitKey(0)
    #     # cv2.destroyAllWindows()

    #     imgTensor = transforms.ToTensor()(img)
    #     labels = torch.tensor([label],dtype=torch.int64)
    #     self.dataset = [imgTensor, labels]
    #     return self.dataset


    # def __len__(self):
    #     return len(self.img_files)

    # def __getitem__(self, idx):
    #     imgTensor, target = self.dataset[idx]
    #     return imgTensor, target


# class BondingBoxDataset(Dataset):
#     def __init__(self):
#         self.dataset = BoundingBoxImageFolder(img_dir, json_dir, transform)

#         if self.transform:
#         # Note: The transforms for object detection usually require applying
#         # the same transformation to both the image and the bounding boxes.
#         # Torchvision's new transforms API handles this with tv_tensors.
#         image, target = self.transform(image, target)


# obj = BoundingBoxImageFolder(None,None,None,None,None,None,None)
# json_dir = "G:\\Shared drives\\RB\\2025-2026\\Spring 2026\\Software\\MiniSumoDataset\\info.json"
# imageInstancesArray = obj.make_dataset(json_dir, obj.find_bounding_boxes(json_dir))

# # print(imageInstancesArray)

# print(obj.create_tensors(imageInstancesArray))

# ('data/minisumo.09(1).jpg.4o4v5mqp.ingestion-6d4b7975-8kjp4.jpg', 0, (33, 0, 525, 404)), 

# "G:\\Shared drives\\RB\\2025-2026\\Spring 2026\\Software\\MiniSumoDataset\\data\\