%function data = getData(path)

clear;clc

% read all filename in dir
img_path = './data/image/';
anno_path = './data/';

dirs = dir([img_path,'*.jpg']);
dircell = struct2cell(dirs)';
imgnames = dircell(:,1);
filename = cell(size(imgnames));
annoname = cell(size(imgnames));
annoroad = cell(size(imgnames));

% get image names & xml file names
for i = 1:size(imgnames)
    file_name = char(imgnames(i));
    k = find('.'== file_name);
    filename{i} = file_name(1:k-1);%remove suffix
    annoname{i} = [filename{i},'.xml'];%add suffix
end

% read rgb images & xml annotations
disp('loading...');
for i = 1:size(imgnames)
    try
        xDoc = xmlread([anno_path,filename{i},'.xml']);
    catch
        error('Failed to read XML file %s.xml',filename{i});
    end

    % get all elements from xml annotations
    annotationNode = xDoc.getElementsByTagName('annoation').item(0);
    scaleNode = annotationNode.getElementsByTagName('scale').item(0);
    typeNode = annotationNode.getElementsByTagName('type').item(0);
    pointsNode = annotationNode.getElementsByTagName('points').item(0);
    point_list = pointsNode.getElementsByTagName('point');
    scale = str2num(char(scaleNode.getTextContent()));
    typea = char(typeNode.getTextContent());
    %disp(typea);
    %disp(point_list.getLength);
    id = cell(1,4);xaxis = cell(1,4);yaxis = cell(1,4);
    for j = 0:point_list.getLength-1
        pointNode = point_list.item(j);
        idText = pointNode.getElementsByTagName('id').item(0).getTextContent();
        id{j+1} = str2num(char(idText));
        xaxis{j+1} = str2num(char(pointNode.getElementsByTagName('xaxis').item(0).getTextContent()));
        yaxis{j+1} = str2num(char(pointNode.getElementsByTagName('yaxis').item(0).getTextContent()));
        
    end
    point = struct('id',id,'x',xaxis,'y',yaxis);
    annopoints.point = point;
    annoroad{i} = struct('type',typea,'scale',scale,'annopoints',annopoints);
end
annolist = struct('image_name',filename,'annoroad',annoroad);
disp('over');

% put all data into struct data
data = struct('annolist',annolist);

save('test1.mat','data');
