'''
Convert COCO keypoints json to txt files
YOLO keypoints text file format: Assuming we only take class "person" category with ID = 1 (obj_id = 0)
0 <center_x> <center_y> <width> <height> <point0_x> <point0_y> <point0_visible> ... <point16_x> <point16y_y> <point16_visible>
All are normalized

COCO 17 keypoints:
["nose", "left_eye", "right_eye", "left_ear", "right_ear", "left_shoulder", "right_shoulder",
"left_elbow", "right_elbow", "left_wrist", "right_wrist", "left_hip", "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle" ]

'''

import json
import os
import cv2
import shutil

json_file = '/path/to/coco/annotations_trainval2017/annotations/person_keypoints_train2017.json'
img_folder = '/path/to/coco/train2017/'

dst_folder = '/your/train/folder/coco_keypoints/train/' # or valid

with open(json_file, 'r') as f:
    coco_data = json.load(f)
    
num_kpt = 17
annotations = coco_data["annotations"]

for annotation in annotations:
        
    img_id = annotation['image_id']
    keypoints = annotation["keypoints"]
    img_path = img_folder + '%012d.jpg' % img_id    
    shutil.copy(img_path, dst_folder + '%012d.jpg' % img_id)
    
    img = cv2.imread(img_path)
    img_h, img_w, c = img.shape
    x, y, w, h = annotation['bbox']
    x_center = x + w / 2
    y_center = y + h / 2
    
    x_center /= img_w
    y_center /= img_h
    w /= img_w
    h /= img_h                  
    
    label_file = dst_folder + '%012d.txt' % img_id
    with open(label_file, 'a+') as wf:
        wf.write('0 {} {} {} {}'.format(x_center, y_center, w, h))
        for i in range(len(keypoints)):
            if i % 3 == 0:
                keypoints[i] /= img_w
            elif i % 3 == 1:
                keypoints[i] /= img_h
            wf.write(' %1.6f' % keypoints[i])
        wf.write('\n')
