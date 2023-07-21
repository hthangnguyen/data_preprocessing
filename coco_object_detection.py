'''
Convert label data from json file into YOLO format
<obj_id> <center_x> <center_y> <width> <height>
'''

import json
import os
import shutil
import cv2

# Path to COCO dataset and annotation file
# dataDir = '/path/to/COCO'
# annFile = os.path.join(dataDir, 'annotations', 'instances_val2017.json')


# Path to COCO dataset annotation file
annFile = '/path/to/COCO/annotations_trainval2017/annotations/instances_train2017.json'

# Path to COCO dataset image folder
img_folder = '/path/to/COCO/images/train2017'

# Path to output folder for YOLO train data
out_folder = '/path/to/dst/folder/'

# Define classes of interest
classes_of_interest = ['person', 'bicycle', 'car', 'motorcycle', 'bus'] # can add more as needed

# Load the annotations from the JSON file
with open(annFile, 'r') as f:
    annotations = json.load(f)

id_of_interest = []
for cls in classes_of_interest:
    for category in annotations['categories']:
        if category['name'] == cls:
            id_of_interest.append(category['id'])

imgIds = []
for ann in annotations['annotations']:
    if ann['category_id'] in id_of_interest:
        imgIds.append(ann['image_id'])
        
# Loop over images in COCO dataset
for img_info in annotations['images']:
    # Load image
    if img_info['id'] in imgIds:
        img_path = os.path.join(img_folder, img_info['file_name'])
        img = cv2.imread(img_path)

        # Create output text file for YOLO annotations
        out_path = os.path.join(out_folder, img_info['file_name'].replace('.jpg', '.txt'))
        out_file = open(out_path, 'w')
        # Loop over object instances in image
        for ann in annotations['annotations']:
            if ann['image_id'] == img_info['id']:
                # Convert COCO bbox format (x, y, w, h) to YOLO format (x_center, y_center, w, h)
                if not ann['category_id'] in id_of_interest:
                    continue
                x, y, w, h = ann['bbox']
                x_center = x + w / 2
                y_center = y + h / 2
                img_w = img_info['width']
                img_h = img_info['height']
                x_center /= img_w
                y_center /= img_h
                w /= img_w
                h /= img_h

                # Write YOLO annotation to output file
                yolo_cls_id = id_of_interest.index(ann['category_id'])
                out_file.write('{} {} {} {} {}\n'.format(yolo_cls_id, x_center, y_center, w, h))
        
        out_file.close()
        shutil.copy(img_path, out_folder+os.sep+img_info['file_name'])
   
        
