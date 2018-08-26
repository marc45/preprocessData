# Preprocess Data

## 1. Matlab

#### 1-1 Main idea
1. Annotate selected images (more details at 2-1);
2. Read data from images and annotation xml files;
3. Reorganize data structure;
4. Save data into .mat files.

#### 1-2 Usage
```
$ matlab
> cd matlab
> run img_anno.m
> run getData.m
> run checkData.m
> run splitData.m
```

## 2. Python

#### 2-1 Main idea
1. Select images every (step=)n pictures from source dir;
2. Get all filenames under certain directory;
3. Create same-name annotation xml file according to example xml annotation;
4. Call GUI & annotate using mouse click.

#### 2-2 File directory structure

```
./--data/----annotation/
  |       |--image/ #target dir
  |       |--validation/---annotation/ #validation dir
  |       |              `-image/
  |       `--rar/   #source dir
  |-python/--anno_img.py
  `-matlab/
```

#### 2-3 Usage
organize data as above and run python script.
```
$ cd python/
$ python anno_img.py 
```
You can change selection-step & target-dir in script file as you like.

#### 2-4 reimplementation using matlab
```
$ matlab
> cd matlab
> run img_anno.m
```

#### 2-5 reimplementation with PyQt5 by wuchuan

