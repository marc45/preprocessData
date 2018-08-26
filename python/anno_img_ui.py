# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 16:31:38 2018

@author: wuchuan
"""
from __future__ import print_function
from xml.dom.minidom import Document
from os import listdir
from os.path import exists,isfile, join, splitext
from PyQt5.QtWidgets import QLabel,QApplication,QDialog,QHBoxLayout,QVBoxLayout,QGroupBox,QPushButton,QMessageBox
import PyQt5.QtCore as QtCore
from PyQt5.QtGui import QPixmap,QPainter, QPen,QPolygon
'''
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
'''
import sys

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
    print(img_name)

class MyLabel(QLabel):
    def __init__(self,parent=None):
        super(MyLabel, self).__init__(parent)
        self.pixel_x = -1  # pixel coordinate
        self.pixel_y = -1
        self.setAlignment(QtCore.Qt.AlignTop)
        self.points = []
        self.counts = 0
        self.imgname = ""
        #self.imgindex = 0
    
    def removeLastPoint(self):
        if(self.counts>0):
            self.points.pop()
            self.counts -= 1            
            self.clear()            
            self.update()
    
    def removeAllPoints(self):
        if(self.counts>0):
            self.points.clear()
            self.counts = 0
            self.clear()
            self.update()
        
    def setImage(self,imgpath):
        self.imgname = QPixmap(imgpath)
        self.ratio = self.imgname.width()/960
        self.imgname = self.imgname.scaled(960, 768, aspectRatioMode = QtCore.Qt.KeepAspectRatio)
        self.removeAllPoints()
    
    def setLimit(self,limit):
        self.limit = limit
        
    def resetCounts(self):
        self.counts = 0

    def mousePressEvent(self, e):
        if self.counts>=self.limit or self.imgname == "":
            return
        self.clear()
        self.pixel_x = e.x()
        self.pixel_y = e.y()
        print(str(self.pixel_x*self.ratio)+','+str(self.pixel_y*self.ratio))
        

    def paintEvent(self, e):
        if self.imgname == "":
            return
        QLabel.paintEvent(self, e)
        qp = QPainter(self)
        qp.drawPixmap(0,0,self.imgname)
        qp.begin(self)
        if self.pixel_x > 0 and self.pixel_y > 0:
            self.counts+=1
            point = QtCore.QPoint(self.pixel_x,self.pixel_y)
            self.points.append(point)
            self.drawPoints(qp)
        if self.pixel_x < 0 and self.pixel_y < 0:
            self.drawPoints(qp)
        qp.end()
        
    def isAnnotated(self):
        return self.counts == self.limit

    def drawPoints(self, qp):
        qp.setPen(QPen(QtCore.Qt.red, 5))
        qp.drawPoints(QPolygon(self.points))
        self.pixel_x = -1
        self.pixel_y = -1

    def getPoints(self):
        pos = []
        for QP in self.points:
            pos.append((QP.x()/0.75,QP.y()/0.75))
        return pos

class ImageDialog(QDialog):
    def __init__(self,  parent = None):
        super(ImageDialog,  self).__init__(parent)
        self.img_index = 0
        self.img_annotated = False
        self.initFile()
        self._title = "图像标注"
        self._diawidth = 1200
        self._diaheight = 900
        self.setWindowTitle(self._title)
        '''
        self.setMinimumHeight(self._diaheight)
        self.setMaximumHeight(self._diaheight)
        self.setMinimumWidth(self._diawidth)
        self.setMaximumWidth(self._diawidth)
        '''
        self.mainlayout = QHBoxLayout()
        self.imagebox = QGroupBox()
        self.buttonbox = QGroupBox()
        
        self.imagelayout = QVBoxLayout()
        #self.imagelayout.setAlignment()
        self.buttonlayout = QVBoxLayout()
        
        self.imageView = MyLabel()
        self.imageView.setLimit(32)
        #self.imageView.setAlignment(QtCore.Qt.AlignCenter)
        #self.imageView.setGeometry(QtCore.QRect(0, 0, 960, 768))
        self.imageView.setFixedWidth(960)
        self.imageView.setFixedHeight(768)
            
        if self.img_annotated:
            QMessageBox.information(self,"Information","当前文件夹中文件已全部标注")
        else: 
            #self.imageView.setImage("road.jpg")
            self.imageView.setImage(self.img_file)
            self.img_index += 1
        self.name = QLabel(self.img_name)
        #self.name.setAlignment(QtCore.Qt.AlignHCenter)
        self.name.setFixedHeight(20)
        self.imagelayout.addWidget(self.name,alignment = QtCore.Qt.AlignHCenter)
        self.imagelayout.addWidget(self.imageView,alignment = QtCore.Qt.AlignHCenter)
        #self.imageView.setAlignment(QtCore.Qt.AlignRight)
        self.imagebox.setLayout(self.imagelayout)
        
        
        self.undo1 = QPushButton("撤销当前点")
        self.undo1.setObjectName('button')
        self.undo2 = QPushButton("撤销全部点")
        self.undo2.setObjectName('button')
        self.confirm = QPushButton("确认")
        self.confirm.setObjectName('button')
        self.buttonlayout.addWidget(self.undo1)
        self.buttonlayout.addWidget(self.undo2)
        self.buttonlayout.addWidget(self.confirm)
        
        self.undo1.clicked.connect(self.on_undo1_clicked)
        self.undo2.clicked.connect(self.on_undo2_clicked)
        self.confirm.clicked.connect(self.on_confirm_clicked)
        
        self.buttonbox.setLayout(self.buttonlayout)
        
        self.mainlayout.addWidget(self.imagebox)
        self.mainlayout.addWidget(self.buttonbox)
        self.mainlayout.setStretch(0,6)
        self.mainlayout.setStretch(1,1) 
        self.setLayout(self.mainlayout)
        app.setStyleSheet('''
            QPushButton#button{
                background-color: #d7d7d7 ;
                height:180px;
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: #333;
                font: 14px;
                min-width: 10em;
                padding: 3px;
            }

            ''')
        
    def initFile(self):
        self.point_num = 32
        self.pic_dir = '../data/rar/'
        self.img_dir = '../data/region2/'
        self.anno_dir = '../data/region_annotation/'
        self.filenames = get_all_files(self.img_dir)
        
        self.n = len(self.filenames)
        for i in range(self.n): 
            self.img_name = self.filenames[i]
            self.anno_file = self.anno_dir + self.img_name + '.xml'
            self.img_file = self.img_dir + self.img_name + '.jpg'
            if exists(self.img_file) and exists(self.anno_file):#检测是否已经有标注
                print(self.img_name + '.xml 已存在！')
                if i == self.n-1:
                    self.img_annotated = True
                    self.img_index = -1
            else:
                self.img_index = i
                break
            
    # @pyqtSlot(bool)
    def on_undo1_clicked(self, checked):
        self.imageView.removeLastPoint()
        
    # @pyqtSlot(bool)     
    def on_undo2_clicked(self, checked):
        self.imageView.removeAllPoints()
        
    # @pyqtSlot(bool)    
    def on_confirm_clicked(self, checked):
        if not self.imageView.isAnnotated():    
            QMessageBox.information(self,"提示","该图片未完成标注！")
            return
        if self.img_index == -1:
            QMessageBox.information(self,"提示","已完成所有标注！")
            return
        pos = self.imageView.getPoints()
        add_anno(self.anno_dir, self.img_dir, self.img_name, pos)
        if 0 <= self.img_index < self.n:
            self.img_name = self.filenames[self.img_index]
            self.anno_file = self.anno_dir + self.img_name + '.xml'
            self.img_file = self.img_dir + self.img_name + '.jpg'
            self.imageView.setImage(self.img_file)
            self.name.setText(self.img_name)
            self.imageView.update()
            self.img_index += 1
                
if __name__ == "__main__":
    app = QApplication(sys.argv)    #创建QApplication类的实例
    app.aboutToQuit.connect(app.deleteLater)
    dia = ImageDialog()            #创建ImageDialog类的实例
    dia.show()                      #显示程序主窗口
    app.exit(app.exec_()) 
