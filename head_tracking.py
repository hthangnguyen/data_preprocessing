'''
Head Tracking dataset: https://motchallenge.net/data/Head_Tracking_21/
Image size: 1920 x 1080
Ground Truth format: frame, id, left, top, width, height, conf, x, y, z
Convert the data to YOLO training format: cls_id cx cy nw nh (cls_id = 0, only head class)

'''

import cv2
import numpy as np
root = '/path/to/HT21/train/HT21-02/' # modify the name to traverse all the folder
annotations = root + 'gt/gt.txt'
img_folder = root + '/img1/'
label_folder = root + 'labels/'

with open(annotations, 'r') as rf:
    lines = rf.read().splitlines()

img_width, img_height = 1920., 1080.

color = (255,0,255)
for line in lines:
    
    data = [int(float(x)) for x in line.split(',')]
    left, top, w, h = data[2:6]
    img_id = data[0]
    label_file = label_folder + '%06d.txt' % img_id
    
    cx = float(left + w / 2) / img_width
    cy = float(top + h / 2) / img_height
    nw = float(w) / img_width
    nh = float(h) / img_height
    with open(label_file, 'a+') as wf:
        wf.write('0 %1.6f %1.6f %1.6f %1.6f\n' % (cx, cy, nw, nh))
