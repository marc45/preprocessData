#!/usr/bin/python
#coding=utf-8
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def unzip_files(file_path, target_path):
    '''
    解压指定目录下的文件
    '''
    pass

def select_pic(pic_path, img_path, n):
    '''
    每隔n张图片选取一张，并存入img_path文件夹
    '''
    
    pass

def add_anno(img_path, example_anno_path):
    '''
    获取文件夹下所有文件的文件名，并依照示例创建同名xml标注文件
    '''
    pass

def img_anno(img_file_path):
    '''
    调用图形接口鼠标点击进行标注
    '''
    #img = Image.open(img_file_path)
    #plt.imshow(img)
    t = np.arange(10)
    plt.plot(t, np.sin(t))
    print('Please click')
    pos = plt.ginput(3)
    print(pos)
    plt.show()
    return pos


if __name__ == "__main__":
    print('begin to process')
    index = 10
    n = 15
    pic_path = '../data/rar/Section' + str(index) + 'CameraC/'
    img_path = '../data/image/'
    example_anno_path = '../data/example.xml'
    #select_pic(pic_path, img_path, n)
    #add_anno(img_path, example_anno_path)
    file_name = '00012c.jpg'
    img_file_path = img_path + file_name
    pos = img_anno(img_file_path)
