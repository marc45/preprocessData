#!/usr/bin/python
#coding=utf-8
from __future__ import print_function
from xml.dom.minidom import Document
from os import listdir
from os.path import exists,isfile, join, splitext
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def select_pic(source_dir, target_dir, step = 20, index = 1):
    '''
    每隔step张图片选取一张，并复制到target_dir文件夹，默认步长为20；
    并根据原文件夹进行重命名
    '''
    files = [f for f in listdir(source_dir) if isfile(join(source_dir,f))]
    n = len(files)
    for i in range(n):
        source_file = join(source_dir, files[i])
        target_file = join(target_dir, 'sec'+str(index)+files[i])#对原文件根据文件夹重命名
        if isfile(source_file) and (i%step == 0):
            with open(target_file, 'wb') as tf:
                with open(source_file, 'rb') as sf: 
                    tf.write(sf.read())

def get_all_files(img_dir):
    '''
    获取文件夹中全部文件的文件名，并且去除后缀名
    '''
    names = [f for f in listdir(img_dir) if isfile(join(img_dir,f))]
    file_names = []
    for i in range(len(names)):
        file_names.append(splitext(names[i])[0])
    return file_names

def add_anno(anno_dir, img_dir, img_name, annotations):
    '''
    获取文件夹下所有文件的文件名，并依照示例创建同名xml标注文件
    '''
    length = len(annotations)
    doc = Document()
    annotation = doc.createElement('annotation')  
    doc.appendChild(annotation)  
    scale = doc.createElement('scale')  
    annotation.appendChild(scale)
    scale_value = doc.createTextNode(str(1.00))
    scale.appendChild(scale_value)
    typea = doc.createElement('type')  
    annotation.appendChild(typea)
    type_value = doc.createTextNode('straight')
    typea.appendChild(type_value)
    points = doc.createElement('points')
    annotation.appendChild(points)
    for i in range(length):
        point = doc.createElement('point')
        points.appendChild(point)
        ida = doc.createElement('id')
        point.appendChild(ida)
        id_value = doc.createTextNode(str(i + 1))  
        ida.appendChild(id_value)
        x_node = doc.createElement('xaxis')
        point.appendChild(x_node)
        x_value = doc.createTextNode(str(annotations[i][0]))
        x_node.appendChild(x_value)
        y_node = doc.createElement('yaxis')
        point.appendChild(y_node)
        y_value = doc.createTextNode(str(annotations[i][1]))
        y_node.appendChild(y_value)
    filename = anno_dir + img_name + '.xml'
    with open(filename,'w') as f:
        f.write(doc.toprettyxml())

def img_anno(anno_dir, img_dir, img_name, point_num = 8):
    '''
    调用图形接口鼠标点击进行标注
    '''
    anno_file = anno_dir + img_name + '.xml'
    img_file = img_dir + img_name + '.jpg'
    if exists(img_file) and exists(anno_file):#检测是否已经有标注
        print(img_name + '.xml annotation already exist~')
        return (0,0)
    img = Image.open(img_file)
    plt.title(img_file)
    plt.imshow(img)
    pos = plt.ginput(point_num)
    print(pos)
    plt.show()
    add_anno(anno_dir, img_dir, img_name, pos)
    return pos

def get_data(point_num, img_dir, anno_dir):
    print('begin to process~')
    filenames = get_all_files(img_dir)
    n = len(filenames)
    for i in range(n):
        img_anno(anno_dir, img_dir, filenames[i], point_num)
    print('process over~')
    
if __name__ == "__main__":
    index = 14
    step = 25
    validation_step = 71
    point_num = 8
    pic_dir = '../data/rar/Section' + str(index) + 'CameraC/'
    img_dir = '../data/image/'
    anno_dir = '../data/annotation/'
    validation_img_dir = '../data/validation/image/'
    validation_anno_dir = '../data/validation/annotation/'
    #选择训练集图片
    #select_pic(pic_dir, img_dir, step, index)
    #选择验证集图片
    #select_pic(pic_dir, validation_img_dir, validation_step, index)
    #标注训练集
    #get_data(point_num, img_dir, anno_dir)
    #标注验证集
    get_data(point_num, validation_img_dir, validation_anno_dir)
