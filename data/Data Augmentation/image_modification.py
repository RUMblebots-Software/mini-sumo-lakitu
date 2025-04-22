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

prob_pipeline1 = 0.90
prob_pipeline2 = 0.80


pipeline = A.OneOf([
    
    A.Compose([
        A.RandomShadow(p=0.90), #Simulates shadows for the image by reducing the brightness of the image in shadow regions.
        A.RandomBrightnessContrast(p=0.90), # 80% chance to adjust brightness/contrast
        A.RandomRotate90(p=0.90), #Randomly rotate the input by 90 degrees zero or more times.
        A.Illumination(p=0.90), #Apply various illumination effects to the image.
   
        A.OneOf([
            A.MotionBlur(p=0.70), #Apply motion blur to the input image using a directional kernel.
            A.ZoomBlur (p=0.90), #Apply zoom blur transform.    
        ], p=0.75)  
    ], p=prob_pipeline1),                  # The entire pipeline has a 100% chance to be applied

    A.Compose([
        A.Downscale(scale_min=0.25, scale_max=0.5, p=0.80), #Decrease image quality by downscaling and upscaling back.
        A.RandomGravel(p=0.50), #Adds gravel-like artifacts to the input image.
        A.Resize(height=256, width=256, p=0.30), #Resize the input to the given height and width
    ], p=prob_pipeline2,)
], p = 0.50)

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

    







