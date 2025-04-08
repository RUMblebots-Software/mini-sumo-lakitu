import albumentations as A
import cv2
import numpy as np
import os

input_folders = ["../Data Acquisition/Flag.class","../Data Acquisition/MiniSumo.class","../Data Acquisition/NotMiniSumo.class"]
output_folders = ["Data Modification/Flag.class","Data Modification/MiniSumo.class","Data Modification/NotMiniSumo.class"]


#Pipeline Definition 
pipeline = A.Compose([
    A.HorizontalFlip(p=0.5), # 50% chance to flip
    A.RandomBrightnessContrast(p=0.8), # 80% chance to adjust brightness/contrast
    A.GaussianBlur(p=0.3), # 30% chance to blur
])


for folder in input_folders:
    for file_name in os.listdir(folder):
        continue 
    







