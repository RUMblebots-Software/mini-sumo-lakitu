import albumentations as A
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt



def visualize(image):
    plt.figure(figsize=(10,10))
    plt.axis("off")
    plt.imshow(image)



input_folders = ["../Data Acquisition/Flag.class", "../Data Acquisition/MiniSumo.class", "../Data Acquisition/NotMiniSumo.class"]
output_folders = ["Flag.Augmented","MiniSumo.Augmented","NotMiniSumo.Augmented"]
names = ["Flag","MiniSumo","NotMiniSumo"]

#---------Look for necessary trasnformation--------------------
#Pipeline Definition 
pipeline = A.Compose([
    A.ToSepia(p=0.99), # 50% chance to flip
    A.RandomBrightnessContrast(p=0.8), # 80% chance to adjust brightness/contrast
    A.GaussianBlur(p=0.3), # 30% chance to blur
])

#------- Applie the pipeline to each photo in the three folders then save it --------------
output_folders_index = -1
output_file_name = 00
for folder in input_folders:
    output_folders_index += 1
    for file_name in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,file_name))

        #If failed to load image this will skip the proccess
        if img is None:
            print(f"Failed to load image {img} from {folder}")
            break

        pipelined = pipeline(image=img)
        trasnformed = pipelined["image"]


        save_to_folder = os.path.join(output_folders[output_folders_index],f"Augmented_{names[output_folders_index]}_{output_file_name}.jpg")
        cv2.imwrite(save_to_folder,trasnformed)
        output_file_name += 1
    output_file_name = 00  

    







