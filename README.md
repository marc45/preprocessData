# Preprocess Data

## 1. Matlab

1. Read data from images and annotation xml files;
2. Reorganize data structure;
3. Save data into .mat files.

## 2. Python

#### 2-1 Main idea
1. Select images every (step=)n pictures from source dir;
2. Get all filenames under certain directory;
3. Create same-name annotation xml file according to example xml annotation;
4. Call GUI & annotate using mouse click.

#### 2-2 file directory structure

```
./--data/----annotation/
  |       |--image/ #target dir
  |       `--rar/   #source dir
  |-python/--anno_img.py
  `-matlab/
```

#### 2-3 usage
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
