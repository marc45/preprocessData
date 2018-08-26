from os import listdir
from os.path import exists, isfile, join, splitext
import shutil

def copy(img_src_dir, anno_src_dir, img_tgt_dir, anno_tgt_dir):
    img_fns = [f for f in listdir(img_src_dir) if isfile(join(img_src_dir, f))]
    count = 0
    for img_fn in img_fns:
        anno_path = anno_src_dir + img_fn[0:-4] + '.xml'
        img_path = img_src_dir + img_fn
        anno_copy_path = anno_tgt_dir + img_fn[0:-4] + '.xml'
        img_copy_path = img_tgt_dir + img_fn
        #print(img_fn)
        if exists(anno_path) and exists(img_path): 
            print(anno_path)
            count += 1
            shutil.copyfile(img_path, img_copy_path)
            shutil.copyfile(anno_path, anno_copy_path)
    print('count = ',count)

if __name__ == '__main__':
    img_src_dir = '/home/supermicro/zc12345/documents/keypoint_detection/data/data/train/image/'
    anno_src_dir = '/home/supermicro/zc12345/documents/keypoint_detection/data/data/train/annotation/'
    img_tgt_dir = '/home/supermicro/zc12345/documents/keypoint_detection/getData/data/train/image/'
    anno_tgt_dir = '/home/supermicro/zc12345/documents/keypoint_detection/getData/data/train/annotation/'
    copy(img_src_dir, anno_src_dir, img_tgt_dir, anno_tgt_dir)
