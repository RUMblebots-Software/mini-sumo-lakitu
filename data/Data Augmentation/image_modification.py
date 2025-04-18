import albumentations as A
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt



def visualize(image):
    plt.figure(figsize=(10,10))
    plt.axis("off")
    plt.imshow(image)



input_folders = ["../Data Acquisition/Flag.class","../Data Acquisition/MiniSumo.class","../Data Acquisition/NotMiniSumo.class"]
output_folders = ["Data Augmentation/Flag.Augmented","Data Augmentation/MiniSumo.Augmented","Data Augmentation/NotMiniSumo.Augmented"]

#---------Look for necessary trasnformation--------------------
#Pipeline Definition 
pipeline = A.Compose([
    A.HorizontalFlip(p=0.5), # 50% chance to flip
    A.RandomBrightnessContrast(p=0.8), # 80% chance to adjust brightness/contrast
    A.GaussianBlur(p=0.3), # 30% chance to blur
])

#------- Applie the pipeline to each photo in the three folders--------------

for folder in input_folders:
    for file_name in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,file_name))

        pipelined = pipeline(image=img)
        trasnformed = pipelined["image"]
        

    







