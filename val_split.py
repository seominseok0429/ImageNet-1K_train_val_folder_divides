import glob
import xml.etree.ElementTree as elemTree
import argparse
import os
import shutil
#shutil.copy('sample.pdf', 'Temp')


parser = argparse.ArgumentParser(description='')
parser.add_argument('--val_path', default='/Data/ILSVRC/Data/CLS-LOC/val', type=str, help='imagenet val folder path')
parser.add_argument('--anno_path', default='/Data/ILSVRC/Annotations/CLS-LOC/val', type=str, help='imagenet anno folder path')
parser.add_argument('--label_path', default='/Data/ILSVRC/Annotations/CLS-LOC/train', type=str, help='imagenet label folder path')
args = parser.parse_args()
label_path = glob.glob(os.path.join(args.label_path,'*'))
img_path = glob.glob(os.path.join(args.val_path,'*'))

if len(label_path) != 1000:
    raise Exception('Please check label path.')

if len(img_path) != 50000 and len(img_path) != 51000:
    raise Exception('Please check val path.')

for i in label_path:
    labeldir = os.path.join(args.val_path,i.split('/')[-1])
    if not os.path.isdir(labeldir):
        os.mkdir(labeldir)

for path in img_path:
    is_img = path.split('/')[-1].split('.')[-1]
    if is_img == 'JPEG':
        anno_path = os.path.join(args.anno_path,path.split('/')[-1][:-4] + 'xml')
        tree = elemTree.parse(anno_path)
        for child in tree.getroot():
            if child.tag != 'object':
                continue
            label = child.find('name')
            target = label.text
        shutil.copy(path, os.path.join(args.val_path, target))
    
