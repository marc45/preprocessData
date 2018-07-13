#!/usr/bin/python
#coding=utf-8
from __future__ import print_function
from xml.dom.minidom import Document
from os import listdir
from os.path import exists,isfile, join, splitext
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def select_pic(source_dir, target_dir, step = 20, header = '0'):
    '''
    每隔step张图片选取一张，并复制到target_dir文件夹，默认步长为20；
    并根据原文件夹进行重命名
    '''
    files = [f for f in listdir(source_dir) if isfile(join(source_dir,f))]
    n = len(files)
    for i in range(n):
        source_file = join(source_dir, files[i])
        target_file = join(target_dir, header + files[i])#对原文件根据文件夹重命名
        if exists(target_file):
            continue
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

def add_anno(anno_dir, img_dir, img_name, annotations, point_num):
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
    if length == point_num:
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
    add_anno(anno_dir, img_dir, img_name, pos, point_num)
    return pos

def get_data(point_num, img_dir, anno_dir):
    print('begin to process~')
    filenames = get_all_files(img_dir)
    n = len(filenames)
    for i in range(n):
        img_anno(anno_dir, img_dir, filenames[i], point_num)
    print('process over~')
    
if __name__ == "__main__":
    train_step = 30 # 训练集步长
    validation_step = 181 # 每隔固定步长取验证集图片
    point_num = 16 # 标注点的数目
    pic_dir = '../data/rar/Section86CameraC/'
    pic_dir2 = '../data/rar/'
    train_img_dir = '../data/val-sequence/image/'
    train_anno_dir = '../data/val-sequence/annotation/'
    validation_img_dir = '../data/validation2/image/'
    validation_anno_dir = '../data/validation2/annotation/'
    #sample_dir = '../data/sample/'
    #names = [f for f in listdir(pic_dir2) if  not isfile(join(pic_dir2,f))]
    #for header in names:
    #    _pic_dir = pic_dir2 + header + '/'
    #    print(_pic_dir)
    #    select_pic(_pic_dir, validation_img_dir, validation_step, header)
    #选择训练集图片
    #select_pic(pic_dir, train_img_dir, train_step, header)
    #选择验证集图片
    #select_pic(pic_dir, validation_img_dir, validation_step, header = 'Section86CameraC')
    #标注训练集
    get_data(point_num, train_img_dir, train_anno_dir)
    #标注验证集
    #get_data(point_num, validation_img_dir, validation_anno_dir)
