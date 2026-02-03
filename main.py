# Edge Impulse - OpenMV FOMO Object Detection Example
#
# This work is licensed under the MIT license.
# Copyright (c) 2013-2024 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE

import sensor
import time
import ml
from ml.utils import NMS
import math
import image

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Let the camera adjust.

min_confidence = 0.7
threshold_list = [(math.ceil(min_confidence * 255), 255)]

# Load built-in model
model = ml.Model("models/model.tflite", load_to_fb=True)
print(model)

# Alternatively, models can be loaded from the filesystem storage.
# model = ml.Model('<object_detection_modelwork>.tflite', load_to_fb=True)
labels = [line.rstrip('\n') for line in open("labels/labels.txt")]

# Define specific colors for the given labels
label_colors = {
    "NotMiniSumo": (255, 255, 0),  # Yellow
    "MiniSumo": (0, 255, 0),        # Green
    "Flag": (255, 0, 0)             # Red
}

default_color = (255, 255, 255)

# FOMO outputs an image per class where each pixel in the image is the centroid of the trained
# object. So, we will get those output images and then run find_blobs() on them to extract the
# centroids. We will also run get_stats() on the detected blobs to determine their score.
# The Non-Max-Supression (NMS) object then filters out overlapping detections and maps their
# position in the output image back to the original input image. The function then returns a
# list per class which each contain a list of (rect, score) tuples representing the detected
# objects.
def fomo_post_process(model, inputs, outputs):
    n, oh, ow, oc = model.output_shape[0]
    nms = NMS(ow, oh, inputs[0].roi)
    for i in range(oc):
        img = image.Image(outputs[0][0, :, :, i] * 255)
        blobs = img.find_blobs(
            threshold_list, x_stride=1, area_threshold=1, pixels_threshold=1
        )
        for b in blobs:
            rect = b.rect()
            x, y, w, h = rect
            score = (
                img.get_statistics(thresholds=threshold_list, roi=rect).l_mean() / 255.0
            )
            nms.add_bounding_box(x, y, x + w, y + h, score, i)
    return nms.get_bounding_boxes()

clock = time.clock()
while True:
    clock.tick()
    img = sensor.snapshot()

    for i, detection_list in enumerate(model.predict([img], callback=fomo_post_process)):
        # Only proceed if the label is 'MiniSumo'
        if labels[i] != "MiniSumo":
            continue

        if len(detection_list) == 0:
            continue  # no detections for this class?

        # For MiniSumo, use the specific color and print details.
        print("********** %s **********" % labels[i])
        color = label_colors.get(labels[i], default_color)

        for (x, y, w, h), score in detection_list:
            center_x = math.floor(x + (w / 2))
            center_y = math.floor(y + (h / 2))
            print(f"x {center_x}\ty {center_y}\tscore {score}")
            
            size_multiplier = 2.5
            img.draw_rectangle(
                int(x - w * (size_multiplier - 1) / 2),
                int(y - h * (size_multiplier - 1) / 2),
                int(w * size_multiplier),
                int(h * size_multiplier),
                color=color,
                thickness=2
            )

    print(clock.fps(), "fps", end="\n")
