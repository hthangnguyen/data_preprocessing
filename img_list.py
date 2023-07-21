'''
create train, valid, test text files for training
  input: image folder
  output: train.txt, valid.txt, test.txt
each file contains image paths i.e. /path/to/image/img_000000.jpg
'''

import os

folder = '/path/to/image/folder'
train, valid, test = [], [], []
cnt = 1
files = os.listdir(folder)
for file in files:
    if 'jpg' in file:
        if cnt % 10 == 0:
            valid.append(folder+file)
        if cnt % 12 == 0:
            test.append(folder+file)
        else:
            train.append(folder+file)
        cnt += 1

with open('train.txt', 'w') as wf:
    for i in train:
        wf.write(i + '\n')
        
with open('valid.txt', 'w') as wf:
    for i in valid:
        wf.write(i + '\n')
        
with open('test.txt', 'w') as wf:
    for i in test:
        wf.write(i + '\n')
